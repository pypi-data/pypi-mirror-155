# # returns a list of links source->target of detected columns and tables
# links = statement.get_lineage_links()
# # work with links to build chains from raw links
# chains = statement.get_lineage_links()
# # returns list of top level expressions as objects
# output = statement.get_output_expressions()
# # returns list of datasets used as an input for the statement (only visible/ in scope)
# input = statement.get_input_datasets()
from flowhigh import parse_sql

# The sql query we want to parse using flowhigh
statement = """SELECT table1.column1
      , table2.column2
      , SUM(table1.column3) AS column_qty 
  FROM table1 
  JOIN table2 
    ON(table1.column4=table2.column5)
 WHERE table2.column6='Ireland'
 GROUP BY table1.column1, table2.column2 
HAVING SUM(table1.column3)>50"""

# the actual parsing is done by parse_sql calling function
parseql = parse_sql(statement)

# to iterate over the statements
for statement in parseql.get_statements():
    # to get list of columns used in the aggregation clauses GROUP BY and HAVING
    agg_columns = statement.get_agg_columns()
    for column in agg_columns:
        # print out the full name of the column
        print(column.get_full_name())

#
#     for column in statement.get_output_columns():
#         # return a list of lists, chained links using depth first search
#         # for example for query SELECT a.A from (select B from b) a
#         # column object converted from "a.A" will return from get_source():
#         # [[<object a.A>, <object B>]]
#         lineage = column.get_source()
#         save(lineage)
#
# mapping = parseql.get_column_full_mapping()
#
# # as a final touch - sort the mapping list by the nesting level of the entry
# mapping.sort(key=lambda a: a.level())
#
# for entry in mapping.as_dict():
#     print("{output_expression}"
#           "\t{output_alias}"
#           "\t{source_dataset_name}"
#           "\t{input_expression}"
#           "\t{input_alias}".format_map(entry))
