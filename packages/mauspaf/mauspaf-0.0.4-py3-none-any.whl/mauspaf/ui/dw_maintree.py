import plotly.express as px
from PyQt5 import QtCore, QtWidgets

from mauspaf.generated.dw_maintree import Ui_DockWidget
from mauspaf.ui.partinfo import PartInfoWindow
from mauspaf import guifun


class DW_MainTree(QtWidgets.QDockWidget):
    def __init__(self):
        super(DW_MainTree, self).__init__()
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        self.show()

    # Part creation/removal
    def add_part(self):
        """ Adds a part to the main input tab tree (same level as the currently
        selected part)
        """
        try:
            selected_part = self.__select_single_part()
        except ValueError:
            return
        if selected_part == self.ui.tw_mainPartTree.topLevelItem(0):
            self.parent().ui.statusbar.showMessage(
                'Only one root item allowed.', 4000)
            return
        new_id = guifun.misc.random_id(selected_part.parent().text(1))
        selected_part.parent().addChild(
            QtWidgets.QTreeWidgetItem(guifun.misc.new_row(new_id)))
        new_part = selected_part.parent().child(
             selected_part.parent().childCount()-1)
        new_part.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
            | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable
            | QtCore.Qt.ItemIsEnabled)
        self.parent().ui.statusbar.showMessage('New part has been created.',
                                               4000)

    def add_subpart(self):
        """ Adds a subpart to the main input tab tree (one level below the
        currently selected part)
        """
        try:
            parent_part = self.__select_single_part()
        except ValueError:
            return
        new_id = guifun.misc.random_id(parent_part.text(1))
        self.ui.tw_mainPartTree.expandItem(parent_part)
        parent_part.addChild(QtWidgets.QTreeWidgetItem(
            guifun.misc.new_row(new_id)))
        new_part = parent_part.child(parent_part.childCount()-1)
        new_part.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
            | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable
            | QtCore.Qt.ItemIsEnabled)
        self.parent().ui.statusbar.showMessage('New subpart has been created.',
                                               4000)

    def remove_part(self):
        """ Removes the currently selected part and all its children from the
        main tab tree
        """
        selected_parts = self.ui.tw_mainPartTree.selectedItems()
        if not selected_parts:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function.', 4000)
            return
        elif selected_parts[0] == self.ui.tw_mainPartTree.topLevelItem(0):
            self.parent().ui.statusbar.showMessage(
                'Removing the top level item is not possible.', 4000)
            return
        parent_part = selected_parts[0].parent()
        part_index = parent_part.indexOfChild(selected_parts[0])
        # Removal
        for part in selected_parts:
            part.parent().removeChild(part)
        # Selection
        if parent_part.childCount() == 0:
            parent_part.setSelected(True)
        elif part_index == parent_part.childCount():
            parent_part.child(parent_part.childCount()-1).setSelected(True)
        else:
            parent_part.child(part_index).setSelected(True)
        # Info
        verb = ' has' if len(selected_parts) == 1 else 's have'
        self.parent().ui.statusbar.showMessage(
            'Selected part' + verb + ' been removed.', 4000)
        self.properties_edited()

    # Part movement
    def promote_part(self):
        """ Promotes the currently selected part in the main tab tree one level
        up
        """
        try:
            selected_part = self.__movement_checks()
            parent_part = selected_part.parent()
            if parent_part == self.ui.tw_mainPartTree.topLevelItem(0):
                self.parent().ui.statusbar.showMessage(
                    'No part can be promoted to root.', 4000)
                raise ValueError()
        except ValueError:
            return
        is_expanded = selected_part.isExpanded()
        grandparent_part = parent_part.parent()
        part_index = parent_part.indexOfChild(selected_part)
        parent_index = grandparent_part.indexOfChild(parent_part)
        taken_part = parent_part.takeChild(part_index)
        grandparent_part.insertChild(parent_index+1, taken_part)
        taken_part.setSelected(True)
        taken_part.setExpanded(is_expanded)
        self.properties_edited()

    def demote_part(self):
        """ Demotes the currently selected part in the main tab tree one level
        down
        """
        try:
            selected_part = self.__movement_checks()
            parent_part = selected_part.parent()
            part_index = parent_part.indexOfChild(selected_part)
            if parent_part.childCount() == 1 or part_index == 0:
                self.parent().ui.statusbar.showMessage(
                    'Single and firstborn child parts can not be demoted.',
                    4000)
                raise ValueError()
        except ValueError:
            return
        is_expanded = selected_part.isExpanded()
        taken_part = parent_part.takeChild(part_index)
        parent_part.child(part_index - 1).addChild(taken_part)
        parent_part.child(part_index - 1).setExpanded(True)
        taken_part.setSelected(True)
        taken_part.setExpanded(is_expanded)
        self.properties_edited()

    def move_part_up(self):
        """ Moves the currently selected part in the main tab tree up (same
        level)
        """
        try:
            selected_part = self.__movement_checks()
        except ValueError:
            return
        is_expanded = selected_part.isExpanded()
        parent_part = selected_part.parent()
        part_index = parent_part.indexOfChild(selected_part)
        taken_part = parent_part.takeChild(part_index)
        if part_index == 0:
            parent_part.addChild(taken_part)
        else:
            parent_part.insertChild(part_index-1, taken_part)
        taken_part.setSelected(True)
        taken_part.setExpanded(is_expanded)

    def move_part_down(self):
        """ Moves the currently selected part in the main tab tree down (same
        level)
        """
        try:
            selected_part = self.__movement_checks()
        except ValueError:
            return
        is_expanded = selected_part.isExpanded()
        parent_part = selected_part.parent()
        part_index = parent_part.indexOfChild(selected_part)
        taken_part = parent_part.takeChild(part_index)
        if part_index == parent_part.childCount():
            parent_part.insertChild(0, taken_part)
        else:
            parent_part.insertChild(part_index+1, taken_part)
        taken_part.setSelected(True)
        taken_part.setExpanded(is_expanded)

    # View function
    def show_probabilistic_columns(self):
        """
        """
        [self.ui.tw_mainPartTree.showColumn(i) for i in
            [1, 3, 4, 5, 6, 8, 9, 10, 11]]
        self.parent().ui.statusbar.showMessage('Probabilistic columns are now'
                                               + ' being shown.', 4000)

    def hide_probabilistic_columns(self):
        """
        """
        [self.ui.tw_mainPartTree.hideColumn(i) for i in
            [1, 3, 4, 5, 6, 8, 9, 10, 11]]
        self.parent().ui.statusbar.showMessage('Probabilistic columns are now'
                                               + ' hidden.', 4000)

    # Plotting functions
    def plot_mass_distribution(self):
        """ Plots the mass distribution of the selected objects
        """
        selected_items = self.ui.tw_mainPartTree.selectedItems()
        if not selected_items:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function', 4000)
            return
        tree_object = guifun.inner.table2masstree(
            guifun.inner.qttree2table(self.ui.tw_mainPartTree))
        for i in selected_items:
            item = tree_object.elements[i.text(1)]
            item.mass.plot_distribution(new_figure=True,
                                        title=item.name+' mass')

    def plot_mass_cdf(self):
        """ Plots the cumulative mass probability distribution of the
        selected objects
        """
        selected_items = self.ui.tw_mainPartTree.selectedItems()
        if not selected_items:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function', 4000)
            return
        tree_object = guifun.inner.table2masstree(
            guifun.inner.qttree2table(self.ui.tw_mainPartTree))
        for i in selected_items:
            item = tree_object.elements[i.text(1)]
            item.mass.plot_distribution(new_figure=True,
                                        title=item.name+' mass',
                                        plot_type='cdf')

    def plot_cg_distribution(self):
        """ Plots the cg distribution of the selected objects
        """
        selected_items = self.ui.tw_mainPartTree.selectedItems()
        if not selected_items:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function', 4000)
            return
        tree_object = guifun.inner.table2masstree(
            guifun.inner.qttree2table(self.ui.tw_mainPartTree))
        for i in selected_items:
            item = tree_object.elements[i.text(1)]
            item.cg.plot_distribution(new_figure=True,
                                      title=item.name+' cg')

    def plot_cg_cdf(self):
        """ Plots the cg distribution of the selected objects
        """
        selected_items = self.ui.tw_mainPartTree.selectedItems()
        if not selected_items:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function', 4000)
            return
        tree_object = guifun.inner.table2masstree(
            guifun.inner.qttree2table(self.ui.tw_mainPartTree))
        for i in selected_items:
            item = tree_object.elements[i.text(1)]
            item.cg.plot_distribution(new_figure=True,
                                      title=item.name+' cg',
                                      plot_type='cdf')

    def plot_cgmass_density(self):
        """ Plots the cg-mass distribution of the selected objects
        """
        selected_items = self.ui.tw_mainPartTree.selectedItems()
        if not selected_items:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function', 4000)
            return
        tree_object = guifun.inner.table2masstree(
            guifun.inner.qttree2table(self.ui.tw_mainPartTree))
        for i in selected_items:
            item = tree_object.elements[i.text(1)]
            if item.mass.lower_bound == item.mass.upper_bound \
               or item.cg.lower_bound == item.cg.upper_bound:
                self.parent().ui.statusbar.showMessage(
                    'Upper and lower bound are equal. No plot '
                    + 'will be generated', 4000)
                return
            item.plot_cgmass()

    def plot_mass_sunburst(self):
        """ Plots a sunburst diagram of the selected part
        """
        try:
            selected_ass = self.__select_single_assembly()
        except ValueError:
            return
        ass_table = guifun.inner.qttree2table(selected_ass)
        names = [i[0] for i in ass_table]
        ids = [i[1] for i in ass_table]
        parent_ids = [i[2] for i in ass_table]
        masses = [float(i[3]) for i in ass_table]
        data = dict(name=names, parent=parent_ids, mass=masses)
        fig = px.sunburst(data, names='name', parents='parent', values='mass',
                          ids=ids, branchvalues='total', title='Masses')
        fig.show()

    def plot_moment_sunburst(self):
        """ Plots a sunburst diagram of the moment (cg*mass)
        """
        self.parent().ui.statusbar.showMessage(
            'Function not yet implemented', 4000)
        # try:
        #     selected_ass = self.__select_single_assembly()
        # except ValueError:
        #     return
        # ass_table = guifun.inner.qttree2table(selected_ass)
        # cg = float(ass_table[0][8])
        # names = [i[0] for i in ass_table]
        # ids = [i[1] for i in ass_table]
        # parent_ids = [i[2] for i in ass_table]
        # masses = [float(i[3]) for i in ass_table]
        # arms = [float(i[8])-cg for i in ass_table]
        # moments = [abs(m*x) for m, x in zip(masses, arms)]
        # data = dict(name=names, parent=parent_ids, moment=moments)
        # fig = px.sunburst(data, names='name', parents='parent',
        #                   values='moment',
        #                   ids=ids, title='Moments')
        # fig.show()

    def show_part_info(self):
        """ Shows statistical information about the part's mass and cg
        """
        selected_items = self.ui.tw_mainPartTree.selectedItems()
        tree_object = guifun.inner.table2masstree(
            guifun.inner.qttree2table(self.ui.tw_mainPartTree))
        for i in selected_items:
            item = tree_object.elements[i.text(1)]
            PartInfoWindow(item.name, item.mass.describe(), item.cg.describe())
        return True

    # Other functions
    def update_tree_properties(self):
        """ Update the properties of the main tree widget

        TODO: instead of rewriting the whole tree, just rewrite the elements
            which need to be rewritten.

        """
        self.parent().ui.statusbar.showMessage('Tree is being update...', 4000)
        try:
            tree_widget = self.ui.tw_mainPartTree
            tree_object = guifun.inner.table2masstree(
                guifun.inner.qttree2table(tree_widget))
            new_tree_widget = guifun.inner.table2qttree(
                guifun.inner.masstree2table(tree_object))
            self.ui.tw_mainPartTree.clear()
            self.ui.tw_mainPartTree.addTopLevelItem(new_tree_widget)
            self.parent().ui.statusbar.showMessage('Tree values were updated.',
                                                   4000)
            iterator = QtWidgets.QTreeWidgetItemIterator(
                self.ui.tw_mainPartTree)
            while True:
                item = iterator.value()
                if item is not None:
                    item.setFlags(
                        QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
                        | QtCore.Qt.ItemIsDragEnabled
                        | QtCore.Qt.ItemIsUserCheckable
                        | QtCore.Qt.ItemIsEnabled)
                    iterator += 1
                else:
                    break
            self.ui.tw_mainPartTree.expandAll()
            self.ui.pb_update.setStyleSheet(
                "background-color: rgb(115, 210, 22);")
            self.ui.pb_update.setText("Updated")
        except BaseException as error:
            self.parent().ui.statusbar.showMessage(
                'update_tree_properties: An exception occurred: {}'
                .format(error), 4000)

    def properties_edited(self):
        """ Changes the status button after editing mass properties

        Button becomes orange and shows the message "Update"

        """
        self.ui.pb_update.setStyleSheet(
            "background-color: rgb(255, 165, 0);")
        self.ui.pb_update.setText("Update")

    # Private methods
    def __select_single_part(self):
        selected_part = self.ui.tw_mainPartTree.selectedItems()
        if not selected_part:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function.', 4000)
            raise ValueError()
        elif len(selected_part) > 1:
            self.parent().ui.statusbar.showMessage(
                'Select a single part before running the function.', 4000)
            raise ValueError()
        return selected_part[0]

    def __movement_checks(self):
        """ Checks that a single, non-root part has been selected
        """
        selected_part = self.ui.tw_mainPartTree.selectedItems()
        if not selected_part:
            self.parent().ui.statusbar.showMessage(
                'Select a part before running the function.', 4000)
            raise ValueError()
        elif len(selected_part) > 1:
            self.parent().ui.statusbar.showMessage(
                'Select a single part before running the function.', 4000)
            raise ValueError()
        elif self.ui.tw_mainPartTree.topLevelItem(0) == selected_part[0]:
            self.parent().ui.statusbar.showMessage(
                'No movement permitted on root part.', 4000)
            raise ValueError()
        return selected_part[0]

    def __select_single_assembly(self):
        """ Checks that a single assembly has been selected
        """
        selected_ass = self.ui.tw_mainPartTree.selectedItems()
        if not selected_ass:
            self.parent().ui.statusbar.showMessage(
                'Select an assembly before running the function.', 4000)
            raise ValueError()
        elif len(selected_ass) > 1:
            self.parent().ui.statusbar.showMessage(
                'Select a single assembly before running the function.', 4000)
            raise ValueError()
        elif selected_ass[0].childCount() == 0:
            self.parent().ui.statusbar.showMessage(
                'Select a single assembly (not a leaf part) before running the'
                + 'function.', 4000)
            raise ValueError()
        return selected_ass[0]
