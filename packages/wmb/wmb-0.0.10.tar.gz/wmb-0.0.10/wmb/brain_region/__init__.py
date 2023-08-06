import joblib
import pandas as pd

from .ccf_ref import StructureTree
from ..files import *


class BrainRegions:
    def __init__(self):
        self.BICCN_BRAIN_REGION_METADATA_PATH = BICCN_BRAIN_REGION_METADATA_PATH
        self._region_meta = pd.read_csv(self.BICCN_BRAIN_REGION_METADATA_PATH,
                                        index_col=0)
        self._region_type = 'all'

        nodes = joblib.load(AIBS_REFERENCE_STRUCTURE_TREE_PATH)
        self.ccf = StructureTree(nodes)
        return

    def get_brain_metadata(self, region_type='all'):
        if region_type != 'all':
            if isinstance(region_type, str):
                region_type = [region_type]
            df = self._region_meta
            df = df[df['RegionType'].isin(region_type)].copy()
            if df.shape[0] == 0:
                raise KeyError(f'Got unknown region_type {region_type}. '
                               f'Possible values are {df["RegionType"].unique().tolist()}')
            return df
        else:
            return self._region_meta.copy()

    def get_value_map(self, k, v, region_type):
        if isinstance(region_type, str):
            region_type = [region_type]
        if region_type is not None:
            use_meta = self._region_meta[self._region_meta['RegionType'].isin(region_type)]
        else:
            use_meta = self._region_meta
        value_map = use_meta.set_index(k)[v].to_dict()
        return value_map

    def get_major_region_palette(self, region_type=None):
        return self.get_value_map('MajorRegion', 'MajorRegionColor', region_type=region_type)

    def get_sub_region_palette(self, region_type=None):
        return self.get_value_map('SubRegion', 'SubRegionColor', region_type=region_type)

    def get_dissection_region_palette(self, region_type=None):
        return self.get_value_map('Acronym', 'DissectionRegionColor', region_type=region_type)

    def get_cemba_id_region_palette(self, region_type=None):
        return self.get_value_map('CEMBAID', 'DissectionRegionColor', region_type=region_type)

    def map_dissection_region_to_sub_region(self, region_type=None):
        return self.get_value_map('Acronym', 'SubRegion', region_type=region_type)

    def map_dissection_region_to_major_region(self, region_type=None):
        return self.get_value_map('Acronym', 'MajorRegion', region_type=region_type)

    def map_sub_region_to_major_region(self, region_type=None):
        return self.get_value_map('SubRegion', 'MajorRegion', region_type=region_type)

    def map_cemba_id_to_dissection_region(self, region_type=None):
        return self.get_value_map('CEMBAID', 'Acronym', region_type=region_type)

    def map_cemba_id_to_sub_region(self, region_type=None):
        return self.get_value_map('CEMBAID', 'SubRegion', region_type=region_type)

    def map_cemba_id_to_major_region(self, region_type=None):
        return self.get_value_map('CEMBAID', 'MajorRegion', region_type=region_type)


brain = BrainRegions()

major_region_names = {
    'Isocortex', 'HPF', 'OLF', 'CTXsp', 'CNU', 'TH', 'HY', 'MB', 'HB', 'CB', 'BS'
}

sub_region_names = {
    'CA', 'DG', 'ENT', 'PAR', 'POST', 'PRE', 'SUB', 'CP', 'ACB', 'HIP', 'RHP', 'FRP', 'MO',
    'SS', 'GU', 'VISC', 'AUD', 'VIS', 'ACA', 'PL', 'ILA', 'ORB', 'AI', 'RSP', 'PTLp', 'TEa',
    'PERI', 'ECT', 'MOB', 'AOB', 'AON', 'TT', 'DP', 'PIR', 'NLOT', 'COA', 'PAA', 'TR', 'PALd',
    'PALv', 'PALm', 'PALc', 'STRd', 'STRv', 'LSX', 'sAMY', 'Isocortex', 'OLF', 'HPF', '6b',
    'CLA', 'EP', 'LA', 'BLA', 'BMA', 'PA', 'P', 'MY', 'TH', 'HY', 'MBsen', 'MBmot', 'MBsta',
    'FN', 'IP', 'DN', 'VeCB', 'VERM', 'HEM', 'STR', 'PAL', 'CTXpl', 'CTXsp', 'IB', 'MB', 'HB',
    'CBX', 'CBN', 'CTX', 'CNU', 'CH', 'BS', 'CB', 'root', 'grey', 'fiber tracts', 'VS', 'grv',
    'retina', 'MOp', 'MOs', 'SSp', 'SSs', 'VISp', 'FS', 'OT', 'DCN', 'GPe', 'GPi', 'SI', 'IC'
}

overlap_names = {
    'CA', 'DG', 'FC', 'IG', 'APr', 'ENT', 'HATA', 'PAR', 'POST', 'PRE', 'ProS',
    'SUB', 'ACAd', 'ACAv', 'AId', 'AIp', 'AIv', 'AUDd', 'AUDp', 'AUDpo',
    'AUDv', 'MOp', 'MOs', 'ORBl', 'ORBm', 'ORBv', 'ORBvl', 'VISa', 'VISrl',
    'RSPagl', 'RSPd', 'RSPv', 'SSp', 'SSs', 'VISal', 'VISam', 'VISl', 'VISli',
    'VISp', 'VISpl', 'VISpm', 'VISpor', 'ACVI', 'ACVII', 'AMB', 'DMX', 'ECO',
    'EV', 'GRN', 'ICB', 'INV', 'IO', 'IRN', 'ISN', 'LIN', 'LRN', 'MARN',
    'MDRN', 'PARN', 'PAS', 'PGRN', 'PHY', 'PMR', 'PPY', 'VI', 'VII', 'VNC',
    'x', 'XII', 'y', 'RM', 'RO', 'RPA', 'AP', 'CN', 'DCN', 'ECU', 'NTB', 'NTS',
    'Pa5', 'SPVC', 'SPVI', 'SPVO', 'z', 'Acs5', 'B', 'DTN', 'I5', 'LTN', 'P5',
    'PC5', 'PCG', 'PDTg', 'PG', 'PRNc', 'PRNv', 'SG', 'SSN', 'SUT', 'TRN', 'V',
    'CS', 'LC', 'LDT', 'NI', 'PRNr', 'RPO', 'SLC', 'SLD', 'NLL', 'PB', 'PSV',
    'SOC', 'LHA', 'LPO', 'PeF', 'PST', 'PSTN', 'RCH', 'STN', 'TU', 'ZI', 'AHN',
    'MBO', 'MPN', 'PH', 'PMd', 'PMv', 'PVHd', 'VMH', 'ADP', 'AHA', 'AVP',
    'AVPV', 'DMH', 'MEPO', 'MPO', 'OV', 'PD', 'PS', 'PSCH', 'PVp', 'PVpo',
    'SBPV', 'SCH', 'SFO', 'VLPO', 'VMPO', 'ARH', 'ASO', 'PVa', 'PVH', 'PVi',
    'SO', 'ATN', 'EPI', 'GENv', 'ILM', 'LAT', 'MED', 'MTN', 'RT', 'GENd', 'PP',
    'SPA', 'SPF', 'VENT', 'BAC', 'BST', 'GPe', 'GPi', 'MSC', 'TRS', 'MA', 'SI',
    'LS', 'SF', 'SH', 'AAA', 'BA', 'CEA', 'IA', 'MEA', 'CP', 'ACB', 'FS',
    'LSS', 'OT', 'HIP', 'RHP', 'ACA', 'AI', 'AUD', 'ECT', 'FRP', 'GU', 'ILA',
    'MO', 'ORB', 'PERI', 'PL', 'PTLp', 'RSP', 'SS', 'TEa', 'VIS', 'VISC',
    'AOB', 'AON', 'COA', 'DP', 'MOB', 'NLOT', 'PAA', 'PIR', 'TR', 'TT', 'BLAa',
    'BLAp', 'BLAv', 'BMAa', 'BMAp', 'EPd', 'EPv', 'MY-mot', 'MY-sat', 'MY-sen',
    'P-mot', 'P-sat', 'P-sen', 'LZ', 'ME', 'MEZ', 'PVR', 'PVZ', 'DORpm',
    'DORsm', 'AT', 'CUN', 'DT', 'EW', 'III', 'InCo', 'IV', 'LT', 'MA3', 'MRN',
    'MT', 'Pa4', 'PAG', 'PN', 'PRT', 'RN', 'RR', 'SCm', 'SNl', 'SNr', 'VTA',
    'VTN', 'IC', 'MEV', 'NB', 'PBG', 'SAG', 'SCO', 'SCs', 'PPN', 'RAmb', 'SNc',
    'AN', 'COPY', 'FL', 'PFL', 'PRM', 'SIM', 'CENT', 'CUL', 'DEC', 'FOTU',
    'LING', 'NOD', 'PYR', 'UVU', 'PALc', 'PALd', 'PALm', 'PALv', 'LSX', 'sAMY',
    'STRd', 'STRv', 'HPF', 'Isocortex', 'OLF', '6b', 'BLA', 'BMA', 'CLA', 'EP',
    'LA', 'PA', 'MY', 'P', 'HY', 'TH', 'MBmot', 'MBsen', 'MBsta', 'DN', 'FN',
    'IP', 'VeCB', 'CBXgr', 'CBXmo', 'CBXpu', 'HEM', 'VERM', 'PAL', 'STR',
    'CTXpl', 'CTXsp', 'HB', 'IB', 'MB', 'CBN', 'CBX', 'CNU', 'CTX', 'cbf',
    'cm', 'eps', 'lfbs', 'mfbs', 'scwm', 'BS', 'CB', 'CH', 'fiber tracts',
    'grey', 'grv', 'retina', 'root', 'VS', 'ENTl', 'ENTm', 'APN', 'MS', 'NDB',
    'CU', 'GR', 'DCO', 'VCO', 'PGRNl', 'PGRNd', 'MPT', 'NOT', 'NPC', 'OP',
    'PPT', 'RPF', 'AD', 'AV', 'AM', 'IAM', 'IAD', 'LD', 'CM', 'LGd', 'LGv',
    'LP', 'MD', 'IMD', 'PCN', 'CL', 'MG', 'SPFp', 'PP', 'POL', 'SGN', 'PoT',
    'PIL', 'MH', 'LH', 'PF', 'PO', 'Eth', 'PVT', 'PT', 'RE', 'RH', 'CM', 'IAM',
    'SMT', 'PR', 'Xi', 'SPFm', 'VAL', 'VM', 'VPL', 'VPM', 'VPMpc', 'VPLpc',
    'IGL'
}
