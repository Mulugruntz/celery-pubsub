import celery
import re

__all__ = [
    "publish",
    "publish_now",
    "subscribe",
    "unsubscribe",
]


class PubSubManager(object):
    def __init__(self):
        super(PubSubManager, self).__init__()
        self.subscribed = set()
        self.jobs = {}

    def publish(self, topic, *args, **kwargs):
        result = self.get_jobs(topic).delay(*args, **kwargs)
        return result

    def publish_now(self, topic, *args, **kwargs):
        result = self.get_jobs(topic).apply(args=args, kwargs=kwargs)
        return result

    def subscribe(self, topic, task):
        key = (topic, self._topic_to_re(topic), task)
        if key not in self.subscribed:
            self.subscribed.add(key)
            self.jobs = {}

    def unsubscribe(self, topic, task):
        key = (topic, self._topic_to_re(topic), task)
        if key in self.subscribed:
            self.subscribed.discard(key)
            self.jobs = {}

    def get_jobs(self, topic):
        if topic not in self.jobs:
            self._gen_jobs(topic)
        return self.jobs[topic]

    def _gen_jobs(self, topic):
        jobs = []
        for job in self.subscribed:
            if job[1].match(topic):
                jobs.append(job[2].s())
        self.jobs[topic] = celery.group(jobs)

    @staticmethod
    def _topic_to_re(topic):
        assert isinstance(topic, str)
        re_topic = topic.replace(".", r"\.").replace("*", r"[^.]+").replace("#", r".+")
        return re.compile(r"^{}$".format(re_topic))


_pubsub_manager = None
if _pubsub_manager is None:  # pragma: no cover
    _pubsub_manager = PubSubManager()


def publish(topic, *args, **kwargs):
    return _pubsub_manager.publish(topic, *args, **kwargs)


def publish_now(topic, *args, **kwargs):
    return _pubsub_manager.publish_now(topic, *args, **kwargs)


def subscribe(topic, task):
    return _pubsub_manager.subscribe(topic, task)


def unsubscribe(topic, task):
    return _pubsub_manager.unsubscribe(topic, task)
