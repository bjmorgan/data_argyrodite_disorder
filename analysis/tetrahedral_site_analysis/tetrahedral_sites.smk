import yaml
import snakemake

data_dir = '../../data'
figures_dir = '../../figures'
analysis_notebooks = ['tetrahedral_site_occupations.ipynb',
                      'tetrahedral_site_transition_probabilities.ipynb',
                      'tetrahedral_site_positions.ipynb',
                      'inherent_structure_site_comparison.ipynb']

def get_data_files():
    with open('../md_runs.yaml', 'r') as f:
        md_runs = yaml.safe_load(f)
    data_files = []
    for system in md_runs:
        for disorder, runs in md_runs[system].items():
            for i in runs:
                data_files.append(f'{data_dir}/{system}/{disorder}/run{i}/actual_XDATCAR.gz')
    return data_files

def get_comparison_data_files():
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
comparison_data_files = get_comparison_data_files()

output_figures = ['tetrahedral_site_populations.pdf',
                  'transition_matrices.pdf',
                  'site_rdf.pdf',
                  'inherent_vs_actual_sites_comparison.pdf']

rule tetrahedral_sites_all:
    input: [f'{figures_dir}/{o}' for o in output_figures]
    
rule tetrahedral_site_occupations:
    input: data_files, 'tetrahedral_site_occupations.ipynb'
    output: f'{figures_dir}/tetrahedral_site_populations.pdf'
    log:
        notebook=".logs/tetrahedral_site_occupations.ipynb"
    notebook: 'tetrahedral_site_occupations.ipynb'

rule tetrahedral_site_transition_probabilities:
    input: data_files, 'tetrahedral_site_transition_probabilities.ipynb'
    output: f'{figures_dir}/transition_matrices.pdf'
    log:
        notebook='.logs/tetrahedral_site_transition_probabilities.ipynb'
    notebook: 'tetrahedral_site_transition_probabilities.ipynb'

rule tetrahedral_site_positions:
    input: data_files, 'tetrahedral_site_positions.ipynb'
    output: f'{figures_dir}/site_rdf.pdf'
    log:
        notebook='.logs/tetrahedral_site_positions.ipynb'
    notebook: 'tetrahedral_site_positions.ipynb'

rule inherent_structure_site_comparison:
    input: comparison_data_files, 'inherent_structure_site_comparison.ipynb'
    output: f'{figures_dir}/inherent_vs_actual_site_comparison.pdf'
    log:
        notebook='.logs/inherent_structure_site_comparison.ipynb'
    notebook: 'inherent_structure_site_comparison.ipynb'

rule clean:
    run:
        for figure in output_figures:
            shell(f'rm -f {figures_dir}/{figure}')
