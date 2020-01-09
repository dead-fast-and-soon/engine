
from setuptools import setup, find_packages

setup(
    name='konkyo',
    version='0.1',
    description='a game framework using pyglet',
    url='https://github.com/dead-fast-soon/engine',
    author='Branden Akana',
    author_email='branden.akana@gmail.com',
    project_urls={
        'Documentation': 'https://dead-fast-soon.github.io/engine/'
    },
    packages=find_packages(include=['konkyo', 'konkyo.*']),
)