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


from typing import Callable, TypeVar

import pytest

import celery
from celery import Task

from celery_pubsub import subscribe
from pkg_resources import get_distribution, parse_version

P = ParamSpec("P")
R = TypeVar("R")
task: Callable[..., Callable[[Callable[P, R]], Task[P, R]]]

if not typing.TYPE_CHECKING:
    task = celery.shared_task

    @pytest.fixture(scope="session")
    def celery_config():
        return {
            "broker_url": "memory://",
            "result_backend": "rpc://",
            "broker_transport_options": {"polling_interval": 0.05},
        }

    if get_distribution("celery").parsed_version >= parse_version("5.0.0"):
        pytest_plugins = ["celery.contrib.pytest"]


@pytest.fixture(scope="session")
def job_a() -> Task[P, str]:
    @task(name="job_a")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print("job_a: {} {}".format(args, kwargs))
        return "a"

    return job


@pytest.fixture(scope="session")
def job_b() -> Task[P, str]:
    @task(name="job_b")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print("job_b: {} {}".format(args, kwargs))
        return "b"

    return job


@pytest.fixture(scope="session")
def job_c() -> Task[P, str]:
    @task(name="job_c")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print("job_c: {} {}".format(args, kwargs))
        return "c"

    return job


@pytest.fixture(scope="session")
def job_d() -> Task[P, str]:
    @task(name="job_d")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print("job_d: {} {}".format(args, kwargs))
        return "d"

    return job


@pytest.fixture(scope="session")
def job_e() -> Task[P, str]:
    @task(name="job_e")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print("job_e: {} {}".format(args, kwargs))
        return "e"

    return job


@pytest.fixture(scope="session")
def job_f() -> Task[P, str]:
    @task(name="job_f")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print("job_f: {} {}".format(args, kwargs))
        return "f"

    return job


@pytest.fixture(scope="session")
def job_g() -> Task[P, str]:
    @task(name="job_g")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print("job_g: {} {}".format(args, kwargs))
        return "g"

    return job


@pytest.fixture(scope="session", autouse=True)
def subscriber(
    job_a: Task[P, str],
    job_b: Task[P, str],
    job_c: Task[P, str],
    job_d: Task[P, str],
    job_e: Task[P, str],
    job_f: Task[P, str],
    job_g: Task[P, str],
) -> None:
    subscribe("index.high", job_a)
    subscribe("index.low", job_b)
    subscribe("index", job_c)
    subscribe("index.#", job_d)
    subscribe("#", job_e)
    subscribe("index.*.test", job_f)
    subscribe("index.#.test", job_g)
