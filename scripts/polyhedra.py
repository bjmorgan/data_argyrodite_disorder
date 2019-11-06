#! /usr/bin/env python3

from pymatgen.io.vasp import Structure, Lattice
from polyhedral_analysis.polyhedra_recipe import PolyhedraRecipe, create_matching_site_generator
from polyhedral_analysis.trajectory import Trajectory

import numpy as np
import argparse
import pickle

def get_trajectory( xdatcar_filenames, verbose=False ):
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

    coordination_cutoff = 2.6
    vertex_graph_cutoff = 4.1
    lithium_indices = list(range(192))

    poly_recipes = [ PolyhedraRecipe( method='distance cutoff',
                                      coordination_cutoff=coordination_cutoff,  
                                      vertex_graph_cutoff=vertex_graph_cutoff, 
                                      central_atom_list_generator=s_4c_matching_sites, 
                                      coordination_atom_list=lithium_indices,
                                      label='4c' ),
                     PolyhedraRecipe( method='distance cutoff',
                                      coordination_cutoff=coordination_cutoff,  
                                      vertex_graph_cutoff=vertex_graph_cutoff, 
                                      central_atom_list_generator=s_4a_matching_sites, 
                                      coordination_atom_list=lithium_indices,
                                      label='4a' ) ]
    
    if verbose:
        print( 'Reading {} XDATCAR files'.format( len( xdatcar_filenames ) ) )
        for x in xdatcar_filenames:
            print( '- {}'.format(x) )
    trajectory = Trajectory.from_xdatcar( xdatcar_filenames[0], recipes=poly_recipes )
    if len( xdatcar_filenames > 1 ):
        for f in xdatcar_filenames[1:]:
            trajectory += Trajectory.from_xdatcar( f, recipes=poly_recipes )

    return trajectory

def pickle_trajectory( output, system, trajectory ):
    rdf_df.to_csv( '{}/{}/rdf.dat'.format(output,system), index=False, sep=' ', float_format='%.6f' )

def parse_args():
    parser = argparse.ArgumentParser( description='TODO' )
    parser.add_argument('system')
    parser.add_argument('nruns', nargs='+')
    parser.add_argument('--data', default='data')
    parser.add_argument('--output', default='outputs')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if args.verbose:
        print( 'Constructing polyhedra trajectories for {}'.format(args.system) )
    xdatcar_filenames = [ '{}/{}/run{}/inherent_XDATCAR.gz'.format( args.data, args.system, i ) for i in args.nruns ]
    trajectory = get_trajectory( xdatcar_filenames, 
                                 verbose=args.verbose )
    save_rdf_data( args.output, args.system, rdfs, labels )
    save_coordination_number_data( args.output, args.system, rdfs, labels )
