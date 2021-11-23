import pytest

import celery
from celery_pubsub import subscribe, unsubscribe


if celery.__version__ < "4.0.0":  # pragma: no cover
    celery.current_app.conf.update(
        CELERY_ALWAYS_EAGER=True,
    )
    task = celery.task

    @pytest.fixture
    def celery_worker():
        pass


else:  # pragma: no cover
    task = celery.shared_task

    @pytest.fixture
    def celery_config():
        return {
            "broker_url": "memory://",
            "result_backend": "rpc://",
            "broker_transport_options": {"polling_interval": 0.05},
        }


@pytest.fixture(scope="session")
def job_a():
    @task(name="job_a")
    def job(*args, **kwargs):
        print("job_a: {} {}".format(args, kwargs))
        return "a"

    return job


@pytest.fixture(scope="session")
def job_b():
    @task(name="job_b")
    def job(*args, **kwargs):
        print("job_b: {} {}".format(args, kwargs))
        return "b"

    return job


@pytest.fixture(scope="session")
def job_c():
    @task(name="job_c")
    def job(*args, **kwargs):
        print("job_c: {} {}".format(args, kwargs))
        return "c"

    return job


@pytest.fixture(scope="session")
def job_d():
    @task(name="job_d")
    def job(*args, **kwargs):
        print("job_d: {} {}".format(args, kwargs))
        return "d"

    return job


@pytest.fixture(scope="session")
def job_e():
    @task(name="job_e")
    def job(*args, **kwargs):
        print("job_e: {} {}".format(args, kwargs))
        return "e"

    return job


@pytest.fixture(scope="session")
def job_f():
    @task(name="job_f")
    def job(*args, **kwargs):
        print("job_f: {} {}".format(args, kwargs))
        return "f"

    return job


@pytest.fixture(scope="session")
def job_g():
    @task(name="job_g")
    def job(*args, **kwargs):
        print("job_g: {} {}".format(args, kwargs))
        return "g"

    return job


@pytest.fixture(scope="session")
def subscriber(job_a, job_b, job_c, job_d, job_e, job_f, job_g):
    subscribe("index.high", job_a)
    subscribe("index.low", job_b)
    subscribe("index", job_c)
    subscribe("index.#", job_d)
    subscribe("#", job_e)
    subscribe("index.*.test", job_f)
    subscribe("index.#.test", job_g)
