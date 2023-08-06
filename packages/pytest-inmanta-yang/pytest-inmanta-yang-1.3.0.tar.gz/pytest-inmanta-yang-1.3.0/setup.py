"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
from pathlib import Path
from setuptools import find_packages, setup


setup(
    name="pytest-inmanta-yang",
    version="1.3.0",
    author="Inmanta NV",
    author_email="code@inmanta.com",
    license="Apache License, Version 2.0",
    description="Common fixtures used in inmanta yang related modules",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"pytest_inmanta_yang": ["resources/*.xml", "resources/*.cfg", "py.typed"]},
    include_package_data=False,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        "lxml",
        "ncclient",
        "pyang==2.5.3",  # Same version as the yang module
        "pytest",
        "ncdiff>=20.10",
        "requests",
        "scrapli",
        "paramiko",
        "inmanta-core",
        "pytest-inmanta",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={"pytest11": ["pytest-inmanta-yang = pytest_inmanta_yang"]},
)
