from distutils.core import setup

setup(
    name = 'svnmock',
    version = '0.3',
    description = "Testing library for Subversion's python bindings",
    
    long_description = """svnmock provides capabilities to emulate the entire python language API for the Subversion revision control system.
    
The purpose of this library is to make it easy for developers to verify that SVN-facing code is working correctly. svnmock provides tools to assert that certain API functions must be called in a certain order with certain parameters, and that certain values should be returned from those function calls.

In addition, svnmock allows assertions of the type, "the return value from api_func_1() must be given as a parameter to api_func_2() and api_func_3()". This allows more fine-grained flow control tracking than simple "was the 4th parameter '6'?" assertions.

In addition to simple "was function X called with arguments Y and Z?" assertions, svnmock provides easy mechanisms for simulating tricky failure conditions that might otherwise be impossible -- or at least, very difficult -- to simulate otherwise.

Lastly, svnmock provides tracing support, allowing you to verify that certain API calls are being made without mocking up the entire session.""",
    
    author = 'Collin Winter',
    author_email = 'collinw@gmail.com',
    url = 'http://oakwinter.com/code/svnmock',
    license = 'MIT License',
    keywords = 'subversion svn testing mock',
    packages = ['svnmock']
)
