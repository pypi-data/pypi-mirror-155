""" Mass calculation formulas for solid bodies.
"""

from mauspaf.masslibrary.misc import eqs_solver, valid_inputs, dict_conv


def cylinder_full(r=None, d=None, le=None, v=None, s=None, rho=None, m=None,
                  ix=None, iy=None, iz=None,
                  units={'r': 'm', 'd': 'm', 'le': 'm', 'v': 'm³', 's': 'm²',
                         'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²',
                         'iy': 'kg·m²', 'iz': 'kg·m²'},
                  calc_mode='values'):
    """ Returns all cylinder properties for any given set of inputs.

    Args:
        r (float): Radius.
        d (float): Diameter.
        le (float): Length.
        v (float): Volume.
        s (float): Surface area.
        rho (float): Density.
        m (float): Mass.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.

    """
    eqs = ["d - 2*r",
           "s - (2*pi*le*r+2*pi*r**2)",
           "v - le*pi*r**2",
           "m - rho*v",
           "ix - (m/12)*(3*r**2+le**2)",
           "iy - ix",
           "iz - m*r**2/2"]

    original_units = {'r': 'm', 'd': 'm', 'le': 'm', 'v': 'm³', 's': 'm²',
                      'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                      'iz': 'kg·m²'}
    default_units = {'r': 'm', 'd': 'm', 'le': 'm', 's': 'm²', 'v': 'm³',
                     'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                     'iz': 'kg·m²'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def hollow_cylinder(ro=None, ri=None, do=None, di=None, t=None, le=None,
                    ix=None, iy=None, iz=None, v=None, rho=None, m=None,
                    s=None,
                    units={'ro': 'm', 'ri': 'm', 'do': 'm', 'di': 'm',
                           't': 'm', 'le': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²',
                           'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                           's': 'm²'},
                    calc_mode='values'):
    """ Returns all hollow cylinder properties for any given set of inputs

    Args:
        ro (float): Outer Radius.
        ri (float): Inner radius.
        do (float): Outer Diameter.
        di (float): Inner diameter.
        t (float): Wall thickness.
        le (float): Length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["do - 2*ro",
           "di - 2*ri",
           "t - (ro - ri)",
           "v - pi*le*(ro**2-ri**2)",
           "m - rho*v",
           "s - 2*pi*(ro+ri)*le - 2*pi*(ro**2-ri**2)",
           "ix - (m/12)*(3*(ro**2+ri**2)+le**2)",
           "iy - ix",
           "iz - (m/2)*(ro**2+ri**2)"]

    original_units = {'ro': 'm', 'ri': 'm', 'do': 'm', 'di': 'm', 'le': 'm',
                      's': 'm²', 'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 't': 'm'}
    default_units = {'ro': 'm', 'ri': 'm', 'do': 'm', 'di': 'm', 'le': 'm',
                     's': 'm²', 'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 't': 'm'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def cube(a=None, ix=None, iy=None, iz=None, v=None, rho=None, m=None, s=None,
         units={'a': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
         calc_mode='values'):
    """ Returns all cube properties for any given set of inputs

    Args:
        a (float): edge lenght of cube.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - a**3",
           "m - rho*v",
           "s - 6*a**2",
           "ix - (m*a**2)/6",
           "iy - ix",
           "iz - ix"]

    original_units = {'a': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    default_units = {'a': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def rectangular_prism(a=None, b=None, h=None, ix=None, iy=None, iz=None,
                      v=None, rho=None, m=None, s=None,
                      units={'a': 'm', 'b': 'm', 'h': 'm', 'ix': 'kg·m²',
                             'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                             'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                      calc_mode='values'):
    """ Returns all rectangular prism properties for any given set of inputs

    Args:
        a (float): Width.
        b (float): Lenght.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - a*b*h",
           "m - rho*v",
           "s - 2*(a*h+a*b+b*h)",
           "ix - (m/12)*(b**2+h**2)",
           "iy - (m/12)*(a**2+h**2)",
           "iz - (m/12)*(a**2+b**2)"]

    original_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def sphere(r=None, d=None, ix=None, iy=None, iz=None, v=None, rho=None, m=None,
           s=None,
           units={'r': 'm', 'd': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²',
                  'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                  's': 'm²'},
           calc_mode='values'):
    """ Returns all sphere properties for any given set of inputs

    Args:
        r (float): Radius
        d (float): Diameter.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["d - 2*r",
           "v - (4/3)*pi*r**3",
           "m - rho*v",
           "s - 4*pi*r**2",
           "ix - (2/5)*m*r**2",
           "iy - ix",
           "iz - ix"]

    original_units = {'r': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    default_units = {'r': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def hollow_sphere(ro=None, ri=None, do=None, di=None, ix=None, iy=None,
                  iz=None, v=None, rho=None, m=None, s=None, t=None,
                  units={'ro': 'm', 'ri': 'm', 'do': 'm', 'di': 'm',
                         'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 't': 'm',
                         'rho': 'kg/m³', 'm': 'kg', 's': 'm²', 'ix': 'kg·m²'},
                  calc_mode='values'):
    """ Returns all hollow sphere properties for any given set of inputs

    Args:
        ro (float): Outer radius.
        ri (float): Inner radius.
        do (float): Outer diameter.
        di (float): Inner diameter.
        t (float): Wall thickness.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["do - 2*ro",
           "di - 2*ri",
           "t - (ro - ri)",
           "v - (4/3)*pi*(ro**3-ri**3)",
           "m - rho*v",
           "s - 4*pi*ro**2 - 4*pi*ri**2",
           "ix - (2/5)*m*((ro**5-ri**5)/(ro**3-ri**3))",
           "iy - ix",
           "iz - ix"]

    original_units = {'ro': 'm', 'ri': 'm', 'do': 'm', 'di': 'm', 's': 'm²',
                      'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                      'iz': 'kg·m²', 'v': 'm³', 't': 'm'}
    default_units = {'ro': 'm', 'ri': 'm', 'do': 'm', 'di': 'm', 's': 'm²',
                     'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                     'iz': 'kg·m²', 'v': 'm³', 't': 'm'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def hemisphere(r=None, d=None, ix=None, iy=None, iz=None, v=None, rho=None,
               m=None, s=None,
               units={'r': 'm', 'd': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²',
                      'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                      's': 'm²'},
               calc_mode='values'):
    """ Returns all hemisphere properties for any given set of inputs

    Args:
        r (float): Radius.
        d (float): Diameter.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["d - 2*r",
           "v - (2/3)*pi*r**3",
           "m - rho*v",
           "s - 3*pi*r**2",
           "ix - 0.26*m*r**2",
           "iy - ix",
           "iz - 0.4*m*r**2"]

    original_units = {'r': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    default_units = {'r': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def elliptical_cylinder(a=None, b=None, h=None, ix=None, iy=None, iz=None,
                        v=None, rho=None, m=None, s=None,
                        units={'a': 'm', 'b': 'm', 'h': 'm', 'ix': 'kg·m²',
                               'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                               'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                        calc_mode='values'):
    """ Returns all elliptical cylinder properties for any given set of inputs

    Args:
        a (float): Semi axis x-direction.
        b (flaot): Semi axis y-direction.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - pi*a*b*h",
           "m - rho*v",
           "s - h*pi*(a+b)",
           "ix - (m/12)*(3*b**2+h**2)",
           "iy - (m/12)*(3*a**2+h**2)",
           "iz - (m/4)*(a**2+b**2)"]

    original_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def ellipsoid(a=None, b=None, c=None, ix=None, iy=None, iz=None, v=None,
              rho=None, m=None, s=None,
              units={'a': 'm', 'b': 'm', 'c': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'},
              calc_mode='values'):
    """ Returns all ellipsoid properties for any given set of inputs

    Args:
        a (float): Semi axis z-direction.
        b (flaot): Semi axis x-direction.
        c (flaot): Semi axis y-direction.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - (4/3)*pi*a*b*c",
           "m - rho*v",
           "s - 4*pi*(((a*b)**1.6+(a*c)**1.6+(b*c)**1.6)/3)**(5/8)",
           "ix - (m/5)*(a**2+c**2)",
           "iy - (m/5)*(a**2+b**2)",
           "iz - (m/5)*(b**2+c**2)"]

    original_units = {'a': 'm', 'b': 'm', 'c': 'm', 's': 'm²', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'a': 'm', 'b': 'm', 'c': 'm', 's': 'm²', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def elliptical_hemispheroid(r=None, h=None, ix=None, iy=None, iz=None, v=None,
                            rho=None, m=None, s=None,
                            units={'r': 'm', 'h': 'm', 'ix': 'kg·m²',
                                   'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                                   'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                            calc_mode='values'):
    """ Returns all elliptical hemisperoid properties for any given set of
    inputs

    Args:
        r (float): Radius.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - (2/3)*pi*r**2*h",
           "m - rho*v",
           "s - (2*pi*(((h*r)**1.6+(h*r)**1.6+(r**2)**1.6)/3)**(5/8)+pi*r**2)",
           "ix - m*((r**2)/5+(19*h**2)/320)",
           "iy - ix",
           "iz - 0.4*m*r**2"]

    original_units = {'r': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    default_units = {'r': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³', 'm': 'kg',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def revolutioned_paraboloid(r=None, h=None, d=None, ix=None, iy=None, iz=None,
                            v=None, rho=None, m=None, s=None,
                            units={'r': 'm', 'h': 'm', 'd': 'm', 'ix': 'kg·m²',
                                   'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                                   'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                            calc_mode='values'):
    """ Returns all revolutioned paraboloid properties for any given set of
    inputs

    Args:
        r (float): Radius.
        h (float): Height.
        d (float): Diameter.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - (pi*r**2*h)/2",
           "d - 2*r",
           "m - rho*v",
           "s - (pi*r**2+((pi*r)/(6*h**2))*((r**2+4*h**2)**1.5-r**3)) ",
           "ix - (m/18)*(3*r**2+h**2)",
           "iy - ix",
           "iz - (m*r**2)/3"]

    original_units = {'r': 'm', 'h': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'r': 'm', 'h': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def rectangular_pyramid(a=None, b=None, h=None, ix=None, iy=None, iz=None,
                        v=None, rho=None, m=None, s=None,
                        units={'a': 'm', 'b': 'm', 'h': 'm', 'ix': 'kg·m²',
                               'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                               'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                        calc_mode='values'):
    """ Returns all rectangular pyramid properties for any given set of
    inputs

    Args:
        a (float): Width
        b (float): Length.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - a*b*h/3",
           "m - rho*v",
           "s - (a*b+a*((b/2)**2+h**2)**0.5+b*((a/2)**2+h**2)**0.5)",
           "ix - (m/20)*(b**2+3*h**2/4)",
           "iy - (m/20)*(a**2+3*h**2/4)",
           "iz - (m/20)*(a**2+b**2)"]

    original_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def right_angled_wedge(a=None, b=None, h=None, ix=None, iy=None, iz=None,
                       v=None, rho=None, m=None, s=None,
                       units={'a': 'm', 'b': 'm', 'h': 'm', 'ix': 'kg·m²',
                              'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                              'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                       calc_mode='values'):
    """ Returns all right angled wedge properties for any given set of
    inputs

    Args:
        a (float): Width.
        b (float): Length.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - a*b*h/2",
           "m - rho*v",
           "s - (a*b+a*h+b*h+b*(a**2+h**2)**0.5)",
           "ix - (m/36)*(2*h**2+3*b**2)",
           "iy - (m/18)*(a**2+h**2)",
           "iz - (m/36)*(2*a**2+3*b**2)"]

    original_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'a': 'm', 'b': 'm', 'h': 'm', 's': 'm²', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def circular_cone(r=None, h=None, d=None, ix=None, iy=None, iz=None, v=None,
                  rho=None, m=None, s=None,
                  units={'r': 'm', 'h': 'm', 'd': 'm', 'ix': 'kg·m²',
                         'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                         'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                  calc_mode='values'):
    """ Returns all circular cone properties for any given set of
    inputs

    Args:
        r (float): Radius.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["d - 2*r",
           "v - pi*r**2*h/3",
           "m - rho*v",
           "s - pi*r*(r+(r**2+h**2)**0.5)",
           "ix - (3*m/20)*(r**2+h**2/4)",
           "iy - ix",
           "iz - (3*m/10)*r**2"]

    original_units = {'r': 'm', 'h': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'r': 'm', 'h': 'm', 'd': 'm', 's': 'm²', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def frustum_cone(R=None, r=None, D=None, d=None, h=None, ix=None, iy=None,
                 iz=None, v=None, rho=None, m=None, s=None,
                 units={'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 'h': 'm',
                        'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                        'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                 calc_mode='values'):
    """ Returns all frustum cone properties for any given set of inputs

    Args:
        R (float): Base radius.
        r (float): Top radius.
        D (float): Base diameter.
        d (float): Top diameter.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["D - 2*r",
           "d - 2*r",
           "v - (pi*h/3)*(R**2+R*r+r**2)",
           "m - rho*v",
           "s - (pi*h*(R+r)+pi*R**2+pi*r**2)",
           "ix - ((m*h**2/10)*((R**2+3*R*r+6*r**2)/(R**2+R*r+r**2))+(3*m/20)*"
           "((R**5-r**5)/(R**3-r**3))-m*(h/4*((R**2+2*R*r+3*r**2)/(R**2+R*r+"
           "r**2)))**2)",
           "iy - ix",
           "iz - (3*m/10)*((R**5-r**5)/(R**3-r**3))"]

    original_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 'h': 'm',
                      's': 'm²', 'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    default_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 'h': 'm',
                     's': 'm²', 'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def elliptic_paraboloid(a=None, b=None, h=None, ix=None, iy=None, iz=None,
                        v=None, rho=None, m=None,
                        units={'a': 'm', 'b': 'm', 'h': 'm', 'ix': 'kg·m²',
                               'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                               'rho': 'kg/m³', 'm': 'kg'},
                        calc_mode='values'):
    """ Returns all elliptic paraboloid properties for any given set of
    inputs.

    Args:
        a (float): Semi axis in x-direction.
        b (float): Semi axis in y-direction.
        h (float): Height.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    # TODO: Add formula to calculate the surface area.
    eqs = ["v - pi*a*b*h/2",
           "m - rho*v",
           # Keine Formel ohne Integral gefunden"s - ",
           "ix - (m/18)*(3*b**2+h**2)",
           "iy - (m/18)*(3*a**2+h**2)",
           "iz - (m/6)*(a**2+b**2)"]

    original_units = {'a': 'm', 'b': 'm', 'h': 'm', 'rho': 'kg/m³',
                      'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³'}
    default_units = {'a': 'm', 'b': 'm', 'h': 'm', 'rho': 'kg/m³',
                     'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                     'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def torus(R=None, r=None, D=None, d=None, ix=None, iy=None, iz=None, v=None,
          rho=None, m=None, s=None,
          units={'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 'ix': 'kg·m²',
                 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                 'm': 'kg', 's': 'm²'},
          calc_mode='values'):
    """ Returns all torus properties for any given set of inputs

    Args:
        R (float): Radius.
        r (float): Truss radius.
        D (float): Diameter.
        d (float): Truss diameter.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["D - 2*R",
           "d - 2*r",
           "v - 2*pi**2*r**2*R",
           "m - rho*v",
           "s - 4*pi**2*R*r",
           "ix - (m/8)*(4*R**2+5*r**2)",
           "iy - (m/4)*(4*R**2+3*r**2)",
           "iz - iy"]

    original_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 's': 'm²',
                      'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                      'iz': 'kg·m²', 'v': 'm³'}
    default_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 's': 'm²',
                     'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                     'iz': 'kg·m²', 'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def outer_half_torus(R=None, r=None, D=None, d=None, ix=None, iy=None, iz=None,
                     v=None, rho=None, m=None, s=None,
                     units={'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm',
                            'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                            'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                     calc_mode='values'):
    """ Returns all outer half torus properties for any given set of inputs

    Args:
        R (float): Radius.
        r (float): Truss radius.
        D (float): Diameter.
        d (float): Truss diameter.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["D - 2*R",
           "d - 2*r",
           "v - ((4/3)*pi*r**3+pi**2*r**2*R)",
           "m - rho*v",
           "s - 2*pi*R*(pi*r+r)",
           "ix - (m/(4.189*r+9.870*R))*(1.6755*r**3+7.4022*R*r**2+12.5664*R**2"
           "*r+9.869*R**3)",
           "iy - (m/12)*(27*pi*R*r**2+36*R**2*r+44*r**3)",
           "iy - iz"]

    original_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 's': 'm²',
                      'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                      'iz': 'kg·m²', 'v': 'm³'}
    default_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 's': 'm²',
                     'rho': 'kg/m³', 'm': 'kg', 'ix': 'kg·m²', 'iy': 'kg·m²',
                     'iz': 'kg·m²', 'v': 'm³'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def spherical_sector(r=None, h=None, iz=None, v=None, rho=None, m=None,
                     units={'r': 'm', 'h': 'm', 'iz': 'kg·m²', 'v': 'm³',
                            'rho': 'kg/m³', 'm': 'kg'},
                     calc_mode='values'):
    """ Returns all spherical sector properties for any given set of inputs

    Args:
        r (float): Radius.
        h (float): Height.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - (2/3)*pi*r**2*h",
           "m - rho*v",
           "iz - (m*h/5)*(3*r-h)"]

    original_units = {'r': 'm', 'h': 'm', 'iz': 'kg·m²', 'v': 'm³',
                      'rho': 'kg/m³', 'm': 'kg'}
    default_units = {'r': 'm', 'h': 'm', 'iz': 'kg·m²', 'v': 'm³',
                     'rho': 'kg/m³', 'm': 'kg'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def spherical_segment(r=None, h=None, iz=None, v=None, rho=None, m=None,
                      s=None,
                      units={'r': 'm', 'h': 'm', 'iz': 'kg·m²', 'v': 'm³',
                             'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                      calc_mode='values'):
    """ Returns all spherical segment properties for any given set of inputs

    Args:
        r (float): Radius.
        h (float): Height.
        iz (float): Moment of inertia about z axis.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - (pi*h**2/3)*(3*r-h)",
           "m - rho*v",
           "s - 2*pi*r*h",
           "iz - ((2*h*m)/(3*r-h))*(r**2-0.75*r*h+0.15*h**2)"]

    original_units = {'r': 'm', 'h': 'm', 'iz': 'kg·m²', 'v': 'm³',
                      'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'h': 'm', 'iz': 'kg·m²', 'v': 'm³',
                     'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def prismoid(b0=None, b1=None, c0=None, c1=None, h=None, A0=None, A1=None,
             Am=None, i0x=None, i0y=None, i0z=None, i1x=None, i1y=None,
             i1z=None, imx=None, imy=None, imz=None, ix=None, iy=None, iz=None,
             x=None, v=None, rho=None, m=None, s=None,
             units={'b0': 'm', 'b1': 'm', 'c0': 'm', 'c1': 'm', 'h': 'm',
                    'A0': 'm²', 'A1': 'm²', 'Am': 'm²', 'i0x': 'm⁴',
                    'i0y': 'm⁴', 'i0z': 'm⁴', 'i1x': 'm⁴', 'i1y': 'm⁴',
                    'i1z': 'm⁴', 'imx': 'm⁴', 'imy': 'm⁴', 'imz': 'm⁴',
                    'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'x': 'm',
                    'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
             calc_mode='values'):
    """ Returns all prismoid properties for any given set of inputs

    Args:
        b0 (float): Lenght of Base.
        b1 (float): Lenght of Top.
        c0 (float): Width of Base.
        c1 (flaot): Width of Top.
        h (float): Height.
        A0 (float): Area of Base.
        A1 (float): Area at h/2.
        Am (float): Area of Top.
        i0x (float): Area moment of inertia about x axis of A0.
        i0y (float): Area moment of inertia about y axis of A0.
        i0z (float): Area moment of inertia about z axis of A0.
        i1x (float): Area moment of inertia about x axis of A1.
        i1y (float): Area moment of inertia about y axis of A1.
        i1z (float): Area moment of inertia about z axis of A1.
        imx (float): Area moment of inertia about x axis of Am.
        imy (float): Area moment of inertia about y axis of Am.
        imz (float): Area moment of inertia about z axis of Am.
        ix (float): Moment of inertia about x.
        iy (float): Moment of inertia about y.
        iz (float): Moment of inertia about z.
        x (float): Centroid.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["A0 - c0*b0",
           "A1 - c1*b1",
           "Am - ((c0+c1)/2)*((b0+b1)/2)",
           "x - (h*(A1+2*Am))/(A0+A1+4*Am)",
           "v - (h/6)*(A0+A1+4*Am)",
           "m - rho*v",
           "s - (c0*b0+c1*b1+2*(((b0-b1)**2+h**2)**0.5*c1+((b0-b1)**2+h**2)"
           "**0.5*(c0-c1))+2*(((c0-c1)**2+h**2)**0.5*b1+((c0-c1)**2+h**2)"
           "**0.5*(b0-b1)))",
           "i0x - b0**3*c0/12",
           "i0y - b0*c0**3/12",
           "i0z - A0*x**2",
           "i1x - b1**3*c1/12",
           "i1y - b1*c1**3/12",
           "i1z - A1*(h-x)**2",
           "imx - ((b0+b1)/2)**3*((c0+c1)/2)/12",
           "imy - ((b0+b1)/2)*((c0+c1)/2)**3/12",
           "imz - Am*((h/2)-x)**2",
           "ix - (rho*h/20)*((3*i0x+16*imx+3*i1x-A1/A0*i0x-A1/A0*i1x)+(h**2/3)"
           "*(-A0+12*Am+9*A1-(10*(2*Am+A1)**2)/(A0+4*Am+A1)))",
           "iy - (rho*h/20)*((3*i0y+16*imy+3*i1y-A1/A0*i0y-A1/A0*i1y)+(h**2/3)"
           "*(-A0+12*Am+9*A1-(10*(2*Am+A1)**2)/(A0+4*Am+A1)))",
           "iz - (rho*h/20)*(3*i0z+16*imz+3*i1z-A1/A0*i0z-A1/A0*i1z)"]

    original_units = {'b0': 'm', 'b1': 'm', 'c0': 'm', 'c1': 'm', 'h': 'm',
                      'A0': 'm²', 'A1': 'm²', 'Am': 'm²', 'i0x': 'm⁴',
                      'i0y': 'm⁴', 'i0z': 'm⁴', 'i1x': 'm⁴', 'i1y': 'm⁴',
                      'i1z': 'm⁴', 'imx': 'm⁴', 'imy': 'm⁴', 'imz': 'm⁴',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'x': 'm',
                      'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'b0': 'm', 'b1': 'm', 'c0': 'm', 'c1': 'm', 'h': 'm',
                     'A0': 'm²', 'A1': 'm²', 'Am': 'm²', 'i0x': 'm⁴',
                     'i0y': 'm⁴', 'i0z': 'm⁴', 'i1x': 'm⁴', 'i1y': 'm⁴',
                     'i1z': 'm⁴', 'imx': 'm⁴', 'imy': 'm⁴', 'imz': 'm⁴',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'x': 'm',
                     'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def solid_ogive(R=None, r=None, d=None, D=None, h=None, v=None, rho=None,
                m=None, s=None,
                units={'R': 'm', 'r': 'm', 'd': 'm', 'D': 'm', 'h': 'm',
                       'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                calc_mode='values'):
    """ Returns all solid ogive properties for any given set of inputs

    Args:
        R (float): Radius of curvature.
        r (float): Radius.
        D (float): Distance to curvature origin.
        d (float): Radius of truncated nose.
        h (float): Height.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    if d == 0:
        eqs = ["D - (R-r)",
               "v - pi*(h*(R**2-(h**2/3))-R**2*D*arcsin(h/R))",
               "m - rho*v",
               "s - (2*pi*r*(h-D*arcsin(h/R))+pi*r**2)"]
    elif d > 0:
        eqs = ["D - (R-r)",
               "v - pi*(h*(R**2+D**2-D*(R**2-h**2)**0.5-(h**2/3))-R**2*D*"
               "arcsin(h/R))",
               "m - rho*v"]
    else:
        raise ValueError('Invalid truncated nose diameter')

    original_units = {'R': 'm', 'r': 'm', 'd': 'm', 'D': 'm', 'h': 'm',
                      'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'R': 'm', 'r': 'm', 'd': 'm', 'D': 'm', 'h': 'm',
                     'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    used_units = {**default_units, **units}

    solver_input = dict_conv(locals(), used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result
