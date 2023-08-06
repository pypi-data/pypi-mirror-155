from PyQt5 import QtWidgets
import numpy as np
from uncertain import UncertainValue

from mauspaf.core.mauspaf import MassElement, MassTree


def qttree2table(tree_widget, id_column=1):
    """ Transform data of a tree widget to a 2D-list array.

    To keep the hierarchy information an additional column is added indicating
    the ID of the parent structure of each part. This "Parent-ID" column is
    inserted just after the normal ID column.

    Args:
        tree_widget (PyQt5.QtWidgets.QTreeWidget): Tree widget
        id_column (int): column of the tree widget with unique ids.

    Returns:
        table (list): 2D list array with the data of `tree_widget`.

    Raises:
        ValueError: If the tree data in `id_column` is not unique.
    """
    table = []
    iterator = QtWidgets.QTreeWidgetItemIterator(tree_widget)
    n_columns = tree_widget.columnCount()
    while True:
        item = iterator.value()
        if item is not None:
            item_properties = [item.text(i).strip() for i in range(n_columns)]
            if item.parent() is not None:
                parent = item.parent().text(id_column).strip()
            else:
                parent = ''
            table.append(item_properties[:id_column+1] + [parent]
                         + item_properties[id_column+1:])
            iterator += 1
        else:
            break
    ids = [x[id_column] for x in table]
    if len(set(ids)) != len(table):
        dup_ids = [x for x in set(ids) if ids.count(x) > 1]
        raise ValueError('IDs ' + str(dup_ids) + ' of tree widget in column '
                         + str(id_column) + ' are not unique.')
    return table


def table2qttree(tree_table, id_column=1):
    """ Uses the data of a 2D list array to generate a tree widget.

    The root part should always be in the first row of the input table. After
    the element IDs column a column with parent IDs should follow.

    Args:
        table (list): two dimensional list array with the `tree_widget` data.
        id_column (int): column of the table with unique ids.

    Returns:
        tree_widget (PyQt5.QtWidgets.QTreeWidget): Tree widget
    """
    tree_widget_items = [QtWidgets.QTreeWidgetItem(
        x[:id_column+1] + x[id_column+2:]) for x in tree_table]
    for i in range(1, len(tree_table)):
        item_id = tree_table[i][1]
        parent_id = tree_table[i][2].strip()
        try:
            parent_index = np.where([x[1].strip() == parent_id
                                     for x in tree_table])[0][0]
        except IndexError:
            print('Error: parent of ' + item_id
                  + 'was not found. Check input.')
        tree_widget_items[parent_index].addChild(tree_widget_items[i])
    return tree_widget_items[0]


def table2masstree(tree_table):
    """ Generates a MassTree object from a table.

    Args:
        tree_table (list): two dimensional list array with the tree data.

    Returns:
        tree_object (MassTree): MassTree object
    """
    elements_dict = {}
    parents_dict = {}
    for i in tree_table:
        mass_args = [float(i[3]),
                     None if i[4] == '' else float(i[4]),
                     None if i[5] == '' else float(i[5]),
                     'uniform' if i[6] == '' else i[6],
                     None if i[7] == '' or i[7] == 'None'
                     else list(eval(i[7]))]
        i_mass = UncertainValue(*mass_args)
        cg_args = [float(i[8]),
                   None if i[9] == '' else float(i[9]),
                   None if i[10] == '' else float(i[10]),
                   'uniform' if i[11] == '' or i[11] == 'custom' else i[11],
                   None if i[12] == '' or i[12] == 'None'
                   else list(eval(i[12]))]
        i_cg = UncertainValue(*cg_args)
        i_id = i[1]
        i_name = i[0]
        i_parent = i[2]
        elements_dict[i_id] = MassElement(i_mass, i_cg, i_id, i_name)
        parents_dict[i_id] = i_parent
    tree_object = MassTree(elements_dict, parents_dict)
    return tree_object


def masstree2table(mass_tree):
    """ Generates a table from a MassTree object.

    Args:
        tree_table (list): two dimensional list array with the tree data.

    Returns:
        tree_object (MassTree): MassTree object
    """
    table = [[i.name, i.id, mass_tree.parent_dict[i.id],
              str(i.mass.nominal_value),
              str(i.mass.lower_bound) if i.mass.prob_distribution != 'constant'
              else '',
              str(i.mass.upper_bound) if i.mass.prob_distribution != 'constant'
              else '',
              str(i.mass.prob_distribution),
              str(i.mass.distribution_param)[1:-1]
              if type(i.mass.distribution_param) == str
              else str(i.mass.distribution_param),
              str(i.cg.nominal_value),
              str(i.cg.lower_bound) if i.cg.prob_distribution != 'constant'
              else '',
              str(i.cg.upper_bound) if i.cg.prob_distribution != 'constant'
              else '',
              str(i.cg.prob_distribution),
              str(i.cg.distribution_param)[1:-1]
              if type(i.cg.distribution_param) == str
              else str(i.cg.distribution_param)]
             for i in mass_tree.elements.values()]
    return table
