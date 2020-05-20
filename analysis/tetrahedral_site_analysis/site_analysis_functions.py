from pymatgen import Structure
from pymatgen.io.vasp import Poscar
import numpy as np
from site_analysis.atom import atoms_from_species_string
from site_analysis.trajectory import Trajectory
from site_analysis.polyhedral_site import PolyhedralSite
from site_analysis.tools import get_nearest_neighbour_indices
import sys
from collections import Counter

sys.path.insert(0, "../../scripts/")
from utils import flatten_list
from crystal_torture.pymatgen_interface import graph_from_structure


def percolating_graph(structure, elements, rcut):
    graph = graph_from_structure(structure, rcut=rcut, elements=set(elements))
    graph.torture()
    return any([c.periodic > 0 for c in graph.minimal_clusters])


def minimum_percolating_graph(
    structure, elements, r_min, r_max, func, conv=1e-2, verbose=False, maxiter=50
):
    # check min and max values give False and True respectively
    v_at_min = func(structure, elements, r_min)
    v_at_max = func(structure, elements, r_max)
    assert v_at_min is False
    assert v_at_max is True
    success = False
    for i in range(maxiter):
        r_mid = (r_min + r_max) / 2.0
        if r_mid - r_min < conv:
            success = True
            break
        v_at_mid = func(structure, elements, r_mid)
        if verbose:
            print(f"step: {i} r: {r_mid} perc: {v_at_mid}")
        if v_at_mid is True:
            r_max = r_mid
        else:
            r_min = r_mid
    return {"x": r_mid, "success": success}


def map_to_nearest_site(input_structure, species_strings, ref_structure, verbose=True):
    mappings = []
    site_indices = [
        i for i, s in enumerate(input_structure) if s.species_string in species_strings
    ]
    sites = [input_structure[i] for i in site_indices]
    frac_coords = [input_structure[i].frac_coords for i in site_indices]
    latt = ref_structure.lattice
    dr = latt.get_all_distances(frac_coords, ref_structure.frac_coords)
    disp = []
    for s, r in zip(sites, dr):
        index = np.argmin(r)
        mappings.append(index)
        disp.append(
            latt.get_distance_and_image(
                s.frac_coords, ref_structure[index].frac_coords
            )[0]
        )
        s.coords = ref_structure[index].coords
        assert len(mappings) == len(set(mappings))
    if verbose:
        print(f'max mapping disp = {max(disp):.2f} Angstroms')


def tetrahedral_site_analysis(structures, x_spec):
    md_structure = structures[0]
    map_to_nearest_site(md_structure, ["S", x_spec], s_sites)

    atoms = atoms_from_species_string(md_structure, "Li")

    t0_indices = get_nearest_neighbour_indices(
        md_structure, t0 * [2, 2, 2], vertex_species=["S", x_spec], n_coord=4
    )
    t1_indices = get_nearest_neighbour_indices(
        md_structure, t1 * [2, 2, 2], vertex_species=["S", x_spec], n_coord=4
    )
    t2_indices = get_nearest_neighbour_indices(
        md_structure, t2 * [2, 2, 2], vertex_species=["S", x_spec], n_coord=4
    )
    t3_indices = get_nearest_neighbour_indices(
        md_structure, t3 * [2, 2, 2], vertex_species=["S", x_spec], n_coord=4
    )
    t4_indices = get_nearest_neighbour_indices(
        md_structure, t4 * [2, 2, 2], vertex_species=["S", x_spec], n_coord=4
    )
    t5_indices = get_nearest_neighbour_indices(
        md_structure, t5 * [2, 2, 2], vertex_species=["S", x_spec], n_coord=4
    )

    PolyhedralSite.reset_index()

    t0_sites = [PolyhedralSite(vertex_indices=vi, label="0") for vi in t0_indices]
    t1_sites = [PolyhedralSite(vertex_indices=vi, label="1") for vi in t1_indices]
    t2_sites = [PolyhedralSite(vertex_indices=vi, label="2") for vi in t2_indices]
    t3_sites = [PolyhedralSite(vertex_indices=vi, label="3") for vi in t3_indices]
    t4_sites = [PolyhedralSite(vertex_indices=vi, label="4") for vi in t4_indices]
    t5_sites = [PolyhedralSite(vertex_indices=vi, label="5") for vi in t5_indices]
    sites = t0_sites + t1_sites + t2_sites + t3_sites + t4_sites + t5_sites

    trajectory = Trajectory(atoms=atoms, sites=sites)
    assert trajectory.site_collection.sites_contain_points(points=t_all.frac_coords, 
               structure=md_structure)
    trajectory.trajectory_from_structures(structures, progress="notebook")
    return trajectory


def site_populations(trajectory):
    c = Counter()
    for site in trajectory.sites:
        c[site.label] += len([1 for ts in site.trajectory if len(ts) > 0])
    total = sum(c.values())
    return {label: n / total for label, n in c.items()}


def pbc_nearest_point(reference, point):
    dr = reference - point
    point[np.where(dr > 0.5)] += 1.0
    point[np.where(dr < -0.5)] -= 1.0
    return point


directory = "../../data"
structure = Poscar.from_file(
    f"{directory}/reference_structures/Li6PS5I_alltet_sites.POSCAR.vasp"
).structure
lattice = structure.lattice
t0 = Structure.from_spacegroup(
    sg="F-43m", lattice=lattice, species=["P"], coords=[[0.5, 0.0, 0.0]]
)
t1 = Structure.from_spacegroup(
    sg="F-43m", lattice=lattice, species=["Li"], coords=[[0.9, 0.9, 0.6]]
)
t2 = Structure.from_spacegroup(
    sg="F-43m", lattice=lattice, species=["Li"], coords=[[0.23, 0.92, 0.08]]
)
t3 = Structure.from_spacegroup(
    sg="F-43m", lattice=lattice, species=["Li"], coords=[[0.25, 0.25, 0.25]]
)
t4 = Structure.from_spacegroup(
    sg="F-43m", lattice=lattice, species=["Li"], coords=[[0.15, 0.15, 0.15]]
)
t5 = Structure.from_spacegroup(
    sg="F-43m", lattice=lattice, species=["Li"], coords=[[0.0, 0.183, 0.183]]
)
tet_sites = [t0, t1, t2, t3, t4, t5]
t_all = Structure.from_sites(flatten_list([(t * [2, 2, 2]).sites for t in tet_sites]))
s_sites = Structure.from_spacegroup(
    sg="F-43m",
    lattice=lattice,
    species=["S", "S", "S"],
    coords=[[0.0, 0.0, 0.0], [0.75, 0.25, 0.25], [0.11824, 0.11824, 0.38176]],
) * [2, 2, 2]
