"""
Kreveik
=======

Kreveik is a Python project that is meant to provide a codebase for research about evolution 
and dynamics of random boolean networks (RBNs).

Kreveik provides: 
    * Class definitions concerning Boolean Networks (BNs) an ensembles of them. 
    * Tools for working on and visualizing Boolean Networks.
    * Tools concerning Genetic Algorithms (GAs), such as mutations, fitness functions.
    * Tools enabling data extraction from processes such as Genetic Algorithms.
    * Tools for motif frequency analysis.

Available Subpackages
---------------------
classes
    class definitions used throughout the code.
        
family
    tools for creating and manipulating families, i.e. ensembles of networks

network
    tools for creating and manipulating networks.
    
probes
    probes, which are data extracting objects, for further data analysis.

genetic
    tools and functions concerning genetic algorithms in general.

"""

import classes
import family
import genetic
import network
import probes

__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil","Ayse Erzan","Burcin Danaci"]
__license__ = ""
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "mehmet.anil@colorado.edu"
__status__ = "Production"