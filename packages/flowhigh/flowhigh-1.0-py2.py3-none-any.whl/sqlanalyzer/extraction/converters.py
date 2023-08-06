"""
Converters module:
Contains all the functions used to convert the json to a tree of nodes
"""
from sqlanalyzer.domain import *
from sqlanalyzer.domain import MatchRecognize
from sqlanalyzer.util.Visitor import Visitor
from sqlanalyzer.util.sdk_visitor import SDKVisitor


class ApiConverter:

    def __init__(self, visitor: Visitor = None) -> None:
        super().__init__()
        self.visitor = visitor

    def convert_parseql(self, values, visitor: Visitor = None) -> ParSeQL:
        """
        Converts json to a ParSeQL Node
        @param values: JSON
        @param visitor: Visitor
        @return: ParSeQL node
        """
        self.visitor = visitor
        statements: List[Statement] = []
        errors: List[Error] = []
        version = ""
        status = ""
        dialect = ""
        timestamp = ""

        if "statement" in values:
            for i, statement in enumerate(values["statement"]):
                # for each statement create a new visitor
                self.visitor = SDKVisitor()
                converted_statement = (self.convert_statement(values["_value"][i]))
                if "antipatterns" in values["_value"][i]:
                    converted_statement.antipatterns = self.convert_antipatterns(values["_value"][i]["antipatterns"])
                statements.append(converted_statement)

        if "error" in values:
            for i, error in enumerate(values["error"]):
                errors.append(self.convert_error(values["_value"][error]))

        if "version" in values:
            version = values["version"]

        if "status" in values:
            status = values["status"]

        if "dialect" in values:
            dialect = values["dialect"]

        if "ts" in values:
            timestamp = values["ts"]

        parseql = ParSeQL(version, status, dialect, timestamp, statements, errors)
        parseql._json_dict = values
        parseql.visitor = visitor
        return parseql

    def convert_antipatterns(self, values) -> AntiPatterns:
        """
        Converts json to a AntiPatterns Node
        @param values: JSON
        @return: AntiPatterns node
        """
        antipatterns: List[AntiPattern] = []
        for antipattern in values:
            antipatterns.append(self.convert_antipattern(antipattern))

        antipatterns_obj = AntiPatterns(antipatterns)
        antipatterns_obj.visitor = self.visitor
        antipatterns_obj._json_dict = values
        return antipatterns_obj

    def convert_antipattern(self, values) -> AntiPattern:
        """
            Converts json to a AntiPattern Node
            @param values: JSON
            @return: AntiPattern node
            """
        antipattern_type = values['type']
        rewritten_ds = None

        if "rewritten" in values:
            rewritten_ds = self.convert_ds(values['rewritten'])

        antipattern = AntiPattern(antipattern_type, rewritten_ds)
        antipattern.visitor = self.visitor
        antipattern._json_dict = values
        return antipattern

    def convert_statement(self, values) -> Statement:
        """
        Converts json to a Statement Node
        @param values: JSON
        @return: Statement node
        """
        if values['_type'] == 'statement':
            ds: List[Ds] = []
            create: List[Create] = []
            create_view: List[CreateView] = []
            create_stage: List[CreateStage] = []
            insert: List[Insert] = []
            delete: List[Delete] = []
            update: List[Update] = []
            merge: List[Merge] = []
            copy: List[Copy] = []
            antipatterns = None

            if "ds" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    ds.append(self.convert_ds(val))

            if "create" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    create.append(self.convert_create(val))

            if "createView" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    create_view.append(self.convert_create_view(val))

            if "createStage" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    create_stage.append(self.convert_create_stage(val))

            if "insert" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    insert.append(self.convert_insert(val))

            if "delete" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    delete.append(self.convert_delete(val))

            if "update" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    update.append(self.convert_update(val))

            if "merge" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    merge.append(self.convert_merge(val))

            if "copy" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    copy.append(self.convert_copy(val))

            if "antipatterns" in values:
                values = values['_value']
                for i, val in enumerate(values):
                    copy.append(self.convert_copy(val))

            statement_obj = Statement(ds, create, create_view, create_stage,
                                      insert, delete, update, merge, copy, antipatterns)
            statement_obj.visitor = self.visitor
            statement_obj._json_dict = values
            return statement_obj
        else:
            raise Exception("Invalid Statement")

    def convert_ds(self, values) -> Ds:
        """
        Converts json to a Ds Node
        @param values: JSON
        @return: Ds node
        """
        if "ds" == values['_type']:
            out_obj = None
            in_obj = None
            match_recognize = None
            table_sample = None
            _filter = None
            agg = None
            vagg = None
            sort = None
            page = None
            set_op: List[Op] = []  # Op
            ds_type = ""
            name = ""
            refdb = ""
            refsch = ""
            refds = ""
            fullref = ""
            _id = None
            _refTo = None
            rawInput = ""

            if "type" in values:
                ds_type = values['type']

            if "name" in values:
                name = values['name']

            if "refdb" in values:
                refdb = values['refdb']

            if "refds" in values:
                refds = values['refds']

            if "refsch" in values:
                refsch = values['refsch']

            if "out" in values:
                out_obj = self.convert_out(values['out'])

            if "in" in values:
                in_obj = (self.convert_in(values['in']))

            if "matchrecognize" in values:
                match_recognize = (self.convert_match_recognize(values['matchrecognize']))

            if "tablesample" in values:
                table_sample = (self.convert_tablesample(values['tablesample']))

            if "filter" in values:
                _filter = self.convert_filter(values['filter'])

            if "agg" in values:
                agg = (self.convert_agg(values['agg']))

            if "vagg" in values:
                vagg = self.convert_vagg(values["vagg"])

            if "sort" in values:
                sort = (self.convert_sort(values['sort']))

            if "page" in values:
                page = (self.convert_page(values['page']))

            if "setOp" in values:
                for val in values['setOp']:
                    set_op.append(self.convert_op(val))

            if "_id" in values:
                _id = values['_id']

            if "_refTo" in values:
                _refTo = values['_refTo']

            if "rawInput" in values:
                rawInput = values['rawInput']

            value = None
            alias = ""
            direction = ""

            if "value" in values:
                value = (values['value'])

            if "alias" in values:
                alias = (values['alias'])

            if "direction" in values:
                direction = values['direction']

            ds_obj = Ds(value, alias, direction, out_obj, in_obj, match_recognize, table_sample, _filter, agg, vagg,
                        sort,
                        page, set_op,
                        ds_type, name, refdb, refds, refsch, fullref, _id, _refTo, rawInput)
            ds_obj.visitor = self.visitor
            ds_obj._json_dict = values
            return ds_obj
        else:
            raise Exception("Invalid Ds")

    def convert_in(self, in_json) -> In:
        """
        Converts json to a In Node
        @param in_json
        @return: In node
        """
        expr: List[Expr] = []
        in_value = in_json['_value']
        for val in in_value:
            expr.append(self.convert_expr(val))
        in_obj = In(expr)
        in_obj.visitor = self.visitor
        in_obj._json_dict = in_json
        return in_obj

    def convert_out(self, out_json) -> Out:
        """
        Converts json to Out Node
        @param out_json: JSON
        @return: Out
        """
        if out_json['_type'] == "out":
            expr: List[Expr] = []
            if "_value" in out_json:
                out_value = out_json['_value']
                for val in out_value:
                    expr.append(self.convert_expr(val))

            out_obj = Out(expr)
            out_obj.visitor = self.visitor
            out_obj._json_dict = out_json
            return out_obj
        else:
            raise Exception("Invalid Out")

    def convert_filter(self, filter_json) -> Filter:
        """
        Converts json to Filter Node
        @param filter_json: JSON
        @return: Filter Node
        """
        _filter = Filter(self.convert_op(filter_json['op']))
        _filter.visitor = self.visitor
        _filter._json_dict = filter_json
        return _filter

    def convert_vfilter(self, vfilter_json) -> Vfilter:
        """
        Converts json to Vfilter Node
        @param vfilter_json: JSON
        @return: Vfilter
        """
        vfilter = Vfilter(self.convert_op(vfilter_json['op']))
        vfilter.visitor = self.visitor
        vfilter._json_dict = vfilter_json
        return vfilter

    def convert_agg(self, agg_json) -> Agg:
        """
        Converts json to Agg Node
        @param agg_json: JSON
        @return: Agg
        """
        if agg_json['_type'] == "agg":
            expr: List[Expr] = []
            _filter = None
            agg_value = agg_json['_value']

            for val in agg_value:
                expr.append(self.convert_expr(val))

            if "filter" in agg_json:
                _filter = (self.convert_filter(agg_json['filter']))

            agg = Agg(expr, _filter)
            agg.visitor = self.visitor
            agg._json_dict = agg_json
            return agg
        else:
            raise Exception("Invalid Agg")

    def convert_vagg(self, vagg_json) -> Vagg:
        """
        Converts json to Vagg Node
        @param vagg_json: JSON
        @return: Vagg
        """
        if vagg_json["_type"] == "vagg":
            vfilter = None
            if "vfilter" in vagg_json:
                vfilter = self.convert_vfilter(vagg_json["vfilter"][0])
            vagg = Vagg(vfilter)
            vagg.visitor = self.visitor
            vagg._json_dict = vagg_json
            return vagg
        else:
            raise Exception("Invalid Vagg")

    def convert_sort(self, sort_json) -> Sort:
        """
        Converts json to Sort Node
        @param sort_json: JSON
        @return: Sort
        """
        if sort_json['_type'] == "sort":
            expr: List[Expr] = []
            sort_values = sort_json["_value"]
            for val in sort_values:
                expr.append(self.convert_expr(val))

            sort = Sort(expr)
            sort.visitor = self.visitor
            sort._json_dict = sort_json
            return sort
        else:
            raise Exception("Invalid Sort")

    def convert_page(self, page_json) -> Page:
        """
        Converts json to Page Node
        @param page_json: JSON
        @return: Page
        """
        if page_json['_type'] == "page":
            page_type = page_json['type']
            value = ""
            if "value" in page_json:
                value = self.convert_expr(page_json['value'])
            page = Page(page_type, value)
            page.visitor = self.visitor
            page._json_dict = page_json
            return page
        else:
            raise Exception("Invalid Page")

    def convert_op(self, op_json) -> Op:
        """
        Converts json to Op Node
        @param op_json: JSON
        @return: Op
        """
        if op_json['_type'] == "op":
            expr: List[Expr] = []
            op_type = op_json["type"]
            raw_input = ""
            if "_value" in op_json:
                for val in op_json["_value"]:
                    expr.append(self.convert_expr(val))

            _expr = self._create_expr(op_json)
            if "rawInput" in op_json:
                raw_input = op_json['rawInput']

            op = Op(_expr.value, _expr.alias, _expr.direction, expr, op_type, raw_input)
            op.visitor = self.visitor
            op._json_dict = op_json
            return op
        else:
            raise Exception("Invalid Op")

    def convert_expr(self, expr_json) -> Expr:
        """
        Converts json to Expr Node
        @param expr_json: JSON
        @return: Expr
        """
        if "multivalue" in expr_json:
            return self.convert_multivalue(expr_json['multivalue'])

        if expr_json["_type"] == "attr":
            return self.convert_attr(expr_json)

        if expr_json["_type"] == "case":
            return self.convert_case(expr_json)

        if expr_json["_type"] == "const":
            return self.convert_const(expr_json)

        if expr_json["_type"] == "cast":
            return self.convert_cast(expr_json)

        if expr_json["_type"] == "current":
            return self.convert_current(expr_json)

        if expr_json["_type"] == "op":
            return self.convert_op(expr_json)

        if expr_json["_type"] == "ds":
            return self.convert_ds(expr_json)

        if expr_json["_type"] == "frame":
            return self.convert_frame(expr_json)

        if expr_json["_type"] == "func":
            return self.convert_func(expr_json)

        if expr_json["_type"] == "insert":
            return self.convert_insert(expr_json)

        if expr_json["_type"] == "inlinetable":
            return self.convert_inlinetable(expr_json)

        if expr_json["_type"] == "join":
            return self.convert_join(expr_json)

        if expr_json["_type"] == "merge":
            return self.convert_merge(expr_json)

        if expr_json["_type"] == "multivalue":
            return self.convert_multivalue(expr_json)

        if expr_json["_type"] == "rotate":
            return self.convert_rotate(expr_json)

        if expr_json["_type"] == "structref":
            return self.convert_structref(expr_json)

        if expr_json["_type"] == "tablefunc":
            return self.convert_tablefunc(expr_json)

        if expr_json["_type"] == "then":
            return self.convert_then(expr_json)

        if expr_json["_type"] == "update":
            return self.convert_update(expr_json)

        if expr_json["_type"] == "wfunc":
            return self.convert_wfunc(expr_json)

        if expr_json["_type"] == "when":
            return self.convert_when(expr_json)

        if expr_json["_type"] == "queryingstage":
            return self.convert_queryingstage(expr_json)

    def convert_case(self, case_json) -> Case:
        """
        Converts json to Case Node
        @param case_json: JSON
        @return: Case
        """
        if case_json['_type'] == "case":
            case_value = case_json["_value"]
            else_obj = None
            when: List[When] = []
            expr = None
            for i, val in enumerate(case_value):
                if "else" in case_json and i in case_json['else']:
                    else_obj = self.convert_else(val)
                if "when" in case_json and i in case_json['when']:
                    when.append(self.convert_when(val))
                if "expr" in case_json and i in case_json['expr']:
                    expr = self.convert_expr(case_json)

            _expr = self._create_expr(case_json)
            case = Case(_expr.value, _expr.alias, _expr.direction, expr, when, else_obj)
            case.visitor = self.visitor
            case._json_dict = case_json
            return case
        else:
            raise Exception("Invalid Case")

    def convert_else(self, else_json) -> Else:
        """
        Converts json to Else Node
        @param else_json: JSON
        @return: Else
        """
        if else_json['_type'] == "else":
            expr = self.convert_expr(else_json['_value'][0])
            else_obj = Else(expr)
            else_obj.visitor = self.visitor
            else_obj._json_dict = else_json
            return else_obj
        else:
            raise Exception("Invalid Else")

    def convert_when(self, when_json) -> When:
        """
        Converts json to When Node
        @param when_json: JSON
        @return: When
        """
        if when_json['_type'] == "when":
            then = None
            expr = None
            for i, val in enumerate(when_json['_value']):
                if i in when_json['then']:
                    then = self.convert_then(val)
                if i in when_json['expr']:
                    expr = self.convert_expr(val)

            _expr = self._create_expr(when_json)

            when = When(_expr.value, _expr.alias, _expr.direction, expr, then)
            when.visitor = self.visitor
            when._json_dict = when_json
            return when
        else:
            raise Exception("Invalid When")

    def convert_then(self, then_json) -> Then:
        """
        Converts json to Then Node
        @param then_json: JSON
        @return: Then
        """
        if then_json['_type'] == "then":
            expr = self.convert_expr(then_json['_value'][0])
            _expr = self._create_expr(then_json)

            then = Then(_expr.value, _expr.alias, _expr.direction, expr)
            then.visitor = self.visitor
            then._json_dict = then_json
            return then
        else:
            raise Exception("Invalid Then")

    def convert_attr(self, attr_json) -> Attr:
        """
        Converts json to Attr Node
        @param attr_json: JSON
        @return: Attr
        """
        if attr_json['_type'] == "attr":
            refvar = ""
            refatt = ""
            refds = ""
            refdb = ""
            refsch = ""
            fullref = ""
            refoutidx = ""
            value = None
            alias = ""
            direction = ""
            raw_input = ""
            if "refvar" in attr_json:
                refvar = attr_json['refvar']
            if "refatt" in attr_json:
                refatt = attr_json['refatt']
            if "refds" in attr_json:
                refds = attr_json['refds']
            if "refdb" in attr_json:
                refdb = attr_json['refdb']
            if "refsch" in attr_json:
                refsch = attr_json['refsch']
            if "fullref" in attr_json:
                fullref = attr_json['fullref']
            if "refoutidx" in attr_json:
                refoutidx = attr_json['refoutidx']

            if "value" in attr_json:
                value = attr_json['value']

            if "alias" in attr_json:
                alias = attr_json['alias']

            if "direction" in attr_json:
                direction = attr_json['direction']

            if "rawInput" in attr_json:
                raw_input = attr_json['rawInput']

            _attr = Attr(value, alias, direction, refvar, refatt, refds, refdb, refsch, fullref, refoutidx, raw_input)
            _attr.visitor = self.visitor
            _attr._json_dict = attr_json
            return _attr
        else:
            raise Exception("Invalid Attr")

    def convert_const(self, const_json) -> Const:
        """
        Converts json to Const Node
        @param const_json: JSON
        @return: Const
        """
        if const_json['_type'] == "const":
            _expr = self._create_expr(const_json)

            const = Const(_expr.value, _expr.alias, _expr.direction)
            const.visitor = self.visitor
            const._json_dict = const_json
            return const
        else:
            raise Exception("Invalid Const")

    def convert_cast(self, cast_json) -> Cast:
        """
        Converts json to Cast Node
        @param cast_json: JSON
        @return: Cast
        """
        if cast_json['_type'] == "cast":
            expr = self.convert_expr(cast_json['_value'][0])
            data_type = cast_json['dataType']

            _expr = self._create_expr(cast_json)

            cast = Cast(_expr.value, _expr.alias, _expr.direction, expr, data_type)
            cast.visitor = self.visitor
            cast._json_dict = cast_json
            return cast
        else:
            raise Exception("Invalid Cast")

    def convert_frame(self, frame_json) -> Frame:
        """
        Converts json to Frame Node
        @param frame_json: JSON
        @return: Frame
        """
        if frame_json['_type'] == "frame":
            expr: List[Expr] = []
            _type = ""
            lower_limit = ""
            upper_limit = ""
            lower_position = ""
            upper_position = ""

            if "type" in frame_json:
                _type = frame_json['type']

            if "expr" in frame_json and len(frame_json['expr']) > 0:
                for val in frame_json['expr']:
                    expr.append(self.convert_expr(val))

            if "lower_limit" in frame_json:
                lower_limit = frame_json['lower_limit']

            if "upper_limit" in frame_json:
                upper_limit = frame_json['upper_limit']

            if "lower_position" in frame_json:
                lower_position = frame_json['lower_position']

            if "upper_position" in frame_json:
                upper_position = frame_json['upper_position']

            _expr = self._create_expr(frame_json)

            frame = Frame(_expr.value, _expr.alias, _expr.direction, expr, _type, lower_limit, upper_limit,
                          lower_position, upper_position)
            frame.visitor = self.visitor
            frame._json_dict = frame_json
            return frame
        else:
            raise Exception("Invalid Frame")

    def convert_func(self, func_json) -> Func:
        """
        Converts json to Func Node
        @param func_json: JSON
        @return: Func
        """
        if func_json["_type"] == "func":
            expr: List[Expr] = []
            within_group = None
            func_type = ""
            name = ""
            if "type" in func_json:
                func_type = func_json['type']

            if "name" in func_json:
                name = func_json['name']

            if "withinGroup" in func_json:
                within_group = self.convert_ds(func_json['withinGroup'])

            for val in func_json['_value']:
                expr.append(self.convert_expr(val))

            _expr = self._create_expr(func_json)

            func = Func(_expr.value, _expr.alias, _expr.direction, expr, within_group, func_type, name)
            func.visitor = self.visitor
            func._json_dict = func_json
            return func

        else:
            raise Exception("Invalid Func")

    def convert_into(self, into_json) -> Into:
        """
        Converts json to Into Node
        @param into_json: JSON
        @return: Into
        """
        if into_json["_type"] == "into":
            column_ref: List[Expr] = []
            insert_values: List[Expr] = []
            target: Union[Ds, None] = None

            if "refAttr" in into_json:
                for val in into_json['refAttr']:
                    key = list(val)[0]
                    column_ref.append(self.convert_expr(val.get(key)))

            if "insertValues" in into_json:
                for val in into_json["insertValues"]:
                    key = list(val)[0]
                    insert_values.append(self.convert_expr(val.get(key)))

            if "target" in into_json:
                target = self.convert_ds(into_json['target'])

            into = Into(column_ref, insert_values, target)
            into.visitor = self.visitor
            into._json_dict = into_json
            return into
        else:
            raise Exception("Invalid Into")

    def convert_insert(self, insert_json) -> Insert:
        """
        Converts json to Insert Node
        @param insert_json: JSON
        @return: Insert
        """
        if insert_json["_type"] == "insert":
            insert_type: str = ""
            is_overwrite: bool = False
            is_else: bool = False
            conditions: List[Expr] = []
            intos: List[Into] = []
            source: Union[Ds, None] = None
            if "type" in insert_json:
                insert_type = insert_json['type']
            if "overwrite" in insert_json:
                is_overwrite = insert_json['overwrite']
            if "else" in insert_json:
                is_else = insert_json['else']
            if "conditions" in insert_json:
                for val in insert_json['conditions']:
                    key = list(val)[0]
                    conditions.append(self.convert_expr(val.get(key)))
            if "insertInto" in insert_json:
                for val in insert_json['insertInto']:
                    key = list(val)[0]
                    intos.append(self.convert_into(val.get(key)))
            if "source" in insert_json:
                source = self.convert_ds(insert_json['source'])

            _expr = self._create_expr(insert_json)
            insert = Insert(_expr.value, _expr.alias, _expr.direction, insert_type, is_overwrite, is_else,
                            conditions, intos, source)
            insert.visitor = self.visitor
            insert._json_dict = insert_json
            return insert
        else:
            raise Exception("Invalid Insert")

    def convert_join(self, join_json) -> Join:
        """
        Converts json to Join Node
        @param join_json: JSON
        @return: Join
        """
        if join_json['_type'] == "join":
            ds = None
            op = None
            join_type = ""
            sub_type = ""
            if "type" in join_json:
                join_type = join_json["type"]

            if "subType" in join_json:
                sub_type = join_json["subType"]

            if "op" in join_json:
                op = self.convert_op(join_json["op"])

            if "ds" in join_json:
                ds = self.convert_ds(join_json["ds"])

            _expr = self._create_expr(join_json)

            join = Join(_expr.value, _expr.alias, _expr.direction, ds, op, join_type, sub_type)
            join.visitor = self.visitor
            join._json_dict = join_json
            return join

        else:
            raise Exception("Invalid Join")

    def convert_merge(self, merge_json) -> Merge:
        """
        Converts json to Merge Node
        @param merge_json: JSON
        @return: Merge
        """
        if merge_json["_type"] == "merge":
            target = None
            source = None
            condition = None
            actions: List[Expr] = []
            if "target" in merge_json:
                target = self.convert_ds(merge_json["target"])

            if "source" in merge_json:
                source = self.convert_ds(merge_json["source"])

            if "condition" in merge_json:
                condition = self.convert_expr(merge_json["condition"])

            if "actions" in merge_json:
                for val in merge_json["actions"]:
                    key = list(val)[0]
                    actions.append(self.convert_expr(val.get(key)))

            _expr = self._create_expr(merge_json)

            merge = Merge(_expr.value, _expr.alias, _expr.direction, target, source, condition, actions)
            merge.visitor = self.visitor
            merge._json_dict = merge_json
            return merge
        else:
            raise Exception("Invalid Merge")

    def convert_multivalue(self, multivalue_json) -> MultiValue:
        """
        Converts json to MultiValue Node
        @param multivalue_json: JSON
        @return: MultiValue
        """
        if multivalue_json["_type"] == "multivalue":
            expressions: List[Expr] = []
            if "_value" in multivalue_json:
                for val in multivalue_json["_value"]:
                    expressions.append(self.convert_expr(val))

            _expr = self._create_expr(multivalue_json)

            multivalue = MultiValue(_expr.value, _expr.alias, _expr.direction, expressions)
            multivalue.visitor = self.visitor
            multivalue._json_dict = multivalue_json
            return multivalue
        else:
            raise Exception("Invalid MultiValue")

    def convert_rotate(self, rotate_json) -> Rotate:
        """
        Converts json to Rotate Node
        @param rotate_json: JSON
        @return: Rotate
        """
        if rotate_json["_type"] == "rotate":
            rotate_type = ""
            aggregate = ""
            pivot_column = None
            for_list: List[Expr] = []  # expr
            column_alias: List[str] = []  # str
            name_column = ""
            value_column = ""
            if "type" in rotate_json:
                rotate_type = rotate_json["type"]

            if "aggregate" in rotate_json:
                aggregate = rotate_json["aggregate"]

            if "pivotColumn" in rotate_json:
                pivot_column = self.convert_expr(rotate_json["pivotColumn"])

            if "nameColumn" in rotate_json:
                name_column = rotate_json["nameColumn"]

            if "valueColumn" in rotate_json:
                value_column = rotate_json["valueColumn"]

            if "columnAlias" in rotate_json:
                for val in rotate_json["columnAlias"]:
                    column_alias.append(val)

            if "for" in rotate_json:
                for val in rotate_json["for"]:
                    key = list(val)[0]
                    for_list.append(self.convert_expr(val.get(key)))

            _expr = self._create_expr(rotate_json)

            rotate = Rotate(_expr.value, _expr.alias, _expr.direction, rotate_type, aggregate, pivot_column,
                            for_list, column_alias, name_column, value_column)
            rotate.visitor = self.visitor
            rotate._json_dict = rotate_json
            return rotate
        else:
            raise Exception("Invalid Rotate")

    def convert_structref(self, structref_json) -> StructRef:
        """
        Converts json to StructRef Node
        @param structref_json: JSON
        @return: StructRef
        """
        if structref_json["_type"] == "structRef":
            column_ref = ""
            structure_ref = ""
            if "columnRef" in structref_json:
                column_ref = structref_json['columnRef']

            if "structureRef" in structref_json:
                structure_ref = structref_json['structureRef']

            _expr = self._create_expr(structref_json)

            structref = StructRef(_expr.value, _expr.alias, _expr.direction, column_ref, structure_ref)
            structref.visitor = self.visitor
            structref._json_dict = structref_json
            return structref
        else:
            raise Exception("Invalid Exception")

    def convert_tablefunc(self, tablefunc_json) -> TableFunc:
        """
        Converts json to TableFunc Node
        @param tablefunc_json: JSON
        @return: TableFunc
        """
        if tablefunc_json["_type"] == "tablefunc":
            tablefunc_type = ""
            func_name = ""
            names: List[str] = []  # str
            options: List[Expr] = []  # expr
            partition: List[Expr] = []  # expr
            sort = None
            frame = None
            sub_query = None
            if "type" in tablefunc_json:
                tablefunc_type = tablefunc_json['type']

            if "funcName" in tablefunc_json:
                func_name = tablefunc_json['funcName']

            if "names" in tablefunc_json:
                for val in tablefunc_json['names']:
                    names.append(val)

            if "args" in tablefunc_json:
                for val in tablefunc_json["args"]:
                    key = list(val)[0]
                    options.append(self.convert_expr(val.get(key)))

            if "partition" in tablefunc_json:
                for val in tablefunc_json["partition"]:
                    key = list(val)[0]
                    partition.append(self.convert_expr(val.get(key)))

            if "sort" in tablefunc_json:
                if len(tablefunc_json['sort']) > 1:
                    sort = self.convert_sort(tablefunc_json['sort'])

            if "frame" in tablefunc_json:
                frame = self.convert_frame(tablefunc_json['frame'])

            if "subQuery" in tablefunc_json:
                sub_query = self.convert_ds(tablefunc_json['subquery'])

            _expr = self._create_expr(tablefunc_json)

            tablefunc = TableFunc(_expr.value, _expr.alias, _expr.direction, tablefunc_type,
                                  func_name, names, options, partition, sort, frame, sub_query)
            tablefunc.visitor = self.visitor
            tablefunc._json_dict = tablefunc_json
            return tablefunc
        else:
            raise Exception("Invalid TableFunc")

    def convert_update(self, update_json) -> Update:
        """
        Converts json to Update Node
        @param update_json: JSON
        @return: Update
        """
        if update_json["_type"] == "update":
            target = None
            in_obj = None
            assign: List[Op] = []  # op
            _filter: List[Filter] = []
            if "target" in update_json:
                target = self.convert_ds(update_json["target"])

            if "in" in update_json:
                in_obj = self.convert_in(update_json["in"])

            if "assign" in update_json:
                for val in update_json["assign"]:
                    assign.append(self.convert_op(val))

            if "filter" in update_json:
                _filter.append(self.convert_filter(update_json['filter']))

            _expr = self._create_expr(update_json)

            update = Update(_expr.value, _expr.alias, _expr.direction, target, in_obj, assign, _filter)
            update.visitor = self.visitor
            update._json_dict = update_json
            return update
        else:
            raise Exception("Invalid Update")

    def convert_wfunc(self, wfunc_json) -> Wfunc:
        """
        Converts json to Wfunc Node
        @param wfunc_json: JSON
        @return: Wfunc
        """
        if wfunc_json["_type"] == "wfunc":
            expr = None
            partition: List[Expr] = []  # expr
            sort = None
            frame = None  # str
            func_name: Union[str, None] = None  # str
            if "expr" in wfunc_json:
                expr = self.convert_expr(wfunc_json["_value"][wfunc_json["expr"][0]])

            if "sort" in wfunc_json:
                sort = self.convert_sort(wfunc_json["_value"][wfunc_json["sort"][0]])

            if "frame" in wfunc_json:
                frame = self.convert_frame(wfunc_json["_value"][wfunc_json["frame"][0]])

            if "name" in wfunc_json:
                func_name = wfunc_json["name"]

            if "partition" in wfunc_json:
                for val in wfunc_json["partition"]:
                    partition.append(self.convert_expr(wfunc_json["_value"][val]))

            _expr = self._create_expr(wfunc_json)

            wfunc = Wfunc(_expr.value, _expr.alias, _expr.direction, expr, partition, sort, frame, func_name)
            wfunc.visitor = self.visitor
            wfunc._json_dict = wfunc_json
            return wfunc
        else:
            raise Exception("Invalid Wfunc")

    def convert_create(self, create_json) -> Create:
        """
        Converts json to Create Node
        @param create_json: JSON
        @return: Create
        """
        if create_json["_type"] == "create":
            column_def: List[ColumnDef] = []  # columnDef
            ds = None
            cluster_by: List[Expr] = []  # expr
            create_type = ""
            scope = ""
            refdb = ""
            refds = ""
            refsch = ""

            if "columnDef" in create_json:
                for val in create_json["columnDef"]:
                    column_def.append(self.convert_columndef(val))

            if "ds" in create_json:
                ds = self.convert_ds(create_json["ds"])

            if "clusterBy" in create_json:
                for val in create_json["clusterBy"]:
                    cluster_by.append(self.convert_expr(val))

            if "type" in create_json:
                create_type = create_json["type"]

            if "scope" in create_json:
                scope = create_json["scope"]

            if "refdb" in create_json:
                refdb = create_json["refdb"]

            if "refds" in create_json:
                refds = create_json["refds"]

            if "refsch" in create_json:
                refsch = create_json["refsch"]

            create = Create(column_def, ds, cluster_by, create_type, scope, refdb, refds,  refsch)
            create.visitor = self.visitor
            create._json_dict = create_json
            return create
        else:
            raise Exception("Invalid Create")

    def convert_columndef(self, columndef_json) -> ColumnDef:
        """
        Converts json to ColumnDef Node
        @param columndef_json: JSON
        @return: ColumnDef
        """
        if columndef_json["_type"] == "columndef":
            name = ""
            data_type = ""
            precision = ""
            scale = ""
            if "name" in columndef_json:
                name = columndef_json["name"]

            if "type" in columndef_json:
                data_type = columndef_json["type"]

            if "scale" in columndef_json:
                scale = columndef_json["scale"]

            if "precision" in columndef_json:
                precision = columndef_json["precision"]

            columndef = ColumnDef(name, data_type, precision, scale)
            columndef.visitor = self.visitor
            columndef._json_dict = columndef_json
            return columndef
        else:
            raise Exception("Invalid ColumnDef")

    def convert_copy(self, copy_json) -> Copy:
        """
        Converts json to Copy Node
        @param copy_json: JSON
        @return: Copy
        """
        if copy_json["_type"] == "copy":
            into = None
            target_columns: List[str] = []
            from_exp: List[str] = []  # str
            from_query: Union[Ds, None] = None  # ds
            select_elements: List[Expr] = []
            from_stage = None
            partition: List[Expr] = []  # expr
            file_format = ""
            file = ""
            header = None
            pattern = ""
            copy_options = ""
            validation = ""

            if "into" in copy_json:
                into = self.convert_ds(copy_json["into"])

            if "targetColumns" in copy_json:
                for val in copy_json["targetColumns"]:
                    target_columns.append(val)

            if "fromExp" in copy_json:
                for val in copy_json["fromExp"]:
                    from_exp.append(val)

            if "fromQuery" in copy_json:
                from_query = self.convert_ds(copy_json["fromQuery"])

            if "selectElements" in copy_json:
                for expr in copy_json["fromStage"]:
                    select_elements.append(self.convert_expr(expr))

            if "fromStage" in copy_json:
                from_stage = self.convert_ds(copy_json["fromStage"])

            if "partition" in copy_json:
                for val in copy_json["partition"]:
                    partition.append(self.convert_expr(val))

            if "fileFormat" in copy_json:
                file_format = copy_json["fileFormat"]

            if "file" in copy_json:
                file = copy_json["file"]

            if "header" in copy_json:
                header = copy_json["header"]

            if "pattern" in copy_json:
                pattern = copy_json["pattern"]

            if "copyOptions" in copy_json:
                copy_options = copy_json["copyOptions"]

            if "validation" in copy_json:
                validation = copy_json["validation"]

            copy = Copy(into, target_columns, from_exp, from_query, select_elements, from_stage,
                        partition, file_format, file, header, pattern, copy_options, validation)
            copy.visitor = self.visitor
            copy._json_dict = copy_json
            return copy
        else:
            raise Exception("Invalid Copy")

    def convert_delete(self, delete_json) -> Delete:
        """
        Converts json to Delete Node
        @param delete_json: JSON
        @return: Delete
        """
        if delete_json["_type"] == "delete":
            target = None
            filters: List[Filter] = []
            using: List[Ds] = []
            if "target" in delete_json:
                target = self.convert_ds(delete_json["_value"][delete_json["target"][0]])

            if "filter" in delete_json:
                for val in delete_json["filter"]:
                    filters.append(self.convert_filter(delete_json["_value"][val]))

            if "using" in delete_json:
                for val in delete_json["using"]:
                    using.append(self.convert_ds(delete_json["_value"][val]))

            delete = Delete(target, using, filters)
            delete.visitor = self.visitor
            delete._json_dict = delete_json
            return delete
        else:
            raise Exception("Invalid Delete")

    def convert_current(self, current_json) -> Current:
        """
        Converts json to Current Node
        @param current_json: JSON
        @return: Current
        """
        if current_json["_type"] == "current":
            current_type = current_json['type']
            _expr = self._create_expr(current_json)

            current = Current(_expr.value, _expr.alias, _expr.direction, current_type)
            current.visitor = self.visitor
            current._json_dict = current_json
            return current
        else:
            raise Exception("Invalid Current")

    def convert_inlinetable(self, inlinetable_json) -> InlineTable:
        """
        Converts json to InlineTable Node
        @param inlinetable_json: JSON
        @return: InlineTable
        """
        if inlinetable_json['_type'] == "inlinetable":
            expr: List[Expr] = []
            if 'row' in inlinetable_json:
                for i in inlinetable_json['row']:
                    expr.append(self.convert_expr(inlinetable_json['_value'][i]))

            _expr = self._create_expr(inlinetable_json)

            inline_table = InlineTable(_expr.value, _expr.alias, _expr.direction, expr)
            inline_table.visitor = self.visitor
            inline_table._json_dict = inlinetable_json
            return inline_table
        else:
            raise Exception("Invalid InlineTable")

    def convert_queryingstage(self, queryingstage_json) -> QueryingStage:
        """
        Converts json to QueryingStage Node
        @param queryingstage_json: JSON
        @return: QueryingStage
        """
        if queryingstage_json['_type'] == "queryingstage":
            value = None
            alias = ""
            direction = ""
            location = queryingstage_json['location']
            file_format = None
            pattern = None

            if 'fileFormat' in queryingstage_json:
                file_format = queryingstage_json['fileFormat']

            if 'pattern' in queryingstage_json:
                pattern = queryingstage_json['pattern']

            if "value" in queryingstage_json:
                value = queryingstage_json['value']

            if "alias" in queryingstage_json:
                alias = queryingstage_json['alias']

            if "direction" in queryingstage_json:
                direction = queryingstage_json['direction']

            queryingstage = QueryingStage(value, alias, direction, location, file_format, pattern)
            queryingstage.visitor = self.visitor
            queryingstage._json_dict = queryingstage_json
            return queryingstage
        else:
            raise Exception("Invalid QueryingStage")

    def convert_tablesample(self, tablesample_json) -> TableSample:
        """
        Converts json to TableSample Node
        @param tablesample_json: JSON
        @return: TableSample
        """
        if tablesample_json['_type'] == "tablesample":
            value = None
            alias = ""
            direction = ""
            sample_method = None
            sample_type = None
            probability = None
            num = None
            seed_type = None
            seed = None

            if 'sampleMethod' in tablesample_json:
                sample_method = tablesample_json['sampleMethod']

            if 'sample_type' in tablesample_json:
                sample_type = tablesample_json['sampleType']

            if 'probability' in tablesample_json:
                probability = tablesample_json['probability']

            if 'num' in tablesample_json:
                num = tablesample_json['num']

            if 'seed_type' in tablesample_json:
                seed_type = tablesample_json['seed_type']

            if 'seed' in tablesample_json:
                seed = tablesample_json['seed']

            if "value" in tablesample_json:
                value = tablesample_json['value']

            if "alias" in tablesample_json:
                alias = tablesample_json['alias']

            if "direction" in tablesample_json:
                direction = tablesample_json['direction']

            table_sample = TableSample(value, alias, direction, sample_method, sample_type, probability,
                                       num, seed_type, seed)
            table_sample.visitor = self.visitor
            table_sample._json_dict = tablesample_json
            return table_sample
        else:
            raise Exception("Invalid TableSample")

    def convert_match_recognize(self, match_recognize_json) -> MatchRecognize:
        """
        Converts json to MatchRecognize Node
        @param match_recognize_json: JSON
        @return: MatchRecognize
        """
        if match_recognize_json['_type'] == "matchrecognize":
            value = None
            alias = ""
            direction = ""
            partition_by = None
            order_by = None
            measure = None
            row_condition = None
            row_action = None
            pattern = None
            define = None

            if 'partitionBy' in match_recognize_json:
                partition_by = match_recognize_json['partitionBy']

            if 'orderBy' in match_recognize_json:
                order_by = match_recognize_json['orderBy']

            if 'measure' in match_recognize_json:
                measure = match_recognize_json['measure']

            if 'rowCondition' in match_recognize_json:
                row_condition = match_recognize_json['rowCondition']

            if 'rowAction' in match_recognize_json:
                row_action = match_recognize_json['rowAction']

            if 'pattern' in match_recognize_json:
                pattern = match_recognize_json['pattern']

            if 'define' in match_recognize_json:
                define = match_recognize_json['define']

            if "value" in match_recognize_json:
                value = match_recognize_json['value']

            if "alias" in match_recognize_json:
                alias = match_recognize_json['alias']

            if "direction" in match_recognize_json:
                direction = match_recognize_json['direction']

            match_recognize = MatchRecognize(value, alias, direction, partition_by, order_by, measure,
                                             row_condition, row_action, pattern, define)
            match_recognize.visitor = self.visitor
            match_recognize._json_dict = match_recognize_json
            return match_recognize
        else:
            raise Exception("Invalid MatchRecognize")

    def convert_create_stage(self, create_stage_json) -> CreateStage:
        """
        Converts json to Create Stage Node
        @param create_stage_json: JSON
        @return: CreateStage
        """
        if create_stage_json["_type"] == "createStage":
            stage_name = None
            location = None
            directory_param = None
            file_format = None
            copy_options = None
            with_used = None
            tag: List[str] = []  # str
            comments = None

            if "stageName" in create_stage_json:
                stage_name = create_stage_json["stageName"]

            if "location" in create_stage_json:
                location = create_stage_json['location']

            if "directoryParam" in create_stage_json:
                directory_param = create_stage_json['directoryParam']

            if "fileFormat" in create_stage_json:
                file_format = create_stage_json['fileFormat']

            if "copyOptions" in create_stage_json:
                copy_options = create_stage_json['copyOptions']

            if "isWith" in create_stage_json:
                with_used = create_stage_json['isWith']

            if "tag" in create_stage_json:
                for val in create_stage_json['tag']:
                    tag.append(val)

            if "comments" in create_stage_json:
                comments = create_stage_json['comments']

            create_stage = CreateStage(stage_name, location, directory_param, file_format, copy_options,
                                       with_used, tag, comments)
            create_stage.visitor = self.visitor
            create_stage._json_dict = create_stage_json
            return create_stage
        else:
            raise Exception("Invalid Create Stage")

    def convert_create_view(self, create_view_json) -> CreateView:
        """
        Converts json to Create View Node
        @param create_view_json: JSON
        @return: CreateView
        """
        if create_view_json["_type"] == "createView":
            replace = None  # bool
            columns: List[str] = []  # List[str]
            not_exists = None  # bool
            dataset = None  # ds
            query = None  # ds

            if "replace" in create_view_json:
                replace = create_view_json["replace"]

            if "notExists" in create_view_json:
                not_exists = create_view_json['notExists']

            if "columns" in create_view_json:
                columns.extend(create_view_json['columns'])

            if "dataset" in create_view_json:
                dataset = self.convert_ds(create_view_json['dataset'])

            if "query" in create_view_json:
                query = self.convert_ds(create_view_json['query'])

            create_view = CreateView(replace, not_exists, columns, dataset, query)
            create_view.visitor = self.visitor
            create_view._json_dict = create_view_json
            return create_view
        else:
            raise Exception("Invalid Create View")

    @staticmethod
    def convert_error(error) -> Error:
        domain_error = Error(error['message'])
        domain_error._json_dict = error
        return domain_error

    @staticmethod
    def _create_expr(values):
        value = None
        alias = ""
        direction = ""

        if "value" in values:
            value = values['value']

        if "alias" in values:
            alias = values['alias']

        if "direction" in values:
            direction = values['direction']

        return Expr(value, alias, direction)
