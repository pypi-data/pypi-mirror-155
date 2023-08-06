from setuptools import setup, find_packages

setup(name='seung-test',

      version='0.1.1.9',

      description='This package is a Python script for deploying and configuring NSX-T TESTLAB. Made by seungwang.',

      author='Seung Wang Kim',

      author_email='seungwangkim@gmail.com',

      license='MIT',

      #py_modules=[],

      python_requires='>=3.9',

      package_data={'NSX':['*.*','data/*.*']},

      install_requires=['requests>=2.25.1'],

      packages=['NSX']

      )