"""
 sdk_visitor:
 Contains SDKVisitor class which is used to obtain list of column names,
  table names, the columns used in joins, and filters applied to each column
"""
from typing import Dict, TypeVar, List, Union, OrderedDict

from sqlanalyzer import domain
from sqlanalyzer.domain import Ds, Expr, Op, Node, Attr, get_full_node_name, Statement, TableMappingList, TableMapping
from sqlanalyzer.util import lineage_visitor
from sqlanalyzer.util.BaseVisitor import BaseVisitor

T = TypeVar('T', Expr, Node)


class Trigger:
    def __init__(self, triggered=False):
        self.triggered = triggered

    def __bool__(self):
        return self.triggered

    def __enter__(self):
        self.triggered = True
        return self

    def __exit__(self, _type, value, traceback):
        self.triggered = False


class SDKVisitor(BaseVisitor):
    # __methods_list__ = []

    def __init__(self) -> None:
        super().__init__()

        self.lineage_visitor = lineage_visitor.LineageVisitor()
        self.column_list: List[T] = []

        self.table_list: List[Ds] = []

        # rework - does not make sense
        self.join_columns = set()
        self._join_tuple = tuple()
        self._join_triggered = Trigger()
        self._join_op_triggered = Trigger()

        self.column_filter_dict: Dict[Attr, List[Op]] = {}
        self._filter_last_op: Union[Op, None] = None
        self._filter_triggered = Trigger()

        # rework - does not make sense
        self._filter_column_join_op_triggered = Trigger()
        self._filter_column_join_triggered = Trigger()

        self.sort_columns: List[T] = []
        self._sort_triggered = Trigger()

        self.agg_columns: List[T] = []
        self._agg_triggered = Trigger()

        self._ds_table_type_out_triggered = Trigger()
        self._ds_table_type_triggered = Trigger()

    def get_columns(self) -> List[Expr]:
        """
        Getter function for column objects
        @rtype: List[Expr]
        @return: List of used columns
        """
        # removing duplicates
        return list(OrderedDict.fromkeys(self.column_list).keys())

    def get_column_names(self, full=False) -> List[str]:
        """
        Getter function for column names
        @param full: If True method returns fully qualified column name, but only if the column was resolved properly
        @rtype: List[str]
        @return: List of used column names
        """
        if full:
            return [x.get_full_name() for x in self.column_list]
        return [x.get_name() for x in self.column_list]

    def get_sort_columns(self) -> List[Expr]:
        """
        Getter function for sort columns
        @return: List of columns used with its direction in Order by
        @rtype: List[Expr]
        """
        return self.sort_columns

    def get_agg_columns(self) -> List[Expr]:
        """
        Getter function for aggregate columns
        @return: List of columns used with its direction in group by
        @rtype: List[Expr]
        """
        return self.agg_columns

    def get_tables(self) -> List[Ds]:
        """
        Getter function for list of tables used
        @return: List of tables names used
        @rtype: List[Ds]
        """
        # removing duplicates
        return list(OrderedDict.fromkeys(self.table_list).keys())

    def get_table_names(self, full=False) -> List[str]:
        """
        Getter function for list of table names
        @param full: If True method returns fully qualified column name, but only if the column was resolved properly
        @return: List of tables names used
        @rtype: List[Ds]
        """
        if full:
            return [x.get_full_name() for x in self.table_list]
        return [x.get_name() for x in self.table_list]

    def get_join_columns(self):
        """
        Getter function for list of columns used in joins
        @return:
        """
        return self.join_columns

    def get_filter_column_operations(self) -> Dict[Attr, List[Op]]:
        """
        Getter function for a dictionary of column and filters applied to it
        @return: Dictionary where key is the column name and values is a list of filters applied to the column
        """
        return self.column_filter_dict

    def get_filter_columns(self) -> List[Attr]:
        """
        Getter function for a dictionary of column and filters applied to it
        @return: List[Expr] List of columns used in the filters
        """
        return list(self.column_filter_dict.keys())

    def get_filter_operations(self, key: Attr) -> List[Op]:
        """
        Getter function for a list of operations for a given column object
        @param key: column object to lookup for operations list
        @return: List[Op] List of operations used in the filters for the given column
        """
        return self.column_filter_dict.get(key)

    def lineage(self):
        return self.lineage_visitor

    def visit_out(self, obj: domain.Out):
        if self._ds_table_type_triggered:
            with self._ds_table_type_out_triggered:
                BaseVisitor.visit_out(self, obj)
        else:
            BaseVisitor.visit_out(self, obj)

    def visit_ds(self, obj: domain.Ds):
        if obj.ds_type == "table":
            with self._ds_table_type_triggered:
                BaseVisitor.visit_ds(self, obj)
        else:
            BaseVisitor.visit_ds(self, obj)
        # Add REFERENCES of all dataset WITH TYPE table to table_names list
        if obj.ds_type == "table":
            self.table_list.append(obj)

    def visit_join(self, obj: domain.Join):
        with self._join_triggered:
            if obj.op is not None:
                with self._filter_column_join_triggered:
                    BaseVisitor.visit_join(self, obj)
            else:
                BaseVisitor.visit_join(self, obj)

    def visit_filter(self, obj: domain.Filter):
        with self._filter_triggered:
            BaseVisitor.visit_filter(self, obj)

    def visit_vfilter(self, obj: domain.Vfilter):
        with self._filter_triggered:
            BaseVisitor.visit_vfilter(self, obj)

    def visit_op(self, obj: domain.Op):
        # when visitor hits operator and filter is triggered, save reference to this operator
        if self._filter_triggered:
            self._filter_last_op = obj

        BaseVisitor.visit_op(self, obj)

    def visit_sort(self, obj: domain.Sort):
        with self._sort_triggered:
            BaseVisitor.visit_sort(self, obj)

    def visit_agg(self, obj: domain.Agg):
        with self._agg_triggered:
            BaseVisitor.visit_agg(self, obj)

    def visit_attr(self, obj: domain.Attr):
        BaseVisitor.visit_attr(self, obj)
        # if the attr is present a table type ds and is in the 'out' tag then don't add it
        if not self._ds_table_type_triggered and not self._ds_table_type_out_triggered:
            self.column_list.append(obj)

        fullref = get_full_node_name(obj)

        if self._join_op_triggered:
            self._join_tuple = (*self._join_tuple, fullref)

        # if filter is triggered (attr inside WHERE clause)
        # save column and last operation
        if self._filter_triggered:
            if obj in self.column_filter_dict.keys():
                self.column_filter_dict.get(obj).append(self._filter_last_op)
            else:
                self.column_filter_dict[obj] = [self._filter_last_op]

        if self._sort_triggered:
            # insert tuple
            self.sort_columns.append(obj)

        if self._agg_triggered.triggered:
            # insert tuple
            self.agg_columns.append(obj)

    def visit_statement(self, obj: Statement):
        super().visit_statement(obj)
        obj.accept(self.lineage_visitor)

    def get_table_mapping(self):
        return self.lineage_visitor.table_mapping

    def get_column_mapping(self):
        return self.lineage_visitor.column_mapping

    def get_column_full_mapping(self):
        return self.lineage_visitor.column_full_mapping


# # Detect available methods
# _visitor = SDKVisitor()
# SDKVisitor.__methods_list__ = [func for func in dir(_visitor) if
#                                callable(getattr(_visitor, func)) and not func.startswith("__") and not func.startswith(
#                                    "visit")]
