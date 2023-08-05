import setuptools
from setuptools import setup

setup(
    name='ButtonRequest-APIv1',
    version='1.0.2',
    url='',
    license='MIT',
    author='Yau Ming Leung',
    author_email='ymleung918@gmail.com',
    description='Button Request API v1 for Python',
    install_requires=[
        'requests==2.27.1',
        'urllib3',
        'jsons'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r").read()
)




