#! /usr/bin/env python3

from pymatgen.io.vasp import Xdatcar, Structure, Lattice
from pymatgen_diffusion.aimd.van_hove import RadialDistributionFunction
from polyhedral_analysis.polyhedra_recipe import create_matching_site_generator
import numpy as np
import pandas as pd
import multiprocessing as mp

from .utils import get_structures
from functools import partial

def species_in_structure( structure ):
    return set( [ site.specie.symbol for site in structure ] )

def reference_structure( ref_file, ref_species, supercell=None ):
    if not supercell:
        supercell = [1,1,1]
    structure = Structure.from_file( ref_file )
    species = species_in_structure( structure )
    species_to_remove = [ s for s in species if s not in ref_species ]
    structure.remove_species( species_to_remove )
    structure.make_supercell(supercell)
    return structure

def distances_per_structure( structure, ref_structures, species ):
    distance = [ [] for i in ref_structures ]
    spec_sites = [ s for s in structure.sites if str(s.specie) == species ]
    for ss in spec_sites:
        dr = [ min( ( ss.distance( site ) for site in ref_structure ) ) for ref_structure in ref_structures ]
        distance[ np.argmin(dr) ].append( min(dr) )
    return distance

def distances_to_sites( structures, ref_structures, species, verbose=True, cores=1 ):
    """
    Collect the minimum distances from ion positions in a series of structures
    to the sites in a reference structure.
    
    Args:
        structures (list(`pymatgen.Structure`)): List of pymatgen Structure objects, e.g. from a MD run.
        ref_structures (list`pymatgen.Structure`): List of pymatgen Structure, containing only the reference sites.
        species (str): Species string for which atoms to analyse from the input Structure objects.
        
    Returns:
        (list(float)): List of distances in Angstroms.
    """
    pool = mp.Pool(processes=cores)
    distance = [ [] for i in ref_structures ]
    p_distances_per_structure = partial( distances_per_structure, ref_structures=ref_structures, species=species )
    dist = pool.map( p_distances_per_structure, structures )
    for d_frame in dist:
        for a, b in zip( distance, d_frame ):
            a.append(b)
    return distance


def main( trajectory, system, nruns, data_dir, out_dir, 
          cores=1, bins=200, verbose=True ):
    if verbose:
        print( 'trajectory: {}'.format( trajectory ) )
        print( 'system: {}'.format( system ) )
        print( 'nruns: {}'.format( nruns ) )
    ref_structures = { '24g': reference_structure( '{}/reference_structures/Li6PS5I_Neutron.cif'.format( data_dir ),
                       'Mg', supercell=[2,2,2] ),
                       '48h': reference_structure( '{}/reference_structures/Li6PS5I_Neutron.cif'.format( data_dir ), 
                       'Li', supercell=[2,2,2] ) }
    xdatcar_filenames = [ '{}/{}/run{}/{}_XDATCAR'.format( data_dir, system, i, trajectory ) for i in nruns ]
    structures = get_structures( xdatcar_filenames )
    sites = list(ref_structures.keys())
    distances = {}
    hist = {}
    for s in sites:
        if verbose:
            print( 'Running distance to sites analysis for sites: {}'.format( s ) )
        distances[s] = distances_to_sites( structures, [ ref_structures[s] ], 'Li', cores=cores )
        hist[s] = np.histogram( distances[s], bins=bins, range=(0,2.0), density=True )
    dr = np.array( hist[sites[0]][1][1:] )
    data = np.array( [ hist[s][0] for s in sites ] )
# TODO: correct dr to midpoint of bins
    df = pd.DataFrame( np.vstack( ( dr, data ) ).T, columns=[ 'r' ] + sites )
    filename = '{}/{}/site_distances_{}.dat'.format( out_dir, system, trajectory )
    if verbose:
        print( 'Writing to {}'.format( filename ) )
    df.to_csv( filename, index=False, sep=' ' )
