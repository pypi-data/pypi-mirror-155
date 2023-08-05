"""gym_qRacing init module."""
__version__ = "0.0.2"

from logging import NullHandler, getLogger

from gym.envs.registration import register

getLogger(__name__).addHandler(NullHandler())

register(
    id="qRacing-base-v0",
    entry_point="gym_qRacing.envs:RaceSimulation",
)