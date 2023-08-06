import setuptools
import warnings
import sys
import glob

try:
	from sphinx.setup_command import BuildDoc
	cmdclass = {'build_sphinx': BuildDoc} #to build with sphinx
except ImportError:
	if sys.argv[1] == 'build_sphinx': warnings.warn("sphinx module not found: impossibile to build the documents")
	pass

required_packages =['numpy>=1.19.2', 'scipy>=1.4.0', 'tqdm>=4.41.1',
		'ray>=0.8.0', 'torch>=1.9.0', 'pycbc>=1.18.3']
#required_packages =[]

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="gengli",
	version="0.1.0",
	author="Melissa Lopez",
	author_email="m.lopez@uu.nl",
	maintainer = "Stefano Schmidt",
	maintainer_email = "s.schmidt@uu.nl",
	description="Glitch generation with Generative Adversarial Network",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://git.ligo.org/melissa.lopez/gengli",
	packages = setuptools.find_packages(),
	package_dir={'gengli': 'gengli','gengli.ctgan': 'gengli/ctgan' }, #Apparently this is understood and done by default :)
	package_data={'gengli.ctgan': ['weights/*G.pth']}, #The package data should be relative to the package dir!!
	#include_package_data = True, #This trash shouldn't be there! It conflicts with package_data option :)
		#this will install any file outside the package directory to a location starting from sys.prefix
	#data_files = [('gengli/ctgan/weights', glob.glob('gengli/ctgan/weights/*.pth'))],
	license = 'GNU GENERAL PUBLIC LICENSE v3',
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
	install_requires=required_packages,
	command_options={
        'build_sphinx': {
            'source_dir': ('setup.py', 'docs'),
            'build_dir': ('setup.py', 'docs/__build'),
            }},
)

