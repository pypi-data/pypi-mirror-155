from setuptools import setup

setup(
    name='dj_ratelimit',
    version='0.1.0',
    description='',
    url='https://github.com/conorbergman/py-ratelimit',
    author='Conor Bergman',
    author_email='conorbergman@gmail.com',
    license='',
    packages=['dj_ratelimit'],
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
