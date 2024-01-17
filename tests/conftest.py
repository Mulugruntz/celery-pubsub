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
from celery.app.task import Task

from celery_pubsub import subscribe, subscribe_to
from packaging.version import parse, Version


# TODO: Simplify this when we drop support for Python 3.7.
if typing.TYPE_CHECKING:

    def get_distribution_version(distribution_name: str) -> Version:
        ...

else:

    def get_distribution_version(distribution_name: str) -> Version:
        try:
            from importlib.metadata import distribution

            return parse(distribution(distribution_name).version)
        except ImportError:
            # Fallback for Python < 3.8. Remove when we drop support for Python 3.7.
            from pkg_resources import get_distribution

            return parse(get_distribution(distribution_name).version)


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

    if get_distribution_version("celery") >= parse("5.0.0"):
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


@pytest.fixture(scope="session")
def job_h() -> Task[P, str]:
    @subscribe_to(topic="foo.#")
    @task(bind=True, name="job_h")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print(f"job_h: {args} {kwargs}")
        return "h"

    return job


@pytest.fixture(scope="session")
def job_i() -> Task[P, str]:
    @subscribe_to(topic="foo")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print(f"job_i: {args} {kwargs}")
        return "i"

    return job


@pytest.fixture(scope="session")
def job_j() -> Task[P, str]:
    @subscribe_to(topic="foo.bar.baz")
    @task(name="job_j")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print(f"job_j: {args} {kwargs}")
        return "j"

    return job


@pytest.fixture(scope="session")
def job_k() -> Task[P, str]:
    @subscribe_to(topic="foo.bar")
    def job(*args: P.args, **kwargs: P.kwargs) -> str:
        print(f"job_k: {args} {kwargs}")
        return "k"

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
    job_h: Task[P, str],
    job_i: Task[P, str],
    job_j: Task[P, str],
    job_k: Task[P, str],
) -> None:
    subscribe("index.high", job_a)
    subscribe("index.low", job_b)
    subscribe("index", job_c)
    subscribe("index.#", job_d)
    subscribe("#", job_e)
    subscribe("index.*.test", job_f)
    subscribe("index.#.test", job_g)
