"""
T O D O list
Mark outliers of CEMBA data
Annotate the major type of CEMBA data
Multi-round clustering of CEMBA data

For each dataset, write a get gene value function, given gene name, return gene value, cache genes

"""

# datasets agents
from .cemba import cemba, cemba_atac
from .aibs import aibs
from .broad import broad
from .glia import glia
from .pbn import pbn

# reference agents
from .brain_region import brain
# from .genes import genes
from .genome import mm10
