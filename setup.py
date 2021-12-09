from setuptools import setup

# Define the CLI tool pyrepo as a python package running click, jinja2, and configparser
setup(
    name='pyrepo',
    version='1.0',
    py_modules=['templater'],
    install_requires=[
        'click', 'jinja2', 'configparser', 'wheel'
    ],
    entry_points='''
        [console_scripts]
        pyrepo=src.templater:main
    ''',
)