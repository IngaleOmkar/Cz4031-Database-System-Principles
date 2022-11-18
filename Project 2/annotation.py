"""
contains code for generating the annotations
"""
import json
import tkinter as tk
import Pmw

#
# GLOBAL VARIABLES
#

RECT_WIDTH = 200
RECT_HEIGHT = 60
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000

all_operators = []
visual_to_node = {}

# Information of rectangle


class Operator:
    def __init__(self, x1, x2, y1, y2, operation, information):
        # four corners coordinates
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.operation = operation
        self.information = information
        self.center = ((x1+x2)/2, (y1+y2)/2)
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def build_plan(current_operator, json_plan):
    plan = json_plan
    current_operator.operation = plan["Node Type"]
    current_operator.information = get_current_operator_info(plan)
    all_operators.append(current_operator)

    if "Plans" in plan:
        children_plans = len(plan["Plans"])
        if children_plans == 1:
            for i in range(children_plans):
                x1 = current_operator.x1
                x2 = current_operator.x2
                y1 = current_operator.y2 + RECT_HEIGHT / 2
                y2 = y1 + RECT_HEIGHT

                child_operator = Operator(x1, x2, y1, y2, "", "")
                current_operator.add_child(child_operator)
                build_plan(child_operator, plan["Plans"][i])

        elif children_plans == 2:
            for i in range(children_plans):
                x2 = current_operator.x1 - RECT_WIDTH + i * (4 * RECT_WIDTH)
                x1 = x2 - RECT_WIDTH
                y1 = current_operator.y2 + RECT_HEIGHT
                y2 = y1 + RECT_HEIGHT

                child_operator = Operator(x1, x2, y1, y2, "", "")
                current_operator.add_child(child_operator)
                build_plan(child_operator, plan["Plans"][i])


def get_current_operator_info(operator):

    info = ""

    node_type = operator['Node Type']

    duration = "\nDuration for " + node_type + ": " + \
        str(round(operator['Actual Total Time'] - operator['Actual Startup Time'], 6)) + " ms"

    # Main Scan Operations
    if node_type == 'Seq Scan':
        info = 'Perform ' + node_type + \
            ', on relation ' + operator['Relation Name']
        if 'Filter' in operator:
            info += ', with filter ' + operator['Filter'].replace("AND", "AND \n")

    elif node_type == 'Index Scan':
        info = 'Perform ' + node_type + ', on index ' + \
            operator['Index Name'] + ', of relation ' + operator['Relation Name']

    # Main Join Operations
    elif node_type == 'Nested Loop':
        info = 'Perform ' + node_type + \
            ', using join type ' + operator['Join Type']

    elif node_type == 'Hash Join':
        info = 'Perform ' + node_type + ', using join type ' + \
            operator['Join Type'] + ', with hash condition ' + operator['Hash Cond']

    elif node_type == 'Merge Join':
        info = 'Perform ' + node_type + ', using join type ' + \
            operator['Join Type'] + ', with merge condition ' + operator['Merge Cond']

    # All Operations
    elif node_type == 'Aggregate':
        info = 'Perform ' + node_type
        if 'Group Key' in operator:
            info += ', with grouping on attribute(s) ' + ''.join(
                str(e) + ", " for e in operator['Group Key'])
        if 'Filter' in operator:
            info += ', with filter on ' + \
                operator['Filter'].replace("AND", "AND \n")
        if 'Hash Key' in operator:
            info += ', with hashing on attribute(s) ' + ''.join(
                str(e) + ", " for e in operator['Hash Key'])

    elif node_type == 'Append':
        info = 'Perform ' + node_type

    elif node_type == 'Bitmap Heap Scan':
        info = 'Perform ' + node_type + ', on table ' + \
            operator['Relation Name']

    elif node_type == 'Bitmap Index Scan':
        info = 'Perform ' + node_type + ', on index ' + \
            operator['Index Name'] + ' with index condition ' + operator['Index Cond']

    elif node_type == 'BitmapAnd':
        info = 'Perform ' + node_type

    elif node_type == 'BitmapOr':
        info = 'Perform ' + node_type

    elif node_type == 'CTE Scan':
        info = 'Perform ' + node_type + ', with filter on ' + \
            operator['Filter'].replace("AND", "AND \n")

    elif node_type == 'Function Scan':
        info = 'Perform ' + node_type + ', with filter on ' + \
            operator['Filter'].replace("AND", "AND \n")

    elif node_type == 'Gather':
        info = 'Perform ' + node_type

    elif node_type == 'Gather Merge':
        info = 'Perform ' + node_type

    elif node_type == 'Group':
        info = 'Perform ' + node_type

    elif node_type == 'GroupAggregate':
        info = 'Perform ' + node_type

    elif node_type == 'Hash':
        info = 'Perform ' + node_type

    elif node_type == 'HashAggregate':
        info = 'Perform ' + node_type
        if 'Group Key' in operator:
            info += ', with grouping on ' + \
                ''.join(str(e) + ", " for e in operator['Group Key'])
        if 'Hash Key' in operator:
            info += ', with grouping on ' + \
                ''.join(str(e) + " " for e in operator['Hash Key'])

    elif node_type == 'HashSetOp':
        info = 'Perform ' + node_type

    elif node_type == 'Incremental Sort':
        info = 'Perform ' + node_type + ', on attribute(s) ' + ''.join(str(
            e) + ", " for e in operator['Sort Key'])

    elif node_type == 'Limit':
        info = 'Perform ' + node_type

    elif node_type == 'Materialize':
        info = 'Perform ' + node_type

    elif node_type == 'Merge Append':
        info = 'Perform ' + node_type + \
            ', on attribute(s) ' + ''.join(str(e) + ", " for e in operator['Sort Key'])

    elif node_type == 'ModifyTable':
        info = 'Perform ' + node_type + \
            ', on relation ' + operator['Relation Name']

    elif node_type == 'Recursive Union':
        info = 'Perform ' + node_type

    elif node_type == 'Result':
        info = 'Perform ' + node_type

    elif node_type == 'SetOp':
        info = 'Perform ' + node_type

    elif node_type == 'Sort':
        info = 'Perform ' + node_type + ', on attribute(s) ' + ''.join(
            str(e) + ", " for e in operator['Sort Key']) + ' using ' + operator['Sort Method']

    elif node_type == 'Subquery Scan':
        info = 'Perform ' + node_type + ', with filter ' + \
            operator['Filter'].replace("AND", "AND \n")

    elif node_type == 'TID Scan':
        info = 'Perform ' + node_type + \
            ', on relation ' + operator['Relation Name']
        if 'Tid Cond' in operator:
            info += ' with TID Cond ' + operator['Tid Cond']

    elif node_type == 'Unique':
        info = 'Perform ' + node_type

    elif node_type == 'Values Scan':
        info = 'Perform ' + node_type

    elif node_type == 'WorkTable Scan':
        info = 'Perform ' + node_type + ', with filter ' + \
            operator['Filter'].replace("AND", "AND \n")

    info += duration
    return info


def draw(query_plan, canvas):

    data = json.loads(query_plan)
    all_operators.clear()

    # CANVAS_WIDTH = 1000, RECT_HEIGHT = 60, CENTER = (500, 35)
    root_op = Operator(500, 500+RECT_WIDTH, 0, 0+RECT_HEIGHT, "", "")
    build_plan(root_op, data)

    # store unique coordinates
    unique_coordinates = []
    for element in all_operators:
        coordinates = (element.x1, element.x2, element.y1, element.y2)
        if coordinates not in unique_coordinates:
            unique_coordinates.append(coordinates)
        else:
            element.x1 += 3*RECT_WIDTH/2
            element.x2 += 3*RECT_WIDTH/2
            element.center = ((element.x1+element.x2)/2,
                              (element.y1+element.y2)/2)
            new_coor = (element.x1, element.x2, element.y1, element.y2)
            unique_coordinates.append(new_coor)

    # create rectangles
    for element in all_operators:
        x1 = element.x1
        x2 = element.x2
        y1 = element.y1
        y2 = element.y2
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill="grey")

        # create tooltip
        balloon = Pmw.Balloon()
        balloon.tagbind(canvas, rect, element.information)
        visual_to_node[rect] = element

    # create text on rectangles
    for element in all_operators:
        gui_text = canvas.create_text(
            (element.center[0], element.center[1]), text=element.operation)
        visual_to_node[gui_text] = element

    # create arrows
    for element in all_operators:
        for child in element.children:
            canvas.create_line(child.center[0], child.center[1] - RECT_HEIGHT/2, element.center[0],
                               element.center[1] + RECT_HEIGHT/2, arrow=tk.LAST)


if __name__ == '__main__':

    draw("query_plan.json")
