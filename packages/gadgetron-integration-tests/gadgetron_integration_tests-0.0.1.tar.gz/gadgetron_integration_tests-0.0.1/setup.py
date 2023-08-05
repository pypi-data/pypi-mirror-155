from setuptools import setup


setup(
    name='gadgetron_integration_tests',
    version='0.0.1',

    url='https://github.com/gadgetron/gadgetron/tree/master/test/integration',
    author='Gadgetron',
    py_modules=['get_data', 'mem_watch', 'run_gadgetron_test', 'run_tests', 'stats_to_junit'],
    install_requires=['h5py','ismrmrd'],
)