"""
 Visitor:
 Contains a bare-bones visitor(design pattern) class for all the nodes.
 @param - Node Object
 @return - None
"""
from abc import ABC, abstractmethod


class Visitor(ABC):

    @abstractmethod
    def visit_agg(self, obj):
        pass

    @abstractmethod
    def visit_attr(self, obj):
        pass

    @abstractmethod
    def visit_antipattern(self, obj):
        pass

    @abstractmethod
    def visit_antipatterns(self, obj):
        pass

    @abstractmethod
    def visit_case(self, obj):
        pass

    @abstractmethod
    def visit_cast(self, obj):
        pass

    @abstractmethod
    def visit_columndef(self, obj):
        pass

    @abstractmethod
    def visit_const(self, obj):
        pass

    @abstractmethod
    def visit_copy(self, obj):
        pass

    @abstractmethod
    def visit_current(self, obj):
        pass

    @abstractmethod
    def visit_create(self, obj):
        pass

    @abstractmethod
    def visit_create_stage(self, obj):
        pass

    @abstractmethod
    def visit_create_view(self, obj):
        pass

    @abstractmethod
    def visit_delete(self, obj):
        pass

    @abstractmethod
    def visit_ds(self, obj):
        pass

    @abstractmethod
    def visit_edge(self, obj):
        pass

    @abstractmethod
    def visit_else(self, obj):
        pass

    @abstractmethod
    def visit_error(self, obj):
        pass

    @abstractmethod
    def visit_expr(self, obj):
        pass

    @abstractmethod
    def visit_filter(self, obj):
        pass

    @abstractmethod
    def visit_frame(self, obj):
        pass

    @abstractmethod
    def visit_func(self, obj):
        pass

    @abstractmethod
    def visit_in(self, obj):
        pass

    @abstractmethod
    def visit_inlinetable(self, obj):
        pass

    @abstractmethod
    def visit_into(self, obj):
        pass

    @abstractmethod
    def visit_insert(self, obj):
        pass

    @abstractmethod
    def visit_join(self, obj):
        pass

    @abstractmethod
    def visit_match_recognize(self, obj):
        pass

    @abstractmethod
    def visit_merge(self, obj):
        pass

    @abstractmethod
    def visit_multivalue(self, obj):
        pass

    @abstractmethod
    def visit_op(self, obj):
        pass

    @abstractmethod
    def visit_out(self, obj):
        pass

    @abstractmethod
    def visit_page(self, obj):
        pass

    @abstractmethod
    def visit_parseql(self, obj):
        pass

    @abstractmethod
    def visit_rotate(self, obj):
        pass

    @abstractmethod
    def visit_sort(self, obj):
        pass

    @abstractmethod
    def visit_statement(self, obj):
        pass

    @abstractmethod
    def visit_queryingstage(self, obj):
        pass

    @abstractmethod
    def visit_structref(self, obj):
        pass

    @abstractmethod
    def visit_tablefunc(self, obj):
        pass

    @abstractmethod
    def visit_tablesample(self, obj):
        pass

    @abstractmethod
    def visit_then(self, obj):
        pass

    @abstractmethod
    def visit_update(self, obj):
        pass

    @abstractmethod
    def visit_vagg(self, obj):
        pass

    @abstractmethod
    def visit_vfilter(self, obj):
        pass

    @abstractmethod
    def visit_wfunc(self, obj):
        pass

    @abstractmethod
    def visit_when(self, obj):
        pass
