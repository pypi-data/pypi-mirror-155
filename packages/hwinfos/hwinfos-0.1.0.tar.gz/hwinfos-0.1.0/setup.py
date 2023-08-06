from setuptools import find_packages, setup
setup(
    name='hwinfos',
    packages=find_packages(include=['hwinfos']),
    version='0.1.0',
    description='Get PC hardware info for Windows OS',
    author='R3FL3X',
    license='MIT',
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    author_email='christos.daglaroglou@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
    ]
)