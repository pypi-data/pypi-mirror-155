from setuptools import setup
from setuptools import find_packages

setup(
    name='ansible_mongodb_store',
    packages=find_packages(exclude=('testing*')),
    install_requires=['bson', 'bson-extra', 'pymongo', 'python-bsonjs'],
    description='MongoDB data storage and retrieval for Ansible playbooks',
    version='0.1',
    url='https://github.com/ParpingTam/ansible_mongodb_store',
    author='Ed McGuigan',
    author_email='ed.mcguigan@palmbeachschools.org',
    keywords=['pip','ansible','mongodb']
    )