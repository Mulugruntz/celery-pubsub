import celery

__all__ = ['publish', 'publish_now', 'subscribe', 'unsubscribe', ]


class PubSubManager(object):
    def __init__(self):
        super(PubSubManager, self).__init__()
        self.subscribed = []
        self.jobs = {}

    def publish(self, topic, *args, **kwargs):
        result = self.get_jobs(topic).delay(*args, **kwargs)
        return result

    def publish_now(self, topic, *args, **kwargs):
        result = self.get_jobs(topic).apply(args=args, kwargs=kwargs)
        return result

    def subscribe(self, topic, task):
        if (topic, task) not in self.subscribed:
            self.subscribed.append((topic, self._topic_to_re(topic), task))
            self.jobs = {}

    def unsubscribe(self, topic, task):
        found = -1
        for idx, triplet in enumerate(self.subscribed):
            if (triplet[0], triplet[2]) == (topic, task):
                found = idx
                break
        if not found == -1:
            del self.subscribed[found]
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
        import re
        re_topic = topic.replace('.', r'\.').replace('*', r'[^.]+').replace('#', r'.+')
        return re.compile(r'^{}$'.format(re_topic))


_pubsub_manager = None
if _pubsub_manager is None:
    _pubsub_manager = PubSubManager()


def publish(topic, *args, **kwargs):
    return _pubsub_manager.publish(topic, *args, **kwargs)


def publish_now(topic, *args, **kwargs):
    return _pubsub_manager.publish_now(topic, *args, **kwargs)


def subscribe(topic, task):
    return _pubsub_manager.subscribe(topic, task)


def unsubscribe(topic, task):
    return _pubsub_manager.unsubscribe(topic, task)
