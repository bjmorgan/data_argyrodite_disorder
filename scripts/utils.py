from pymatgen.io.vasp import Xdatcar

def flatten_list( this_list ):
    return [ item for sublist in this_list for item in sublist ]

def get_structures( xdatcar_filenames ):
    xdatcars = ( Xdatcar( f ) for f in xdatcar_filenames )
    return flatten_list( [ x.structures for x in xdatcars ] )

def indices_by_species( structure, species ):
    return [j for j, site in enumerate(structure) if site.specie.symbol == species]
