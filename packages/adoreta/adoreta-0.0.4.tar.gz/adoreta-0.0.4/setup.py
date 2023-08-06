from setuptools import setup

setup(
    name='adoreta',
    version='0.0.4',
    description='Simple Logging using CSV',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='GNU GPLv3',
    author="Ansari Akram",
    author_email='ansariakramobaid@gmail.com',
    packages=['adoreta'],
    url='https://github.com/ansari-akram/adoreta',
    keywords='log',
    install_requires=[
        'prettytable',
    ],
)