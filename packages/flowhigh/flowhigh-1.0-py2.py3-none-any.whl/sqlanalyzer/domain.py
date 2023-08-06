"""
 domain module:
 Contains all the classes that are used to create individual nodes from the message received from the API.
"""
import json
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import List, Union, TypeVar
from typing import TYPE_CHECKING

from sqlanalyzer.util.generic_repr import generic_repr

if TYPE_CHECKING:
    from sqlanalyzer.util.sdk_visitor import SDKVisitor


def decorator_func(func):
    def new_func(*args, **kwargs):
        out = func(*args, **kwargs)
        return out

    return new_func


@dataclass
class Node(ABC):
    """
    The base class for all the nodes in the sdk.
    Contains a visitor which is used to obtain specific details about the query that is being processed.
    """
    visitor: 'SDKVisitor' = field(init=False, default=None)
    _json_dict: dict = field(init=False, default=None)

    def as_json(self, **kwargs) -> str:
        """
        @param ** kwargs: All parameters are passed to json.dumps() function
        @return: Json string representing current object
        """
        return json.dumps(self._json_dict, **kwargs)

    def as_dict(self) -> dict:
        """
        @return: Dict object representing current object
        """
        return self._json_dict

    @abstractmethod
    def accept(self, visitor):
        pass

    # def __getattr__(self, name: str):
    #     delegate = self.visitor
    #     try:
    #         if name in self.visitor.__methods_list__:
    #             attribute = delegate.__getattribute__(name)
    #             return decorator_func(attribute)
    #         raise AttributeError()
    #     except AttributeError as e:
    #         raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))

    def get_table_mapping(self):
        return self.visitor.get_table_mapping()

    def get_column_mapping(self):
        return self.visitor.get_column_mapping()

    def get_column_full_mapping(self):
        return self.visitor.get_column_full_mapping()


@dataclass
class Expr(Node):
    """
    Expr - Expression: A unit comprising another expression, function, window function,
            constant, column attributes, or operation.
    """
    value: object  # object
    alias: str
    direction: str

    def get_full_name(self):
        return None

    def get_name(self):
        return self.alias

    def get_table(self):
        return None

    def get_raw(self):
        return ""

    def accept(self, visitor):
        pass

    def __hash__(self) -> int:
        return hash(str(self))


T = TypeVar('T', Expr, Node)


@generic_repr
@dataclass
class Op(Expr):
    """
    Op - Operation: This node consists of comprising operations between other operators, functions,
            attributes, Case/when, constants, datasets, joins, and windows.
    This node contains a list of expressions and the type of operation applied to them.
    """
    expr: List[T]
    op_type: str
    rawInput: str = ""

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def get_table(self):
        pass

    def accept(self, visitor):
        visitor.visit_op(self)

    def get_raw(self):
        return self.rawInput

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass
class Filter(Node):
    """
    Filter contains information regarding the where, having, and qualify clauses.
            This in-turn involves operations.
    """
    op: Op

    def accept(self, visitor):
        visitor.visit_filter(self)

    def __hash__(self) -> int:
        return hash(self.op)


@dataclass()
@generic_repr
class Agg(Node):
    """
    Agg - Aggregation - Is the order by clause which contains a list of attributes
            and a having clause.
    """
    expr: List[T]
    filter: Filter

    def accept(self, visitor):
        visitor.visit_agg(self)

    def __hash__(self) -> int:
        return hash((tuple(self.expr), self.filter))


@generic_repr
@dataclass()
class Vfilter(Node):
    """
    Vertical filters are the filters which are applied in the Qualify clause.
    """
    expr: T

    def accept(self, visitor):
        visitor.visit_vfilter(self)


@generic_repr
@dataclass()
class Vagg(Node):
    """
    VAgg - Vertical Aggregation - Is the Qualify Clause which contains vertical filter applied to the dataset.
    """
    vfilter: Vfilter

    def accept(self, visitor):
        visitor.visit_vagg(self)


@generic_repr
@dataclass()
class Attr(Expr):
    """
    Attr - Attributes: The smallest unit in the query. Can contain reference to other
    attributes(in the case of alias), tables, datasets, tables, databases, and schema.
    refvar - Contains the name of the variable to which the attribute references to
    refatt - Contains the name of reference to the source attribute which has been aliased.
    refds - Contains the name of the dataset which has been referenced.
    refdb - Contains the name of the database which has been referenced.
    refsch - Contains the name of the schema which has been referenced.
    fullref - Combined full reference(name) of the attribute
    refoutidx - Number which is used to indicate an attribute from the select clause's attribute list
    """
    refvar: str
    refatt: str
    refds: str
    refdb: str
    refsch: str
    fullref: str
    refoutidx: str
    rawInput: str = ""

    def accept(self, visitor):
        visitor.visit_attr(self)

    def get_full_name(self):
        # fullref_list = []
        # if self.fullref != "":
        #     return self.fullref
        # else:
        #     if self.refdb != "":
        #         fullref_list.append(self.refdb)
        #     if self.refsch != "":
        #         fullref_list.append(self.refsch)
        #     if self.refds != "":
        #         fullref_list.append(self.refds)
        #     elif self.reftab != "":
        #         fullref_list.append(self.reftab)
        #     if self.refatt != "":
        #         fullref_list.append(self.refatt)
        #
        #     fullref = ".".join(fullref_list)
        return get_full_node_name(self)

    def get_name(self):
        return self.refatt

    def get_table(self):
        if self.refds != "":
            return self.refds

    def get_raw(self):
        return self.rawInput

    def __hash__(self) -> int:
        return hash((self.refvar, self.refatt, self.refds, self.refdb, self.refsch, self.refoutidx))

    def __eq__(self, other):
        return (other and isinstance(other, Attr)
                and hash(self) == hash(other)
                # and self.refvar == other.refvar
                # and self.refatt == other.refatt
                # and self.refds == other.refds
                # and self.refdb == other.refds
                # and self.refsch == other.refsch
                # and self.refoutidx == other.refoutidx
                )


@generic_repr
@dataclass()
class Else(Node):
    """
    Contains information about what should occur if none of the when clause conditions are satisfied.
    """
    expr: T

    def accept(self, visitor):
        visitor.visit_else(self)


@generic_repr
@dataclass()
class Then(Expr):
    """
    Contains information about what to do after the corresponding when condition is satisfied.
    """
    expr: T

    def accept(self, visitor):
        visitor.visit_then(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class When(Expr):
    """
    Contains information about the conditions that are checked for the then clause to take effect.
    """
    expr: T
    then: Then

    def accept(self, visitor):
        visitor.visit_when(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Case(Expr):
    """
    Case clause - Contains information regarding the case when clause.
    It includes attribute/expression, list of when clause (includes then clause), and else clause
    """
    expr: T
    when: List[When]
    else_obj: Else

    def accept(self, visitor):
        visitor.visit_case(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class In(Node):
    """
    In - Input - Is the from clause which contains all the inputs for the query. (Joins, dataset, operations on dataset)
    """
    expr: List[T]  # expr

    def accept(self, visitor):
        visitor.visit_in(self)


@generic_repr
@dataclass()
class InlineTable(Expr):
    """
    Inline table node - Contains a list of expressions which in the query are separated by a comma
    Ex - SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three'));
        -> VALUES (1, 'one'), (2, 'two'), (3, 'three') is the inline table
    """
    expr: List[T]  # expr

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def get_table(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_inlinetable(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Out(Node):
    """
    Out - Output - Is the select clause which contains list of expressions.
    """
    expr: List[T]

    def accept(self, visitor):
        visitor.visit_out(self)


@generic_repr
@dataclass()
class Sort(Node):
    """
    Sort - Order By - Comprised of the attributes or constant with which the
            output must be sorted in either direction(ascending or descending).
            (Default - ascending)
    """
    expr: List[T]

    def accept(self, visitor):
        visitor.visit_sort(self)


@generic_repr
@dataclass()
class Page(Node):
    """
    Contains information about paging. Used to only display a limited number of results.
    Page type can be - limit, fetch, or top.
    """
    page_type: str
    value: T

    def accept(self, visitor):
        visitor.visit_page(self)


@generic_repr
@dataclass()
class TableSample(Expr):
    """
    Table Sample or Sample is used to return a subset of rows sampled randomly from the specified table
    Sampling method can contain - BERNOULLI, ROW, SYSTEM, or BLOCK
    sample type is either SAMPLE or TABLESAMPLE
    probability specifies the percentage probability to use for selecting the sample
    num specifies the number of rows to sample from the table
    seed type can be either REPEATABLE or SEED
    seed is used to specify a seed value to make the sampling deterministic
    """
    sample_method: str
    sample_type: str
    probability: str
    num: str
    seedType: str
    seed: str

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_queryingstage(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class MatchRecognize(Expr):
    """
    MATCH_RECOGNIZE accepts a set of rows (from a table, view, subquery, or other source) as input,
        and returns all matches for a given row pattern within this set
    Define is used to define symbols for expressions
    Pattern stores the pattern that is used to match a valid sequence of rows
    Order By - This is the order in which the individual rows of each partition are passed
        to the MATCH_RECOGNIZE operator
    Partition by is used to specify an expression that groups rows that are related to each other
    Row condition specifies what should occur for the row action to take place
    Row action defines what should happen when the condition is met
    """
    partition_by: str
    order_by: str
    measure: str
    row_condition: str
    row_action: str
    pattern: str
    define: str

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_match_recognize(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Ds(Expr):
    """
    Ds - Dataset - Acts as a wrapper and contains all the data for a full or partial query.
            Contains select, from, joins, where, groupBy, having, qualify, sorting, sampling, pattern matching
            and paging details.
    """
    # order matters for new visit_all behaviour
    out_obj: Out
    in_obj: In
    match_recognize: MatchRecognize
    table_sample: TableSample
    filter: Filter
    agg: Agg
    vagg: Vagg
    sort: Sort
    page: Page
    setOp: List[Op]  # Op
    ds_type: str
    name: str
    refdb: str
    refds: str
    refsch: str
    fullref: str
    _id: str
    _refTo: str
    rawInput: str

    def __hash__(self) -> int:
        return hash((self.refds, self.refdb, self.refsch, self.ds_type, self.filter, self.agg, self.vagg))

    # def __eq__(self, other):
    #     return (other
    #             and (self.reftab == other.reftab
    #                  or self.refds == other.refds)
    #             and self.refdb == other.refds
    #             and self.refsch == other.refsch
    #             and self.ds_type == other.ds_type
    #             )

    def accept(self, visitor):
        visitor.visit_ds(self)

    def get_name(self):
        if self.refds != "":
            return self.refds

    def get_full_name(self):
        # fullref_list = []
        # if self.fullref != "":
        #     return self.fullref
        # else:
        #     if self.refdb != "":
        #         fullref_list.append(self.refdb)
        #     if self.refsch != "":
        #         fullref_list.append(self.refsch)
        #     if self.refds != "":
        #         fullref_list.append(self.refds)
        #     elif self.reftab != "":
        #         fullref_list.append(self.reftab)
        #     # if self.refatt != "":
        #     #     fullref_list.append(self.refatt)
        #
        #     fullref = ".".join(fullref_list)
        return get_full_node_name(self)

    def get_table(self):
        pass


@generic_repr
@dataclass()
class QueryingStage(Expr):
    """
    Contains staged data files' details
    Location specifies where the data is being used from
    File format specifies the format of the file
    Pattern is used to further filter the files in the staged location
    """
    location: str
    file_format: str
    pattern: str

    def accept(self, visitor):
        visitor.visit_queryingstage(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Func(Expr):
    """
    Func - Function: Contains all function names and their types.
            attributes(in the case of alias), tables, datasets, tables, databases, and schema.
            FuncType - Contains the type of function being used (Scalar, Window, Aggregate).
            Name - Contains the name of the function.
            Within group specifies order by part of the function in the case of "listagg" or similar
    """
    expr: List[T]
    within_group: Ds
    func_type: str
    name: str

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_func(self)

    def get_raw(self):
        args = ""
        args_list = [x.get_raw() for x in self.expr]
        if len(args_list) > 0:
            args = ", ".join(args_list)
        return "{name}({args})".format(name=self.name, args=args)

    def __hash__(self) -> int:
        return hash((self.expr, self.name, self.alias, self.func_type, self.within_group))


@generic_repr
@dataclass()
class Cast(Expr):
    """
    Cast node contains the data and the data type to which the input needs to be converted into.
    """
    exp: T
    data_type: str

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_cast(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class ColumnDef(Node):
    """
    Column definitions - Are used in create table/view clause
    Contains the name of column, the data type, precision, and scale.
    """
    name: str
    data_type: str
    precision: str
    scale: str

    def accept(self, visitor):
        visitor.visit_columndef(self)


@generic_repr
@dataclass()
class Const(Expr):
    """
    Const - Constants: A unit comprising a constant value.
    """

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def get_table(self):
        pass

    def accept(self, visitor):
        visitor.visit_const(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Copy(Node):
    """
    Copy node contains details about data that is to be loaded from staged files to an existing table/location
    into contains the dataset to which the data needs to be loaded
    target columns contains the list of columns to which the data will be loaded
    from exp is the data source in case the source is specified through select statement
    from query is the data source if the source is an entire query
    from stage is the data source if the location of the stage is specified
    partition contains list of expressions which are used for partitioning
    file format specifies the format of the data source
    file specifies the name of the file
    Header specifies if header is used
    pattern is used for pattern matching (regex)
    copy options contains information about things like specifying size limit, enabling purging etc
    validation defines the validation mode
    """
    into: Ds
    target_columns: List[str]
    from_exp: List[str]  # str
    from_query: Ds  # ds
    select_element: List[T]
    from_stage: Ds
    partition: List[T]  # expr
    file_format: str
    file: str
    header: bool
    pattern: str
    copy_options: str
    validation: str

    def accept(self, visitor):
        visitor.visit_copy(self)


@generic_repr
@dataclass()
class Current(Expr):
    """
    Current expressions are store in this node
    Ex - CURRENT_TIME
    """
    current_type: str

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_current(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Create(Node):
    """
    Create table contains ColumnDefinition, Cluster By, and Queries.
    type can be either TEMPORARY, VOLATILE, TRANSIENT
    """
    column_def: List[ColumnDef]  # columnDef
    ds: Ds
    cluster_by: List[T]  # expr
    create_type: str
    scope: str
    refdb: str
    refds: str
    refsch: str

    def get_name(self):
        # fullref_list = []
        # if self.fullref != "":
        #     return self.fullref
        # else:
        #     if self.refdb != "":
        #         fullref_list.append(self.refdb)
        #     if self.refsch != "":
        #         fullref_list.append(self.refsch)
        #     if self.refds != "":
        #         fullref_list.append(self.refds)
        #     elif self.reftab != "":
        #         fullref_list.append(self.reftab)
        #
        #     fullref = ".".join(fullref_list)
        return get_full_node_name(self)

    def accept(self, visitor):
        visitor.visit_create(self)


@generic_repr
@dataclass()
class CreateView(Node):
    """
    Create view node is used to store details about create view statement
    replace specifies if the view being created can be replaced if it exists already
    not exists specifies action on whether we should check if a view exists or not
    columns contains a list of names of the columns in the view
    dataset contains the view's data
    query is used when create view as select select statement
    """
    replace: bool
    not_exists: bool
    columns: List[str]
    dataset: Ds
    query: Ds

    def accept(self, visitor):
        visitor.visit_create_view(self)


@generic_repr
@dataclass()
class CreateStage(Node):
    """
    Create stage contains info on creating a new named internal or external stage to use for loading data from files
    stage name - contains the name of the new stage
    location - is the source of the data for the stage
    directory parameters - used to specify if it is enabled and whether auto refreshing is enabled
    file format species the format of the file
    with is used to specify if "with" is used in the "tag" part of the statement
    tag contains a list of tag names and it's values
    comments contain comments about the stage
    """
    stage_name: str
    location: str
    directory_param: str
    file_format: str
    copy_options: str
    with_used: bool
    tag: List[str]  # str
    comments: str

    def get_name(self):
        return self.stage_name

    def accept(self, visitor):
        visitor.visit_create_stage(self)


@generic_repr
@dataclass()
class Delete(Node):
    """
    Delete node contains information about the dataset that is to be deleted along with
        the filters to refine the deletion
    using contains list of datasets which are used to refer in the filter part of the statement
    """
    target: Ds
    using: List[Ds]
    filters: List[Filter]

    def accept(self, visitor):
        visitor.visit_delete(self)


@generic_repr
@dataclass()
class Edge(Node):
    """
    Edge - The LATERAL VIEW clause is used in conjunction with generator functions such as EXPLODE,
    which will generate a virtual table containing one or more rows.
    LATERAL VIEW will apply the rows to each original output row.
    """
    edge_type: str
    generator_function: str
    expressions: List[T]  # expr
    column_alias: List[str]  # str

    def accept(self, visitor):
        visitor.visit_edge(self)


@generic_repr
@dataclass()
class Error(Node):
    """
    Contains the error message from the API
    """
    message: str

    def accept(self, visitor):
        visitor.visit_error(self)


@generic_repr
@dataclass()
class Frame(Expr):
    """
    Frame - Between: Used in logical operations and in window functions.
            Sets upper and lower limits with positional values in window functions.
            Performs range operations in Logical operations.
    """
    expr: List[T]
    type: str
    lower_limit: str
    upper_limit: str
    lower_position: str
    upper_position: str

    def accept(self, visitor):
        visitor.visit_frame(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Into(Node):
    """
    Contains information to be inserted in an insert statement
    Column ref holds list of columns to which values need to be inserted
    target specifies the dataset to which the data needs to be inserted
    """
    column_ref: List[T]
    values: List[T]
    target: Ds

    def accept(self, visitor):
        visitor.visit_into(self)


@generic_repr
@dataclass()
class Insert(Expr):
    """
    Insert node contains info about insert statement
    insert type can be ALL or FIRST
    overwrite specifies whether data can be overwritten
    else specifies whether else part is used during conditional multi table inserts
    conditions contains list of expressions which if satisfied then the data is inserted
    intos contains list of into nodes
    source specifies the source of the data
    """
    insert_type: str
    is_overwrite: bool
    is_else: bool
    conditions: List[T]
    intos: List[Into]
    source: Ds

    def accept(self, visitor):
        visitor.visit_insert(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Join(Expr):
    """
    Join - Contains the data to be joined, the type of join,
            and the condition on which it should do so.
    """
    ds: Ds
    op: T
    join_type: str
    sub_type: str

    def accept(self, visitor):
        visitor.visit_join(self)

    def get_full_name(self):
        pass

    def get_name(self):
        pass

    def get_table(self) -> Ds:
        """
        Returns the dataset (table/subquery) which is used in the join claus
        @return: Ds
        @rtype: Ds
        """
        return self.ds

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Merge(Expr):
    """
    Inserts, updates, and deletes values in a table based on values in a second table or a subquery
    target specifies the target dataset to which the source is being merged into
    source is the primary dataset from where the data is being pulled from
    conditions contains expressions which specify the merge to happen in a certain way
    actions specifies actions to perform if data is matched or if it isn't matched
    """
    target: Ds
    source: Ds
    condition: T
    actions: List[T]

    def accept(self, visitor):
        visitor.visit_merge(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class MultiValue(Expr):
    """
    A wrapper node for comma separated expressions in brackets
    Ex- select * from tab where a in ('1', '2', '3')
    ('1', '2', '3') is the multivalue expression
    """
    expressions: List[T]

    def accept(self, visitor):
        visitor.visit_multivalue(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Rotate(Expr):
    """
    Rotate - Pivot: Rotates a table by turning the unique values from one column in the input
        expression into multiple columns and aggregating results where required on any remaining column values
        OR
        Unpivot: Rotates a table by transforming columns into rows.
    rotate type specifies the whether the operation is pivot or unpivot
    aggregate is the aggregate function for combining the grouped values from pivot column
    pivot column specifies the column from the source table or subquery that will be aggregated.
    for_list contains the column from the source table or subquery that contains the values from
        which column names will be generated.
    column_alias contains the name of the columns
    name column is the name to assign to the generated column that will be populated with the names of the
        columns in the column list.
    value column is the column from the source table or subquery that contains the values from which column names
        will be generated.
    """
    rotate_type: str
    aggregate: str
    pivot_column: T
    for_list: List[T]  # expr
    column_alias: List[str]  # str
    name_column: str
    value_column: str

    def accept(self, visitor):
        visitor.visit_rotate(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class AntiPattern(Node):
    """
    Contains the type of anti pattern that was encountered in the query
    """
    antipattern_type: str
    rewritten_ds: Ds

    def accept(self, visitor):
        visitor.visit_antipattern(self)


@generic_repr
@dataclass()
class AntiPatterns(Node):
    """
    Contains list of anti patterns encountered in the entire statement
    """
    antipatterns: List[AntiPattern]  # Antipatterns

    def accept(self, visitor):
        visitor.visit_antipatterns(self)


@generic_repr
@dataclass()
class StructRef(Expr):
    """
    Struct ref - Structured References: Contains the column to which the semi structured data is referring to
    column ref contains the name of the column
    structure_ref contains the full reference to the semi structured data (JSON, Avro etc)
    """
    column_ref: str
    structure_ref: str

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_structref(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class TableFunc(Expr):
    """
    Table function -  table function returns a set of rows for each input row.
        The returned set can contain zero, one, or more rows
    Type can be either TABLE or LATERAL
    func name is the name of the function used in the table function
    names contains the name of the operation in the function
    options contains the options being applied to the operation in the function
    partition contains list of expressions which are used for partitioning
    sort contains the order by clause
    frame contains the between statement
    sub query contains a subquery dataset
    """
    tablefunc_type: str
    func_name: str
    names: List[str]  # str
    options: List[T]  # expr
    partition: List[T]  # expr
    sort: Sort
    frame: Frame
    sub_query: Ds

    def get_name(self):
        return self.alias

    def get_full_name(self):
        return self.alias

    def accept(self, visitor):
        visitor.visit_tablefunc(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Update(Expr):
    """
    Update node contains the dataset that needs to be updated with the inputs needed to update the target dataset
    assign contains a list of operations which are performed to the columns of the dataset
    filter is used to refine the rows to which the operations are performed
    """
    target: Ds
    in_obj: In
    assign: List[Op]  # op
    filter: List[Filter]  # filter

    def accept(self, visitor):
        visitor.visit_update(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Wfunc(Expr):
    """
    Window function: ontains information to perform window analytics functions.
            Contains function, partition, sorting, and frame information.
    """
    expr: T
    partition: List[T]  # expr
    sort: Sort
    frame: Frame
    func_name: str

    def accept(self, visitor):
        visitor.visit_wfunc(self)

    def __hash__(self) -> int:
        return super().__hash__()


@generic_repr
@dataclass()
class Statement(Node):
    """
    The wrapper node for each type of statement.
    """
    ds: List[Ds]
    create: List[Create]
    create_view: List[CreateView]
    create_stage: List[CreateStage]
    insert: List[Insert]
    delete: List[Delete]
    update: List[Update]
    merge: List[Merge]
    copy: List[Copy]
    antipatterns: Union[AntiPatterns, None]

    def accept(self, visitor):
        visitor.visit_statement(self)


@generic_repr
@dataclass()
class ParSeQL(Node):
    """
    The base of the response from the API
    The main application schema. Contains a number of statement, version attribute,
        status attribute, dialect attribute, and timestamp attribute.
    """
    version: str
    status: str
    dialect: str
    ts: str
    statement: List[Statement]
    errors: List[Error]

    def accept(self, visitor):
        visitor.visit_parseql(self)


def get_full_node_name(node: T, prefer_alias=False) -> str:
    """
    Function to obtain the full reference of an attribute
    @param prefer_alias: select alias instead of refatt
    @param node: T of Expr
    @return: Full reference of a column
    """
    if node is None:
        return None
    fullref_list = []
    if hasattr(node, 'fullref') and node.fullref != "":
        return node.fullref
    else:
        if hasattr(node, 'refdb') and node.refdb != "":
            fullref_list.append(node.refdb)
        if hasattr(node, 'refsch') and node.refsch != "":
            fullref_list.append(node.refsch)
        if hasattr(node, 'refds') and node.refds != "":
            fullref_list.append(node.refds)
        if hasattr(node, 'alias') and node.alias != "" and prefer_alias:
            fullref_list.append(node.alias)
        elif hasattr(node, "refatt") and node.refatt != "":
            fullref_list.append(node.refatt)

        fullref = ".".join(fullref_list)
    return fullref


class AttrRef(dict):
    @staticmethod
    def from_ds(ds: Ds):
        o = AttrRef()
        o['attr'] = None
        o['ds'] = ds
        return o

    @staticmethod
    def from_attr(obj: Expr, ds: Ds):
        o = AttrRef()
        o['attr'] = obj
        o['ds'] = ds
        return o

    def get_fullref(self):
        fullref_list = []
        if self.get('ds'):
            if self.get('ds').alias != '':
                fullref_list.append(self.get('ds').alias)
            elif self.get('ds').name != '':
                fullref_list.append(self.get('ds').name)
            elif self.get('ds').refds != "":
                fullref_list.append(self.get('ds').refds)
        if hasattr(self.get('attr'), "alias") and self.get('attr').alias != "":
            fullref_list.append(self.get('attr').alias)
        elif hasattr(self.get('attr'), "refatt") and self.get('attr').refatt != "":
            fullref_list.append(self.get('attr').refatt)

        fullref = ".".join(fullref_list)
        return fullref

    def get_ds_name(self):
        ds = self.get('ds')
        if ds.refds != "":
            return ds.refds
        if ds.alias != "":
            return ds.alias
        if ds.name != "":
            return ds.name

    def get_attr_name(self):
        attr = self.get('attr')
        if hasattr(attr, 'refatt') and attr.refatt != "":
            return attr.refatt
        if attr.alias != "":
            return attr.alias
        if attr.name != "":
            return attr.name

    def get_attr_alias(self):
        attr = self.get('attr')
        if attr.alias != "":
            return attr.alias
        if hasattr(attr, 'refatt') and attr.refatt != "":
            return attr.refatt
        if attr.name != "":
            return attr.name

    def get_attr_raw(self):
        attr = self.get('attr')
        return attr.get_raw()

    def __hash__(self) -> int:
        return hash((self.get('ds'), self.get('attr')))


class TableMapping(dict):
    def source(self):
        return self.get('source')

    def target(self):
        return self.get('target')

    def as_json(self, **kwargs) -> str:
        """
        @param ** kwargs: All parameters are passed to json.dumps() function
        @return: Json string representing current object
        """
        return json.dumps(self.as_dict(), **kwargs)

    def as_dict(self):
        return {
            "source": get_full_node_name(self['source']) if self['source'] else None,
            "target": get_full_node_name(self['target'], True)
        }


class TableMappingList(list):
    def as_json(self, **kwargs) -> str:
        """
        @param ** kwargs: All parameters are passed to json.dumps() function
        @return: Json string representing current object
        """
        return json.dumps(self.as_dict(), **kwargs)

    def as_dict(self):
        return [x.as_dict() for x in self]


class ColumnMapping(dict):

    def __init__(self, level=0) -> None:
        super().__init__()
        self['level'] = level

    def source(self):
        return self.get('source')

    def target(self):
        return self.get('target')

    def level(self):
        return self.get('level')

    def as_json(self, **kwargs) -> str:
        """
        @param ** kwargs: All parameters are passed to json.dumps() function
        @return: Json string representing current object
        """
        return json.dumps(self.as_dict(), **kwargs)

    def as_dict(self):
        return {
            "source_dataset_name": self['source'].get_ds_name(),
            "input_expression": self['source'].get_attr_alias(),
            "output_expression": self['target'].get_attr_raw(),
            "output_alias": self['target'].get_attr_alias(),
            "level": self.level()
        }

    def __hash__(self) -> int:
        return hash((self.source(), self.target()))

    def __eq__(self, o: object) -> bool:
        return isinstance(o, ColumnMapping) \
               and self.source() == o.source() \
               and self.target() == o.target()


class ColumnMappingList(list):
    def as_json(self, **kwargs) -> str:
        """
        @param ** kwargs: All parameters are passed to json.dumps() function
        @return: Json string representing current object
        """
        return json.dumps(self.as_dict(), **kwargs)

    def as_dict(self):
        return [x.as_dict() for x in self]
