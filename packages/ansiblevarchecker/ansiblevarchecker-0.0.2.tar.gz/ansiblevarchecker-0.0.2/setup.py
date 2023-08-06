#!/usr/bin/env python
import re

from setuptools import setup, find_packages

__version__ = ''
with open('ansiblevarchecker/__init__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')

setup(
    name='ansiblevarchecker',
    version=__version__,
    description='Variable checker for ansible playbooks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='KlutzyBubbles',
    author_email='LTzilantois@gmail.com',
    url='https://github.com/KlutzyBubbles/ansible-var-checker',
    project_urls={
        'Documentation': 'https://ansible_var_checker.readthedocs.io',
        'Source': 'https://github.com/KlutzyBubbles/ansible-var-checker',
        'Issues': 'https://github.com/KlutzyBubbles/ansible-var-checker/issues',
    },
    packages=find_packages(include=['ansiblevarchecker', 'ansiblevarchecker.jinja', 'ansiblevarchecker.jinja.visitors', 'ansiblevarchecker.scope']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
    install_requires=[
        'ansible==2.9.*',
        'jinja2~=2.11',
        'six~=1.14',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': [
            'ansiblevarchecker = ansiblevarchecker:main'
        ]
    }
)
