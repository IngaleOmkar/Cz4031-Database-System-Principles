"""
contains code for reading inputs and any preprocessing necessary to make your algorithm work
"""
import json

import psycopg2
from annotation import *


class ConnectAndQuery():

    def __init__(self, host, port, database, username, password):

        self.connect = psycopg2.connect(
            host=host, port=port, database=database, user=username, password=password)
        self.cur = self.connect.cursor()

    def getQueryPlan(self, query=None, params=None):

        self.query_plan = ""

        if params == None:
            self.params_map = {
                "enable_bitmapscan": True,
                "enable_hashagg": True,
                "enable_hashjoin": True,
                "enable_indexscan": True,
                "enable_indexonlyscan": True,
                "enable_material": True,
                "enable_mergejoin": True,
                "enable_nestloop": True,    # Does not disable, but discourages using it
                "enable_seqscan": True,     # Does not disable, but discourages using it
                "enable_sort": True,        # Does not disable, but discourages using it
                "enable_tidscan": True,
                "enable_gathermerge": True,
            }
        else:
            self.params_map = {
                "enable_bitmapscan": params[0],
                "enable_hashagg": params[1],
                "enable_hashjoin": params[2],
                "enable_indexscan": params[3],
                "enable_indexonlyscan": params[4],
                "enable_material": params[5],
                "enable_mergejoin": params[6],
                "enable_nestloop": params[7],    # Does not disable, but discourages using it
                "enable_seqscan": params[8],     # Does not disable, but discourages using it
                "enable_sort": params[9],        # Does not disable, but discourages using it
                "enable_tidscan": params[10],
                "enable_gathermerge": params[11],
            }

        if query:
            self.query = query

            filters = ""

            for key, value in self.params_map.items():
                if value == False:
                    filters = filters + "SET " + key + " = OFF;\n"
                else:
                    filters = filters + "SET " + key + " = ON;\n"

            try:
                self.cur.execute(filters + "EXPLAIN (ANALYZE, FORMAT JSON)" + self.query)
                plan = self.cur.fetchall()
                self.query_plan = plan[0][0][0]["Plan"]

            except Exception as e:
                print("\nError: %s" % str(e))
                self.connect.rollback()

        else:
            self.query_plan = "Query plan failed to generate."

        parse_query_plan = (json.dumps(
            self.query_plan, sort_keys=False, indent=4))
        return parse_query_plan


if __name__ == '__main__':
    query = "SELECT sum(l_extendedprice * l_discount) as revenue FROM lineitem WHERE l_shipdate >= date '1994-01-01' AND l_shipdate < date '1994-01-01' + interval '1' year AND l_discount between 0.06 - 0.01 AND 0.06 + 0.01 AND l_quantity < 24"
    connect = ConnectAndQuery(
        'localhost', '5432', 'test', 'postgres', 'password')
    sample = connect.getQueryPlan(query)
