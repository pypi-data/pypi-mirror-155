from setuptools import setup, find_packages


setup(
    name='hellomath101', # Package name for use on pip install
    version='0.0.4',
    license='MIT',
    author="Tester",
    author_email='email@example.com',
    packages=['math1', 'math2'],
    package_dir={'': 'master_math'},
    keywords = "example documentation tutorial",
    url='https://github.com/gmyrianthous/example-publish-pypi',
    classifiers=[
        "Development Status :: 3 - Alpha", # 3 = Alpha, 4 = Beta, 5 = Production
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ]
)