#!/usr/bin/env python
# coding: utf-8

# In[1]:



from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Calculate Primer Concentrations for RT-PCR'
LONG_DESCRIPTION = 'Calculates dilution coefficients based on measured concentrations for a desired molarity to be used in RT-PCR.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pccalc", 
        version=VERSION,
        author="Emma Courtney",
        author_email="<emmaclairecourtney@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

