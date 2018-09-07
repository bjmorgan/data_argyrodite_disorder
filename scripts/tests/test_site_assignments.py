import unittest
from unittest.mock import patch, Mock, MagicMock
from pymatgen.core.structure import Structure
from pymatgen.core.sites import Site
from .. import site_assignments

class TestSiteAssignments( unittest.TestCase ):

    def test_species_in_structure( self ):
        symbols = [ 'A', 'B' ]
        mock_sites = [ Mock( spec=Site ), Mock( spec=Site ) ]
        for m, s in zip( mock_sites, symbols ):
            m.specie = Mock()
            m.specie.symbol = s
        mock_structure = MagicMock( spec=Structure )
        mock_structure.__iter__.return_value = mock_sites
        self.assertEqual( site_assignments.species_in_structure( mock_structure ), set( symbols ) )
        
if __name__ == '__main__':
    unittest.main()
