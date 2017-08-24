from distutils.core import setup
setup(
    name='celery-pubsub',
    packages=['celery_pubsub'],
    version='0.1.5',
    description='A Publish and Subscribe library for Celery',
    author='Samuel GIFFARD',
    author_email='mulugruntz@gmail.com',
    license='MIT',
    url='https://github.com/Mulugruntz/celery-pubsub',
    download_url='https://github.com/Mulugruntz/celery-pubsub/tarball/0.1.4',
    keywords=['celery', 'publish', 'subscribe', 'pubsub'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Distributed Computing',
        'Topic :: Utilities',
    ],
    install_requires=['celery'],
)