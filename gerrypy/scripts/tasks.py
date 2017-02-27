"""Celery scripts to run fishscales asynchronously."""

from gerrypy.scripts.fish_scales import State
from celery import Celery
from celery.signals import worker_init


# @worker_init.connect
# def bootstrap_pyramid(signal, sender):
#     import os
#     from pyramid.paster import bootstrap
#     sender.app.settings = \
#         bootstrap(os.environ['YOUR_CONFIG'])['registry'].settings

app = Celery('tasks', broker='amqp://localhost//')
# app.config_from_object('celeryconfig')
app.conf.result_backend = 'redis://'
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['json', 'pickle']


@app.task
def sample_states(request, num_dst, criteria):
    """Make several states and fill their districts."""
    this_state = State(request, num_dst)
    this_state.fill_state(criteria)
    return this_state


def make_states(request, num_dst, times, criteria):
    states = []
    for i in range(times):
        states.append(sample_states.delay(request, num_dst, criteria))
    return states
