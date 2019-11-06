import os

configfile: 'snakemake_config.yaml'

runs = config['runs']
polyhedra_input_files = config['polyhedra']['inputs']
polyhedra_outputs = config['polyhedra']['outputs']

exec = 'scripts/polyhedra.py'

SYSTEMS = runs.keys()

def polyhedra_inputs( wildcards ):
    inputs = []
    for w in wildcards:
        print( w )
        for i in runs[w]:
            for d in polyhedra_input_files:
                inputs.append( f'data{w}/run{i}/{d}' )
    return inputs

rule polyhedra_all:
    input: expand( 'outputs/{system}/{output}', system=SYSTEMS, output=polyhedra_outputs )

rule polyhedra_Li6PS5I_0p:
    input: expand( 'data/Li6PS5I/0p/run{n}/{input_file}', n=runs['Li6PS5I/0p'], input_file=polyhedra_input_files )
    output: expand( 'outputs/Li6PS5I/0p/{output}', output=polyhedra_outputs )
    run:
        system = 'Li6PS5I'
        disorder = '0p'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {nruns} --verbose' )

rule polyhedra_Li6PS5I_50p:
    input: expand( 'data/Li6PS5I/50p/run{n}/{input_file}', n=runs['Li6PS5I/50p'], input_file=polyhedra_input_files )
    output: expand( 'outputs/Li6PS5I/50p/{output}', output=polyhedra_outputs )
    run:
        system = 'Li6PS5I'
        disorder = '50p'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {nruns} --verbose' )

rule polyhedra_Li6PS5I_100p:
    input: expand( 'data/Li6PS5I/100p/run{n}/{input_file}', n=runs['Li6PS5I/100p'], input_file=polyhedra_input_files )
    output: expand( 'outputs/Li6PS5I/100p/{output}', output=polyhedra_outputs )
    run:
        system = 'Li6PS5I'
        disorder = '100p'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {nruns} --verbose' )

rule polyhedra_Li6PS5Cl_0p:
    input: expand( 'data/Li6PS5Cl/0p/run{n}/{input_file}', n=runs['Li6PS5Cl/0p'], input_file=polyhedra_input_files )
    output: expand( 'outputs/Li6PS5Cl/0p/{output}', output=polyhedra_outputs )
    run:
        system = 'Li6PS5Cl'
        disorder = '0p'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {nruns} --verbose' )

rule polyhedra_Li6PS5Cl_50p:
    input: expand( 'data/Li6PS5Cl/50p/run{n}/{input_file}', n=runs['Li6PS5Cl/50p'], input_file=polyhedra_input_files )
    output: expand( 'outputs/Li6PS5Cl/50p/{output}', output=polyhedra_outputs )
    run:
        system = 'Li6PS5Cl'
        disorder = '50p'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {nruns} --verbose' )

rule polyhedra_Li6PS5Cl_100p:
    input: expand( 'data/Li6PS5Cl/100p/run{n}/{input_file}', n=runs['Li6PS5Cl/100p'], input_file=polyhedra_input_files )
    output: expand( 'outputs/Li6PS5Cl/100p/{output}', output=polyhedra_outputs )
    run:
        system = 'Li6PS5Cl'
        disorder = '100p'
        nruns = ' '.join( [ str(i) for i in runs[ '{}/{}'.format( system, disorder ) ] ] )
        shell( f'{exec} {system}/{disorder} {nruns} --verbose' )

rule polyhedra_clean:
    run:
        for system in SYSTEMS:
            for output in polyhedra_outputs:
                try:
                    os.remove( f'outputs/{system}/{output}' )
                except OSError:
                    pass

