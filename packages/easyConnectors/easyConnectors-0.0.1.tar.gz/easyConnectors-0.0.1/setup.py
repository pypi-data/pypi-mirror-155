from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='easyConnectors',
    version='0.0.1',
    description='This provide boiler plate code for connectors and its crud operations',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Lalitya Sawant',
    author_email='sawant.lalitya@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['connectors','postgress','crud','select','get','data'],
    packages=find_packages(),
    install_requires=['psycopg2']
)