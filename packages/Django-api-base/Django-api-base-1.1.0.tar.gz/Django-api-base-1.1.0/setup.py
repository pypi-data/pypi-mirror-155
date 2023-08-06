import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Django-api-base',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A simple Django app to make the RESTFULL APIs',
    long_description = README,
    long_description_content_type='text/markdown',
    url='https://maneeshv.github.io',
    author='Maneesh Shaji',
    author_email='maneeshvettukattil@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['django', 'rollbar'],
)
