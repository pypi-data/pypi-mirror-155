from setuptools import setup, find_packages

VERSION = '0.1.5' 
DESCRIPTION = 'Scripture (Word) Visualization'
LONG_DESCRIPTION = 'Package to provide API for the Holy Scripture visualization'

# Setting up
setup(
       # the name must match the folder name 'wordjc'
        name="wordjc", 
        version=VERSION,
        author="Johnny Cheng",
        author_email="<drjohnnycheng@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas'], # add any additional packages that 
        # needs to be installed along with your package.

		include_package_data=True,
		package_dir={"": "."},

        keywords=['word', 'scripture', 'visualization'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
