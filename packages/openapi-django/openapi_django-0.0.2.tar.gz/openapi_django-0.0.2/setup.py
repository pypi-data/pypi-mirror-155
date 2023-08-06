import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'CHANGELOG.md')).read()

setup(
     name='openapi_django',
     author="Y. Chudakov",
     author_email="kappasama.ks@gmail.com",
     version='0.0.2',
     packages=['openapi_django'],
     description='OpenApi for django',
     long_description=README,
     url='https://gitlab.com/kappasama.ks/openapi_django',
     install_requires=[
          'Django>=3.2.6',
     ]
)
