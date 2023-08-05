from setuptools import setup, find_packages


setup(
    name='hellomath101', # Package name for use on pip install
    version='0.0.1',
    license='MIT',
    author="Tester",
    author_email='email@example.com',
    packages=find_packages('math'),
    package_dir={'': 'master_math'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project'
)