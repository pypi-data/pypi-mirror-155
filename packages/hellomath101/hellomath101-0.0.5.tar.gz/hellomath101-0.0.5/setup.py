from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='hellomath101', # Package name for use on pip install
    version='0.0.5',
    license='MIT',
    author="Tester",
    author_email='email@example.com',
    description = "short package description",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=['math1', 'math2'],
    package_dir={'': 'master_math'},
    keywords = "example documentation tutorial",
    url='https://github.com/gmyrianthous/example-publish-pypi',
    python_requires = ">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha", # 3 = Alpha, 4 = Beta, 5 = Production
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ]
)