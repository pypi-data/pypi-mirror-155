from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ansible_mongodb_store',
    version='0.2.0',
    author='Ed McGuigan',
    author_email='ed.mcguigan@palmbeachschools.org',
    description='MongoDB data storage and retrieval for Ansible playbooks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ParpingTam/ansible_mongodb_store',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['bson', 'bson-extra', 'pymongo', 'python-bsonjs'],
    keywords=['pip','ansible','mongodb']
    )