from setuptools import find_packages
from setuptools import setup


def read(file):
    with open(file) as f:
        return f.read()


setup(
    name='ustick',
    version='0.1',
    url='https://github.com/hexpizza/ustick',
    author='Sergey Koryagin',
    author_email='skoryagin96@gmail.com',
    description='Tool for creating console stickers',
    long_description=read("README.md"),
    install_requires=['colorama', 'docopt', 'PyYAML', 'termcolor', 'textwrap3'],
    packages=find_packages(),
    entry_points={
        'console_scripts':
            [
                'ustick = ustick.ustick:main'
            ]
    }
)
