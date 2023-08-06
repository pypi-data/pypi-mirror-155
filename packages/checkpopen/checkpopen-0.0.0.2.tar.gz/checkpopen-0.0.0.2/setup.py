from setuptools import setup

import sys

setup(
    name='checkpopen',
    description='Popen context manager variant that raises CalledProcessError like check_call',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    version='0.0.0.2',
    url='https://github.com/cielavenir/checkpopen',
    license='MIT',
    author='cielavenir',
    author_email='cielartisan@gmail.com',
    py_modules=['checkpopen'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
