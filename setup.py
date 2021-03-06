
#    Copyright 2012 Mehmet Ali ANIL
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#    http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

#from distribute_setup import use_setuptools
#use_setuptools()

from setuptools import setup, find_packages, Extension
import numpy

numpy_include = str(numpy.get_include())
module = Extension('kreveik.network.boolfuncs.boolfuncs_c', 
                   #extra_compile_args= ['-fopenmp'],
                   #extra_link_args=['-lgomp'],
                   sources = ['kreveik/network/boolfuncs/boolfuncs.c'], 
                   include_dirs=[numpy_include])

setup(
    name = "Kreveik",
    version = "0.6.0",
    packages = find_packages(),
    install_requires = ['docutils>=0.3','numpy>=1.5','matplotlib>=1.0'],

    package_data = {
        # If any package contains *.md files, include them:
        '': ['*.md','README'],
    },

    # metadata for upload to PyPI
    author = "Mehmet Ali Anil",
    author_email = "mehmet.ali.anil@ieee.org",
    description = "Kreveik is a Python module for Boolean networks. With Kreveik, one can create, investigate dynamics of, form families of random Boolean networks.",
    license = "LICENSE.txt",
    keywords = "random boolean networks genetic algorithm",
    url = "http://github.com/mehmetalianil/Kreveik/",    
    # project home page, if any

    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: Other/Proprietary License',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: C',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Physics'
          ],
      ext_modules = [module]

)
