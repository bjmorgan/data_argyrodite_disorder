import os
from scripts import diffusion_analysis

configfile: 'snakemake_config.yaml'
runs = config['runs']
diffusion_input_files = config['diffusion']['inputs']
diffusion_outputs = config['diffusion']['outputs']

SYSTEMS = runs.keys()

def diffusion_inputs( wildcards ):
    inputs = []
    for w in wildcards:
        print( w )
        for i in runs[w]:
            for d in diffusion_input_files:
                inputs.append( f'data{w}/run{i}/{d}' )
    return inputs

rule diffusion_all:
    input: expand( 'outputs/{system}/{output}', system=SYSTEMS, output=diffusion_outputs )

rule diffusion_Li6PS5I_0p:
    input: expand( 'data/Li6PS5I/0p/run{n}/{input_file}', n=runs['Li6PS5I/0p'], input_file=diffusion_input_files )
    output: expand( 'outputs/Li6PS5I/0p/{output}', output=diffusion_outputs )
    run:
        system = 'Li6PS5I'
        disorder = '0p'
        nruns = runs[ '{}/{}'.format( system, disorder ) ]
        diffusion_analysis.main( system=system, disorder=disorder, runs=nruns )
    
rule diffusion_Li6PS5I_50p:
    input: expand( 'data/Li6PS5I/50p/run{n}/{input_file}', n=runs['Li6PS5I/50p'], input_file=diffusion_input_files )
    output: expand( 'outputs/Li6PS5I/50p/{output}', output=diffusion_outputs )
    run:
        system = 'Li6PS5I'
        disorder = '50p'
        nruns = runs[ '{}/{}'.format( system, disorder ) ]
        diffusion_analysis.main( system=system, disorder=disorder, runs=nruns )

rule diffusion_Li6PS5I_100p:
    input: expand( 'data/Li6PS5I/100p/run{n}/{input_file}', n=runs['Li6PS5I/100p'], input_file=diffusion_input_files )
    output: expand( 'outputs/Li6PS5I/100p/{output}', output=diffusion_outputs )
    run:
        system = 'Li6PS5I'
        disorder = '100p'
        nruns = runs[ '{}/{}'.format( system, disorder ) ]
        diffusion_analysis.main( system=system, disorder=disorder, runs=nruns )

rule diffusion_Li6PS5Cl_0p:
    input: expand( 'data/Li6PS5Cl/0p/run{n}/{input_file}', n=runs['Li6PS5Cl/0p'], input_file=diffusion_input_files )
    output: expand( 'outputs/Li6PS5Cl/0p/{output}', output=diffusion_outputs )
    run:
        system = 'Li6PS5Cl'
        disorder = '0p'
        nruns = runs[ '{}/{}'.format( system, disorder ) ]
        diffusion_analysis.main( system=system, disorder=disorder, runs=nruns )

rule diffusion_Li6PS5Cl_50p:
    input: expand( 'data/Li6PS5Cl/50p/run{n}/{input_file}', n=runs['Li6PS5Cl/50p'], input_file=diffusion_input_files )
    output: expand( 'outputs/Li6PS5Cl/50p/{output}', output=diffusion_outputs )
    run:
        system = 'Li6PS5Cl'
        disorder = '50p'
        nruns = runs[ '{}/{}'.format( system, disorder ) ]
        diffusion_analysis.main( system=system, disorder=disorder, runs=nruns )

rule diffusion_Li6PS5Cl_100p:
    input: expand( 'data/Li6PS5Cl/100p/run{n}/{input_file}', n=runs['Li6PS5Cl/100p'], input_file=diffusion_input_files )
    output: expand( 'outputs/Li6PS5Cl/100p/{output}', output=diffusion_outputs )
    run:
        system = 'Li6PS5Cl'
        disorder = '100p'
        nruns = runs[ '{}/{}'.format( system, disorder ) ]
        diffusion_analysis.main( system=system, disorder=disorder, runs=nruns )

rule diffusion_clean:
    run:
        for system in SYSTEMS:
            for output in diffusion_outputs:
                try:
                    os.remove( f'outputs/{system}/{output}' )
                except OSError:
                    pass


