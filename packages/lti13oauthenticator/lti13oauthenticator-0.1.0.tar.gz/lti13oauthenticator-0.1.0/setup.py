#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.bdist_egg import bdist_egg

class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg
    Prevents setup.py install from performing setuptools' default easy_install,
    which it should never ever do.
    """

    def run(self):
        sys.exit(
            "Aborting implicit building of eggs. Use `pip install .` to install from source."
        )

here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(os.path.join(here, 'lti13oauthenticator', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name                = 'lti13oauthenticator',
    packages            = find_packages(),
    version             = version_ns['__version__'],
    description         = "LTI13OAuthenticator: Authenticate JupyterHub users with common LTI1.3 providers",
    long_description    = open("README.md").read(),
    long_description_content_type = "text/markdown",
    author              = "Jupyter Development Team",
    author_email        = "jupyter@googlegroups.com",
    url                 = "https://jupyter.org",
    license             = "BSD",
    platforms           = "Linux, Mac OS X",
    keywords            = ['Interactive', 'Interpreter', 'Shell', 'Web'],
    python_requires     = ">=3.6",
    entry_points={
        'jupyterhub.authenticators': [
            'lti13 = lti13oauthenticator.lti13:LTI13OAuthenticator',
        ],
    },
    classifiers         = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

setup_args['install_requires'] = ["jupyterhub>=0.5","oauthenticator>0.12","pyjwt"]

def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
