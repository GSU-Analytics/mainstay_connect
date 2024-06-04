
from setuptools import setup, find_packages

setup(
    name='mainstay_connect',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'keyring',
        'requests',
        'pandas'
    ],
    extras_require={
        'test': ['pytest']
    },
    author='Isaac Kerson',
    author_email='ikerson@gsu.edu',
    description='A Mainstay API connection handler.',
    keywords='mainstay API python requests pandas',
    url='https://github.com/GSU-Analytics/mainstay_connect.git',
    python_requires='>=3.6',
)