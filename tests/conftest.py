import pytest

import celery
from celery_pubsub import subscribe

celery.current_app.conf.update(
    CELERY_ALWAYS_EAGER=True,
)

if celery.__version__ < "4.0.0":  # pragma: no cover
    task = celery.task
else:  # pragma: no cover
    app = celery.Celery()
    task = app.task


@pytest.fixture
def job_a():
    @task(name="job_a")
    def job(*args, **kwargs):
        print("job_a: {} {}".format(args, kwargs))
        return "a"

    return job


@pytest.fixture
def job_b():
    @task(name="job_b")
    def job(*args, **kwargs):
        print("job_b: {} {}".format(args, kwargs))
        return "b"

    return job


@pytest.fixture
def job_c():
    @task(name="job_c")
    def job(*args, **kwargs):
        print("job_c: {} {}".format(args, kwargs))
        return "c"

    return job


@pytest.fixture
def job_d():
    @task(name="job_d")
    def job(*args, **kwargs):
        print("job_d: {} {}".format(args, kwargs))
        return "d"

    return job


@pytest.fixture
def job_e():
    @task(name="job_e")
    def job(*args, **kwargs):
        print("job_e: {} {}".format(args, kwargs))
        return "e"

    return job


@pytest.fixture
def job_f():
    @task(name="job_f")
    def job(*args, **kwargs):
        print("job_f: {} {}".format(args, kwargs))
        return "f"

    return job


@pytest.fixture
def job_g():
    @task(name="job_g")
    def job(*args, **kwargs):
        print("job_g: {} {}".format(args, kwargs))
        return "g"

    return job


@pytest.fixture
def subscriber(job_a, job_b, job_c, job_d, job_e, job_f, job_g):
    def run():
        subscribe("index.high", job_a)
        subscribe("index.low", job_b)
        subscribe("index", job_c)
        subscribe("index.#", job_d)
        subscribe("#", job_e)
        subscribe("index.*.test", job_f)
        subscribe("index.#.test", job_g)

    return run
