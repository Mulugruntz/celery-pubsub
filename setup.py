import codecs
import os
import setuptools.command.test


def long_description():
    try:
        return codecs.open("README.md", "r", "utf-8").read()
    except IOError:
        return "Long description error: Missing README.md file"


def _strip_comments(line):
    return line.split("#", 1)[0].strip()


def parse_req_file(filename):
    full_path = os.path.join(os.getcwd(), filename)
    return [
        _strip_comments(req)
        for req in codecs.open(full_path, "r", "utf-8").readlines()
        if req
    ]


def install_requires():
    return parse_req_file("requirements.txt")


def tests_require():
    return parse_req_file("requirements_test.txt")


setuptools.setup(
    name="celery-pubsub",
    packages=["celery_pubsub"],
    version="1.0.1",
    description="A Publish and Subscribe library for Celery",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Samuel GIFFARD",
    author_email="mulugruntz@gmail.com",
    license="MIT",
    url="https://github.com/Mulugruntz/celery-pubsub",
    download_url="https://github.com/Mulugruntz/celery-pubsub/tarball/1.0.1",
    keywords=["celery", "publish", "subscribe", "pubsub"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Distributed Computing",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    install_requires=install_requires(),
    tests_require=tests_require(),
)
