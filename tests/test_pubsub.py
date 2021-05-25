from celery_pubsub import publish, unsubscribe, publish_now


def test_subscription(subscriber, job_c):
    from celery_pubsub import publish, subscribe

    subscriber()

    res = publish("dummy", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e"])

    subscribe("dummy", job_c)

    res = publish("dummy", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e", "c"])

    unsubscribe("dummy", job_c)

    res = publish("dummy", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e"])


def test_1(subscriber):
    subscriber()
    res = publish("index.low.test", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["d", "e", "f", "g"])


def test_2(subscriber):
    subscriber()
    res = publish("something.else", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e"])


def test_3(subscriber):
    subscriber()
    res = publish("index.high", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["a", "d", "e"])


def test_4(subscriber):
    subscriber()
    res = publish_now("index", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["c", "e"])


def test_5(subscriber):
    subscriber()
    from celery_pubsub import publish as pub

    res = pub("index.low", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["b", "d", "e"])


def test_6(subscriber):
    import celery_pubsub as pubsub

    subscriber()

    res = pubsub.publish("index.high.some.test", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["d", "e", "g"])


def test_7(subscriber):
    from celery_pubsub import publish

    subscriber()

    res = publish("index.high.test", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["d", "e", "f", "g"])


def test_subscription_redundant(subscriber, job_a):
    import celery_pubsub

    subscriber()
    jobs_init = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks
    celery_pubsub.subscribe("redundant.test", job_a)
    jobs_before = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks
    celery_pubsub.subscribe("redundant.test", job_a)
    jobs_after = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks
    celery_pubsub.unsubscribe("redundant.test", job_a)
    jobs_end = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks

    assert jobs_before == jobs_after
    assert jobs_init == jobs_end


def test_unsubscribe_nonexistant(subscriber, job_a):
    import celery_pubsub

    subscriber()
    jobs_before = celery_pubsub.pubsub._pubsub_manager.get_jobs("not.exists").tasks
    celery_pubsub.unsubscribe("not.exists", job_a)
    jobs_after = celery_pubsub.pubsub._pubsub_manager.get_jobs("not.exists").tasks

    assert jobs_before == jobs_after
