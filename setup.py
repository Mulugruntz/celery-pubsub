from distutils.core import setup
setup(
  name = 'celery_pubsub',
  packages = ['celery_pubsub'], # this must be the same as the name above
  version = '0.1',
  description = 'A Publish and Subscribe library for Celery',
  author = 'Samuel GIFFARD',
  author_email = 'mulugruntz@gmail.com',
  url = 'https://github.com/Mulugruntz/celery-pubsub', # use the URL to the github repo
  download_url = 'https://github.com/Mulugruntz/celery-pubsub/tarball/0.1', # I'll explain this in a second
  keywords = ['celery', 'publish', 'subscribe', 'pubsub'], # arbitrary keywords
  classifiers = [],
)