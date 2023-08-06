import pandas as pd

from ..files import *


class MM10GenomeRef:
    def __init__(self, annot_version='GENCODE_vm22'):
        self.ENCODE_BLACKLIST_PATH = ENCODE_BLACKLIST_PATH
        self.GENCODE_MM10_vm22 = GENCODE_MM10_vm22
        self._gene_id_to_name = None
        self._gene_name_to_id = None
        self._gene_id_base_to_name = None
        self._gene_name_to_id_base = None
        self._get_gene_id_name_dict(annot_version=annot_version)
        return

    def get_gene_metadata(self, annot_version='GENCODE_vm22'):
        if annot_version == 'GENCODE_vm22':
            gene_meta = pd.read_csv(self.GENCODE_MM10_vm22, sep='\t', index_col='gene_id')
        else:
            raise NotImplementedError
        return gene_meta

    def _get_gene_id_name_dict(self, annot_version='GENCODE_vm22'):
        if annot_version == 'GENCODE_vm22':
            self._gene_id_to_name = self.get_gene_metadata()['gene_name'].to_dict()
        else:
            raise NotImplementedError

        self._gene_name_to_id = {v: k for k, v in self._gene_id_to_name.items()}
        self._gene_id_base_to_name = {k.split('.')[0]: v for k, v in self._gene_id_to_name.items()}
        self._gene_name_to_id_base = {v: k for k, v in self._gene_id_base_to_name.items()}
        return

    def gene_id_to_name(self, gene_id):
        try:
            return self._gene_id_to_name[gene_id]
        except KeyError as e:
            try:
                return self._gene_id_base_to_name[gene_id]
            except KeyError:
                raise e

    def gene_name_to_id(self, gene_name):
        return self._gene_name_to_id[gene_name]

    def gene_name_to_id_base(self, gene_name):
        return self._gene_name_to_id_base[gene_name]


mm10 = MM10GenomeRef()
