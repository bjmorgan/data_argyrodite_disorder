# Data

This directory contains nested subdirectories for each molecular dynamics simulation run, with each
subdirectory containing the following trajectory data:

- `actual_XDATCAR.gz`: gzipped copy of the raw XDATCAR taken from the simulation run.
- `inherent_XDATCAR.gz`: gzipped copy of the inherent structures for the same trajectory, in XDATCAR format.
- `frame_numbers.dat.gz`: A list of frame numbers for the trajectory frames in `actual_XDATCAR.gz` and `inherent_XDATCAR.gz`

## Molecular dynamics data directory structure:

```
.
├── Li6PS5Cl
│   ├── 0p
│   │   ├── run1
│   │   ├── run2
│   │   ├── run3
│   │   ├── run4
│   │   └── run5
│   ├── 100p
│   │   ├── run1
│   │   ├── run2
│   │   ├── run3
│   │   ├── run4
│   │   ├── run5
│   │   └── run6
│   └── 50p
│       ├── run1
│       ├── run2
│       ├── run3
│       ├── run4
│       ├── run5
│       └── run6
├── Li6PS5I
│   ├── 0p
│   │   ├── run1
│   │   ├── run2
│   │   ├── run3
│   │   ├── run4
│   │   ├── run5
│   │   └── run6
│   ├── 100p
│   │   ├── run1
│   │   ├── run2
│   │   ├── run3
│   │   ├── run4
│   │   ├── run5
│   │   ├── run6
│   │   └── run7
│   └── 50p
│       ├── run1
│       ├── run2
│       ├── run3
│       ├── run4
│       ├── run5
│       ├── run6
│       └── run7
```

## Additional structural data

The `reference_structures` directory contains additional structure files used for structural reference in the data analysis.


