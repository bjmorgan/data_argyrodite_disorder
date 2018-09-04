#! /usr/bin/env python3

from pymatgen.io.vasp import Structure, Lattice
from pymatgen_diffusion.aimd.van_hove import RadialDistributionFunction
from polyhedral_analysis.polyhedra_recipe import create_matching_site_generator

from functools import partial
import numpy as np
import pandas as pd
import argparse
import multiprocessing as mp

from utils import flatten_list, get_structures, indices_by_species

def generate_rdf( reference_indices, indices, structures, rdf_params ):
    return RadialDistributionFunction( structures, indices=indices, 
               reference_indices=reference_indices, **rdf_params )

def generate_rdf_wrapped( params, structures, rdf_params, verbose=False ):
    if verbose:
        print( 'Calculating RDF {}'.format( params[0] ) )
    rdf = generate_rdf( reference_indices=params[1], indices=params[2],
                         structures=structures, rdf_params=rdf_params )
    return rdf

def get_rdfs( xdatcar_filenames, x_spec, nprocs, rdf_params=None, verbose=False ):
    if verbose:
        print( 'Initialising' )
    # Create reference structures containing ideal 4c and 4a sites in 2x2x2 supercells.
    ## define a 2x2x2 cell of 4c sites
    coords_4c = np.array( [ [ 0.25, 0.25, 0.75 ],
                            [ 0.75, 0.25, 0.25 ],
                            [ 0.25, 0.75, 0.25 ],
                            [ 0.75, 0.75, 0.75 ] ] )
    atom_list = [ 'S' ] * len( coords_4c )
    lattice = Lattice.from_parameters( a=3.0, b=3.0, c=3.0, alpha=90, beta=90, gamma=90 )
    structure = Structure( lattice, atom_list, coords_4c )
    reference_structure_4c = structure * [ 2, 2, 2 ]
    ## define a 2x2x2 cell of 4a sites
    coords_4a = np.array( [ [ 0.0, 0.0, 0.0 ],
                            [ 0.5, 0.5, 0.0 ],
                            [ 0.0, 0.5, 0.5 ],
                            [ 0.5, 0.0, 0.5 ] ] )
    atom_list = [ 'S' ] * len( coords_4a )
    lattice = Lattice.from_parameters( a=3.0, b=3.0, c=3.0, alpha=90, beta=90, gamma=90 )
    structure = Structure( lattice, atom_list, coords_4a )
    reference_structure_4a = structure * [ 2, 2, 2 ]

    reference_structures = { '4c': reference_structure_4c, 
                             '4a': reference_structure_4a }

    s_4c_matching_sites = create_matching_site_generator( reference_structure=reference_structure_4c, species=['S'] )
    s_4a_matching_sites = create_matching_site_generator( reference_structure=reference_structure_4a, species=['S'] )

    if verbose:
        print( 'Reading {} XDATCAR files'.format( len( xdatcar_filenames ) ) )
        for x in xdatcar_filenames:
            print( '- {}'.format(x) )
    structures = get_structures( xdatcar_filenames )

    # Find indices of S/Cl atoms closest to 4c/4a crystallographic sites
    li_indices = indices_by_species( structures[0], 'Li' )
    s_indices = indices_by_species( structures[0], 'S' )
    x_indices = indices_by_species( structures[0], x_spec )

    s_4c_indices = s_4c_matching_sites( structures[0], species='S' )
    s_4a_indices = s_4a_matching_sites( structures[0], species='S' )
    x_4c_indices = s_4c_matching_sites( structures[0], species=x_spec )
    x_4a_indices = s_4a_matching_sites( structures[0], species=x_spec )
    
    rdf_indices = { 'Li-Li': [ li_indices, li_indices ],
                    'S_4c-Li': [ s_4c_indices, li_indices ],
                    'S_4a-Li': [ s_4a_indices, li_indices ],
                    '{}_4c-Li'.format( x_spec ): [ x_4c_indices, li_indices ],
                    '{}_4a-Li'.format( x_spec ): [ x_4a_indices, li_indices ],
                    'Li-S': [ li_indices, s_indices ],
                    'Li-{}'.format( x_spec ): [ li_indices, x_indices ] }

    if not rdf_params:
        rdf_params = { 'rmax': 5.0,
                       'sigma': 0.01,
                       'ngrid': 501 }

    pool = mp.Pool(processes=nprocs)
    indices = [ list(v) for v in rdf_indices.values() ]
    labels = [ k for k in rdf_indices.keys() ]
    params = [ [ l ] + i for l, i in zip( labels, indices ) ]
    p_generate_rdf = partial( generate_rdf_wrapped, structures=structures, rdf_params=rdf_params, verbose=verbose )
    rdfs = pool.map( p_generate_rdf, params )
    return labels, rdfs

def save_rdf_data( output, system, rdfs, labels ):
    data = np.vstack( [ rdfs[0].interval ] + [ r.rdf for r in rdfs ] ).T
    columns = [ 'r' ] + labels
    rdf_df = pd.DataFrame( data, columns=columns )
    rdf_df.to_csv( '{}/{}/rdf.dat'.format(output,system), index=False, sep=' ', float_format='%.6f' )

def save_coordination_number_data( output, system, rdfs, labels ):
    data = np.vstack( [ rdfs[0].interval ] + [ r.coordination_number for r in rdfs ] ).T
    columns = [ 'r' ] + labels
    rdf_df = pd.DataFrame( data, columns=columns )
    rdf_df.to_csv( '{}/{}/coordination_numbers.dat'.format(output,system), index=False, sep=' ', float_format='%.6f' )

def parse_args():
    parser = argparse.ArgumentParser( description='TODO' )
    parser.add_argument('system')
    parser.add_argument('x_spec')
    parser.add_argument('nruns', nargs='+')
    parser.add_argument('-n', '--nprocs', type=int, default=1 )
    parser.add_argument('--sigma', type=float, default=0.01 )
    parser.add_argument('--rmax', type=float, default=5.0 )
    parser.add_argument('--ngrid', type=int, default=501 )
    parser.add_argument('--data', default='data')
    parser.add_argument('--output', default='outputs')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if args.verbose:
        print( 'RDF calculation for {}'.format(args.system) )
    rdf_params = { 'sigma': args.sigma,
                   'rmax': args.rmax,
                   'ngrid': args.ngrid }
    xdatcar_filenames = [ '{}/{}/run{}/inherent_XDATCAR'.format( args.data, args.system, i ) for i in args.nruns ]
    labels, rdfs = get_rdfs( xdatcar_filenames, 
                             x_spec=args.x_spec, 
                             nprocs=args.nprocs,
                             rdf_params=rdf_params,
                             verbose=args.verbose )
    save_rdf_data( args.output, args.system, rdfs, labels )
    save_coordination_number_data( args.output, args.system, rdfs, labels )
