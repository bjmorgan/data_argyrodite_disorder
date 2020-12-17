import yaml
import snakemake

data_dir = '../../data'
figures_dir = '../../figures'
      
def get_data_files():
    with open('../md_runs.yaml', 'r') as f:
        md_runs = yaml.safe_load(f)
    data_files = []
    for system in md_runs:
        for disorder, runs in md_runs[system].items():
            for i in runs:
                data_files.append(f'{data_dir}/{system}/{disorder}/run{i}/actual_XDATCAR.gz')
    return data_files
 
def get_dynamics_data_files():
    with open('../md_runs.yaml', 'r') as f:
        md_runs = yaml.safe_load(f)
    data_files = []
    system = 'Li6PS5I'
    disorder = '0p'
    for i in md_runs['Li6PS5I']['0p']:
        data_files.append(f'{data_dir}/{system}/{disorder}/run{i}/actual_XDATCAR.gz')
    return data_files
 
data_files = get_data_files()
dynamics_data_files = get_dynamics_data_files()

output_figures = ['polyhedra_types.pdf',
                  'Li6PS5I_octahedral_projection.pdf']

rule polyhedra_all:
    input: [f'{figures_dir}/{o}' for o in output_figures]
    
rule polyhedral_classification:
    input: data_files, 'polyhedral_classification.ipynb'
    output: f'{figures_dir}/polyhedra_types.pdf'
    log:
        notebook=".logs/polyhedral_classification.ipynb"
    notebook: 'polyhedral_classification.ipynb'

rule polyhedral_dynamics:
    input: dynamics_data_files, 'polyhedral_dynamics.ipynb'
    output: f'{figures_dir}/Li6PS5I_octahedral_projection.pdf'
    log:
        notebook=".logs/polyhedral_dynamics.ipynb"
    notebook: 'polyhedral_dynamics.ipynb'

rule clean:
    run:
        for figure in output_figures:
            shell(f'rm -f {figures_dir}/{figure}')
