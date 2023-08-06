"""dj-ratelimit

dj-ratelimit is a redis backed ratelimit for django requests. To use set the following
environment variables in your django settings:

    - ENVIRONMENT: default 'local'
    - DJ_RATELIMIT_REDIS_ADDRESS: default 'localhost'
    - DJ_RATELIMIT_REDIS_PORT: default '6379'

For more information see project github page 'py-ratelimit'
"""

from setuptools import setup

DOCLINES = (__doc__ or "").split("\n")

setup(
    name='dj_ratelimit',
    version='0.1.1',
    description='Redis backed library implementing a django ratelimit',
    long_description="\n".join(DOCLINES[2:]),
    url='https://github.com/conorbergman/py-ratelimit',
    author='Conor Bergman',
    author_email='conorbergman@gmail.com',
    license='',
    packages=[
        'dj_ratelimit',
        'dj_ratelimit.tst',
    ],
    install_requires=[
        'Django>=4.0.5',
        'djangorestframework>=3.12.4',
        'redis>=4.3.1',
        # TESTING
        'fakeredis',
        'freezegun>=1.2.1',
        'pytest>=6.2.5',
        'requests-mock>=1.8.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
