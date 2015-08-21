import os
from setuptools import setup
from django_spaghetti import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-spaghetti-and-meatballs',
    version=__version__,
    packages=['django_spaghetti'],
    include_package_data=True,
    license='MIT License',
    description='Its a spicy meatball for serving up fresh hot entity-relationship diagrams straight from your django models.',
    long_description=README,
    url='https://github.com/LegoStormtroopr/django-spaghetti-and-meatballs/',
    author='Samuel Spencer',
    author_email='sam@sqbl.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='django entity relationship diagram erd uml',
    install_requires=['django'], # I mean obviously you'll have django installed if you want to use this.

)
