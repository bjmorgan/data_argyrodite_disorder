from scripts import environment
import yaml
import os

figures_dir = 'figures'
analysis_dir = 'analysis'
data_dir = 'data'

# analysis notebooks
notebooks = ['msds/msds.ipynb',
             'strings/strings.ipynb',
             'rdfs/rdfs.ipynb']

# output figures
figures = ['msd.pdf',
           'string_populations.pdf',
           'X-Li-coordination_numbers.pdf',
           'X-Li-rdf.pdf']

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

rule all: 
    input:
       data_files,
       expand('analysis/{notebook}', notebook=notebooks),
       'system_info.txt',
       msds(f'../../{figures_dir}/msd.pdf'),
       strings(f'../../{figures_dir}/string_populations.pdf'),
       rdfs(f'../../{figures_dir}/X-Li-rdf.pdf'),
       rdfs(f'../../{figures_dir}/X-Li-coordination_numbers.pdf')

rule environment:
    output: 'system_info.txt'
    run: environment.main(output='system_info.txt')

rule clean:
    run:
        for figure in figures:
            shell(f'rm -f {figures_dir}/{figure}')
        shell('rm -f system_info.txt')

