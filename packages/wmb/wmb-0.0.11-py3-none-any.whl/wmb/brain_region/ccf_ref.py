# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2017. Allen Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Redistributions for commercial purposes are not permitted without the
# Allen Institute's written permission.
# For purposes of this license, commercial purposes is the incorporation of the
# Allen Institute's software into anything for which you will charge fees or
# other compensation. Contact terms@alleninstitute.org for commercial licensing
# opportunities.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import functools
import operator as op

import numpy as np
import pandas as pd


class SimpleTree(object):
    def __init__(self, nodes,
                 node_id_cb,
                 parent_id_cb):
        """A tree structure

        Parameters
        ----------
        nodes : list of dict
            Each dict is a node in the tree. The keys of the dict name the 
            properties of the node and should be consistent across nodes.
        node_id_cb : function | node dict -> node id
            Calling node_id_cb on a node dictionary ought to produce a unique 
            identifier for that node (we call this the node's id). The type 
            of the node id is up to you, but ought to be consistent across 
            nodes and must be hashable.
        parent_id_cb : function | node_dict => parent node's id
            As node_id_cb, but returns the id of the node's parent.

        Notes
        -----
        It is easy to pass a pandas DataFrame as the nodes. Just use the 
        to_dict method of the dataframe like so:
            list_of_dict = your_dataframe.to_dict('record')
            your_tree = SimpleTree(list_of_dict, ...)
        Converting a list of dictionaries to a pandas DataFrame is also very 
        easy. The DataFrame constructor does it for you:
            your_dataframe = pandas.DataFrame(list_of_dict)

        """

        self._nodes = {node_id_cb(n): n for n in nodes}
        self._parent_ids = {nid: parent_id_cb(n) for nid, n in self._nodes.items()}
        self._child_ids = {nid: [] for nid in self._nodes}

        for nid in self._parent_ids:
            pid = self._parent_ids[nid]
            if pid is not None:
                self._child_ids[pid].append(nid)

        self.node_id_cb = node_id_cb
        self.parent_id_cb = parent_id_cb

    def filter_nodes(self, criterion):
        """Obtain a list of nodes filtered by some criterion

        Parameters
        ----------
        criterion : function | node dict => bool
            Only nodes for which criterion returns true will be returned.

        Returns
        -------
        list of dict :
            Items are node dictionaries that passed the filter.

        """

        return list(filter(criterion, self._nodes.values()))

    def value_map(self, from_fn, to_fn):
        """Obtain a look-up table relating a pair of node properties across
        nodes

        Parameters
        ----------
        from_fn : function | node dict => hashable value
            The keys of the output dictionary will be obtained by calling 
            from_fn on each node. Should be unique.
        to_fn : function | node_dict => value
            The values of the output function will be obtained by calling 
            to_fn on each node.

        Returns
        -------
        dict :
            Maps the node property defined by from_fn to the node property 
            defined by to_fn across nodes.

        """

        vm = {}
        for node in self._nodes.values():
            key = from_fn(node)
            value = to_fn(node)

            if key in vm:
                raise RuntimeError('from_fn is not unique across nodes. '
                                   'Collision between {0} and {1}.'.format(value, vm[key]))
            vm[key] = value

        return vm

    def nodes_by_property(self, key, values, to_fn=None):
        """Get nodes by a specified property

        Parameters
        ----------
        key : hashable or function
            The property used for lookup. Should be unique. If a function, will 
            be invoked on each node.
        values : list
            Select matching elements from the lookup.
        to_fn : function, optional
            Defines the outputs, on a per-node basis. Defaults to returning 
            the whole node.

        Returns
        -------
        list : 
            outputs, 1 for each input value.

        """

        if to_fn is None:
            def to_fn(x):
                return x

        if not callable(key):
            def from_fn(x):
                return x[key]
        else:
            from_fn = key

        value_map = self.value_map(from_fn, to_fn)
        return [value_map[vv] for vv in values]

    def node_ids(self):
        """Obtain the node ids of each node in the tree

        Returns
        -------
        list :
            elements are node ids 

        """

        return list(self._nodes)

    def parent_ids(self, node_ids):
        """Obtain the ids of one or more nodes' parents

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose parents you wish to find.

        Returns
        -------
        list of hashable : 
            Items are ids of input nodes' parents in order.

        """

        return [self._parent_ids[nid] for nid in node_ids]

    def child_ids(self, node_ids):
        """Obtain the ids of one or more nodes' children

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose children you wish to find.

        Returns
        -------
        list of list of hashable : 
            Items are lists of input nodes' children's ids.

        """

        return [self._child_ids[nid] for nid in node_ids]

    def ancestor_ids(self, node_ids):
        """Obtain the ids of one or more nodes' ancestors

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose ancestors you wish to find.

        Returns
        -------
        list of list of hashable : 
            Items are lists of input nodes' ancestors' ids.

        Notes
        -----
        Given the tree:
        A -> B -> C
         `-> D

        The ancestors of C are [C, B, A]. The ancestors of A are [A]. The 
        ancestors of D are [D, A]

        """

        out = []
        for nid in node_ids:

            current = [nid]
            while current[-1] is not None:
                current.extend(self.parent_ids([current[-1]]))
            out.append(current[:-1])

        return out

    def descendant_ids(self, node_ids):
        """Obtain the ids of one or more nodes' descendants

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose descendants you wish to find.

        Returns
        -------
        list of list of hashable : 
            Items are lists of input nodes' descendants' ids.

        Notes
        -----
        Given the tree:
        A -> B -> C
         `-> D

        The descendants of A are [B, C, D]. The descendants of C are [].

        """

        out = []
        for ii, nid in enumerate(node_ids):

            current = [nid]
            children = self.child_ids([nid])[0]

            if children:
                current.extend(functools.reduce(op.add, map(list,
                                                            self.descendant_ids(children))))

            out.append(current)
        return out

    def nodes(self, node_ids=None):
        """Get one or more nodes' full dictionaries from their ids.

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes to be returned. Default is all.

        Returns
        -------
        list of dict :
            Items are nodes corresponding to argued ids.
        """

        if node_ids is None:
            node_ids = self.node_ids()

        return [self._nodes[nid] if nid in self._nodes else None for nid in node_ids]

    def parents(self, node_ids):
        """Get one or mode nodes' parent nodes

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose parents will be found.

        Returns
        -------
        list of dict : 
            Items are parents of nodes corresponding to argued ids.

        """

        return self.nodes([self._parent_ids[nid] for nid in node_ids])

    def children(self, node_ids):
        """Get one or mode nodes' child nodes

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose children will be found.

        Returns
        -------
        list of list of dict : 
            Items are lists of child nodes corresponding to argued ids.

        """

        return list(map(self.nodes, self.child_ids(node_ids)))

    def descendants(self, node_ids):
        """Get one or mode nodes' descendant nodes

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose descendants will be found.

        Returns
        -------
        list of list of dict : 
            Items are lists of descendant nodes corresponding to argued ids.

        """

        return list(map(self.nodes, self.descendant_ids(node_ids)))

    def ancestors(self, node_ids):
        """Get one or mode nodes' ancestor nodes

        Parameters
        ----------
        node_ids : list of hashable
            Items are ids of nodes whose ancestors will be found.

        Returns
        -------
        list of list of dict : 
            Items are lists of ancestor nodes corresponding to argued ids.

        """

        return list(map(self.nodes, self.ancestor_ids(node_ids)))


def list_or_single(func):
    def wrapper(*args):
        obj, value = args
        if isinstance(value, (int, str)):
            result = func(obj, [value])[0]
        else:
            result = func(obj, value)
        return result

    return wrapper


class StructureTree(SimpleTree):

    def __init__(self, nodes):
        """A tree whose nodes are brain structures and whose edges indicate
        physical containment.

        Parameters
        ----------
        nodes : list of dict
            Each specifies a structure. Fields are:

            'acronym' : str
                Abbreviated name for the structure.
            'rgb_triplet' : str
                Canonical RGB uint8 color assigned to this structure
            'graph_id' : int
                Specifies the structure graph containing this structure.
            'graph_order' : int
                Canonical position in the flattened structure graph.
            'id': int
                Unique structure specifier.
            'name' : str
                Full name of structure.
            'structure_id_path' : list of int
                This structure's ancestors (inclusive) from the root of the
                tree.
            'structure_set_ids' : list of int
                Unique identifiers of structure sets to which this structure
                belongs.

        """

        def _get_id(s):
            return int(s['id'])

        def _get_parent(s):
            if len(s['structure_id_path']) > 1:
                if s['structure_id_path'] is not None:
                    if np.isfinite(s['structure_id_path'][-2]):
                        return s['structure_id_path'][-2]
            return None

        super(StructureTree, self).__init__(nodes, _get_id, _get_parent)
        self._id_to_acronym = self.get_id_acronym_map()
        self._acronym_to_id = self.get_acronym_id_map()
        return

    def id_to_acronym(self, structure_id):
        return self._id_to_acronym[structure_id]

    def acronym_to_id(self, acronym):
        return self._acronym_to_id[acronym]

    @list_or_single
    def get_structures_by_id(self, structure_ids):
        """Obtain a list of brain structures from their structure ids

        Parameters
        ----------
        structure_ids : list of int
            Get structures corresponding to these ids.

        Returns
        -------
        list of dict :
            Each item describes a structure.

        """

        return self.nodes(structure_ids)

    @list_or_single
    def get_structures_by_name(self, names):
        """Obtain a list of brain structures from their names,

        Parameters
        ----------
        names : list of str
            Get structures corresponding to these names.

        Returns
        -------
        list of dict :
            Each item describes a structure.

        """

        return self.nodes_by_property('name', names)

    @list_or_single
    def get_structures_by_acronym(self, acronyms):
        """Obtain a list of brain structures from their acronyms

        Parameters
        ----------
        acronyms : list of str
            Get structures corresponding to these acronyms.

        Returns
        -------
        list of dict :
            Each item describes a structure.

        """

        return self.nodes_by_property('acronym', acronyms)

    @list_or_single
    def get_structures_by_set_id(self, structure_set_ids):
        """Obtain a list of brain structures from by the sets that contain
        them.

        Parameters
        ----------
        structure_set_ids : list of int
            Get structures belonging to these structure sets.

        Returns
        -------
        list of dict :
            Each item describes a structure.

        """

        def overlap(x):
            return set(structure_set_ids) & set(x['structure_set_ids'])

        return self.filter_nodes(overlap)

    def get_colormap(self, key='acronym', value='hex'):
        """Get a dictionary mapping structure ids to colors across all nodes.

        Returns
        -------
        dict :
            Keys are structure ids. Values are RGB lists of integers.

        """
        if key == 'acronym':
            cmap = self.value_map(lambda x: x['acronym'],
                                  lambda y: y['rgb_triplet'])
        else:
            cmap = self.value_map(lambda x: x['id'],
                                  lambda y: y['rgb_triplet'])
        if value == 'hex':
            from matplotlib.colors import rgb2hex
            cmap = {k: rgb2hex(np.array(v) / 255) for k, v in cmap.items()}
        return cmap

    def get_name_map(self):
        """Get a dictionary mapping structure ids to names across all nodes.

        Returns
        -------
        dict :
            Keys are structure ids. Values are structure name strings.

        """

        return self.value_map(lambda x: x['id'],
                              lambda y: y['name'])

    def get_id_acronym_map(self):
        """Get a dictionary mapping structure acronyms to ids across all nodes.

        Returns
        -------
        dict :
            Keys are structure acronyms. Values are structure ids.

        """
        return self.value_map(lambda x: x['id'],
                              lambda y: y['acronym'])

    def get_acronym_id_map(self):
        """Get a dictionary mapping ids to structure acronyms across all nodes.

        Returns
        -------
        dict :
            Keys are structure acronyms. Values are structure ids.

        """

        return self.value_map(lambda x: x['acronym'],
                              lambda y: y['id'])

    def get_ancestor_id_map(self):
        """Get a dictionary mapping structure ids to ancestor ids across all
        nodes.

        Returns
        -------
        dict :
            Keys are structure ids. Values are lists of ancestor ids.

        """

        return self.value_map(lambda x: x['id'],
                              lambda y: self.ancestor_ids([y['id']])[0])

    def structure_descends_from(self, child_id, parent_id):
        """Tests whether one structure descends from another.

        Parameters
        ----------
        child_id : int or str
            ID or acronym of the putative child structure.
        parent_id : int or str
            ID or acronym of the putative parent structure.

        Returns
        -------
        bool :
            True if the structure specified by child_id is a descendant of
            the one specified by parent_id. Otherwise False.

        """
        # convert acronym to id
        if isinstance(child_id, str):
            child_id = self.acronym_to_id(child_id)
        if isinstance(parent_id, str):
            parent_id = self.acronym_to_id(parent_id)

        return parent_id in self.ancestor_ids([child_id])[0]

    def get_structure_sets(self):
        """Lists all unique structure sets that are assigned to at least one
        structure in the tree.

        Returns
        -------
        list of int :
            Elements are ids of structure sets.

        """

        return set(functools.reduce(op.add, map(lambda x: x['structure_set_ids'],
                                                self.nodes())))

    def has_overlaps(self, structure_ids):
        """Determine if a list of structures contains structures along with
        their ancestors

        Parameters
        ----------
        structure_ids : list of int
            Check this set of structures for overlaps

        Returns
        -------
        set :
            Ids of structures that are the ancestors of other structures in
            the supplied set.

        """

        ancestor_ids = functools.reduce(op.add,
                                        map(lambda x: x[1:],
                                            self.ancestor_ids(structure_ids)))
        return set(ancestor_ids) & set(structure_ids)

    def export_label_description(self, alphas=None, exclude_label_vis=None, exclude_mesh_vis=None, label_key='acronym'):
        """Produces an itksnap label_description table from this structure tree

        Parameters
        ----------
        alphas : dict, optional
            Maps structure ids to alpha levels. Optional - will only use provided ids.
        exclude_label_vis : list, optional
            The structures denoted by these ids will not be visible in ITKSnap.
        exclude_mesh_vis : list, optional
            The structures denoted by these ids will not have visible meshes in ITKSnap.
        label_key: str, optional
            Use this column for display labels.

        Returns
        -------
        pd.DataFrame :
            Contains data needed for loading as an ITKSnap label description file.

        """

        if alphas is None:
            alphas = {}
        if exclude_label_vis is None:
            exclude_label_vis = set([])
        if exclude_mesh_vis is None:
            exclude_mesh_vis = set([])

        df = pd.DataFrame([
            {
                'IDX': node['id'],
                '-R-': node['rgb_triplet'][0],
                '-G-': node['rgb_triplet'][1],
                '-B-': node['rgb_triplet'][2],
                '-A-': alphas.get(node['id'], 1.0),
                'VIS': 1 if node['id'] not in exclude_label_vis else 0,
                'MSH': 1 if node['id'] not in exclude_mesh_vis else 0,
                'LABEL': node[label_key]
            }
            for node in self.nodes()
        ]).loc[:, ('IDX', '-R-', '-G-', '-B-', '-A-', 'VIS', 'MSH', 'LABEL')]

        return df

    @staticmethod
    def clean_structures(structures, whitelist=None, data_transforms=None, renames=None):
        """Convert structures_with_sets query results into a form that can be
        used to construct a StructureTree

        Parameters
        ----------
        structures : list of dict
            Each element describes a structure. Should have a structure id path
            field (str values) and a structure_sets field (list of dict).
        whitelist : list of str, optional
            Only these fields will be included in the final structure record. Default is
            the output of StructureTree.whitelist.
        data_transforms : dict, optional
            Keys are str field names. Values are functions which will be applied to the
            data associated with those fields. Default is to map colors from hex to rgb and
            convert the structure id path to a list of int.
        renames : dict, optional
            Controls the field names that appear in the output structure records. Default is
            to map 'color_hex_triplet' to 'rgb_triplet'.

        Returns
        -------
        list of dict :
            structures, after conversion of structure_id_path and structure_sets

        """

        if whitelist is None:
            whitelist = StructureTree.whitelist()

        if data_transforms is None:
            data_transforms = StructureTree.data_transforms()

        if renames is None:
            renames = StructureTree.renames()
            whitelist.extend(renames.values())

        for ii, st in enumerate(structures):

            StructureTree.collect_sets(st)
            record = {}

            for name in whitelist:

                if name not in st:
                    continue
                data = st[name]

                if name in data_transforms:
                    data = data_transforms[name](data)

                if name in renames:
                    name = renames[name]

                record[name] = data

            structures[ii] = record

        return structures

    @staticmethod
    def data_transforms():
        return {'color_hex_triplet': StructureTree.hex_to_rgb,
                'structure_id_path': StructureTree.path_to_list}

    @staticmethod
    def renames():
        return {'color_hex_triplet': 'rgb_triplet'}

    @staticmethod
    def whitelist():
        return ['acronym', 'color_hex_triplet', 'graph_id', 'graph_order', 'id',
                'name', 'structure_id_path', 'structure_set_ids']

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert a hexadecimal color string to an uint8 triplet

        Parameters
        ----------
        hex_color : string
            Must be 6 characters long, unless it is 7 long and the first
            character is #. If hex_color is a triplet of int, it will be
            returned unchanged.

        Returns
        -------
        list of int :
            3 characters long - 1 per two characters in the input string.

        """

        if not isinstance(hex_color, str):
            return list(hex_color)

        if hex_color[0] == '#':
            hex_color = hex_color[1:]

        return [int(hex_color[a * 2: a * 2 + 2], 16) for a in range(3)]

    @staticmethod
    def path_to_list(path):
        """Structure id paths are sometimes formatted as "/"-seperated strings.
        This method converts them to a list of integers, if needed.
        """

        if not isinstance(path, str):
            return list(path)

        return [int(stid) for stid in path.split('/') if stid != '']

    @staticmethod
    def collect_sets(structure):
        """
        Structure sets may be specified by full records or id. This method
        collects all structure set records/ids in a structure record and
        replaces them with a single list of id records.
        """

        if 'structure_sets' not in structure:
            structure['structure_sets'] = []
        if 'structure_set_ids' not in structure:
            structure['structure_set_ids'] = []

        structure['structure_set_ids'].extend([sts['id'] for sts
                                               in structure['structure_sets']])
        structure['structure_set_ids'] = list(set(structure['structure_set_ids']))

        del structure['structure_sets']
