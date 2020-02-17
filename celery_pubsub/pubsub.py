import re
import celery


class PubSubManager(object):

    def __init__(self):
        self.jobs = {}

    def publish(self, topic, *args, **kwargs):
        group = []
        for (regex, task) in self.jobs.values():
            if regex.match(topic):
                group.append(task)
        out = celery.group(group)
        return out

    def publish_now(self, topic, *args, **kwargs):
        # REVIEW: useless shortcut?
        result = self.publish(topic, *args, **kwargs).apply(args=args, kwargs=kwargs)
        return result

    def subscribe(self, topic, task):
        assert isinstance(topic, str)
        re_topic = topic.replace('.', r'\.').replace('*', r'[^.]+').replace('#', r'.+')
        # REVIEW: what happens if TOPIC already exists?
        self.jobs[topic] = (regex, task)

    def unsubscribe(self, topic, task):
        del self.jobs[topic]


# Hence the class is useless?
_pubsub_manager = PubSubManager()


def publish(topic, *args, **kwargs):
    return _pubsub_manager.publish(topic, *args, **kwargs)


def publish_now(topic, *args, **kwargs):
    return _pubsub_manager.publish_now(topic, *args, **kwargs)


def subscribe(topic, task):
    return _pubsub_manager.subscribe(topic, task)


def unsubscribe(topic, task):
    return _pubsub_manager.unsubscribe(topic, task)
