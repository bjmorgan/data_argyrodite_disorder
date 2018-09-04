configfile: 'snakemake_config.yaml'
from scripts import environment

runs = config['runs']
rdf_outputs = config['rdfs']['outputs']
diffusion_outputs = config['diffusion']['outputs']
sites_outputs = config['sites']['outputs']['inherent'] + config['sites']['outputs']['actual']

SYSTEMS = runs.keys()

all_outputs = rdf_outputs + diffusion_outputs + sites_outputs

rule all: 
    input: 
        expand( 'outputs/{system}/{output}', system=SYSTEMS, output=all_outputs ),
        'system_info.txt'

include: 'sites.smk'
include: 'diffusion.smk'
include: 'rdfs.smk'

rule environment:
    output: 'system_info.txt'
    run: environment.main( output='system_info.txt' )

rule clean:
    run:
        for system in SYSTEMS:
            for output in all_outputs:
                try:
                    os.remove( f'outputs/{system}/{output}' )
                except OSError:
                    pass
        try:
            os.remove( 'system_info.txt' )
        except:
            pass

