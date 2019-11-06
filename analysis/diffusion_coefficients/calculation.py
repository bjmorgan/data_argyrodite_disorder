import pandas as pd
import yaml
import numpy as np
from pymatgen.analysis.diffusion_analyzer import DiffusionAnalyzer
from pymatgen.io.vasp import Xdatcar, Poscar
from pymatgen_diffusion.aimd.pathway import ProbabilityDensityAnalysis
import os

class Calculation:

    def __init__( self, system, disorder, data_dir, runs, da_params ):
        self.system = system
        self.disorder = disorder
        self.runs = runs
        self.data_dir = data_dir
        self.da_params = da_params
        self.load_da_inherent()
        self.load_da_actual()
        self._inherent_pda = None
        self._actual_pda = None

    @property
    def md_data_dir( self ):
        return os.path.join( self.data_dir, self.system, self.disorder )

    @property
    def output_dir( self ):
        return '.'

    def load_da_inherent( self ):
        xdatcar_list = [ Xdatcar( f'{self.md_data_dir}/run{i}/inherent_XDATCAR.gz' ) for i in self.runs ]
        structures = [ s for xdatcar in xdatcar_list for s in xdatcar.structures ]
        self.da_inherent = DiffusionAnalyzer.from_structures( structures, **self.da_params )

    def load_da_actual( self ):
        xdatcar_list = [ Xdatcar( f'{self.md_data_dir}/run{i}/actual_XDATCAR.gz' ) for i in self.runs ]
        structures = [ s for xdatcar in xdatcar_list for s in xdatcar.structures ]
        self.da_actual = DiffusionAnalyzer.from_structures( structures, **self.da_params )

    @property
    def output_data( self ):
        data = {}
        data[ 'system' ] = self.system
        data[ 'disorder' ] = self.disorder
        data[ 'runs' ] = self.runs
        data[ 'inherent_diffusivity' ] = float( str( self.da_inherent.diffusivity ) )
        data[ 'actual_diffusivity' ] = float( str( self.da_actual.diffusivity ) )
        data[ 'inherent_conductivity' ] = float( str( self.da_inherent.conductivity ) )
        data[ 'actual_conductivity' ] = float( str( self.da_actual.conductivity ) )
        data[ 'inherent_max_displacement' ] = float( str( np.max( self.da_inherent.max_ion_displacements ) ) )
        data[ 'actual_max_displacement' ] = float( str( np.max( self.da_actual.max_ion_displacements ) ) )
        return data
    
    def save_data( self, filename='data.yaml' ):
        with open( f'{self.output_dir}/{filename}', 'w' ) as f:
            f.write( f'# {self.system} {self.disorder} {self.runs}\n' )
            yaml.dump( self.output_data, f )

    def save_msd( self, filename='msd.dat' ):
        msd_data = np.vstack( [ self.da_actual.dt/1000.0,
                                self.da_inherent.msd,
                                self.da_inherent.mscd,
                                self.da_actual.msd,
                                self.da_actual.mscd ] ).T
        columns = [ 'time', 'inherent MSD', 'inherent MSCD', 'actual MSD', 'actual MSCD' ]
        df = pd.DataFrame( msd_data, columns=columns )
        df.to_csv( f'{self.output_dir}/{filename}' )

    def construct_inherent_pda( self ):
        self._inherent_pda = ProbabilityDensityAnalysis.from_diffusion_analyzer( self.da_inherent )

    def construct_actual_pda( self ):
        self._actual_pda = ProbabilityDensityAnalysis.from_diffusion_analyzer( self.da_actual )

    @property
    def inherent_pda( self ):
        if not self._inherent_pda:
            self.construct_inherent_pda()
        return self._inherent_pda

    @property
    def actual_pda( self ):
        if not self._actual_pda:
            self.construct_actual_pda()
        return self._actual_pda

    def save_inherent_density( self, filename='Li_density.vasp' ):
        self.inherent_pda.to_chgcar(filename=f'{self.output_dir}/{filename}')

    def save_stable_site_cif( self, filename='full_structure.cif', d_cutoff=0.6, p_ratio=0.2 ):
        self.inherent_pda.generate_stable_sites(d_cutoff=d_cutoff, p_ratio=p_ratio)
        self.inherent_pda.get_full_structure().to(filename=f'{self.output_dir}/{filename}')
