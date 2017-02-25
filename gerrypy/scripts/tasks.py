"""Celery scripts to run fishscales asynchronously."""

from fish_scales import State
from celery import Celery


app = Celery('tasks', broker='amqp://localhost//')
app.conf.result_backend = 'redis://'


@app.task
def sample_states(request, num_dst, times):
    """Make several states and fill their districts."""
    states = []
    for i in range(times):
        states.append(State(request, num_dst))
    return states
