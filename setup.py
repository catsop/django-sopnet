import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sopnet',
    version='0.1',
    packages=['djsopnet'],
    include_package_data=True,
    license='GPL3 License',
    description='A simple Django app to talk to Sopnet',
    long_description=README,
    url='https://github.com/catsop/django-sopnet',
    author='Tom Kazimiers',
    author_email='tom@voodoo-arts.net',
    classifiers=[],
)
