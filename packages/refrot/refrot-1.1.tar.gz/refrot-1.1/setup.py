from setuptools import setup

with open('README', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name = 'refrot',
    version = '1.1',
    author = 'Craig Howard',
    author_email = 'craig@seagrape.us',
    description = 'Verify website links',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = ['requests', 'lxml'],
    license = 'MIT',
    keywords = 'linkrot checker',
    url = 'https://seagrape.us/spider.html',
    scripts = ['refrot.py']
)
