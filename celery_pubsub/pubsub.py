"""Contains the pubsub manager and the pubsub functions."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    from typing_extensions import TypeAlias
else:
    try:
        from typing import TypeAlias as TypeAlias
    except ImportError:
        try:
            from typing_extensions import TypeAlias as TypeAlias
        except ImportError:
            TypeAlias = None

import celery
import re

__all__ = [
    "publish",
    "publish_now",
    "subscribe",
    "unsubscribe",
]

from celery import Task, group
from celery.result import AsyncResult, EagerResult


PA: TypeAlias = typing.Any  # ParamSpec args
PK: TypeAlias = typing.Any  # ParamSpec kwargs
P: TypeAlias = typing.Any  # ParamSpec
R: TypeAlias = typing.Any  # Return type


class PubSubManager:
    def __init__(self) -> None:
        super(PubSubManager, self).__init__()
        self.subscribed: set[tuple[str, re.Pattern[str], Task[P, R]]] = set()
        self.jobs: dict[str, group] = {}

    def publish(self, topic: str, *args: PA, **kwargs: PK) -> AsyncResult[R]:
        result = self.get_jobs(topic).delay(*args, **kwargs)
        return result

    def publish_now(self, topic: str, *args: PA, **kwargs: PK) -> EagerResult[R]:
        # Ignoring type because of this: https://github.com/sbdchd/celery-types/issues/111
        result = self.get_jobs(topic).apply(args=args, kwargs=kwargs)  # type: ignore
        return result

    def subscribe(self, topic: str, task: Task[P, R]) -> None:
        key = (topic, self._topic_to_re(topic), task)
        if key not in self.subscribed:
            self.subscribed.add(key)
            self.jobs = {}

    def unsubscribe(self, topic: str, task: Task[P, R]) -> None:
        key = (topic, self._topic_to_re(topic), task)
        if key in self.subscribed:
            self.subscribed.discard(key)
            self.jobs = {}

    def get_jobs(self, topic: str) -> group:
        if topic not in self.jobs:
            self._gen_jobs(topic)
        return self.jobs[topic]

    def _gen_jobs(self, topic: str) -> None:
        jobs = []
        for job in self.subscribed:
            if job[1].match(topic):
                jobs.append(job[2].s())
        self.jobs[topic] = celery.group(jobs)

    @staticmethod
    def _topic_to_re(topic: str) -> re.Pattern[str]:
        assert isinstance(topic, str)
        re_topic = topic.replace(".", r"\.").replace("*", r"[^.]+").replace("#", r".+")
        return re.compile(r"^{}$".format(re_topic))


_pubsub_manager: PubSubManager = PubSubManager()


def publish(topic: str, *args: PA, **kwargs: PK) -> AsyncResult[R]:
    return _pubsub_manager.publish(topic, *args, **kwargs)


def publish_now(topic: str, *args: PA, **kwargs: PK) -> EagerResult[R]:
    return _pubsub_manager.publish_now(topic, *args, **kwargs)


def subscribe(
    topic: str, task: typing.Optional[Task[P, R]] = None
) -> typing.Optional[typing.Callable[[Task[P, R]], Task[P, R]]]:
    if task is None:

        def _wrapper(task: Task[P, R]) -> Task[P, R]:
            _pubsub_manager.subscribe(topic, task)
            return task

        return _wrapper
    else:
        _pubsub_manager.subscribe(topic, task)
        return None


def unsubscribe(topic: str, task: Task[P, R]) -> None:
    return _pubsub_manager.unsubscribe(topic, task)
