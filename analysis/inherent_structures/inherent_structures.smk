import yaml
import snakemake

data_dir = '../../data'
figures_dir = '../../figures'
analysis_notebook = 'inherent_structure_comparison.ipynb'

def get_data_files():
    with open('../md_runs.yaml', 'r') as f:
        md_runs = yaml.safe_load(f)
    data_files = []
    to_get = {'Li6PS5I': '0p',
              'Li6PS5Cl': '50p'}
    for system, disorder in to_get.items():
        for i in md_runs[system][disorder]:
            data_files.append(f'{data_dir}/{system}/{disorder}/run{i}/inherent_XDATCAR.gz')
            data_files.append(f'{data_dir}/{system}/{disorder}/run{i}/actual_XDATCAR.gz')
    return data_files
 
data_files = get_data_files()

output_figures = ['raw_versus_inherent_trajectory.pdf']

rule inherent_structure_comparison:
    input: data_files, analysis_notebook
    output: [f'{figures_dir}/{o}' for o in output_figures]
    log:
        notebook=f".logs/{analysis_notebook}"
    notebook: f"{analysis_notebook}"

rule clean:
    run:
        for figure in output_figures:
            shell(f'rm -f {figures_dir}/{figure}')
