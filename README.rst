celery-pubsub
=============

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
    print res.get()
 
    # This will get nowhere, as no task subscribed to this topic
    res = celery_pubsub.publish('nowhere', data='something else', value=23)
 
Advanced usage:
===============
 
Wildcards can be used in topic names:
 
 * `*` matches any one group
    * `some.*.test` will match `some.awesome.test`, `some.random.test`
      but not `some.pretty.cool.test`, `elsewhere` or `here.some.up.test`
    * `some.*` will match `some.test` and `some.thing` but it won't
      match `some` or `some.testy.test`

 * `#` matches any number of groups
    * `some.#.test` will match `some.awesome.test`, `some.random.test`,
      `some.pretty.cool.test` but not `elsewhere` or `here.some.up.test`
    * `some.#` will match anything that starts with `some.`, such as
      `some.very.specific.topic.indeed`
    * `#` will match anything
 
 
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
 
* 0.1.1
    * Added README
    * Refined setup
    * No need to access celery_pubsub.pubsub anymore. Direct access in celery_pubsub.
    * Tests moved out of package
    * Added Travis for CI
* 0.1
    * Initial version
