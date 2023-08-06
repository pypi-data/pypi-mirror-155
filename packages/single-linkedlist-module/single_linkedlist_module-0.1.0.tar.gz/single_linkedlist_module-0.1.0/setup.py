from setuptools import find_packages, setup

setup(
    name='single_linkedlist_module',
    packages= find_packages(include=['single_linkedlist_module']),
    version='0.1.0',
    description="Single LinkedList library",
    author='Me',
    license='MIT',
    install_requires = [],
    setup_requires = ['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)