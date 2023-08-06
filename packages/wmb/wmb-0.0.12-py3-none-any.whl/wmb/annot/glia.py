from .annot import CellAnnotation


class GliamCTCellAnnotation(CellAnnotation):
    __slots__ = ()

    def __init__(self, annot_path):
        super().__init__(annot_path)
        return
