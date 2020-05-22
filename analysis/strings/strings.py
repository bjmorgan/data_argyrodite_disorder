from collections import Counter
from copy import copy
import numpy as np

class String(object):
    
    def __init__(self, sites):
        self.sites = sites
        
    def __eq__(self, other):
        return self.sites == other.sites
    
    def __getitem__(self, index):
        return self.sites[index]
    
    def __iter__(self):
        yield self.sites
        
    def extend(self, other):
        assert(self[-1] == other[0])
        self.sites.extend( other[1:] )
        
    def is_closed(self):
        return self.sites[0] == self.sites[-1]
    
    def __len__(self):
        return np.unique(self.sites).shape[0]
    
class StringCollection(object):
    
    def __init__(self, strings, timestep=None):
        self.strings = strings
        self.merged_strings = merge_strings(strings)
        self.timestep = timestep
        
    def string_lengths(self):
        return [ len(s) for s in self.merged_strings ]

    def closed(self):
        return [ s.is_closed() for s in self.merged_strings ]
    
    def __add__(self, other):
        summed_string_data = copy(self)
        summed_string_data.strings = self.strings + other.strings
        summed_string_data.merged_strings = self.merged_strings + other.merged_strings
        return summed_string_data
    
    def __iadd__(self, other):
        return self + other
    
    def length_counter(self):
        return Counter(self.string_lengths())

def merge_strings(strings):
    """Merges strings with common end-members.
    
    Args:
        strings (list(String)): List of `String` objects.
        
    Returns:
        list(String): List of merged strings.
        
    """
    finished = False
    while not finished:
        finished = True
        for s1 in strings:
            for s2 in strings:
                if s1 == s2:
                    continue
                if s2[0] == s1[-1]:
                    s1.extend(s2)
                    strings.remove(s2)
                    finished = False
                    break
                elif s2[-1] == s1[0]:
                    s2.extend(s1)
                    strings.remove(s1)
                    finished = False
                    break
    return strings

def find_length_2_strings(dr_ij, cutoff=1.0):
    strings = []
    for i, dr_i in enumerate(dr_ij):
        if dr_i[i] < cutoff: # distance moved by atom i
            continue
        where = np.where(dr_i < cutoff )[0]
        if where.size > 0:
            strings.append(String(sites=[i, where[0]]))
    return strings