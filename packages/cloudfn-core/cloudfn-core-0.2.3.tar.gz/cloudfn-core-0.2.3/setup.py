"""cloudfn-core package config"""

from setuptools import setup
from setuptools import find_namespace_packages

PACKAGE_VERSION = '0.2.3'

setup(
	name='cloudfn-core',
	version=PACKAGE_VERSION,
	description='cloudfn-core',
	url='https://github.com/akrymskiy/cloudfn',
	author='Aleksandr Krymskiy',
	author_email='alex@krymskiy.net',
	license='MIT',
	packages=find_namespace_packages(include=['cloudfn', 'cloudfn.*']),
	install_requires=[],
	entry_points = {
		'console_scripts': ['cfn=cloudfn.core.cli:main'],
	},
	zip_safe=False,
	python_requires=">=3.9"
)
