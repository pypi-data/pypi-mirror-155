#!/usr/bin/env python

from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="django-torque-enhanced-curation",
    version="0.1.0",
    description="django app for torque enhanced curation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Open Tech Strategies, LLC",
    author_email="frankduncan@opentechstrategies.com",  # For now, this works
    url="https://code.librehq.com/ots/mediawiki/enhanced-curation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    packages=["enhanced_curation"],
    install_requires=[
        "django-torque",
    ],
    package_dir={"": "."},
    python_requres=">=3.6",
)
