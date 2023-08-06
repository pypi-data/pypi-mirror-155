# django-status-signal
enhanced django signal which enable you to trigger a signal only if the model instance is in a certain status

# Install

    pip3 install django-status-signal


# Usage
In many scenarios, you may want to trigger a function only when a model's status has been changed to a certain status. But the default django's signal can only use the sender(an model instance) to search the receivers. Here comes the solution.


    from django_status_signal import Signal
    class Task(models.Model):
        status = models.CharField(
            choices=(
                ("start", "start"),
                ("doing", "doing"),
                ("success", "success"),
                ("fail", "fail"),
            ),
            max_length=31,
        )
    # create a signal and connect it to different status
    mysignal = Singal()
    mysignal.connect(send_message, Task, dispatch_status="fail")
    mysignal.connect(reward, Task, dispatch_status="success")
    # call the signal
    task = Task.objects.create('start')
    mysignal.send(Task, instance=task, task.status)  # nothing will happen
    task.status = 'success'
    task.save()
    mysignal.send(Task, instance=task, task.status)  # the send_message will be called


# TODO
when this project is stable enough, I want to merge the code into [django](https://github.com/django/django) project, so all the `post_save`, `post_delete` can accept `dispatch_status` parameter.



# LICENSE
there are many code copied from the [django](https://github.com/django/django) project, so the LICENSE should stay the same as django's LICENSE.
