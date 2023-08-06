from .annot import CellAnnotation

from ..brain_region import brain


class CEMBAmCCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        # add snmC specific attributes
        metadata['MajorRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_major_region(region_type='CEMBA'))
        self['MajorRegion'] = self.get_index('cell').map(metadata['MajorRegion'])

        metadata['SubRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_sub_region(region_type='CEMBA'))
        self['SubRegion'] = self.get_index('cell').map(metadata['SubRegion'])
        return


class CEMBAm3CCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        # add snm3C specific attributes
        metadata['MajorRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_major_region(region_type='CEMBA_3C'))
        self['MajorRegion'] = self.get_index('cell').map(metadata['MajorRegion'])

        metadata['SubRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_sub_region(region_type='CEMBA_3C'))
        self['SubRegion'] = self.get_index('cell').map(metadata['SubRegion'])
        return


class CEMBAATACCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path):
        super().__init__(annot_path)

        return
