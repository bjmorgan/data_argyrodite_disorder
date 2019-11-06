#! /usr/bin/env python3

from utils import flatten_list, get_structures, indices_by_species
from collections import Counter
import numpy as np

data = '../data'

def count_site_neighbours( site, structure, species, rcut ):
    neighbours = Counter()
    neighbours.update( { x:0 for x in species } )
    neighbours.update( [ s.specie.symbol for s, r in structure.get_neighbors( site=site, r=rcut ) ] )
    return neighbours

def count_neighbours( structures, rcut, central_site_species, neighbour_species, max_neighbour_count ):
    neighbour_counts = np.zeros((max_neighbour_count+1)**len( neighbour_species ))
    shape = [ max_neighbour_count+1 ]*len( neighbour_species )
    neighbour_counts = neighbour_counts.reshape( shape )
    n_central_site = len( [ site for site in structures[0]
                            if site.specie.symbol == central_site_species ] )
    normalisation_factor = len( structures ) * n_central_site
    for structure in structures:
        for site in structure:
            if site.specie.symbol == central_site_species:
                neighbours = count_site_neighbours( site, structure, neighbour_species, rcut )
                index = tuple( neighbours[spec] for spec in neighbour_species )
                neighbour_counts[index] += 1
    assert( normalisation_factor == neighbour_counts.sum() )
    return neighbour_counts / normalisation_factor

def main( system, nruns, central_species, neighbour_species, max_neighbour_count, rcut ):
    xdatcar_filenames = [ f'{data}/{system}/run{i}/inherent_XDATCAR.gz' for i in nruns ]
    structures = get_structures( xdatcar_filenames )
    count = count_neighbours( structures, rcut, central_species, neighbour_species, max_neighbour_count )
    print( count )

if __name__ == '__main__':
    system = 'Li6PS5I/50p'
    nruns = [ 1, 2, 3, 4, 5 ]
    central_species = 'Li'
    neighbour_species = [ 'S', 'I' ]
    max_neighbour_count = 4
    rcut =2.75
    main( system, nruns, central_species, neighbour_species, max_neighbour_count, rcut )
