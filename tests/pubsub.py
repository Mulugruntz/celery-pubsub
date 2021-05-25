import unittest
import celery
import celery_pubsub

celery.current_app.conf.update(
    CELERY_ALWAYS_EAGER=True,
)

if celery.__version__ < '4.0.0':
    task = celery.task
else:
    app = celery.Celery()
    task = app.task


@task
def job_a(*args, **kwargs):
    print("job_a: {} {}".format(args, kwargs))
    return "a"


@task
def job_b(*args, **kwargs):
    print("job_b: {} {}".format(args, kwargs))
    return "b"


@task
def job_c(*args, **kwargs):
    print("job_c: {} {}".format(args, kwargs))
    return "c"


@task
def job_d(*args, **kwargs):
    print("job_d: {} {}".format(args, kwargs))
    return "d"


@task
def job_e(*args, **kwargs):
    print("job_e: {} {}".format(args, kwargs))
    return "e"


@task
def job_f(*args, **kwargs):
    print("job_f: {} {}".format(args, kwargs))
    return "f"


@task
def job_g(*args, **kwargs):
    print("job_g: {} {}".format(args, kwargs))
    return "g"


celery_pubsub.subscribe('index.high', job_a)
celery_pubsub.subscribe('index.low', job_b)
celery_pubsub.subscribe('index', job_c)
celery_pubsub.subscribe('index.#', job_d)
celery_pubsub.subscribe('#', job_e)
celery_pubsub.subscribe('index.*.test', job_f)
celery_pubsub.subscribe('index.#.test', job_g)


class PubsubTest(unittest.TestCase):
    def test_subscription(self):
        from celery_pubsub import publish, subscribe
        res = publish('dummy', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e']))

        subscribe('dummy', job_c)

        res = publish('dummy', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e', 'c']))

        celery_pubsub.unsubscribe('dummy', job_c)

        res = publish('dummy', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e']))

    def test_1(self):
        res = celery_pubsub.publish('index.low.test', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['d', 'e', 'f', 'g']))

    def test_2(self):
        res = celery_pubsub.publish('something.else', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['e']))

    def test_3(self):
        res = celery_pubsub.publish('index.high', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['a', 'd', 'e']))

    def test_4(self):
        res = celery_pubsub.publish_now('index', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['c', 'e']))

    def test_5(self):
        from celery_pubsub import publish as pub
        res = pub('index.low', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['b', 'd', 'e']))

    def test_6(self):
        import celery_pubsub as pubsub
        res = pubsub.publish('index.high.some.test', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['d', 'e', 'g']))

    def test_7(self):
        from celery_pubsub import publish
        res = publish('index.high.test', 4, 8, a15=16, a23=42).get()
        self.assertListEqual(sorted(res), sorted(['d', 'e', 'f', 'g']))

    def test_subscription_redundant(self):
        jobs_init = celery_pubsub.pubsub._pubsub_manager.get_jobs('redundant.test').tasks
        celery_pubsub.subscribe('redundant.test', job_a)
        jobs_before = celery_pubsub.pubsub._pubsub_manager.get_jobs('redundant.test').tasks
        celery_pubsub.subscribe('redundant.test', job_a)
        jobs_after = celery_pubsub.pubsub._pubsub_manager.get_jobs('redundant.test').tasks
        celery_pubsub.unsubscribe('redundant.test', job_a)
        jobs_end = celery_pubsub.pubsub._pubsub_manager.get_jobs('redundant.test').tasks

        self.assertListEqual(jobs_before, jobs_after)
        self.assertListEqual(jobs_init, jobs_end)

    def test_unsubscribe_nonexistant(self):
        jobs_before = celery_pubsub.pubsub._pubsub_manager.get_jobs('not.exists').tasks
        celery_pubsub.unsubscribe('not.exists', job_a)
        jobs_after = celery_pubsub.pubsub._pubsub_manager.get_jobs('not.exists').tasks

        self.assertListEqual(jobs_before, jobs_after)

if __name__ == '__main__':
    unittest.main()
