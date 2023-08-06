from functools import lru_cache

import pandas as pd

from wmb.files import *
from ..annot import AIBSTENXCellAnnotation, AIBSSMARTCellAnnotation
from ..brain_region import brain
from ..genome import mm10


def _get_mapping_metric(path, pass_basic_qc_only=True):
    df = pd.read_csv(path, index_col=0)
    df.index.name = 'cell'
    if pass_basic_qc_only:
        df = df[df['PassBasicQC']].copy()
    return df


class AIBS:
    def __init__(self):
        self.AIBS_SMART_CELL_METADATA_PATH = AIBS_SMART_CELL_METADATA_PATH
        self.AIBS_SMART_CELL_FULL_METADATA_PATH = AIBS_SMART_CELL_FULL_METADATA_PATH
        self.AIBS_SMART_ZARR_PATH = AIBS_SMART_ZARR_PATH
        self.AIBS_SMART_OUTLIER_IDS_PATH = AIBS_SMART_OUTLIER_IDS_PATH
        self.AIBS_SMART_CELL_TYPE_ANNOTATION_PATH = AIBS_SMART_CELL_TYPE_ANNOTATION_PATH

        self.AIBS_TENX_SAMPLE_METADATA_PATH = AIBS_TENX_SAMPLE_METADATA_PATH
        self.AIBS_TENX_SAMPLE_FULL_METADATA_PATH = AIBS_TENX_SAMPLE_FULL_METADATA_PATH
        self.AIBS_TENX_SAMPLE_TOTAL_METADATA_PATH = AIBS_TENX_SAMPLE_TOTAL_METADATA_PATH
        self.AIBS_TENX_SAMPLE_TOTAL_FULL_METADATA_PATH = AIBS_TENX_SAMPLE_TOTAL_FULL_METADATA_PATH
        self.AIBS_TENX_ZARR_PATH = AIBS_TENX_ZARR_PATH
        self.AIBS_TENX_OUTLIER_IDS_PATH = AIBS_TENX_OUTLIER_IDS_PATH
        self.AIBS_TENX_SAMPLE_TYPE_ANNOTATION_PATH = AIBS_TENX_CELL_TYPE_ANNOTATION_PATH

        # internal variables
        self._smart_gene_zarr = None
        self._smart_cell_million_reads = None
        self._smart_gene_index = None
        self._tenx_gene_zarr = None
        self._tenx_cell_million_reads = None
        self._tenx_gene_index = None
        return

    def get_smart_cell_metadata(self, pass_basic_qc_only=True, remove_outlier_ids=True):
        df = pd.read_csv(self.AIBS_SMART_CELL_METADATA_PATH, index_col=0)
        df.index.name = 'cell'
        if pass_basic_qc_only:
            df = df[df['PassBasicQC']].copy()
        if remove_outlier_ids:
            df = df.drop(self.get_smart_outlier_ids())

        df['MajorRegion'] = df['Substructure'].map(
            brain.map_dissection_region_to_major_region(region_type='AIBS_SMART'))
        df['SubRegion'] = df['Substructure'].map(brain.map_dissection_region_to_sub_region(region_type='AIBS_SMART'))
        return df

    def get_tenx_sample_metadata(self):
        df = pd.read_csv(self.AIBS_TENX_SAMPLE_METADATA_PATH, index_col=0)

        # three sample has missing values in the current manifest file, 05/08/2022
        df.fillna('nan', inplace=True)

        df.index.name = 'sample'

        df['MajorRegion'] = df['Structure'].map(brain.map_dissection_region_to_major_region(region_type='AIBS_TENX'))
        df['SubRegion'] = df['Structure'].map(brain.map_dissection_region_to_sub_region(region_type='AIBS_TENX'))
        return df

    def get_tenx_outlier_ids(self):
        ids = pd.read_csv(self.AIBS_TENX_OUTLIER_IDS_PATH, index_col=0, header=None).index
        ids.name = 'cell'
        return ids

    def get_smart_outlier_ids(self):
        ids = pd.read_csv(self.AIBS_SMART_OUTLIER_IDS_PATH, index_col=0, header=None).index
        ids.name = 'cell'
        return ids

    def get_smart_annot(self):
        return AIBSSMARTCellAnnotation(self.AIBS_SMART_CELL_TYPE_ANNOTATION_PATH,
                                       self.get_smart_cell_metadata())

    def get_tenx_annot(self):
        return AIBSTENXCellAnnotation(self.AIBS_TENX_SAMPLE_TYPE_ANNOTATION_PATH,
                                      self.get_tenx_sample_metadata())

    def _open_smart_zarr(self):
        import xarray as xr
        self._smart_gene_zarr = xr.open_zarr(self.AIBS_SMART_ZARR_PATH)
        self._smart_cell_million_reads = self._smart_gene_zarr['read_count'].to_pandas()
        self._smart_cell_million_reads /= 1000000
        self._smart_gene_index = self._smart_gene_zarr.get_index('gene')
        return

    def _open_tenx_zarr(self):
        import xarray as xr
        self._tenx_gene_zarr = xr.open_zarr(self.AIBS_TENX_ZARR_PATH)
        self._tenx_cell_million_reads = self._tenx_gene_zarr['umi_count'].to_pandas()
        self._tenx_cell_million_reads /= 1000000
        self._tenx_gene_index = self._tenx_gene_zarr.get_index('gene')
        return

    @staticmethod
    def _standardize_gene_index(gene, dataset, gene_index):
        # check if gene is gene name:
        try:
            if dataset == 'smart':
                # current smart gene index is gene name
                if gene not in gene_index:
                    use_gene_text = mm10.gene_id_to_name(gene)
                else:
                    use_gene_text = gene
            else:
                # current tenx gene index is gene id base
                if gene not in gene_index:
                    use_gene_text = mm10.gene_name_to_id_base(gene)
                else:
                    use_gene_text = gene
                if use_gene_text not in gene_index:
                    raise KeyError
        except KeyError:
            raise KeyError(f'gene {gene} can not be recognized.')
        return use_gene_text

    @lru_cache(maxsize=200)
    def _get_gene_data(self, gene, normalize, dataset):
        if dataset == 'smart':
            gene_zarr = self._smart_gene_zarr
            cell_million_reads = self._smart_cell_million_reads
        elif dataset == 'tenx':
            gene_zarr = self._tenx_gene_zarr
            cell_million_reads = self._tenx_cell_million_reads
        else:
            raise ValueError('dataset must be smart or tenx, got {}'.format(dataset))

        # raw counts
        gene_data = gene_zarr['gene_da'].sel(gene=gene).to_pandas()
        # normalize to CPM
        if normalize:
            gene_data /= cell_million_reads
        return gene_data

    def get_tenx_gene_data(self, gene, normalize=True):
        if self._tenx_gene_zarr is None:
            self._open_tenx_zarr()

        gene_index = self._tenx_gene_index
        gene = self._standardize_gene_index(gene, 'tenx', gene_index)
        return self._get_gene_data(gene, normalize, 'tenx')

    def get_smart_gene_data(self, gene, normalize=True):
        if self._smart_gene_zarr is None:
            self._open_smart_zarr()

        gene_index = self._smart_gene_index
        gene = self._standardize_gene_index(gene, 'smart', gene_index)
        return self._get_gene_data(gene, normalize, 'smart')


aibs = AIBS()
