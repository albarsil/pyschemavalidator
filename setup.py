from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pyschemavalidator',
    version='1.0.4',
    description='Decorator for endpoint inputs on APIs and a dictionary/JSON validator.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/albarsil/pyschemavalidator',
    author='Allan Barcelos',
    author_email='albarsil@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords=['api', 'flask', 'graphql', 'json', 'validation', 'schema', 'dictionary', 'graphql'],
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=[],
    test_suite='tests.test_suite'
)
