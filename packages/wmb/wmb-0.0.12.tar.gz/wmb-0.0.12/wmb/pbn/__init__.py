import pandas as pd
import numpy as np
from functools import lru_cache
from ..genome import mm10


class PBNMCT:
    def __init__(self):
        self.metadata = '/gale/netapp/cemba3c/projects/PBN/metadata/MappingSummary.csv.gz'
        self.MCDS_PATH = '/gale/netapp/cemba3c/projects/PBN/dataset/PBN.mcds'

        self._gene_dataset = None
        self._rna_dataset = None
        self._per_cell_million_rna_reads = None

    def get_metadata(self):
        return pd.read_csv(self.metadata, index_col=0)

    # def get_glia_annot(self):
    #    return GliamCTCellAnnotation(self.MCDS_PATH)

    def _open_gene_mcds(self):
        from ALLCools.mcds import MCDS
        mcds = MCDS.open(self.MCDS_PATH, var_dim='geneslop2k')

        if 'geneslop2k_da_frac' not in mcds:
            mcds.add_mc_frac()

        self._gene_dataset = mcds

    @lru_cache(maxsize=200)
    def get_gene_mc_frac(self, gene, mc_type='CHN'):
        if self._gene_dataset is None:
            self._open_gene_mcds()

        # check if gene is gene name:
        try:
            # gene_name = gene
            gene_id = mm10.gene_name_to_id(gene)
        except KeyError:
            gene_id = gene
            # gene_name = mm10.gene_id_to_name(gene)

        gene_data = self._gene_dataset['geneslop2k_da_frac'].sel(
            mc_type=mc_type, geneslop2k=gene_id
        ).to_pandas()
        return gene_data

    def _open_rna_zarr(self):
        from ALLCools.mcds import MCDS
        self._rna_dataset = MCDS.open(self.MCDS_PATH, var_dim='rna')
        self._per_cell_million_rna_reads = self.get_metadata()['FinalRNAReads'] / 1e6

    @lru_cache(maxsize=200)
    def get_gene_rna(self, gene, normalize=True, log1p=True):
        if self._rna_dataset is None:
            self._open_rna_zarr()

        # check if gene is gene name:
        try:
            # gene_name = gene
            gene_id = mm10.gene_name_to_id(gene)
        except KeyError:
            gene_id = gene
            # gene_name = mm10.gene_id_to_name(gene)

        gene_data = self._rna_dataset['gene_da'].sel(gene=gene_id).to_pandas()
        if normalize:
            gene_data = gene_data / self._per_cell_million_rna_reads
        if log1p:
            gene_data = np.log1p(gene_data)
        return gene_data


pbn = PBNMCT()
