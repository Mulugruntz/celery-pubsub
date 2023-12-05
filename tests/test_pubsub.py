from __future__ import annotations

import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    from typing_extensions import ParamSpec
else:
    try:
        from typing import ParamSpec as ParamSpec
    except ImportError:
        try:
            from typing_extensions import ParamSpec as ParamSpec
        except ImportError:
            ParamSpec = None

from celery import Task
from celery.worker import WorkController

from celery_pubsub import publish, unsubscribe, publish_now

P = ParamSpec("P")


def test_subscription(job_c: Task[P, str], celery_worker: WorkController) -> None:
    from celery_pubsub import publish, subscribe

    res = publish("dummy", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e"])

    subscribe("dummy", job_c)

    res = publish("dummy", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e", "c"])

    unsubscribe("dummy", job_c)

    res = publish("dummy", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e"])


def test_1(celery_worker: WorkController) -> None:
    res = publish("index.low.test", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["d", "e", "f", "g"])


def test_2(celery_worker: WorkController) -> None:
    res = publish("something.else", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e"])


def test_3(celery_worker: WorkController) -> None:
    res = publish("index.high", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["a", "d", "e"])


def test_4(celery_worker: WorkController) -> None:
    res = publish_now("index", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["c", "e"])


def test_5(celery_worker: WorkController) -> None:
    from celery_pubsub import publish as pub

    res = pub("index.low", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["b", "d", "e"])


def test_6(celery_worker: WorkController) -> None:
    import celery_pubsub as pubsub

    res = pubsub.publish("index.high.some.test", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["d", "e", "g"])


def test_7(celery_worker: WorkController) -> None:
    from celery_pubsub import publish

    res = publish("index.high.test", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["d", "e", "f", "g"])


def test_8(celery_worker: WorkController) -> None:
    from celery_pubsub import publish

    res = publish("foo", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e", "i"])


def test_9(celery_worker: WorkController) -> None:
    from celery_pubsub import publish

    res = publish("foo.bar.blur", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e", "h"])


def test_10(celery_worker: WorkController) -> None:
    from celery_pubsub import publish

    res = publish("foo.bar.baz", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e", "h", "j"])


def test_11(celery_worker: WorkController) -> None:
    from celery_pubsub import publish

    res = publish("foo.bar", 4, 8, a15=16, a23=42).get()
    assert sorted(res) == sorted(["e", "h", "k"])


def test_subscription_redundant(
    job_a: Task[P, str], celery_worker: WorkController
) -> None:
    import celery_pubsub

    # Ignoring attr-defined because of this: https://github.com/sbdchd/celery-types/issues/112

    jobs_init = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks  # type: ignore[attr-defined]
    celery_pubsub.subscribe("redundant.test", job_a)
    jobs_before = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks  # type: ignore[attr-defined]
    celery_pubsub.subscribe("redundant.test", job_a)
    jobs_after = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks  # type: ignore[attr-defined]
    celery_pubsub.unsubscribe("redundant.test", job_a)
    jobs_end = celery_pubsub.pubsub._pubsub_manager.get_jobs("redundant.test").tasks  # type: ignore[attr-defined]

    assert jobs_before == jobs_after
    assert jobs_init == jobs_end


def test_unsubscribe_nonexistant(
    job_a: Task[P, str], celery_worker: WorkController
) -> None:
    import celery_pubsub

    # Ignoring attr-defined because of this: https://github.com/sbdchd/celery-types/issues/112

    jobs_before = celery_pubsub.pubsub._pubsub_manager.get_jobs("not.exists").tasks  # type: ignore[attr-defined]
    celery_pubsub.unsubscribe("not.exists", job_a)
    jobs_after = celery_pubsub.pubsub._pubsub_manager.get_jobs("not.exists").tasks  # type: ignore[attr-defined]

    assert jobs_before == jobs_after
