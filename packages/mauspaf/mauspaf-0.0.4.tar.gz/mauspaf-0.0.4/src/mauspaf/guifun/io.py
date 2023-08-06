import pickle

from mauspaf.guifun.inner import qttree2table


def save2file(tree_widget, mspfile, id_column=1):
    """ Saves the information of a tree widget as a csv file.

    Args:
        tree_widget (PyQt5.QtWidgets.QTreeWidget): Tree widget.
        mspfile (str): String with path to the file the data is to be saved.
        id_column (int): Column of the tree widget with unique ids.
    """
    table = qttree2table(tree_widget, id_column)
    with open(mspfile, 'w') as f:
        for part in table:
            f.write('; '.join(part)+'\n')


def export2file(var, file):
    """ Saves a given variable to a pickle file

    Args:
        var (): Any python variable
        file (str): String with path to file

    """
    with open(file, 'wb') as f:
        pickle.dump(var, f, protocol=-1)
