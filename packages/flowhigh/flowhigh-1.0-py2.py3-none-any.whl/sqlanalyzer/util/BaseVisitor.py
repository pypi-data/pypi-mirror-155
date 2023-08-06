"""
 BaseVisitor:
 Implements Visitor class and prints the object.
 It is meant to be a basic visitor which can be built upon.
"""

from sqlanalyzer.domain import *
from sqlanalyzer.util.Visitor import Visitor

N = TypeVar('N', Node, Node)


class BaseVisitor(Visitor):
    verbose = False

    def visit_agg(self, obj: Agg):
        """
        Visits Agg Node
        @param obj: Agg
        @return: None
        """
        if self.verbose:
            print("visit_agg")
            print(obj)
        self.visit_all(obj)

    def visit_attr(self, obj: Attr):
        """
        Visits Attr Node
        @param obj: Attr
        @return: None
        """
        if self.verbose:
            print("visit_attr")
            print(obj)

    def visit_antipattern(self, obj):
        """
        Visits AntiPattern Node
        @param obj: AntiPattern
        @return: None
        """
        if self.verbose:
            print("visit_antipattern")
            print(obj)
        self.visit_all(obj)

    def visit_antipatterns(self, obj):
        """
        Visits AntiPatterns Node
        @param obj: AntiPatterns
        @return: None
        """
        if self.verbose:
            print("visit_antipatterns")
            print(obj)
        self.visit_all(obj)

    def visit_case(self, obj: Case):
        """
        Visits Case Node
        @param obj: Case
        @return: None
        """
        if self.verbose:
            print("visit_agg")
            print(obj)
        self.visit_all(obj)

    def visit_cast(self, obj: Cast):
        """
        Visits Cast Node
        @param obj: Cast
        @return: None
        """
        if self.verbose:
            print("visit_cast")
            print(obj)
        self.visit_all(obj)

    def visit_columndef(self, obj: ColumnDef):
        """
        Visits ColumnDef Node
        @param obj: ColumnDef
        @return: None
        """
        if self.verbose:
            print("visit_columnDef")
            print(obj)

    def visit_const(self, obj: Const):
        """
        Visits Const Node
        @param obj: Const
        @return: None
        """
        if self.verbose:
            print("visit_const")
            print(obj)

    def visit_copy(self, obj: Copy):
        """
        Visits Copy Node
        @param obj: Copy
        @return: None
        """
        if self.verbose:
            print("visit_copy")
            print(obj)
        self.visit_all(obj)

    def visit_current(self, obj: Current):
        """
        Visits Current Node
        @param obj: Current
        @return: None
        """
        if self.verbose:
            print("visit_current")
            print(obj)

    def visit_create(self, obj: Create):
        """
        Visits Create Node
        @param obj: Create
        @return: None
        """
        if self.verbose:
            print("visit_create")
            print(obj)
        self.visit_all(obj)

    def visit_create_view(self, obj: CreateView):
        """
        Visits Create View Node
        @param obj: CreateView
        @return: None
        """
        if self.verbose:
            print("visit_create_view")
            print(obj)
        self.visit_all(obj)

    def visit_create_stage(self, obj: CreateStage):
        """
        Visits Create Stage Node
        @param obj: CreateStage
        @return: None
        """
        if self.verbose:
            print("visit_create_stage")
            print(obj)

    def visit_delete(self, obj: Delete):
        """
        Visits Delete Node
        @param obj: Delete
        @return: None
        """
        if self.verbose:
            print("visit_delete")
            print(obj)
        self.visit_all(obj)

    def visit_ds(self, obj: Ds):
        """
        Visits Ds Node
        @param obj: Ds
        @return: None
        """
        if self.verbose:
            print("visit_ds")
            print(obj)
        self.visit_all(obj)

    def visit_edge(self, obj: Edge):
        """
        Visits Edge Node
        @param obj: Edge
        @return: None
        """
        if self.verbose:
            print("visit_edge")
            print(obj)
        self.visit_all(obj)

    def visit_else(self, obj: Else):
        """
        Visits Else Node
        @param obj: Else
        @return: None
        """
        if self.verbose:
            print("visit_else")
            print(obj)
        self.visit_all(obj)

    def visit_error(self, obj: Error):
        """
        Visits Error Node
        @param obj: Error
        @return: None
        """
        if self.verbose:
            print("visit_error")
            print(obj)

    def visit_expr(self, obj: Expr):
        """
        Visits Expr Node
        @param obj: Expr
        @return: None
        """
        if self.verbose:
            print("visit_expr")
            print(obj)

    def visit_filter(self, obj: Filter):
        """
        Visits Filter Node
        @param obj: Filter
        @return: None
        """
        if self.verbose:
            print("visit_filter")
            print(obj)
        self.visit_all(obj)

    def visit_frame(self, obj: Frame):
        """
        Visits Frame Node
        @param obj: Frame
        @return: None
        """
        if self.verbose:
            print("visit_frame")
            print(obj)
        self.visit_all(obj)

    def visit_func(self, obj: Func):
        """
        Visits Func Node
        @param obj: Func
        @return: None
        """
        if self.verbose:
            print("visit_func")
            print(obj)
        self.visit_all(obj)

    def visit_in(self, obj: In):
        """
        Visits In Node
        @param obj: In
        @return: None
        """
        if self.verbose:
            print("visit_in")
            print(obj)
        self.visit_all(obj)

    def visit_inlinetable(self, obj: InlineTable):
        """
        Visits InlineTable Node
        @param obj: InlineTable
        @return: None
        """
        if self.verbose:
            print("visit_inlinetable")
            print(obj)
        self.visit_all(obj)

    def visit_into(self, obj: Into):
        """
        Visits Into Node
        @param obj: Into
        @return: None
        """
        if self.verbose:
            print("visit_into")
            print(obj)
        self.visit_all(obj)

    def visit_insert(self, obj: Insert):
        """
        Visits Insert Node
        @param obj: Insert
        @return: None
        """
        if self.verbose:
            print("visit_insert")
            print(obj)
        self.visit_all(obj)

    def visit_join(self, obj: Join):
        """
        Visits Join Node
        @param obj: Join
        @return: None
        """
        if self.verbose:
            print("visit_join")
            print(obj)
        self.visit_all(obj)

    def visit_match_recognize(self, obj: MatchRecognize):
        """
        Visits MatchRecognize Node
        @param obj: MatchRecognize
        @return: None
        """
        if self.verbose:
            print("visit_match_recognize")
            print(obj)

    def visit_merge(self, obj: Merge):
        """
        Visits Merge Node
        @param obj: Merge
        @return: None
        """
        if self.verbose:
            print("visit_merge")
            print(obj)
        self.visit_all(obj)

    def visit_multivalue(self, obj: MultiValue):
        """
        Visits MultiValue Node
        @param obj: MultiValue
        @return: None
        """
        if self.verbose:
            print("visit_multivalue")
            print(obj)
        self.visit_all(obj)

    def visit_op(self, obj: Op):
        """
        Visits Op Node
        @param obj: Op
        @return: None
        """
        if self.verbose:
            print("visit_op")
            print(obj)
        self.visit_all(obj)

    def visit_out(self, obj: Out):
        """
        Visits Out Node
        @param obj: Out
        @return: None
        """
        if self.verbose:
            print("visit_out")
            print(obj)
        self.visit_all(obj)

    def visit_page(self, obj: Page):
        """
        Visits Page Node
        @param obj: Page
        @return: None
        """
        if self.verbose:
            print("visit_page")
            print(obj)

    def visit_parseql(self, obj: ParSeQL):
        """
        Visits ParSeQL Node
        @param obj: ParSeQL
        @return: None
        """
        if self.verbose:
            print("visit_parseql")
            print(obj)
        self.visit_all(obj)

    def visit_rotate(self, obj: Rotate):
        """
        Visits Rotate Node
        @param obj: Rotate
        @return: None
        """
        if self.verbose:
            print("visit_rotate")
            print(obj)
        self.visit_all(obj)

    def visit_sort(self, obj: Sort):
        """
        Visits Sort Node
        @param obj: Sort
        @return: None
        """
        if self.verbose:
            print("visit_sort")
            print(obj)
        self.visit_all(obj)

    def visit_statement(self, obj: Statement):
        """
        Visits Statement Node
        @param obj: Statement
        @return: None
        """
        if self.verbose:
            print("visit_statement")
            print(obj)

        self.visit_all(obj)

    def visit_queryingstage(self, obj: QueryingStage):
        """
        Visits QueryingStage Node
        @param obj: QueryingStage
        @return: None
        """
        if self.verbose:
            print("visit_queryingstage")
            print(obj)

    def visit_structref(self, obj: StructRef):
        """
        Visits StructRef Node
        @param obj: StructRef
        @return: None
        """
        if self.verbose:
            print("visit_structref")
            print(obj)

    def visit_tablefunc(self, obj: TableFunc):
        """
        Visits TableFunc Node
        @param obj: TableFunc
        @return: None
        """
        if self.verbose:
            print("visit_tablefunc")
            print(obj)
        self.visit_all(obj)

    def visit_tablesample(self, obj: TableSample):
        """
        Visits TableSample Node
        @param obj: TableSample
        @return: None
        """
        if self.verbose:
            print("visit_tablesample")
            print(obj)

    def visit_then(self, obj: Then):
        """
        Visits Then Node
        @param obj: Then
        @return: None
        """
        if self.verbose:
            print("visit_then")
            print(obj)
        self.visit_all(obj)

    def visit_update(self, obj: Update):
        """
        Visits Update Node
        @param obj: Update
        @return: None
        """
        if self.verbose:
            print("visit_update")
            print(obj)
        self.visit_all(obj)

    def visit_vagg(self, obj: Vagg):
        """
        Visits Vagg Node
        @param obj: Vagg
        @return: None
        """
        if self.verbose:
            print("visit_vagg")
            print(obj)
        self.visit_all(obj)

    def visit_vfilter(self, obj: Vfilter):
        """
        Visits Vfilter Node
        @param obj: Vfilter
        @return: None
        """
        if self.verbose:
            print("visit_vfilter")
            print(obj)
        self.visit_all(obj)

    def visit_wfunc(self, obj: Wfunc):
        """
        Visits Wfunc Node
        @param obj: Wfunc
        @return: None
        """
        if self.verbose:
            print("visit_wfunc")
            print(obj)
        self.visit_all(obj)

    def visit_when(self, obj: When):
        """
        Visits When Node
        @param obj: When
        @return: None
        """
        if self.verbose:
            print("visit_when")
            print(obj)
        self.visit_all(obj)

    def visit_all(self, obj: N):
        z = vars(obj)
        for k, v in z.items():
            if v and type(v) is list:
                v_list: List = v
                for item in v_list:
                    if issubclass(type(item), Node):
                        item: Node = item
                        item.accept(self)
            elif v and issubclass(type(v), Node):
                v_node: Node = v
                v_node.accept(self)
