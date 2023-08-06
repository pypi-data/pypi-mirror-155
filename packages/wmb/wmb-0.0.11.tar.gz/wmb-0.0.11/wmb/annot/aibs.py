from .annot import CellAnnotation
from ..brain_region import brain


class AIBSTENXCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        # add AIBS specific attributes
        self['sample'] = self.get_index('cell').map(lambda i: i.split('-')[0])

        metadata['MajorRegion'] = metadata['Structure'].map(
            brain.map_dissection_region_to_major_region())
        self['MajorRegion'] = self['sample'].to_pandas().map(metadata['MajorRegion'])

        metadata['SubRegion'] = metadata['Structure'].map(
            brain.map_dissection_region_to_sub_region())
        self['SubRegion'] = self['sample'].to_pandas().map(metadata['SubRegion'])
        return


class AIBSSMARTCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path, metadata):
        super().__init__(annot_path)

        self['MajorRegion'] = metadata['Substructure'].map(
            brain.map_dissection_region_to_major_region())

        self['SubRegion'] = metadata['Substructure'].map(
            brain.map_dissection_region_to_sub_region())
        return
