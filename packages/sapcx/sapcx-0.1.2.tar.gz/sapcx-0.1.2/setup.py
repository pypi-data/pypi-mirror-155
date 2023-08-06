import setuptools
import pathlib

cwd = pathlib.Path(__file__).parent
requirements = (cwd / 'requirements.txt').read_text().split("\n")

short_description = 'CLI Utility for SAP CX (Hybris) developers'
long_description = ''
with open('README.md', 'r') as fd:
    long_description = fd.read()

setuptools.setup(
    name='sapcx',
    packages=setuptools.find_packages(),
    version='0.1.2',
    entry_points={'console_scripts': ['sap = src.main:main']},
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ablil',
    author_email='ablil@protonmail.com',
    license='MIT',
    url='https://github.com/ablil/sapcx',
    install_requires=requirements,
    python_requires='>3.2',
)
