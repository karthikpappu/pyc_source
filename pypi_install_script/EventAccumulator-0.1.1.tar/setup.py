from distutils.core import setup

setup(
    name='EventAccumulator',
    url='https://bitbucket.org/ottokruse/event-accumulator',
    author='Otto Kruse',
    author_email='ottokruse@gmail.com',
    version='0.1.1',
    packages=['accumulator',],
    license='MIT',
    long_description='Accumulate (aka replay) events into a projection, useful for Event Sourcing applications',
)
