#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import weakref

from django.dispatch.dispatcher import _make_id, Signal as _Signal, NO_RECEIVERS, NONE_ID
from django.utils.inspect import func_accepts_kwargs


class Signal(_Signal):
    """
    Base class for all signals

    Internal attributes:

        receivers
            { receiverkey (id) : weakref(receiver) }
    generally, the dispatch_status is used like a filter. when you connect a signal with certain dispatch_status,
    you should also send the same dispatch_status to trigger the connected function
    the origin code come's from https://github.com/django/django/blob/main/django/dispatch/dispatcher.py
    this project only add some extra code about dispatch_status
    """

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None, dispatch_status=""):
        """
        Connect receiver to sender for signal.

        Arguments:

            receiver
                A function or an instance method which is to receive signals.
                Receivers must be hashable objects.

                If weak is True, then receiver must be weak referenceable.

                Receivers must be able to accept keyword arguments.

                If a receiver is connected with a dispatch_uid argument, it
                will not be added if another receiver was already connected
                with that dispatch_uid.

            sender
                The sender to which the receiver should respond. Must either be
                a Python object, or None to receive events from any sender.

            weak
                Whether to use weak references to the receiver. By default, the
                module will attempt to use weak references to the receiver
                objects. If this parameter is false, then strong references will
                be used.

            dispatch_uid
                An identifier used to uniquely identify a particular instance of
                a receiver. This will usually be a string, though it may be
                anything hashable.

            dispatch_status
                An identifier used to identify a particular status of an receiver
        """
        from django.conf import settings

        # If DEBUG is on, check that we got a good receiver
        if settings.configured and settings.DEBUG:
            assert callable(receiver), "Signal receivers must be callable."

            # Check for **kwargs
            if not func_accepts_kwargs(receiver):
                raise ValueError("Signal receivers must accept keyword arguments (**kwargs).")

        if dispatch_uid:
            lookup_key = (dispatch_uid, _make_id(sender), dispatch_status)
        else:
            lookup_key = (_make_id(receiver), _make_id(sender), dispatch_status)

        if weak:
            ref = weakref.ref
            receiver_object = receiver
            # Check for bound methods
            if hasattr(receiver, '__self__') and hasattr(receiver, '__func__'):
                ref = weakref.WeakMethod
                receiver_object = receiver.__self__
            receiver = ref(receiver)
            weakref.finalize(receiver_object, self._remove_receiver)

        with self.lock:
            self._clear_dead_receivers()
            if not any(r_key == lookup_key for r_key, _ in self.receivers):
                self.receivers.append((lookup_key, receiver))
            self.sender_receivers_cache.clear()

    def disconnect(self, receiver=None, sender=None, dispatch_uid=None, dispatch_status=""):
        """
        Disconnect receiver from sender for signal.

        If weak references are used, disconnect need not be called. The receiver
        will be removed from dispatch automatically.

        Arguments:

            receiver
                The registered receiver to disconnect. May be none if
                dispatch_uid is specified.

            sender
                The registered sender to disconnect

            dispatch_uid
                the unique identifier of the receiver to disconnect

            dispatch_status
                whick kind of signal you want to filter

        """
        if dispatch_uid:
            lookup_key = (dispatch_uid, _make_id(sender), dispatch_status)
        else:
            lookup_key = (_make_id(receiver), _make_id(sender), dispatch_status)

        disconnected = False
        with self.lock:
            self._clear_dead_receivers()
            for index in range(len(self.receivers)):
                (r_key, _) = self.receivers[index]
                if r_key == lookup_key:
                    disconnected = True
                    del self.receivers[index]
                    break
            self.sender_receivers_cache.clear()
        return disconnected

    def send(self, sender, dispatch_status="", **named):
        """
        Send signal from sender to all connected receivers.

        If any receiver raises an error, the error propagates back through send,
        terminating the dispatch loop. So it's possible that all receivers
        won't be called if an error is raised.

        Arguments:

            sender
                The sender of the signal. Either a specific object or None.

            dispatch_status
                whick kind of signal you want to accept the event

            named
                Named arguments which will be passed to receivers.

        Return a list of tuple pairs [(receiver, response), ... ].
        """
        if not self.receivers or self.sender_receivers_cache.get((sender, dispatch_status)) is NO_RECEIVERS:
            return []

        return [
            (receiver, receiver(signal=self, sender=sender, **named))
            for receiver in self._live_receivers(sender, dispatch_status)
        ]

    def _live_receivers(self, sender, dispatch_status=""):
        """
        Filter sequence of receivers to get resolved, live receivers.

        This checks for weak references and resolves them, then returning only
        live receivers.
        """
        receivers = None
        if self.use_caching and not self._dead_receivers:
            receivers = self.sender_receivers_cache.get((sender, dispatch_status))
            # We could end up here with NO_RECEIVERS even if we do check this case in
            # .send() prior to calling _live_receivers() due to concurrent .send() call.
            if receivers is NO_RECEIVERS:
                return []
        if receivers is None:
            with self.lock:
                self._clear_dead_receivers()
                senderkey = _make_id(sender)
                receivers = []
                for (receiverkey, r_senderkey, r_dispatch_status), receiver in self.receivers:
                    if dispatch_status != r_dispatch_status:
                        continue
                    if r_senderkey == NONE_ID or r_senderkey == senderkey:
                        receivers.append(receiver)
                if self.use_caching:
                    if not receivers:
                        self.sender_receivers_cache[(sender, dispatch_status)] = NO_RECEIVERS
                    else:
                        # Note, we must cache the weakref versions.
                        self.sender_receivers_cache[(sender, dispatch_status)] = receivers
        non_weak_receivers = []
        for receiver in receivers:
            if isinstance(receiver, weakref.ReferenceType):
                # Dereference the weak reference.
                receiver = receiver()
                if receiver is not None:
                    non_weak_receivers.append(receiver)
            else:
                non_weak_receivers.append(receiver)
        return non_weak_receivers
