from setuptools import setup, find_packages

setup(
    name='certbot-dns-rockenstein',
    version='0.0.6',
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
            'certbot-dns-rockenstein = certbot_dns_rockenstein.certbot_dns_rockenstein:Authenticator'
        ],
    },
    packages=find_packages(),
)
