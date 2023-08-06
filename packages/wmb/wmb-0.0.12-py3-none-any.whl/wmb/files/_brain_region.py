import pathlib

import wmb

PACKAGE_DIR = pathlib.Path(wmb.__path__[0])

BICCN_BRAIN_REGION_METADATA_PATH = PACKAGE_DIR / 'files/BICCN.BrainRegionMetadata.csv'
AIBS_REFERENCE_STRUCTURE_TREE_PATH = PACKAGE_DIR / 'files/AIBS.StructureTree.lib'
