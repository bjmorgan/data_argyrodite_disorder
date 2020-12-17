from scripts import environment
import yaml
import os

figures_dir = 'figures'
analysis_dir = 'analysis'
data_dir = 'data'

# analysis notebooks
notebooks = ['msds/msds.ipynb',
             'strings/strings.ipynb',
             'rdfs/rdfs.ipynb',
             'tetrahedral_site_analysis/tetrahedral_site_occupations.ipynb',
             'tetrahedral_site_analysis/tetrahedral_site_transition_probabilities.ipynb',
             'tetrahedral_site_analysis/tetrahedral_site_positions.ipynb',
             'tetrahedral_site_analysis/inherent_structure_site_comparison.ipynb',
             'polyhedral_analysis/polyhedral_classification.ipynb',
             'polyhedral_analysis/polyhedral_dynamics.ipynb',
             'inherent_structures/inherent_structure_comparison.ipynb']

# output figures
figures = ['msd.pdf',
           'string_populations.pdf',
           'X-Li-coordination_numbers.pdf',
           'X-Li-rdf.pdf',
           'tetrahedral_site_populations.pdf',
           'transition_matrices.pdf',
           'site_rdf.pdf',
           'polyhedra_types.pdf',
           'Li6PS5I_octahedral_projection.pdf',
           'inherent_vs_actual_sites_comparison.pdf',
           'raw_vs_inherent_trajectory.pdf']

def get_data_files():
    with open('analysis/md_runs.yaml', 'r') as f:
        md_runs = yaml.safe_load(f)
    data_files = []
    for system in md_runs:
        for disorder, runs in md_runs[system].items():
            for i in runs:
                data_files.append(f'{data_dir}/{system}/{disorder}/run{i}/actual_XDATCAR.gz')
    return data_files

data_files = get_data_files()

subworkflow msds:
    workdir:
        "analysis/msds"
    snakefile:
        "analysis/msds/msds.smk"

subworkflow strings:
    workdir:
        "analysis/strings"
    snakefile:
        "analysis/strings/strings.smk"

subworkflow rdfs:
    workdir:
        "analysis/rdfs"
    snakefile:
        "analysis/rdfs/rdfs.smk"

subworkflow tetrahedral_sites:
    workdir:
        "analysis/tetrahedral_site_analysis"
    snakefile:
        "analysis/tetrahedral_site_analysis/tetrahedral_sites.smk"

subworkflow polyhedral_analysis:
    workdir:
        "analysis/polyhedral_analysis"
    snakefile:
        "analysis/polyhedral_analysis/polyhedra.smk"

subworkflow inherent_structures:
    workdir:
        "analysis/inherent_structures"
    snakefile:
        "analysis/inherent_structures/inherent_structures.smk"

rule all: 
    input:
       data_files,
       expand('analysis/{notebook}', notebook=notebooks),
       'system_info.txt',
       msds(f'../../{figures_dir}/msd.pdf'),
       strings(f'../../{figures_dir}/string_populations.pdf'),
       rdfs(f'../../{figures_dir}/X-Li-rdf.pdf'),
       rdfs(f'../../{figures_dir}/X-Li-coordination_numbers.pdf'),
       tetrahedral_sites(f'../../{figures_dir}/tetrahedral_site_populations.pdf'),
       tetrahedral_sites(f'../../{figures_dir}/transition_matrices.pdf'),
       tetrahedral_sites(f'../../{figures_dir}/site_rdf.pdf'),
       tetrahedral_sites(f'../../{figures_dir}/inherent_vs_actual_sites_comparison.pdf'),
       polyhedral_analysis(f'../../{figures_dir}/polyhedra_types.pdf'),
       polyhedral_analysis(f'../../{figures_dir}/Li6PS5I_octahedral_projection.pdf',
       inherent_structures(f'../../{figures_dir)/raw_versus_inherent_trajectory.pdf')

rule environment:
    output: 'system_info.txt'
    run: environment.main(output='system_info.txt')

rule clean:
    run:
        for figure in figures:
            shell(f'rm -f {figures_dir}/{figure}')
        shell('rm -f system_info.txt')

