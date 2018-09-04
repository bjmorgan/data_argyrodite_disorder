import os

configfile: 'snakemake_config.yaml'

runs = config['runs']
rdf_input_files = config['rdfs']['inputs']
rdf_outputs = config['rdfs']['outputs']

exec = 'scripts/rdfs.py'

SYSTEMS = runs.keys()

def rdf_inputs( wildcards ):
    inputs = []
    for w in wildcards:
        print( w )
        for i in runs[w]:
            for d in rdf_input_files:
                inputs.append( f'data{w}/run{i}/{d}' )
    return inputs

rule rdfs_all:
    input: expand( 'outputs/{system}/{output}', system=SYSTEMS, output=rdf_outputs )

rule rdf_Li6PS5I_0p:
    input: expand( 'data/Li6PS5I/0p/run{n}/{input_file}', n=runs['Li6PS5I/0p'], input_file=rdf_input_files )
    output: expand( 'outputs/Li6PS5I/0p/{output}', output=rdf_outputs )
    threads: 6
    run:
        system = 'Li6PS5I'
        disorder = '0p'
        x_species = 'I'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {x_species} {nruns} --nprocs {threads} --verbose' )

rule rdf_Li6PS5I_50p:
    input: expand( 'data/Li6PS5I/50p/run{n}/{input_file}', n=runs['Li6PS5I/50p'], input_file=rdf_input_files )
    output: expand( 'outputs/Li6PS5I/50p/{output}', output=rdf_outputs )
    threads: 6
    run:
        system = 'Li6PS5I'
        disorder = '50p'
        x_species = 'I'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {x_species} {nruns} --nprocs {threads} --verbose' )

rule rdf_Li6PS5I_100p:
    input: expand( 'data/Li6PS5I/100p/run{n}/{input_file}', n=runs['Li6PS5I/100p'], input_file=rdf_input_files )
    output: expand( 'outputs/Li6PS5I/100p/{output}', output=rdf_outputs )
    threads: 6
    run:
        system = 'Li6PS5I'
        disorder = '100p'
        x_species = 'I'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {x_species} {nruns} --nprocs {threads} --verbose' )

rule rdf_Li6PS5Cl_0p:
    input: expand( 'data/Li6PS5Cl/0p/run{n}/{input_file}', n=runs['Li6PS5Cl/0p'], input_file=rdf_input_files )
    output: expand( 'outputs/Li6PS5Cl/0p/{output}', output=rdf_outputs )
    threads: 6
    run:
        system = 'Li6PS5Cl'
        disorder = '0p'
        x_species = 'Cl'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {x_species} {nruns} --nprocs {threads} --verbose' )

rule rdf_Li6PS5Cl_50p:
    input: expand( 'data/Li6PS5Cl/50p/run{n}/{input_file}', n=runs['Li6PS5Cl/50p'], input_file=rdf_input_files )
    output: expand( 'outputs/Li6PS5Cl/50p/{output}', output=rdf_outputs )
    threads: 6
    run:
        system = 'Li6PS5Cl'
        disorder = '50p'
        x_species = 'Cl'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {x_species} {nruns} --nprocs {threads} --verbose' )

rule rdf_Li6PS5Cl_100p:
    input: expand( 'data/Li6PS5Cl/100p/run{n}/{input_file}', n=runs['Li6PS5Cl/100p'], input_file=rdf_input_files )
    output: expand( 'outputs/Li6PS5Cl/100p/{output}', output=rdf_outputs )
    threads: 6
    run:
        system = 'Li6PS5Cl'
        disorder = '100p'
        x_species = 'Cl'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {x_species} {nruns} --nprocs {threads} --verbose' )

rule rdf_clean:
    run:
        for system in SYSTEMS:
            for output in rdf_outputs:
                try:
                    os.remove( f'outputs/{system}/{output}' )
                except OSError:
                    pass

