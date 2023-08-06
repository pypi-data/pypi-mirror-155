from setuptools import setup, find_packages

setup(
    name='certbot-dns-rockenstein',
    package='certbot_dns_rockenstein.py',
    version='0.0.2',
    description="rockenstein DNS Authenticator plugin for Certbot",
    url='https://www.rockenstein.de',
    author="Frank Mueller",
    author_email='fm@rockenstein.de',
    install_requires=[
        'certbot',
        'requests'
    ],
    entry_points={
        'certbot.plugins': [
            'certbot-dns-rockenstein = certbot_dns_rockenstein:Authenticator'
        ],
    },
    packages=find_packages(
        where='.',
        exclude=("tests", "etc", "logs",)
    ),
)
