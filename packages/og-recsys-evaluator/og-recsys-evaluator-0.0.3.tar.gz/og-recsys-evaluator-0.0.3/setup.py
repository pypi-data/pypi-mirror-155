from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Recsys Evaluator package'
LONG_DESCRIPTION = 'Recsys Evaluator package'

# Setting up
setup(
        name="og-recsys-evaluator", 
        version=VERSION,
        author="OG",
        author_email="blogphp.biz@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['surprise'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'evaluator'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)