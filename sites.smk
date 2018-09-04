import os
from scripts import site_assignments
from functools import partial

configfile: 'snakemake_config.yaml'

runs = config['runs']
sites_input_files = config['sites']['inputs']
sites_output = config['sites']['outputs']
data_dir = config['data_dir']
output_dir = config['output_dir']

def sites_exec( trajectory, system, disorder, cores, data_dir=data_dir, out_dir=output_dir ):
    nruns = runs[ '{}/{}'.format( system, disorder ) ]
    sys_str = '{}/{}'.format( system, disorder )
    site_assignments.main( trajectory=trajectory, system=sys_str, nruns=nruns, 
                           cores=cores, data_dir=data_dir, out_dir=output_dir )

SYSTEMS = runs.keys()

def sites_inputs( wildcards ):
    inputs = []
    for w in wildcards:
        print( w )
        for i in runs[w]:
            for d in sites_input_files:
                inputs.append( f'data{w}/run{i}/{d}' )
    return inputs

rule sites_all:
    input: 
        expand( 'outputs/{system}/{output}', system=SYSTEMS, output=sites_output['inherent'] ),
        expand( 'outputs/{system}/{output}', system=SYSTEMS, output=sites_output['actual'] )


rule sites_Li6PS5I_0p_inherent:
    input: expand( 'data/Li6PS5I/0p/run{n}/{input_file}', n=runs['Li6PS5I/0p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5I/0p/{output}', output=sites_output['inherent'] )
    threads: 32
    run:
        system = 'Li6PS5I'
        disorder = '0p'
        trajectory = 'inherent'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5I_50p_inherent:
    input: expand( 'data/Li6PS5I/50p/run{n}/{input_file}', n=runs['Li6PS5I/50p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5I/50p/{output}', output=sites_output['inherent'] )
    threads: 32
    run:
        system = 'Li6PS5I'
        disorder = '50p'
        trajectory = 'inherent'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5I_100p_inherent:
    input: expand( 'data/Li6PS5I/100p/run{n}/{input_file}', n=runs['Li6PS5I/100p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5I/100p/{output}', output=sites_output['inherent'] )
    threads: 32
    run:
        system = 'Li6PS5I'
        disorder = '100p'
        trajectory = 'inherent'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5Cl_0p_inherent:
    input: expand( 'data/Li6PS5Cl/0p/run{n}/{input_file}', n=runs['Li6PS5Cl/0p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5Cl/0p/{output}', output=sites_output['inherent'] )
    threads: 32
    run:
        system = 'Li6PS5Cl'
        disorder = '0p'
        trajectory = 'inherent'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5Cl_50p_inherent:
    input: expand( 'data/Li6PS5Cl/50p/run{n}/{input_file}', n=runs['Li6PS5Cl/50p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5Cl/50p/{output}', output=sites_output['inherent'] )
    threads: 32
    run:
        system = 'Li6PS5Cl'
        disorder = '50p'
        trajectory = 'inherent'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5Cl_100p_inherent:
    input: expand( 'data/Li6PS5Cl/100p/run{n}/{input_file}', n=runs['Li6PS5Cl/100p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5Cl/100p/{output}', output=sites_output['inherent'] )
    threads: 32
    run:
        system = 'Li6PS5Cl'
        disorder = '100p'
        trajectory = 'inherent'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5I_0p_actual:
    input: expand( 'data/Li6PS5I/0p/run{n}/{input_file}', n=runs['Li6PS5I/0p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5I/0p/{output}', output=sites_output['actual'] )
    threads: 32
    run:
        system = 'Li6PS5I'
        disorder = '0p'
        trajectory = 'actual'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5I_50p_actual:
    input: expand( 'data/Li6PS5I/50p/run{n}/{input_file}', n=runs['Li6PS5I/50p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5I/50p/{output}', output=sites_output['actual'] )
    threads: 32
    run:
        system = 'Li6PS5I'
        disorder = '50p'
        trajectory = 'actual'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5I_100p_actual:
    input: expand( 'data/Li6PS5I/100p/run{n}/{input_file}', n=runs['Li6PS5I/100p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5I/100p/{output}', output=sites_output['actual'] )
    threads: 32
    run:
        system = 'Li6PS5I'
        disorder = '100p'
        trajectory = 'actual'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5Cl_0p_actual:
    input: expand( 'data/Li6PS5Cl/0p/run{n}/{input_file}', n=runs['Li6PS5Cl/0p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5Cl/0p/{output}', output=sites_output['actual'] )
    threads: 32
    run:
        system = 'Li6PS5Cl'
        disorder = '0p'
        trajectory = 'actual'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5Cl_50p_actual:
    input: expand( 'data/Li6PS5Cl/50p/run{n}/{input_file}', n=runs['Li6PS5Cl/50p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5Cl/50p/{output}', output=sites_output['actual'] )
    threads: 32
    run:
        system = 'Li6PS5Cl'
        disorder = '50p'
        trajectory = 'actual'
        sites_exec( trajectory, system, disorder, threads )

rule sites_Li6PS5Cl_100p_actual:
    input: expand( 'data/Li6PS5Cl/100p/run{n}/{input_file}', n=runs['Li6PS5Cl/100p'], input_file=sites_input_files['inherent'] )
    output: expand( 'outputs/Li6PS5Cl/100p/{output}', output=sites_output['actual'] )
    threads: 32
    run:
        system = 'Li6PS5Cl'
        disorder = '100p'
        trajectory = 'actual'
        sites_exec( trajectory, system, disorder, threads )

rule sites_clean:
    run:
        for system in SYSTEMS:
            for output in sites_output['inherent'] + sites_output['actual']:
                try:
                    os.remove( f'outputs/{system}/{output}' )
                except OSError:
                    pass

