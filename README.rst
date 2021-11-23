celery-pubsub 1.0.0
===================

.. image:: https://travis-ci.org/Mulugruntz/celery-pubsub.svg?branch=master
    :target: https://travis-ci.org/Mulugruntz/celery-pubsub

.. image:: https://codeclimate.com/github/Mulugruntz/celery-pubsub/badges/gpa.svg
   :target: https://codeclimate.com/github/Mulugruntz/celery-pubsub
   :alt: Code Climate

.. image:: https://codeclimate.com/github/Mulugruntz/celery-pubsub/badges/coverage.svg
   :target: https://codeclimate.com/github/Mulugruntz/celery-pubsub/coverage
   :alt: Test Coverage

.. image:: https://codeclimate.com/github/Mulugruntz/celery-pubsub/badges/issue_count.svg
   :target: https://codeclimate.com/github/Mulugruntz/celery-pubsub
   :alt: Issue Count

.. image:: https://pepy.tech/badge/celery-pubsub
   :target: https://pepy.tech/project/celery-pubsub
   :alt: Downloads

Publish and Subscribe with Celery
 
Basic usage:
============
 
.. code-block:: python
 
    import celery
    import celery_pubsub
 
    @celery.task
    def my_task_1(*args, **kwargs):
        return "task 1 done"
 
 
    @celery.task
    def my_task_2(*args, **kwargs):
        return "task 2 done"
 
 
    # First, let's subscribe
    celery_pubsub.subscribe('some.topic', my_task_1)
    celery_pubsub.subscribe('some.topic', my_task_2)
 
    # Now, let's publish something
    res = celery_pubsub.publish('some.topic', data='something', value=42)
 
    # We can get the results if we want to (and if the tasks returned something)
    # But in pub/sub, usually, there's no result.
    print(res.get())
 
    # This will get nowhere, as no task subscribed to this topic
    res = celery_pubsub.publish('nowhere', data='something else', value=23)
 
Advanced usage:
===============
 
Wildcards can be used in topic names:
 
* ``*`` matches any one group
   * ``some.*.test`` will match ``some.awesome.test``, ``some.random.test``
     but not ``some.pretty.cool.test``, ``elsewhere`` or ``here.some.up.test``
   * ``some.*`` will match ``some.test`` and ``some.thing`` but it won't
     match ``some`` or ``some.testy.test``

* ``#`` matches any number of groups
   * ``some.#.test`` will match ``some.awesome.test``, ``some.random.test``,
     ``some.pretty.cool.test`` but not ``elsewhere`` or ``here.some.up.test``
   * ``some.#`` will match anything that starts with ``some.``, such as
     ``some.very.specific.topic.indeed``
   * ``#`` will match anything


.. code-block:: python
 
    # Let's subscribe
    celery_pubsub.subscribe('some.*', my_task_1)
    celery_pubsub.subscribe('some.*.test', my_task_2)
    celery_pubsub.subscribe('some.#', my_task_3)
    celery_pubsub.subscribe('#', my_task_4)
    celery_pubsub.subscribe('some.beep', my_task_5)
    # it's okay to have more than one task on the same topic
    celery_pubsub.subscribe('some.beep', my_task_6)
 
    # Let's publish
    celery_pubsub.publish('nowhere', 4)               # task 4 only
    celery_pubsub.publish('some', 8)                  # task 4 only
    celery_pubsub.publish('some.thing', 15)           # tasks 1, 3 and 4
    celery_pubsub.publish('some.true.test', 16)       # tasks 2, 3 and 4
    celery_pubsub.publish('some.beep', 23)            # tasks 1, 3, 4, 5 and 6
    celery_pubsub.publish('some.very.good.test', 42)  # tasks 3 and 4
 
    # And if you want to publish synchronously:
    celery_pubsub.publish_now('some.very.good.test', 42)  # tasks 3 and 4
 
    # You can unsubscribe too
    celery_pubsub.unsubscribe('#', my_task_4)
 
    # Now, task 4 will not be called anymore
    celery_pubsub.publish('some.very.good.test', 42)  # task 3 only
 
 
Changelog:
==========

* 1.0.0
    * Flexible requirements (no more pinned). Better to support a wide range of environments.
    * Changed test framework from nose to pytest.
    * Flake8
    * Support for Python 3.9 and 3.10.
* 0.2.1
    * Performance: Internally uses a ``set`` to store the subscribed tasks.
    * Updated Codeclimate as the `old reporter <https://github.com/codeclimate/python-test-reporter>`_ is deprecated.
    * Pinned requirements' dependency versions.
        * celery 4.3.0 -> 4.4.0
        * kombu 4.6.4 -> 4.6.7
        * billiard 3.6.1.0 -> 3.6.2.0
        * codeclimate-test-reporter 0.2.3 -> removed!
* 0.2.0
    * Removed Python 3.4 support. Reason: no longer supported by Kombu 4.6+.
    * Officially supported by Python 3.8.
    * Pinned requirements' dependency versions.
        * celery 4.2.1 -> 4.3.0
        * kombu 4.2.1 -> 4.6.4
        * billiard 3.5.0.4 -> 3.6.1.0
        * vine 1.1.4 -> 1.3.0
* 0.1.9
    * Added Python 3.4, 3.5, 3.7, and multiple branches of pypy
    * Pinned requirements' dependency versions.
        * celery 4.1.0 -> 4.2.1
        * kombu 4.1.0 -> 4.2.1
        * billiard 3.5.0 -> 3.5.0.4
        * nose pinned to 1.3.7
        * coverage pinned to 4.3.4 (was already 4.3.4 but fuzzy)
        * codeclimate-test-reported pinned to 0.2.3
    * Extra badge to show the number of downloads (thanks to PePy)
* 0.1.8
    * Fixup for broken ``pip install celery_pubsub==0.1.7``
* 0.1.7
    * PyPI long description fixed
    * Removed README.md and fixed README.rst
    * Added command ``python setup.py test`` to run unit tests with coverage
    * pypy support
* 0.1.5
    * Python 3 support
* 0.1.1
    * Added README
    * Refined setup
    * No need to access celery_pubsub.pubsub anymore. Direct access in celery_pubsub.
    * Tests moved out of package
    * Added Travis for CI
* 0.1
    * Initial version
