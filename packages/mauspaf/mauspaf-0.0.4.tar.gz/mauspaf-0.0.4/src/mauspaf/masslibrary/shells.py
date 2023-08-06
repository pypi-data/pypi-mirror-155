from mauspaf.masslibrary.misc import eqs_solver, valid_inputs, dict_conv


def lateral_cylindrical_shell(r=None, d=None, h=None, t=None, ix=None, iy=None,
                              iz=None, v=None, rho=None, m=None, s=None,
                              units={'r': 'm', 'd': 'm', 'h': 'm', 't': 'm',
                                     'ix': 'kg·m²', 'iy': 'kg·m²',
                                     'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                                     'm': 'kg', 's': 'm²'},
                              calc_mode='values'):
    """ Returns all lateral cylindrical shell properties for any given set of
    inputs

    Args:
        r (float): Radius.
        d (float): Diameter.
        h (float): Height.
        t (float): Thickness.
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
           "v - s*t",
           "m - rho*v",
           "s - 2*pi*r*h",
           "ix - (m/2)*(r**2+h**2/6)",
           "iy - ix",
           "iz - m*r**2"]

    original_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def total_cylindrical_shell(r=None, d=None, h=None, t=None, ix=None, iy=None,
                            iz=None, v=None, rho=None, m=None, s=None,
                            units={'r': 'm', 'd': 'm', 'h': 'm', 't': 'm',
                                   'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                                   'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                                   's': 'm²'},
                            calc_mode='values'):
    """ Returns all total cylindrical shell properties for any given set of
    inputs

    Args:
        r (float): Radius.
        d (float): Diameter.
        h (float): Height.
        t (float): Thickness.
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
           "v - s*t",
           "m - rho*v",
           "s - 2*pi*r*(r+h)",
           "ix - (m/(12*(r+h)))*(3*r**2*(r+2*h)+h**2*(3*r+h))",
           "iy - ix",
           "iz - (m*r**2/2)*((r+2*h)/(r+h))"]

    original_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def elliptical_shell(a=None, b=None, h=None, t=None, ix=None, iy=None, iz=None,
                     v=None, rho=None, m=None, s=None,
                     units={'a': 'm', 'b': 'm', 'h': 'm', 't': 'm',
                            'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                            'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                     calc_mode='values'):
    """ Returns all total elliptical shell properties for any given set of
    inputs

    Args:
        a (float): Semi axis in x-direction.
        b (float): Semi axis in y-direction.
        h (float): Height.
        t (float): Thickness.
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
    eqs = ["v - s*t",
           "m - rho*v",
           "s - 2*pi*(a*b+h*((a**2+b**2)/2)**0.5)",
           "ix - ((m*b**2/4)*((7*a**2+b**2)/(3*a**2+b**2))+(m*h**2/12))",
           "iy - ((m*a**2/4)*((7*b**2+a**2)/(3*a**2+b**2))+(m*h**2/12))",
           "iz - (m/4)*((a**4+14*a**2*b**2+b**4)/(3*a**2+b**2))"]

    original_units = {'a': 'm', 'b': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'a': 'm', 'b': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def hollow_box(a=None, b=None, c=None, t=None, ix=None, iy=None, iz=None,
               v=None, rho=None, m=None, s=None,
               units={'a': 'm', 'b': 'm', 'c': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'},
               calc_mode='values'):
    """ Returns all hollow box shell properties for any given set of
    inputs

    Args:
        a (float): Width.
        b (float): Height.
        c (float): Lenght.
        t (float): Thickness.
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
    eqs = ["v - s*t",
           "m - rho*v",
           "s - 2*(a*b+a*c+b*c)",
           "ix - ((m/12)*(b**2+c**2)+(m/6)*((a*b*c*(b+c))/(a*b+a*c+b*c)))",
           "iy - ((m/12)*(a**2+b**2)+(m/6)*((a*b*c*(a+b))/(a*b+a*c+b*c)))",
           "iz - ((m/12)*(a**2+c**2)+(m/6)*((a*b*c*(a+c))/(a*b+a*c+b*c)))"]

    original_units = {'a': 'm', 'b': 'm', 'c': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'a': 'm', 'b': 'm', 'c': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def open_hollow_box(a=None, b=None, c=None, t=None, ix=None, iy=None, iz=None,
                    v=None, rho=None, m=None, s=None,
                    units={'a': 'm', 'b': 'm', 'c': 'm', 't': 'm',
                           'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                           'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                    calc_mode='values'):
    """ Returns all hollow box shell properties for any given set of
    inputs

    Args:
        a (float): Width.
        b (float): Height.
        c (float): Lenght.
        t (float): Thickness.
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
    eqs = ["v - s*t",
           "m - rho*v",
           "s - 2*c*(a+b)",
           "ix - ((m/12)*(b**2+c**2)+((m*a*b**2)/(6*(a+b))))",
           "iy - (m/12)*(a**2+b**2)",
           "iz - ((m/12)*(a**2+c**2)+((m*b*a**2)/(6*(a+b))))"]

    original_units = {'a': 'm', 'b': 'm', 'c': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'a': 'm', 'b': 'm', 'c': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def frustum_cone_shell(R=None, r=None, D=None, d=None, h=None, t=None, ix=None,
                       iy=None, iz=None, v=None, rho=None, m=None, s=None,
                       units={'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 'h': 'm',
                              't': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²',
                              'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                              'm': 'kg', 's': 'm²'},
                       calc_mode='values'):
    """ Returns all frustum cone shell properties for any given set of
    inputs

    Args:
        R (float): Base Radius.
        r (float): Top Radius.
        D (float): Base diameter.
        d (float): Top diameter.
        h (flaot): Height.
        t (float): Thickness.
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
           "v - s*t",
           "m - rho*v",
           "s - pi*(R+r)*(h**2+(R-r)**2)**0.5",
           "ix - ((m/4)*(R**2+r**2)+(m*h**2/18)*(1+((2*R*r)/(R+r)**2)))",
           "iy - ix",
           "iz - (m/2)*(R**2+r**2)"]

    original_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 'h': 'm',
                      't': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                      'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'R': 'm', 'r': 'm', 'D': 'm', 'd': 'm', 'h': 'm',
                     't': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
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


def circular_cone_shell(r=None, d=None, h=None, t=None, ix=None, iy=None,
                        iz=None, v=None, rho=None, m=None, s=None,
                        units={'r': 'm', 'd': 'm', 'h': 'm', 't': 'm',
                               'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²',
                               'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                               's': 'm²'},
                        calc_mode='values'):
    """ Returns all circular cone shell properties for any given set of
    inputs

    Args:
        r (float): Radius.
        d (float): Diameter.
        h (flaot): Height.
        t (float): Thickness.
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
           "v - s*t",
           "m - rho*v",
           "s - pi*r*(r**2+h**2)**0.5",
           "ix - (m/4)*(r**2+(2/9)*h**2)",
           "iy - ix",
           "iz - (m*r**2/2)"]
    original_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def spherical_shell(r=None, d=None, t=None, ix=None, iy=None, iz=None, v=None,
                    rho=None, m=None, s=None,
                    units={'r': 'm', 'd': 'm', 't': 'm', 'ix': 'kg·m²',
                           'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                           'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                    calc_mode='values'):
    """ Returns all spherical shell properties for any given set of
    inputs

    Args:
        r (float): Radius.
        d (float): Diameter.
        t (float): Thickness.
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
           "v - s*t",
           "m - rho*v",
           "s - 4*pi*r**2",
           "ix - (2/3)*m*r**2",
           "iy - ix",
           "iz - ix"]
    original_units = {'r': 'm', 'd': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'd': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def hemispherical_shell(r=None, d=None, t=None, ix=None, iy=None, iz=None,
                        v=None, rho=None, m=None, s=None,
                        units={'r': 'm', 'd': 'm', 't': 'm', 'ix': 'kg·m²',
                               'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                               'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                        calc_mode='values'):
    """ Returns all hemispherical shell properties for any given set of
    inputs

    Args:
        r (float): Radius.
        d (float): Diameter.
        t (float): Thickness.
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
           "v - s*t",
           "m - rho*v",
           "s - 2*pi*r**2",
           "ix - (5/12)*m*r**2",
           "iy - ix",
           "iz - (2/3)*m*r**2"]
    original_units = {'r': 'm', 'd': 'm', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'd': 'm', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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


def elliptical_hemispheriodal_shell(r=None, h=None, e=None, axis=None, t=None,
                                    v=None, rho=None, m=None, s=None,
                                    units={'r': 'm', 'h': 'm', 'e': None,
                                           't': 'm', 'v': 'm³',
                                           'rho': 'kg/m³', 'm': 'kg',
                                           's': 'm²'},
                                    calc_mode='values'):
    """ Returns all elliptical hemispheriodal shell properties for any given
    set of inputs

    Args:
        r (float): Major axis.
        h (float): Minor axis.
        e (float): Eccentricity.
        axis (string): 'major' for rotation about major axis, 'minor' for
            rotation about the minor axis
        t (float): Thickness.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    if axis == 'minor':
        eqs = ["v - s*t",
               "m - rho*v",
               "s - pi*(r**2+(h**2/(2*e))*ln((1+e)/(1-e)))",
               "e - (r**2-h**2)**0.5/r"]
    elif axis == 'major':
        eqs = ["v - s*t",
               "m - rho*v",
               "s - 2*pi*(h**2+(r*h/e)*arcsin(e))",
               "e - (r**2-h**2)**0.5/r"]
    else:
        raise ValueError('Unknown rotation direction ' + axis)

    original_units = {'r': 'm', 'h': 'm', 'e': None, 't': 'm',
                      'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'h': 'm', 'e': None, 't': 'm',
                     'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    used_units = {**default_units, **units}

    used_locals = locals().copy()
    used_locals.pop('axis')
    solver_input = dict_conv(used_locals, used_units, original_units, 'input')

    if calc_mode == 'values':
        eq_res = eqs_solver(eqs, **solver_input)
        result = dict_conv(eq_res, original_units,
                           used_units, 'output')
    elif calc_mode == 'sets':
        result = valid_inputs(eqs)
    else:
        raise ValueError('Unknown calculation mode ' + calc_mode)
    return result


def revolutioned_paraboloid_shell(r=None, h=None, d=None, t=None, P=None,
                                  ix=None, iy=None, iz=None, v=None, rho=None,
                                  m=None, s=None,
                                  units={'r': 'm', 'h': 'm', 't': 'm',
                                         'P': 'm³', 'ix': 'kg·m²',
                                         'iy': 'kg·m²', 'iz': 'kg·m²',
                                         'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                                         's': 'm²'},
                                  calc_mode='values'):
    """ Returns all revolutioned paraboloid shell properties for any given set
    of inputs

    Args:
        r (float): Radius.
        d (float): Diameter.
        t (float): Thickness.
        P (float): Parameter.
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
           "P - (4*h**2+r**2)**1.5",
           "v - s*t",
           "m - rho*v",
           "s - ((pi*r)/(6*h**2))*(P-r**3)",
           "ix - ((m/(28*h**2))*((P*(12*h**4+6*r**2*h**2-r**4)+r**7)/(P-r**3))"
           "-(m/(100*h**2))*((P*(6*h**2-r**2)+r**5)/(P-r**3))**2)",
           "iy - ix",
           "iz - ((m*r**2)/(10*h**2))*((P*(6*h**2-r**2)+r**5)/(P-r**3))"]

    original_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'P': 'm³',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                      'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'd': 'm', 'h': 'm', 't': 'm', 'P': 'm³',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
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


def hollow_torus_sector(R=None, ro=None, ri=None, alpha=None, A=None, K=None,
                        t=None, ix=None, iy=None, iz=None, v=None, rho=None,
                        m=None, s=None,
                        units={'R': 'm', 'ro': 'm', 'ri': 'm', 'alpha': 'rad',
                               'A': 'm²', 'K': 'm²', 't': 'm', 'ix': 'kg·m²',
                               'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³',
                               'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                        calc_mode='values'):
    """ Returns all sector of a hollow torus properties for any given set
    of inputs

    Args:
        R (float): Radius.
        ro (float): Outer Radius.
        ri (float): Inner Radius.
        alpha (float): Angle.
        A (float): Parameter.
        K (float): Parameter.
        t (float): Thickness.
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
    eqs = ["A - (ro**2+ri**2)",
           "K - (2*(sin(alpha))**2/alpha)*(2*R**2+A+(A**2/(8*R**2)))",
           "v - 2*pi*R*alpha*(ro**2-ri**2)",
           "m - rho*v",
           "s - 4*pi*ro*R*alpha",
           "t - (ro-ri)",
           "ix - (m/(16*alpha))*(4*R**2*(2*alpha-sin(2*alpha))+A*(10*alpha-3*"
           "sin(2*alpha)))",
           "iy - (m/(16*alpha))*(4*R**2*(2*alpha+sin(2*alpha))+A*(10*alpha+3*"
           "sin(2*alpha))-4*K)",
           "iz - (m/(4*alpha))*(4*R**2*alpha+3*A*alpha-K)"]
    original_units = {'R': 'm', 'ro': 'm', 'ri': 'm', 'alpha': 'rad',
                      'A': 'm²', 'K': 'm²', 't': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'R': 'm', 'ro': 'm', 'ri': 'm', 'alpha': 'rad',
                     'A': 'm²', 'K': 'm²', 't': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'iz': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                     'm': 'kg', 's': 'm²'}
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
