from mauspaf.masslibrary.misc import eqs_solver, valid_inputs, dict_conv


def circular_rod(R=None, r=None, le=None, ix=None, iy=None, ip=None, v=None,
                 rho=None, m=None, s=None,
                 units={'r': 'm', 'R': 'm', 'le': 'm', 'ix': 'kg·m²',
                        'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³',
                        'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                 calc_mode='values'):
    """ Returns all circular rod properties for any given set of inputs

    Args:
        R (float): Radius.
        r (float): Rod radius.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "le - 2*pi*R",
           "s - 4*pi**2*r*R",
           "ix - m*R**2/2",
           "iy - ix",
           "ip - m*R**2"]

    original_units = {'r': 'm', 'R': 'm', 'le': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'R': 'm', 'le': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
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


def semi_circular_rod(R=None, r=None, le=None, ix=None, iy=None, ip=None,
                      v=None, rho=None, m=None, s=None,
                      units={'r': 'm', 'R': 'm', 'le': 'm', 'ix': 'kg·m²',
                             'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³',
                             'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                      calc_mode='values'):
    """ Returns all semi circular rod properties for any given set of inputs

    Args:
        R (float): Radius.
        r (float): Rod radius.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "le - pi*R",
           "s - 2*pi**2*r*R",
           "ix - 0.0947*m*R**2",
           "iy - 0.5*m*R**2",
           "ip - 0.5947*m*R**2"]

    original_units = {'r': 'm', 'R': 'm', 'le': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'R': 'm', 'le': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
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


def segment_circular_rod(R=None, r=None, alpha=None, le=None, ix=None, iy=None,
                         ip=None, v=None, rho=None, m=None, s=None,
                         units={'r': 'm', 'R': 'm', 'alpha': 'rad', 'le': 'm',
                                'ix': 'kg·m²', 'iy': 'kg·m²', 'ip': 'kg·m²',
                                'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                                's': 'm²'},
                         calc_mode='values'):
    """ Returns all segment of a circular rod properties for any given set of
    inputs

    Args:
        R (float): Radius.
        r (float): Rod radius.
        alpha (float): Angle.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "le - 2*R*alpha",
           "s - 4*pi*r*R*alpha",
           "ix - m*R**2*(0.5-((sin(alpha)*cos(alpha))/(2*alpha)))",
           "iy - m*R**2*(0.5+((sin(alpha)*cos(alpha))/(2*alpha))-(sin(alpha)"
           "**2/alpha**2))",
           "ip - m*R**2*(1-(sin(alpha)**2/alpha**2))"]

    original_units = {'r': 'm', 'R': 'm', 'alpha': 'rad', 'le': 'm',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³',
                      'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'R': 'm', 'alpha': 'rad', 'le': 'm',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³',
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


def straight_rod(r=None, le=None, ix=None, iy=None, ip=None, v=None, rho=None,
                 m=None, s=None,
                 units={'r': 'm', 'le': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²',
                        'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                        's': 'm²'},
                 calc_mode='values'):
    """ Returns all straight rod properties for any given set of inputs

    Args:
        r (float): Rod radius.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "s - le*2*pi*r",
           "ix - 0",
           "iy - m*le**2/12",
           "ip - iy"]

    original_units = {'r': 'm', 'le': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²',
                      'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                      's': 'm²'}
    default_units = {'r': 'm', 'le': 'm', 'ix': 'kg·m²', 'iy': 'kg·m²',
                     'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³', 'm': 'kg',
                     's': 'm²'}
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


def elliptic_rod(r=None, a=None, b=None, le=None, ix=None, iy=None, ip=None,
                 v=None, rho=None, m=None, s=None,
                 units={'r': 'm', 'a': 'm', 'b': 'm', 'le': 'm', 'ix': 'kg·m²',
                        'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³',
                        'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                 calc_mode='values'):
    """ Returns all elliptic rod properties for any given set of inputs

    Args:
        r (float): Rod radius.
        a (float): Semi axis in x-direction.
        b (float): Semi axis in y-direction.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "s - le*2*pi*r",
           "le - (pi/(32*a**3))*(45*a**4+22*a**2*b**2-3*b**4)",
           "ix - (m*b**2*(55*a**4+10*a**2*b**2-b**4))/(2*(45*a**4+22*a**2*"
           "b**2-3*b**4))",
           "iy - (m*a**2*(35*a**4+34*a**2*b**2-5*b**4))/(2*(45*a**4+22*a**2*"
           "b**2-3*b**4))",
           "ip - (ix+iy)"]

    original_units = {'r': 'm', 'a': 'm', 'b': 'm', 'le': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'a': 'm', 'b': 'm', 'le': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
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


# PARABOLIC ROD: TOO SLOW!!
#
# def parabolic_rod(r=None, a=None, b=None, le=None, ix=None, iy=None, ip=None,
#                   v=None, rho=None, m=None, s=None,
#                   units={'r': 'm', 'a': 'm', 'b': 'm', 'le': 'm',
#                          'ix': 'kg·m²', 'iy': 'kg·m²', 'ip': 'kg·m²',
#                          'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
#                   calc_mode='values'):
#     """ Returns all parabolic rod properties for any given set of inputs

#     Args:
#         r (float): Rod radius.
#         a (float): Semi axis in x-direction.
#         b (float): Semi axis in y-direction.
#         le (float): Rod length.
#         ix (float): Moment of inertia about x axis.
#         iy (float): Moment of inertia about y axis.
#         ip (float): Polar moment of inertia.
#         v (float): Volume.
#         rho (float): Density.
#         m (float): Mass.
#         s (float): Surface area.
#         calc_mode (str): Calculation mode. Either 'values' (to calculate
#             missing numerical values) or 'sets' (to calculate valid input sets
#             of variables). Default value is 'values'.
#     """
#     eqs = ["v - le*pi*r**2",
#            "m - rho*v",
#            "le - ((4*a**2+b**2)**0.5+(b**2/(2*a))*log((2*a+(4*a**2+b**2)**0.5)"
#            "/b))",
#            "s - le*2*pi*r",
#            "ix - ((m*b**2)/(8*a**2))*((4*a**2+b**2)**1.5/le-b**2/2)",
#            "iy - (m*(4*a**2+b**2)**1.5/(12*le)-(ix/8)-m*(((4*a**2+b**2)**1.5)/"
#            "(8*a*le)-(b**2/(16*a)))**2)",
#            "ip - (ix+iy)"]
#     if calc_mode == 'values':
#         result = eqs_solver(eqs, r_i=r, a_i=a, b_i=b, le_i=le, ix_i=ix,
#                             iy_i=iy, ip_i=ip, v_i=v, rho_i=rho, m_i=m, s_i=s)
#     elif calc_mode == 'sets':
#         result = valid_inputs(eqs)
#     else:
#         raise ValueError('Unknown calculation mode ' + calc_mode)
#     return result

#     original_units = {'r': 'm', 'a': 'm', 'b': 'm', 'le': 'm', 'ix': 'kg·m²',
#                       'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
#                       'm': 'kg', 's': 'm²'}
#     default_units = {'r': 'm', 'a': 'm', 'b': 'm', 'le': 'm', 'ix': 'kg·m²',
#                      'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
#                      'm': 'kg', 's': 'm²'}
#     used_units = {**default_units, **units}

#     solver_input = dict_conv(locals(), used_units, original_units, 'input')

#     if calc_mode == 'values':
#         eq_res = eqs_solver(eqs, **solver_input)
#         result = dict_conv(eq_res, original_units,
#                            used_units, 'output')
#     elif calc_mode == 'sets':
#         result = valid_inputs(eqs)
#     else:
#         raise ValueError('Unknown calculation mode ' + calc_mode)
#     return result


def u_rod(r=None, l1=None, l2=None, le=None, ix=None, iy=None, ip=None,
          v=None, rho=None, m=None, s=None,
          units={'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                 'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                 'm': 'kg', 's': 'm²'},
          calc_mode='values'):
    """ Returns all u-rod properties for any given set of inputs

    Args:
        r (float): Rod radius.
        l1 (float): Length in y-direction.
        l2 (float): Length in x-direction.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "le - (l1+2*l2)",
           "s - le*2*pi*r",
           "ix - (m*l1**2*(l1+6*l2))/(12*(l1+2*l2))",
           "iy - (m*l2**3*(2*l1+l2))/(3*(l1+2*l2)**2)",
           "ip - (ix+iy)"]

    original_units = {'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
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


def rectangular_rod(r=None, l1=None, l2=None, le=None, ix=None, iy=None,
                    ip=None, v=None, rho=None, m=None, s=None,
                    units={'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm',
                           'ix': 'kg·m²', 'iy': 'kg·m²', 'ip': 'kg·m²',
                           'v': 'm³', 'rho': 'kg/m³', 'm': 'kg', 's': 'm²'},
                    calc_mode='values'):
    """ Returns all rectangular rod properties for any given set of inputs

    Args:
        r (float): Rod radius.
        l1 (float): Length in y-direction.
        l2 (float): Length in x-direction.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "le - 2*(l1+l2)",
           "s - le*2*pi*r",
           "ix - (m*l1**2*(l1+3*l2))/(12*(l1+l2))",
           "iy - (m*l2**2*(3*l1+l2))/(12*(l1+l2))",
           "ip - (ix+iy)"]

    original_units = {'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
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


def v_rod(r=None, l1=None, alpha=None, le=None, ix=None, iy=None, ip=None,
          v=None, rho=None, m=None, s=None,
          units={'r': 'm', 'l1': 'm', 'alpha': 'rad', 'le': 'm', 'ix': 'kg·m²',
                 'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                 'm': 'kg', 's': 'm²'},
          calc_mode='values'):
    """ Returns all v-rod properties for any given set of inputs

    Args:
        r (float): Rod radius.
        l1 (float): Length of one side.
        alpha (float): Angle.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "le - 2*l1",
           "s - le*2*pi*r",
           "ix - m*l1**2/3*cos(alpha)**2",
           "iy - m*l1**2/12*sin(alpha)**2",
           "ip - (ix+iy)"]

    original_units = {'r': 'm', 'l1': 'm', 'alpha': 'rad', 'le': 'm',
                      'ix': 'kg·m²', 'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³',
                      'rho': 'kg/m³', 'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'l1': 'm', 'alpha': 'rad', 'le': 'm',
                     'ix': 'kg·m²', 'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³',
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


def l_rod(r=None, l1=None, l2=None, le=None, ix=None, iy=None, ip=None, v=None,
          rho=None, m=None, s=None,
          units={'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                 'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                 'm': 'kg', 's': 'm²'},
          calc_mode='values'):
    """ Returns all l-rod properties for any given set of inputs

    Args:
        r (float): Rod radius.
        l1 (float): Length in y-direction.
        l2 (float): Length in x-direction.
        le (float): Rod length.
        ix (float): Moment of inertia about x axis.
        iy (float): Moment of inertia about y axis.
        ip (float): Polar moment of inertia.
        v (float): Volume.
        rho (float): Density.
        m (float): Mass.
        s (float): Surface area.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input sets
            of variables). Default value is 'values'.
    """
    eqs = ["v - le*pi*r**2",
           "m - rho*v",
           "le - (l1+l2)",
           "s - le*2*pi*r",
           "ix - (m/12)*(l1**3*(l1+4*l2))/(l1+l2)**2",
           "iy - (m/12)*(l2**3*(4*l1+l2))/(l1+l2)**2",
           "ip - (ix+iy)"]

    original_units = {'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                      'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
                      'm': 'kg', 's': 'm²'}
    default_units = {'r': 'm', 'l1': 'm', 'l2': 'm', 'le': 'm', 'ix': 'kg·m²',
                     'iy': 'kg·m²', 'ip': 'kg·m²', 'v': 'm³', 'rho': 'kg/m³',
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
