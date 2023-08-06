import pathlib

import wmb

PACKAGE_DIR = pathlib.Path(wmb.__path__[0])

# =================================
# CEMBA RS1.1
# =================================

# the code to prepare cemba metadata is in
# /home/hanliu/project/cemba/study/BasicFilteringAndPrepareMetadata 04/20/2022
CEMBA_SNMC_MAPPING_METRIC_PATH = PACKAGE_DIR / 'files/CEMBA.CellMetadata.snmC-seq.small.csv.gz'
CEMBA_SNM3C_MAPPING_METRIC_PATH = PACKAGE_DIR / 'files/CEMBA.CellMetadata.snm3C-seq.small.csv.gz'
CEMBA_SNMC_FULL_MAPPING_METRIC_PATH = '/home/hanliu/project/cemba/metainfo/CEMBA.CellMetadata.snmC-seq.hdf'
CEMBA_SNM3C_FULL_MAPPING_METRIC_PATH = '/home/hanliu/project/cemba/metainfo/CEMBA.CellMetadata.snm3C-seq.hdf'

# the code to prepare cemba file path is in
# /home/hanliu/cemba3c/BICCN/wmb/file_path 04/20/2022
CEMBA_SNMC_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.ALLCPaths.csv.gz'
CEMBA_SNM3C_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.ALLCPaths.csv.gz'
CEMBA_SNMC_MCG_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.mCGALLCPaths.csv.gz'
CEMBA_SNM3C_MCG_ALLC_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.mCGALLCPaths.csv.gz'

# snm3C contact related
# /home/hanliu/cemba3c/BICCN/wmb/file_path 04/20/2022
CEMBA_SNM3C_CONTACT_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.ContactPaths.csv.gz'
CEMBA_SNM3C_10K_RAW_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.10KRawCoolURLs.csv.gz'
CEMBA_SNM3C_25K_RAW_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.25KRawCoolURLs.csv.gz'
CEMBA_SNM3C_100K_RAW_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.100KRawCoolURLs.csv.gz'
CEMBA_SNM3C_10K_IMPUTED_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.10KImputedCoolURLs.csv.gz'
CEMBA_SNM3C_25K_IMPUTED_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.25KImputedCoolURLs.csv.gz'
CEMBA_SNM3C_100K_IMPUTED_COOL_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.100KImputedCoolURLs.csv.gz'

# MCDS Path 04/20/2022
# MCDS is ordered according to the first pass clustering, data type is standardized
CEMBA_SNMC_MCDS_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_RS1/dataset/CEMBA.snmC.mcds'
CEMBA_SNM3C_MCDS_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.mcds'
# snm3C compartment, embedding, domain
# prepared in /gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/prepare_3c_matrix 05/15/2022
CEMBA_SNM3C_3C_COMPARTMENT_ZARR = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.3C.mcds/chrom100k'
CEMBA_SNM3C_3C_DOMAIN_INSULATION_ZARR = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.3C.mcds/chrom25k'
CEMBA_SNM3C_3C_CHROM100K_RAW_ZARR = '/gale/netapp/cemba3c/BICCN/CEMBA_3C/mcds/CEMBA.snm3C.chrom100k_raw.zarr'

# cluster assignments
# cell class, major type, subtype
CEMBA_SNMC_CELL_TYPE_ANNOTATION_PATH = '/home/hanliu/project/cemba/study/Clustering/' \
                                       'CEMBA_MC/Summary/CEMBA.snmC.Annotations.zarr'
# TODO snm3C cell type annotation
CEMBA_SNM3C_CELL_TYPE_ANNOTATION_PATH = None
# CEMBA_SNM3C_CELL_TYPE_ANNOTATION_PATH = '/home/hanliu/project/cemba/study/Clustering/' \
#                                        'CEMBA_3C/Summary/CEMBA.snm3C.Annotations.zarr'

# Outlier IDs
# /home/hanliu/project/cemba/study/MarkOutlier 05/12/2022
CEMBA_SNMC_OUTLIER_IDS_PATH = PACKAGE_DIR / 'files/CEMBA.snmC.DoubletsID.txt.gz'
CEMBA_SNM3C_OUTLIER_IDS_PATH = PACKAGE_DIR / 'files/CEMBA.snm3C.DoubletsID.txt.gz'

# Liu 2021 Nature metadata
CEMBA_LIU_2021_NATURE_SNMC_METADATA_PATH = PACKAGE_DIR / 'files/CEMBA.Liu2021Nature.snmC.metadata.csv.gz'


# =================================
# CEMBA ATAC
# =================================

CEMBA_ATAC_ZARR_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_ATAC/zarr/CEMBA.snATAC.zarr'
CEMBA_ATAC_CELL_TYPE_ANNOTATION_PATH = '/gale/netapp/cemba3c/BICCN/CEMBA_ATAC/meta/CEMBA.snATAC.Annotations.zarr'
CEMBA_ATAC_CLUSTER_FULL_NAME_PATH = PACKAGE_DIR / 'files/CEMBA.snATAC.ClusterDescription.tsv'
