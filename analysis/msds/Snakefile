import yaml
import snakemake

data_dir = '../../data'
figures_dir = '../../figures'
analysis_notebook = 'msds.ipynb'

def get_data_files():
    with open('../md_runs.yaml', 'r') as f:
        md_runs = yaml.safe_load(f)
    data_files = []
    for system in md_runs:
        for disorder, runs in md_runs[system].items():
            for i in runs:
                data_files.append(f'{data_dir}/{system}/{disorder}/run{i}/actual_XDATCAR.gz')
    return data_files
 
data_files = get_data_files()

output_figures = ['msd.pdf']

rule msds:
    input: data_files, analysis_notebook
    output: [f'{figures_dir}/{o}' for o in output_figures]
    log:
        notebook=f".logs/{analysis_notebook}"
    notebook: f"{analysis_notebook}"

rule clean:
    run:
        for figure in output_figures:
            shell(f'rm -f {figures_dir}/{figure}')
