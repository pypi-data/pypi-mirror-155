"""
 lineage_visitor module:

 Contains a class LineageVisitor which extends BaseVisitor to find lineage of all columns,
 and a function to obtain the full reference of a column.
"""

from flowhigh.domain import *
from flowhigh.util.BaseVisitor import BaseVisitor


def get_ds_scope(ds: Ds) -> List[Expr]:
    if ds.out_obj is not None:
        output = []
        for expr in ds.out_obj.expr:
            ref = AttrRef.from_attr(expr, ds)
            output.append(ref)
        return output
    return []


class AttrDetector(BaseVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.attr_list: List[Attr] = []

    def visit_attr(self, obj: Attr):
        self.attr_list.append(obj)

    @staticmethod
    def detect(expr):
        detector = AttrDetector()
        expr.accept(detector)
        return detector.attr_list


class LineageVisitor(BaseVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.ds_scope = {}
        self.ds_attr_link = {}
        self.columns = []

        self.current_ds = None
        self.id_to_ds = {}
        self.ds_scope_id = {}

        self.column_mapping = ColumnMappingList()
        self.column_full_mapping = ColumnMappingList()
        self.table_mapping = TableMappingList()

    def get_column_and_lineage(self):
        """
        Getter function for column and lineage dictionary
        @return: Column and Lineage dictionary
        """
        return self.column_mapping

    def visit_ds(self, obj: Ds):
        # save to id_to_ds map
        if not obj.id:
            print("Error - no id found on DS")
            return

        if obj.id not in self.ds_scope_id.keys():
            self.ds_scope_id[obj.id] = []

        if obj.id not in self.ds_scope.keys():
            self.ds_scope[obj.id] = get_ds_scope(obj)

        # enter object, save global pointer to local variable and move global pointer to current object
        self.id_to_ds[obj.id] = obj
        prev_ds = self.current_ds
        self.current_ds = obj
        # also add current DS to a scope of saved DS if saved DS is present
        if prev_ds is not None:
            # but add only if it does not reference to CTE
            if obj._refTo is None:
                self.ds_scope_id[prev_ds.id].append(obj)
            else:
                ref_obj = self.id_to_ds[obj._refTo]
                self.ds_scope_id[prev_ds.id].append(ref_obj)
        # BaseVisitor.visit_ds(self, obj)
        if obj.in_obj is not None:
            for expr in obj.in_obj.expr:
                expr.accept(self)
        if obj.out_obj is not None:
            for expr in obj.out_obj.expr:
                expr.accept(self)
        # restore global variable
        self.current_ds = prev_ds

    def visit_statement(self, obj: Statement):
        """
        Visit statement node and all the sub-nodes to find the lineage of all columns
        @param obj: Statement
        @return: None
        """
        # visit all the nodes first and then try to find lineage of all columns
        BaseVisitor.visit_statement(self, obj)
        # the main select goes last one
        if len(obj.ds) > 0:
            self.follow_trail(obj.ds[-1])

        for create in obj.create:
            if create.ds:
                self.follow_trail(create.ds)

        for insert in obj.insert:
            for into in insert.intos:
                self.follow_trail(into.target)

        for merge in obj.merge:
            self.follow_trail(merge.target)

    def follow_trail(self, ds: Ds):
        # simple check for expressions presence
        if not ds.out_obj:
            return

        for column in ds.out_obj.expr:
            # for each column - get number of attributes to trail
            # for example - for attr it's singleton list
            # for functions or other complex expressions it will be a list of 0 to many attributes
            # each should be as an entry for mapping
            for attr in AttrDetector.detect(column):
                self.traverse_attr(attr, ds, [AttrRef.from_attr(column, ds)])

    def add_trail_to_mapping(self, trail):
        mapping_entry = self._trail_to_column_mapping_entry(trail)
        mapping_entries = self._trail_to_column_mapping_entries(trail)
        table_mapping_entry = self._trail_to_table_mapping_entry(trail)
        self.column_mapping.append(mapping_entry)
        for entry in mapping_entries:
            if entry not in self.column_full_mapping:
                self.column_full_mapping.append(entry)
        #self.column_full_mapping.extend(mapping_entries)
        self.table_mapping.append(table_mapping_entry)

    def traverse_attr(self, obj, ds, trail: List):
        if not isinstance(obj, Attr):
            self.add_trail_to_mapping(trail)
            return trail

        if not hasattr(obj, "refds") or obj.refds is None:
            self.add_trail_to_mapping(trail)
            return trail

        if ds.id is None:
            self.add_trail_to_mapping(trail)
            return trail

        # lookup Datasets in scope based on obj.refds value
        #
        scope = self.ds_scope_id[ds.id]
        for entry in scope:
            if not hasattr(entry, "refds") or entry.refds is None:
                continue

            if entry.refds != obj.refds and entry.alias != obj.refds:
                continue

            # if entry is table, then nothing to lookup, and just add trail
            if entry.out_obj is None:
                trail.append(AttrRef.from_attr(obj, entry))
                self.add_trail_to_mapping(trail)
                return trail

            # we need to look up in entry (dataset we found, the proper attribute)
            for entry_obj in entry.out_obj.expr:
                # in entry primary name we use is alias, otherwise - refatt
                entry_obj_name = None
                if entry_obj.alias != '':
                    entry_obj_name = entry_obj.alias
                elif hasattr(entry_obj, 'refatt'):
                    entry_obj_name = entry_obj.refatt
                else:
                    continue

                if entry_obj_name != obj.refatt:
                    continue

                trail.append(AttrRef.from_attr(entry_obj, entry))
                for attr in AttrDetector.detect(entry_obj):
                    self.traverse_attr(attr, entry, trail.copy())
                return trail

        self.add_trail_to_mapping(trail)
        return trail

    def _trail_to_column_mapping_entry(self, trail: List):
        entry = ColumnMapping()
        entry['target'] = trail[0]
        if len(trail) > 1:
            entry['source'] = trail[-1]
        else:
            entry['source'] = AttrRef()
        return entry

    def _trail_to_column_mapping_entries(self, trail: List):
        entries = []
        if len(trail) > 1:
            for i in range(0, len(trail) - 1):
                target = trail[i]
                source = trail[i + 1]
                entry = ColumnMapping(i)
                entry['target'] = target
                entry['source'] = source
                entries.append(entry)
        else:
            entries.append(self._trail_to_column_mapping_entry(trail))
        return entries

    def _trail_to_table_mapping_entry(self, trail):
        entry = TableMapping()
        entry['target'] = trail[0]['ds']
        if len(trail) > 1:
            entry['source'] = trail[-1]['ds']
        else:
            entry['source'] = None
        return entry
