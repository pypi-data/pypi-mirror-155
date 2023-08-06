import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'CHANGELOG.md')).read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
     name='openapi_django',
     author="Y. Chudakov",
     author_email="kappasama.ks@gmail.com",
     version='0.0.8',
     packages=['openapi_django'],
     package_data={'': package_files(os.path.join(here))},
     description='OpenApi for django',
     long_description=README,
     url='https://gitlab.com/kappasama.ks/openapi_django',
     install_requires=[
          'Django>=3.2.6', 'djantic==0.7.0'
     ]
)
