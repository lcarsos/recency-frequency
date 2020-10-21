from setuptools import setup, find_packages

setup(
    name='recfreq',
    version='1',
    description='Check how many branches have recently been pushed to that have a certain change in them',
    author='Ezekiel Chopper',
    author_email='lcarsos@lcarsos.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords='github git',
    install_requires=[
        'gitpython',
    ],
    entry_points={
        'console_scripts': ['ricky=recfreq:init'],
    }
)
