from setuptools import setup, find_packages


setup(
   name='awesome_messages',
   version='0.1.0',
   author='Samuel López Saura',
   author_email='samuellopezsaura@gmail.com',
   packages=find_packages(),
   license='MIT',
   url='https://github.com/elchicodepython/awesome_messages',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='This module provides interfaces to work with any kind of message publisher and consumer like rabbitmq pubsub.',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "pika>=1.2.1",
   ],
)
