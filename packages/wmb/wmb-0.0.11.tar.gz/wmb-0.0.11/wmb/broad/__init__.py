import pandas as pd
from ..genome import mm10
from wmb.files import *
from ..annot import BROADTENXCellAnnotation
from functools import lru_cache


class BROAD:
    def __init__(self):
        self.BROAD_TENX_SAMPLE_METADATA_PATH = BROAD_TENX_SAMPLE_METADATA_PATH
        self.BROAD_TENX_ZARR_PATH = BROAD_TENX_ZARR_PATH
        self.BROAD_TENX_OUTLIER_IDS_PATH = BROAD_TENX_OUTLIER_IDS_PATH
        self.BROAD_TENX_CELL_TYPE_ANNOTATION_PATH = BROAD_TENX_CELL_TYPE_ANNOTATION_PATH

        self._gene_zarr = None
        self._cell_million_reads = None
        self._gene_index = None
        return

    def get_tenx_sample_metadata(self):
        df = pd.read_csv(self.BROAD_TENX_SAMPLE_METADATA_PATH, index_col=0)
        df.index.name = 'sample'
        return df

    def get_tenx_outlier_ids(self):
        ids = pd.read_csv(self.BROAD_TENX_OUTLIER_IDS_PATH, index_col=0, header=None).index
        ids.name = 'cell'
        return ids

    def get_tenx_annot(self):
        return BROADTENXCellAnnotation(self.BROAD_TENX_CELL_TYPE_ANNOTATION_PATH,
                                       self.get_tenx_sample_metadata())

    def _open_zarr(self):
        import xarray as xr
        self._gene_zarr = xr.open_zarr(self.BROAD_TENX_ZARR_PATH)
        self._cell_million_reads = self._gene_zarr['umi_count'].to_pandas()
        self._cell_million_reads /= 1000000
        self._gene_index = self._gene_zarr.get_index('gene')
        return

    @lru_cache(maxsize=200)
    def get_tenx_gene_data(self, gene, normalize=True):
        if self._gene_zarr is None:
            self._open_zarr()

        # check if gene is gene name:
        if gene in self._gene_index:
            # gene is gene name
            gene_name = gene
        else:
            gene_name = mm10.gene_id_to_name(gene)

        # raw counts
        gene_data = self._gene_zarr['gene_da'].sel(
            gene=gene_name).to_pandas()
        # normalize to CPM
        if normalize:
            gene_data /= self._cell_million_reads
        return gene_data


broad = BROAD()
