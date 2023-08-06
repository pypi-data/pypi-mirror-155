from .annot import CellAnnotation

from ..brain_region import brain


class BROADTENXCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        # add BROAD specific attributes
        self['sample'] = self.get_index('cell').map(lambda i: i[:-18])

        metadata['MajorRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_major_region())
        self['MajorRegion'] = self['sample'].to_pandas().map(metadata['MajorRegion'])

        metadata['SubRegion'] = metadata['DissectionRegion'].map(
            brain.map_dissection_region_to_sub_region())
        self['SubRegion'] = self['sample'].to_pandas().map(metadata['SubRegion'])
        return
