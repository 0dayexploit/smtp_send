# smtp_send setup.py

from setuptools import setup

setup(
    name = 'smtp_send',
    packages = ['smtp_send'],
    version = '0.0.1.dev0',
    description = 'Simple smtp sending',
    author = 'Kord E.',
    author_email = 'e-kord@mail.ru',
    url = 'http://example.com',
    download_url = 'http://example.com',
    keywords = ['smtp', 'network'],
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: The MIT License (MIT)',
        'Operating System :: OS Independent'
    ],
    entry_points = {
        'console_scripts': ['smtp_send = smtp_send:main'],
    },
    test_suite='smtp_send.tests',
    long_description = '''\

Smtp sending messages.
README.md
------------------
'''
)

