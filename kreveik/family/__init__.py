
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

"""
family package
==============

This package includes functions that act on family objects (kreveik.classes.Family)

Modules
-------
killer
    Houses functions that kill a portion of a population.
    
Functions
---------
motif_freqs
    Extracts motif frequencies of a population
    
mean connectivity
    Returns the mean value of the connectivity of a population.
"""

import killer
from motifs import motif_freqs

def mean_connectivity(family):
    """
    The mean connectivity of a Family of networks is returned.
    """
    #[network.network for network in family]
    pass

    