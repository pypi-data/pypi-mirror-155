"""
.. module:: mauspaf
.. moduleauthor:: Miguel Nuño <mnunos@outlook.com>
    :synopsis: Module used to perform mass and c.g. calculations on products
        accounting for uncertainties in the position and mass of its
        constituting elements.

"""
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy.stats as st
import random
import string

from mauspaf.core.misc import rodrigues_rotation


class MassElement:
    """ Class to describe objects with mass properties.

    Simplified class for longitudinal calculations without taking inertia into
    account.

    Attributes:
        mass (int or float or uncertain.UncertainValue): Mass of the element.
        cg (int or float or uncertain.UncertainValue, optional): x-Position of
            the center of gravity of the element. Default value is 0.
        id (string, optional): unique ID to identify the mass element. Relevant
            for working with tree structures. If not given, a random 8-digit
            string is used.
        name (string, optional): Name of the mass element.

    """
    def __init__(self, mass, cg=0, id=None, name=None):
        self.id = id
        self.mass = mass
        self.cg = cg
        self.name = name

        if self.id is None:
            chars = string.ascii_lowercase + string.digits
            self.id = ''.join(random.choices(chars, k=8))

    def plot_cgmass(self, title='CG-Mass density plot'):
        x = self.cg.samples
        y = self.mass.samples
        xmin, xmax = self.cg.lower_bound, self.cg.upper_bound
        ymin, ymax = self.mass.lower_bound, self.mass.upper_bound

        xx, yy = np.mgrid[xmin:xmax:20j, ymin:ymax:20j]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([x, y])
        kernel = st.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xx.shape)

        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        # Contourf plot
        ax.contourf(xx, yy, f, cmap='Blues')
        # # Or kernel density estimate plot instead of the contourf plot
        # ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
        #  Contour plot
        cset = ax.contour(xx, yy, f, colors='k')
        # Label plot
        ax.clabel(cset, inline=1, fontsize=10)
        ax.set_xlabel('CG [?]')
        ax.set_ylabel('Mass [?]')
        ax.set_title(title)
        # Nominal value
        plt.scatter(self.cg.nominal_value, self.mass.nominal_value, marker='P',
                    color='red', label='Nominal value')
        # Legend
        plt.legend()
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = Line2D([0], [0], color='k', linestyle='-',
                       linewidth=1, label='Kernel density')
        handles.append(patch)
        plt.legend(handles=handles, loc="upper left")
        # Show
        plt.show(block=False)


class MassElement3D:
    """ Class to describe objects with mass properties.

    Full properties in 3D: mass, cg (x, y, z) and inertias (ixx, iyy, izz,
    ixy, iyz, izx). For the asymmetric inertias, the convention with a negative
    factor is used:

    .. math::

       I_{xy} = - \sum{m_{k} \cdot x_{k} \cdot y_{k}}

    The moments and products of inertia are given around a coordinate system
    parallel to the global coordinate system and located on the center of
    gravity of the object.

    Attributes:
        mass (int or float or uncertain.UncertainValue): Mass of the element.
        x (int or float or uncertain.UncertainValue, optional): x-Position of
            the center of gravity of the element. Default value is 0.
        y (int or float or uncertain.UncertainValue, optional): y-Position of
            the center of gravity of the element. Default value is 0.
        z (int or float or uncertain.UncertainValue, optional): z-Position of
            the center of gravity of the element. Default value is 0.
        ixx (int or float or uncertain.UncertainValue, optional): Inertia of
            the object around the x-axis (moment of inertia). Default value
            is 0.
        iyy (int or float or uncertain.UncertainValue, optional): Inertia of
            the object around the y-axis (moment of inertia). Default value
            is 0.
        izz (int or float or uncertain.UncertainValue, optional): Inertia of
            the object around the z-axis (moment of inertia). Default value
            is 0.
        ixy (int or float or uncertain.UncertainValue, optional): Inertia of
            the object around the y-axis when the object is rotated around the
            x-axis (product of inertia). Default value is 0.
        iyz (int or float or uncertain.UncertainValue, optional): Inertia of
            the object around the z-axis when the object is rotated around the
            y-axis (product of inertia). Default value is 0.
        izx (int or float or uncertain.UncertainValue, optional): Inertia of
            the object around the x-axis when the object is rotated around the
            z-axis (product of inertia). Default value is 0.
        id (string, optional): unique ID to identify the mass element. Relevant
            for working with tree structures. If not given, a random 8-digit
            string is used.
        name (string, optional): Name of the mass element.

    """
    def __init__(self, mass, x=0, y=0, z=0, ixx=0, iyy=0, izz=0, ixy=0, iyz=0,
                 izx=0, id=None, name=None):
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.ixx = ixx
        self.iyy = iyy
        self.izz = izz
        self.ixy = ixy
        self.iyz = iyz
        self.izx = izx
        self.name = name

        if id is None:
            chars = string.ascii_lowercase + string.digits
            self.id = ''.join(random.choices(chars, k=8))
        else:
            self.id = id

    def __add__(self, other):
        if other == 0:
            return self
        new_mass = self.mass + other.mass
        new_x = (self.x * self.mass + other.x * other.mass)/new_mass
        new_y = (self.y * self.mass + other.y * other.mass)/new_mass
        new_z = (self.z * self.mass + other.z * other.mass)/new_mass
        new_ixx = self.ixx + self.mass * ((self.x - new_x)**2 +
                                          + (self.y - new_y)**2) \
            + other.ixx + other.mass * ((other.x - new_x)**2
                                        + (other.y - new_y)**2)
        new_iyy = self.iyy + self.mass * ((self.x - new_x)**2 +
                                          + (self.z - new_z)**2) \
            + other.iyy + other.mass * ((other.x - new_x)**2
                                        + (other.z - new_z)**2)
        new_izz = self.izz + self.mass * ((self.x - new_x)**2 +
                                          + (self.y - new_y)**2) \
            + other.izz + other.mass * ((other.x - new_x)**2
                                        + (other.y - new_y)**2)
        new_ixy = self.ixy - self.mass * (self.x - new_x)*(self.y - new_y) \
            + other.ixy - other.mass * (other.x - new_x)*(other.y - new_y)
        new_iyz = self.iyz - self.mass * (self.z - new_z)*(self.y - new_y) \
            + other.iyz - other.mass * (other.z - new_z)*(other.y - new_y)
        new_izx = self.izx - self.mass * (self.x - new_x)*(self.z - new_z) \
            + other.izx - other.mass * (other.x - new_x)*(other.z - new_z)
        return MassElement3D(new_mass, new_x, new_y, new_z, new_ixx, new_iyy,
                             new_izz, new_ixy, new_iyz, new_izx)

    def __radd__(self, other):
        return self + other

    def cg_vector(self):
        """ Returns the cg as an array.

        Returns:
            numpy.ndarray: [1 x 3] Vector
        """
        return np.array([self.x, self.y, self.z])

    def inertia_matrix(self):
        """ Returns the inertial data as a matrix.

        Returns:
            numpy.ndarray: [3 x 3] Inertia matrix.
        """
        return np.array([[self.ixx, self.ixy, self.izx],
                         [self.ixy, self.iyy, self.iyz],
                         [self.izx, self.iyz, self.izz]])

    def rotate(self, axis, angle, point=[0, 0, 0]):
        """ Rotates the object around an axis by a given angle.

        .. image:: ./../../resources/images/doc_inertia_rotation_01.svg

        This function updates the center of gravity, moments and products of
        inertia. If you want a new instance with the rotated properties, use a
        copy (deepcopy) of the object.

        Arguments:
            axis (list or numpy.ndarray): Vector [1 x 3] describing the
                rotation axis in the global coordinate system.
            angle (float): Rotation angle.
            point (list or numpy.ndarray or None): Vector [1 x 3] describing
                the point the object is rotated around. The default value is
                the center of gravity of the part.
        """
        rotation_matrix = rodrigues_rotation(axis, angle)

        new_cg = rotation_matrix @ self.cg_vector()
        self.x = new_cg[0]
        self.y = new_cg[1]
        self.z = new_cg[2]

        new_inertia = np.transpose(rotation_matrix) @ self.inertia_matrix() \
            @ rotation_matrix

        self.ixx = new_inertia[0][0]
        self.iyy = new_inertia[1][1]
        self.izz = new_inertia[2][2]
        self.ixy = new_inertia[0][1]
        self.iyz = new_inertia[1][2]
        self.izx = new_inertia[0][2]

    def describe(self):
        """ Prints the mass properties of the element.
        """
        print("Mass objects with the following properties:\n"
              + f"\tMass: {self.mass}\n"
              + f"\tX-Coordinate c.g.: {self.x}\n"
              + f"\tY-Coordinate c.g.: {self.y}\n"
              + f"\tZ-Coordinate c.g.: {self.z}\n"
              + f"\tMoment of inertia X: {self.ixx}\n"
              + f"\tMoment of inertia Y: {self.iyy}\n"
              + f"\tMoment of inertia Z: {self.izz}\n"
              + f"\tProduct of inertia XY: {self.ixy}\n"
              + f"\tProduct of inertia YZ: {self.iyz}\n"
              + f"\tProduct of inertia ZX: {self.izx}\n")


class MassObject3D:
    """ Class to describe objects with different types of mass properties.

    Attributes:
        estimated (MassElement3D): Estimated properties of the object.
        calculated (MassElement3D): Calculated properties of the object adding
            the values of all children mass objects.
        measured (MassElement3D): Measured properties of the object.
        id (string, optional): unique ID to identify the mass object. Relevant
            for working with tree structures. If not given, a random 8-digit
            string is used.
        name (string, optional): Name of the mass object.

    """
    states = ['estimated', 'calculated', 'measured']

    def __init__(self, estimated=None, calculated=None, measured=None,
                 active='estimated', id=None, name=None):
        self.estimated = estimated
        self.calculated = calculated
        self.measured = measured
        self.name = name
        self.active = active
        if active not in self.states:
            raise ValueError('Unknown active state. Should be one of the '
                             + 'following: {self.states}.')

        if id is None:
            chars = string.ascii_lowercase + string.digits
            self.id = ''.join(random.choices(chars, k=8))
        else:
            self.id = id

    def active_properties(self):
        """ Return the currently active properties.
        """
        if self.active == 'estimated':
            return self.estimated
        elif self.active == 'calculated':
            return self.calculated
        elif self.active == 'measured':
            return self.measured


class MassTree:
    """ Hierarchy between several simple mass elements (MassElements).

    Attributes:
        elements (dict): dictionary with MassElements. Their IDs are used as a
            key.
        parent_dict (dict): dictionary ponting to the ID of the parent of each
            element. The keys used are the IDs of the elements. The root
            element is not a key in the dictionary.

    """

    def __init__(self, elements, parent_dict):
        self.elements = elements
        self.parent_dict = parent_dict
        self.__determine_types()
        self.post_order = self.__post_order()
        self.__compute_values()

    def __determine_types(self):
        """ Determines the node ids, branch, root and leaf nodes
        """
        # Node IDs
        nodes = set(self.elements.keys())
        if len(nodes) != len(self.elements):
            raise ValueError("Duplicate element IDs. Check input.")
        self.nodes = nodes

        # Branch nodes
        self.branch_nodes = set(self.parent_dict.values())

        # Root
        self.root = self.nodes - set(self.parent_dict.keys())

        # Leafs
        self.leafs = self.nodes - self.branch_nodes

        # Children
        child_dict = defaultdict(list)
        for k, v in self.parent_dict.items():
            child_dict[v].append(k)
        self.child_dict = dict(child_dict)

    def __post_order(self):
        """ Determines a post-order sequence to traverse the tree

        Returns:
            seq (list): list with a post-order sequence to
                traverse the tree
        """
        sequence = list(self.leafs)
        while set(sequence) != self.nodes:
            elements_left = self.nodes - set(sequence)
            for element in elements_left:
                if set(self.child_dict[element]).issubset(set(sequence)):
                    sequence.append(element)
        return sequence

    def __compute_values(self):
        """ Computes the mass and cg of every non-leaf element.
        The correlation between the masses in the denominator and numerator
        are not taken into account!!! The bounds are handled separately
        """
        branch_sequence = self.post_order[len(self.leafs):]
        for i in branch_sequence:
            self.elements[i].mass = sum([self.elements[x].mass
                                         for x in self.child_dict[i]])
            self.elements[i].cg = sum(
                [self.elements[x].mass * self.elements[x].cg
                 for x in self.child_dict[i]]) \
                / self.elements[i].mass
            # Bounds
            m_lbs = np.array([self.elements[x].mass.lower_bound
                              for x in self.child_dict[i]])
            m_ubs = np.array([self.elements[x].mass.upper_bound
                              for x in self.child_dict[i]])
            cg_lbs = np.array([self.elements[x].cg.lower_bound
                               for x in self.child_dict[i]])
            cg_ubs = np.array([self.elements[x].cg.upper_bound
                               for x in self.child_dict[i]])
            self.elements[i].cg.lower_bound = \
                self.__min_cg(m_lbs, m_ubs, cg_lbs)
            self.elements[i].cg.upper_bound = \
                self.__max_cg(m_lbs, m_ubs, cg_ubs)

    def __min_cg(self, m_lbs, m_ubs, cg_lbs):
        """ Calculates the minimum possible value for the cg of a system
        consisting of n masses

        Args:
            m_lbs (list): [n] list of the lower bounds of the masses
            m_ubs (list): [n] list of the upper bounds of the masses
            cg_lbs (list): [n] list of the lower bounds of the cgs
        """
        n_el = len(m_lbs)
        cgs = [None]*n_el
        for i in np.arange(n_el):
            ids_1 = (cg_lbs <= cg_lbs[i])
            ids_2 = [not(x) for x in ids_1]
            cgs[i] = sum(ids_1*m_ubs*cg_lbs + ids_2*m_lbs*cg_lbs) \
                / sum(ids_1*m_ubs+ids_2*m_lbs)
        return min(cgs)

    def __max_cg(self, m_lbs, m_ubs, cg_ubs):
        """ Calculates the maximum possible value for the cg of a system
        consisting of n masses

        Args:
            m_lbs (list): [n] list of the lower bounds of the masses
            m_ubs (list): [n] list of the upper bounds of the masses
            cg_ubs (list): [n] list of the upper bounds of the cgs
        """
        n_el = len(m_lbs)
        cgs = [None]*n_el
        for i in np.arange(n_el):
            ids_1 = (cg_ubs <= cg_ubs[i])
            ids_2 = [not(x) for x in ids_1]
            cgs[i] = sum(ids_1*m_lbs*cg_ubs + ids_2*m_ubs*cg_ubs) \
                / sum(ids_1*m_lbs+ids_2*m_ubs)
        return max(cgs)


class MassObjectTree:
    """ Hierarchy between several mass objects (MassObject3D).

    Attributes:
        elements (dict): dictionary with MassElements. Their IDs are used as a
            key.
        parent_dict (dict): dictionary ponting to the ID of the parent of each
            element. The keys used are the IDs of the elements. The root
            element is not a key in the dictionary.

    """

    def __init__(self, elements_list, parent_dict):
        self.elements = dict({x.id: x for x in elements_list})
        self.parent_dict = parent_dict
        self.__determine_types()
        self.post_order = self.__post_order()
        self.__compute_values()

    def __determine_types(self):
        """ Determines the node ids, branch, root and leaf nodes
        """
        # Node IDs
        nodes = set(self.elements.keys())
        if len(nodes) != len(self.elements):
            raise ValueError("Duplicate element IDs. Check input.")
        self.nodes = nodes

        # Branch nodes
        self.branch_nodes = set(self.parent_dict.values())

        # Root
        self.root = self.nodes - set(self.parent_dict.keys())

        # Leafs
        self.leafs = self.nodes - self.branch_nodes

        # Children
        child_dict = defaultdict(list)
        for k, v in self.parent_dict.items():
            child_dict[v].append(k)
        self.child_dict = dict(child_dict)

    def __post_order(self):
        """ Determines a post-order sequence to traverse the tree

        Returns:
            seq (list): list with a post-order sequence to
                traverse the tree
        """
        sequence = list(self.leafs)
        while set(sequence) != self.nodes:
            elements_left = self.nodes - set(sequence)
            for element in elements_left:
                if set(self.child_dict[element]).issubset(set(sequence)):
                    sequence.append(element)
        return sequence

    def __compute_values(self):
        """ Computes the mass and properties of every non-leaf element.
        The correlation between the masses in the denominator and numerator
        are not taken into account!!!
        """
        branch_sequence = self.post_order[len(self.leafs):]
        for i in branch_sequence:
            self.elements[i].calculated = sum([
                self.elements[x].active_properties()
                for x in self.child_dict[i]])

    def update(self):
        """ Recalculates the mass properties of non-leaf elements.
        """
        self.__compute_values()
