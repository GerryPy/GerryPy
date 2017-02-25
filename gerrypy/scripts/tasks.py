"""Celery scripts to run fishscales asynchronously."""

from gerrypy.scripts.fish_scales import State
from celery import Celery


app = Celery('tasks', broker='amqp://localhost//')
app.conf.result_backend = 'redis://'


@app.task
def sample_states(request, num_dst, criteria):
    """Make several states and fill their districts."""
    this_state = State(request, num_dst)
    this_state.fillstate(criteria)
    return this_state


def makes_states(request, num_dst, times, criteria):
    states = []
    for i in range(times):
        states.append(sample_states.delay(request, num_dst, criteria))
    return states
