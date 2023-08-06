from matplotlib.pyplot import cla
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='thanhtungcalculator',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('README.txt').read()+'\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Thanh Tung',
    author_email='thanhtung247@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['']

)
