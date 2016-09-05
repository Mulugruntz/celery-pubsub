import unittest
import celery
import celery_pubsub.pubsub

celery.current_app.conf.update(
    CELERY_ALWAYS_EAGER=True,
)


@celery.task
def job_a(*args, **kwargs):
    print "job_a: {} {}".format(args, kwargs)
    return "a"


@celery.task
def job_b(*args, **kwargs):
    print "job_b: {} {}".format(args, kwargs)
    return "b"


@celery.task
def job_c(*args, **kwargs):
    print "job_c: {} {}".format(args, kwargs)
    return "c"


@celery.task
def job_d(*args, **kwargs):
    print "job_d: {} {}".format(args, kwargs)
    return "d"


@celery.task
def job_e(*args, **kwargs):
    print "job_e: {} {}".format(args, kwargs)
    return "e"


@celery.task
def job_f(*args, **kwargs):
    print "job_f: {} {}".format(args, kwargs)
    return "f"


@celery.task
def job_g(*args, **kwargs):
    print "job_g: {} {}".format(args, kwargs)
    return "g"


celery_pubsub.pubsub.subscribe('index.high', job_a)
celery_pubsub.pubsub.subscribe('index.low', job_b)
celery_pubsub.pubsub.subscribe('index', job_c)
celery_pubsub.pubsub.subscribe('index.#', job_d)
celery_pubsub.pubsub.subscribe('#', job_e)
celery_pubsub.pubsub.subscribe('index.*.test', job_f)
celery_pubsub.pubsub.subscribe('index.#.test', job_g)


class PubsubTest(unittest.TestCase):
    def test_subscription(self):
        res = celery_pubsub.pubsub.publish('dummy', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e']))

        celery_pubsub.pubsub.subscribe('dummy', job_c)

        res = celery_pubsub.pubsub.publish('dummy', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e', 'c']))

        celery_pubsub.pubsub.unsubscribe('dummy', job_c)

        res = celery_pubsub.pubsub.publish('dummy', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e']))

    def test_1(self):
        res = celery_pubsub.pubsub.publish('index.low.test', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['d', 'e', 'f', 'g']))

    def test_2(self):
        res = celery_pubsub.pubsub.publish('something.else', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e']))

    def test_3(self):
        res = celery_pubsub.pubsub.publish('index.high', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['a', 'd', 'e']))

    def test_4(self):
        res = celery_pubsub.pubsub.publish_now('index', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['c', 'e']))

    def test_5(self):
        from celery_pubsub.pubsub import publish as pub
        res = pub('index.low', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['b', 'd', 'e']))

    def test_6(self):
        import celery_pubsub.pubsub as pubsub
        res = pubsub.publish('index.high.some.test', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['d', 'e', 'g']))

    def test_7(self):
        from celery_pubsub.pubsub import publish
        res = publish('index.high.test', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['d', 'e', 'f', 'g']))


if __name__ == '__main__':
    unittest.main()
