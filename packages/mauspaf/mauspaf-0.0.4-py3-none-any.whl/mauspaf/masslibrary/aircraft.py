from mauspaf.masslibrary.misc import eqs_solver, valid_inputs, dict_conv


def ga_wing_raymer(ar=None, mdg=None, mf=None, nz=None, phi=None,
                   qc=None, s=None, tc=None, tr=None, mw=None,
                   units={'ar': None, 'mdg': 'kg', 'mf': 'kg', 'nz': None,
                          'phi': 'rad', 'qc': 'Pa', 's': 'm²', 'tc': None,
                          'tr': None, 'mw': 'kg'},
                   calc_mode='values'):
    """ Returns all wing properties for any given set of inputs using
        Raymer's GA wing mass estimating function.

    Args:
        ar (float): Aspect ratio.
        mdg (float): Design gross mass.
        mf (float): Mass of fuel in wing.
        nz (float): Ultimate load factor.
        phi (float): Wing sweep at 25% MAC.
        qc (float): Dynamic pressure in cruise.
        s (float): Surface area.
        tc (float): Thickness to chord ratio.
        tr (float): Taper ratio.
        mw (float): Wing mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mw - 0.036*s**0.758*mf**0.0035*(ar/cos(phi)**2)**0.6*qc**0.006"
           "*tr**0.04*(100*tc/cos(phi))**(-0.3)*(nz*mdg)**0.49"]
    original_units = {'ar': None, 'mdg': 'lb', 'mf': 'lb', 'nz': None,
                      'phi': 'rad', 'qc': 'lbf/ft²', 's': 'ft²', 'tc': None,
                      'tr': None, 'mw': 'lb'}
    default_units = {'ar': None, 'mdg': 'kg', 'mf': 'kg', 'nz': None,
                     'phi': 'rad', 'qc': 'Pa', 's': 'm²', 'tc': None,
                     'tr': None, 'mw': 'kg'}
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


def ga_wing_nicolai(ar=None, mdg=None, nz=None, phi=None,
                    s=None, tc=None, tr=None, vh=None, mw=None,
                    units={'ar': None, 'mdg': 'kg', 'nz': None, 'phi': 'rad',
                           's': 'm²', 'tc': None, 'tr': None, 'vh': 'm/s',
                           'mw': 'kg'},
                    calc_mode='values'):
    """ Returns all wing properties for any given set of inputs using
        Nicolai's GA wing mass estimating function.

    Args:
        ar (float): Aspect ratio.
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        phi (float): Wing sweep at 25% MAC.
        s (float): Surface area.
        tc (float): Thickness to chord ratio.
        tr (float): Taper ratio.
        mw (float): Wing mass.
        vh (float): maximum level airspeed
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mw - 96.948*((nz*mdg/10**5)**0.65*(ar/cos(phi)**2)**0.57*"
           "(s/100)**0.61*((1+tr)/(2*tc)**0.36*(1+vh/500)**0.5))**0.993"]
    original_units = {'ar': None, 'mdg': 'lb', 'nz': None, 'phi': 'rad',
                      's': 'ft²', 'tc': None, 'tr': None, 'vh': 'kt',
                      'mw': 'lb'}
    default_units = {'ar': None, 'mdg': 'kg', 'nz': None, 'phi': 'rad',
                     's': 'm²', 'tc': None, 'tr': None, 'vh': 'm/s',
                     'mw': 'kg'}
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


def ga_horizontal_tail_raymer(ar=None, mdg=None, nz=None, phi=None, qc=None,
                              s=None, tc=None, tr=None, mht=None,
                              units={'ar': None, 'mdg': 'kg', 'nz': None,
                                     'phi': 'rad', 's': 'm²', 'tc': None,
                                     'tr': None, 'mht': 'kg'},
                              calc_mode='values'):
    """ Returns all horizontal tail properties for any given set of inputs
    using Raymer's GA horizontal tail mass estimating function

    Args:
        ar (float): Aspect ratio.
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        phi (float): horizontal tail sweep at 25% MAC.
        s (float): Surface area.
        tc (float): Thickness to chord ratio.
        tr (float): Taper ratio.
        mht (float): horizontal tail mass.
        qc (float): Dynamic pressure in cruise.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mht - 0.016*(nz*mdg)**0.414*qc**0.168*s**0.896*((100*tc)/"
           "cos(phi))**(-0.12)*(ar/cos(phi)**2)**0.043*tr**(-0.02)"]
    original_units = {'ar': None, 'mdg': 'lb', 'nz': None, 'phi': 'rad',
                      'qc': 'lbf/ft²', 's': 'ft²', 'tc': None, 'tr': None,
                      'mht': 'lb'}
    default_units = {'ar': None, 'mdg': 'kg', 'nz': None, 'phi': 'rad',
                     'qc': 'Pa', 's': 'm²', 'tc': None, 'tr': None,
                     'mht': 'kg'}
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


def ga_horizontal_tail_nicolai(bht=None, lht=None, mdg=None, nz=None,
                               s=None, tht=None, mht=None,
                               units={'bht': 'm', 'lht': 'm', 'mdg': 'kg',
                                      'nz': None, 's': 'm²', 'tht': 'm',
                                      'mht': 'kg'},
                               calc_mode='values'):
    """ Returns all horizontal tail properties for any given set of inputs
    using Nicolai's GA horizontal tail mass estimating function.

    Args:
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        s (float): Surface area.
        mht (float): horizontal tail mass.
        lht (float): horizontal tail arm, from C/4 to HT C/4
        bht (float): HT span
        tht (float): max root chorf thickness
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mht - 127*((nz*mdg/(10**5))**0.87*(s/100)**1.2*(lht/10)**0.483*"
           "(bht/tht)**0.5)**0.458"]
    original_units = {'bht': 'ft', 'lht': 'ft', 'mdg': 'lb', 'nz': None,
                      's': 'ft²', 'tht': 'in', 'mht': 'lb'}
    default_units = {'bht': 'm', 'lht': 'm', 'mdg': 'kg', 'nz': None,
                     's': 'm²', 'tht': 'm', 'mht': 'kg'}
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


def ga_vertical_tail_raymer(ar=None, F=None, mdg=None, nz=None, phi=None,
                            qc=None, s=None, tc=None, tr=None, mvt=None,
                            units={'ar': None, 'F': None,  'mdg': 'kg',
                                   'nz': None, 'phi': 'rad', 'qc': 'Pa',
                                   's': 'm²', 'tc': None, 'tr': None,
                                   'mvt': 'kg'},
                            calc_mode='values'):
    """ Returns all vertical tail properties for any given set of inputs using
    Raymer's GA vertical tail mass estimating function.

    Args:
        ar (float): Vertical tail aspect ratio
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        s (float): Surface area.
        mvt (float): vertical tail mass.
        tc (float): Thickness to chord ratio.
        tr (float): Taper ratio.
        qc (float): Dynamic pressure in cruise.
        phi (float): vertical tail sweep at 25% MAC.
        F (float): 0 for conventional tail, 1 fot T-tail.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mvt - 0.073*(1+0.2*F)*(nz*mdg)**0.376*qc**0.122*s**0.873*(100*tc/"
           "cos(phi))**(-0.49)*(ar/cos(phi)**2)**0.357*tr**0.039"]
    original_units = {'ar': None, 'F': None,  'mdg': 'lb', 'nz': None,
                      'phi': 'rad', 'qc': 'lbf/ft²', 's': 'ft²', 'tc': None,
                      'tr': None, 'mvt': 'lb'}
    default_units = {'ar': None, 'F': None,  'mdg': 'kg', 'nz': None,
                     'phi': 'rad', 'qc': 'Pa', 's': 'm²', 'tc': None,
                     'tr': None, 'mvt': 'kg'}
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


def ga_vertical_tail_nicolai(bvt=None, mdg=None, nz=None, s=None, tvt=None,
                             mvt=None,
                             units={'bvt': 'm', 'mdg': 'kg', 'nz': None,
                                    's': 'm²', 'tvt': 'm', 'mvt': 'kg'},
                             calc_mode='values'):
    """ Returns all vertical tail properties for any given set of inputs using
    Nicolai's GA vertical tail mass estimating function.

    Args:
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        s (float): Surface area.
        mvt (float): vertical tail mass.
        bvt (float): Vertical tail span.
        tvt (float): max root chord thickness.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mvt - 98.5*(((nz*mdg/(10**5))**0.87*(s/100)**1.2*(bvt/tvt)**0.5))"]
    original_units = {'bvt': 'ft', 'mdg': 'lb', 'nz': None, 's': 'ft²',
                      'tvt': 'in', 'mvt': 'lb'}
    default_units = {'bvt': 'm', 'mdg': 'kg', 'nz': None, 's': 'm²',
                     'tvt': 'm', 'mvt': 'kg'}
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


def ga_fuselage_raymer(dp=None, dfs=None, lfs=None, lht=None, mdg=None,
                       nz=None, s=None, qc=None, vp=None, mfs=None,
                       units={'dp': 'Pa', 'dfs': 'm', 'lfs': 'm', 'lht': 'm',
                              'mdg': 'kg', 'nz': None, 's': 'm²', 'qc': 'Pa',
                              'vp': 'm³', 'mfs': 'kg'},
                       calc_mode='values'):
    """ Returns all fuselage properties for any given set of inputs using
    Raymer's GA fuselage mass estimating function.

    Args:
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        s (float): fuselage wetted area.
        mfs (float): fuselage mass.
        lht (float): horizontal tail arm, from C/4 to HT C/4.
        lfs (float): lenght of fuselage structure.
        dfs (float): depth of fuselage structure.
        qc (float): Dynamic pressure in cruise.
        vp (float): Volume of pressurized cabin section.
        dp (float): cabin pressure differential.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mfs - (0.052*s**1.086*(nz*mdg)**0.177*lht**(-0.051)*"
           "(lfs/dfs)**(-0.072)*qc**0.241+(11.9*(vp*dp)**0.271))"]
    original_units = {'dp': 'psi', 'dfs': 'ft', 'lfs': 'ft', 'lht': 'ft',
                      'mdg': 'lb', 'nz': None, 's': 'ft²', 'qc': 'lbf/ft²',
                      'vp': 'ft³', 'mfs': 'lb'}
    default_units = {'dp': 'Pa', 'dfs': 'm', 'lfs': 'm', 'lht': 'm',
                     'mdg': 'kg', 'nz': None, 's': 'm²', 'qc': 'Pa',
                     'vp': 'm³', 'mfs': 'kg'}
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


def ga_fuselage_nicolai(df=None, lf=None, mdg=None, nz=None,
                        vh=None, wf=None, mfs=None,
                        units={'df': 'm', 'lf': 'm', 'mdg': 'kg', 'nz': None,
                               'vh': 'm/s', 'wf': 'm', 'mfs': 'kg'},
                        calc_mode='values'):
    """ Returns all fuselage properties for any given set of inputs using
    Nicolai's GA fuselage mass estimating function.

    Args:
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        lf (float): Fuselage lenght.
        mfs (float): Fuselage mass.
        wf (float): Fuselage max width.
        df (float): Fuselage max depth.
        vh (float): Maximum level airspeed.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mfs - 200*((nz*mdg/(10**5))**0.286*(lf/10)**0.857*((wf+df)/10)*"
           "(vh/100)**0.338)**1.1"]
    original_units = {'df': 'ft', 'lf': 'ft', 'mdg': 'lb', 'nz': None,
                      'vh': 'kt', 'wf': 'ft', 'mfs': 'lb'}
    default_units = {'df': 'm', 'lf': 'm', 'mdg': 'kg', 'nz': None,
                     'vh': 'm/s', 'wf': 'm', 'mfs': 'kg'}
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


def ga_main_landing_gear_raymer(lm=None, ml=None, nl=None, mlg=None,
                                units={'lm': 'm', 'ml': 'kg', 'nl': None,
                                       'mlg': 'kg'},
                                calc_mode='values'):
    """ Returns all main landing gear properties for any given set of inputs
    using Raymer's GA main landing gear mass estimating function.

    Args:
        ml (float): Design landing weight.
        nl (float): Ultimate landing load factor.
        lm (float): Lenght of main landing gear structure.
        mlg (float): main landing gear mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mlg - 0.095*(nl*ml)**0.768*(lm/12)**0.409"]
    original_units = {'lm': 'ft', 'ml': 'lb', 'nl': None, 'mlg': 'lb'}
    default_units = {'lm': 'm', 'ml': 'kg', 'nl': None, 'mlg': 'kg'}
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


def ga_main_landing_gear_nicolai(lm=None, ml=None, nl=None, mmnlg=None,
                                 units={'lm': 'm', 'ml': 'kg', 'nl': None,
                                        'mmnlg': 'kg'},
                                 calc_mode='values'):
    """ Returns all main landing gear properties for any given set of input
    using Nicolai's GA entire landing gear mass estimating function.

    Args:
        ml (float): Design landing weight.
        nl (float): Ultimate landing load factor.
        lm (float): Lenght of main landing gear structure.
        mmnlg (float): entire landing gear mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mmnlg - 0.054*(nl*ml)**0.684*(lm/12)**0.601"]
    original_units = {'lm': 'in', 'ml': 'lb', 'nl': None, 'mmnlg': 'lb'}
    default_units = {'lm': 'm', 'ml': 'kg', 'nl': None, 'mmnlg': 'kg'}
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


def ga_nose_landing_gear_raymer(l_n=None, ml=None, nl=None, mnlg=None,
                                units={'l_n': 'm', 'ml': 'kg', 'nl': None,
                                       'mnlg': 'kg'},
                                calc_mode='values'):
    """ Returns all nose landing gear properties for any given set of inputs
    using Raymer's GA nose landing gear mass estimating function.

    Args:
        ml (float): Design landing weight.
        nl (float): Ultimate landing load factor.
        ln (float): Lenght of nose landing gear structure.
        mnlg (float): nose landing gear mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mnlg - 0.125*(nl*ml)**0.566*(l_n/12)**0.845"]
    original_units = {'l_n': 'in', 'ml': 'lb', 'nl': None, 'mnlg': 'lb'}
    default_units = {'l_n': 'm', 'ml': 'kg', 'nl': None, 'mnlg': 'kg'}
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


def ga_installed_engine_raymer(meng=None, neng=None, mei=None,
                               units={'meng': 'kg', 'neng': None, 'mei': 'kg'},
                               calc_mode='values'):
    """ Returns all installed engine properties for any given set of inputs
    using Raymer's GA installed engine mass estimating function.

    Args:
        mei (float): installed engine mass.
        meng (float): uninstalled engine mass.
        neng (float): number of engines.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mei - 2.575*meng**0.922*neng"]
    original_units = {'meng': 'lb', 'neng': None, 'mei': 'lb'}
    default_units = {'meng': 'kg', 'neng': None, 'mei': 'kg'}
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


def ga_installed_engine_nicolai(
        meng=None, neng=None, mei=None,
        units={'meng': 'kg', 'neng': None, 'mei': 'kg'},
        calc_mode='values'):
    """ Returns all installed engine properties for any given set of inputs
    using Nicolai's GA installed engine mass estimating function.

    Args:
        mei (float): installed engine mass.
        meng (float): uninstalled engine mass.
        neng (float): number of engines.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mei - 2.575*meng**0.922*neng"]
    original_units = {'meng': 'lb', 'neng': None, 'mei': 'lb'}
    default_units = {'meng': 'kg', 'neng': None, 'mei': 'kg'}
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


def ga_fuel_system_raymer(
        neng=None, ntank=None, qint=None, qtot=None, mfsy=None,
        units={'neng': None, 'ntank': None, 'qint': 'm³',
               'qtot': 'm³', 'mfsy': 'kg'},
        calc_mode='values'):
    """ Returns all fuel system properties for any given set of inputs using
    Raymer's GA fuel system mass estimating function.

    Args:
        mfsy (float): fuel system mass.
        qtot (float): total fuel quantity.
        qint (float): fuel quantity in integral fuel tanks.
        ntank (float): number of fuel tanks.
        neng (float): number of engines.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mfsy -2.49*qtot**0.726*(qtot/(qtot+qint))**0.363*ntank**0.242*"
           "neng**0.157"]
    original_units = {'neng': None, 'ntank': None, 'qint': 'gal',
                      'qtot': 'gal', 'mfsy': 'lb'}
    default_units = {'neng': None, 'ntank': None, 'qint': 'm³', 'qtot': 'm³',
                     'mfsy': 'kg'}
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


def ga_fuel_system_nicolai(
        neng=None, ntank=None, qint=None, qtot=None, mfsy=None,
        units={'neng': None, 'ntank': None, 'qint': 'm³',
               'qtot': 'm³', 'mfsy': 'kg'},
        calc_mode='values'):
    """ Returns all fuel system properties for any given set of inputs using
    Nicolai's GA fuel system mass estimating function.

    Args:
        mfsy (float): fuel system mass.
        qtot (float): total fuel quantity.
        qint (float): fuel quantity in integral fuel tanks.
        ntank (float): number of fuel tanks.
        neng (float): number of engines.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mfsy -2.49*((qtot**0.6*(qtot/(qtot+qint))**0.3*ntank**0.2*"
           "neng**0.13)**1.21)"]
    original_units = {'neng': None, 'ntank': None, 'qint': 'gal',
                      'qtot': 'gal', 'mfsy': 'lb'}
    default_units = {'neng': None, 'ntank': None, 'qint': 'm³', 'qtot': 'm³',
                     'mfsy': 'kg'}
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


def ga_flight_control_system_raymer(
        b=None, lfs=None, mdg=None, nz=None, mctrl=None,
        units={'b': 'm', 'lfs': 'm', 'mdg': 'kg',
               'nz': None, 'mctrl': 'kg'},
        calc_mode='values'):
    """ Returns all flight control system properties for any given set of
    inputs using Raymer's GA flight control system mass estimating function.

    Args:
        mdg (float): Design gross mass.
        nz (float): Ultimate load factor.
        b (float): wing span.
        lfs (float): lenght of fuselage structure.
        mctrl (float): flight control system mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mctrl - 0.053*lfs**1.536*b**0.371*(nz*mdg*10**(-4))**0.8"]
    original_units = {'b': 'ft', 'lfs': 'ft', 'mdg': 'lb', 'nz': None,
                      'mctrl': 'lb'}
    default_units = {'b': 'm', 'lfs': 'm', 'mdg': 'kg', 'nz': None,
                     'mctrl': 'kg'}
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


def ga_flight_control_system_nicolai(mdg=None, mctrl=None, ctrlsys='manual',
                                     units={'mdg': 'kg', 'mctrl': 'kg'},
                                     calc_mode='values'):
    """ Returns all flight control system properties for any given set of
    inputs using Nicolai's GA flight control system mass estimating function.

    Args:
        mdg (float): Design gross mass.
        mctrl (float): flight control system mass.
        ctrlsys (float): 'powered' for powered control systems, 'manual' for
            manual control systems.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    if ctrlsys == 'powered':
        eqs = ["mctrl - 1.08*mdg**0.7"]
    elif ctrlsys == 'manual':
        eqs = ["mctrl - 1.066*mdg**0.626"]
    else:
        raise ValueError('Unknown control system type ' + ctrlsys)
    original_units = {'mdg': 'lb', 'mctrl': 'lb'}
    default_units = {'mdg': 'kg', 'mctrl': 'kg'}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('ctrlsys')
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


def ga_hydraulic_system_raymer(mdg=None, mhyd=None,
                               units={'mdg': 'kg', 'mhyd': 'kg'},
                               calc_mode='values'):
    """ Returns all hydraulic system properties for any given set of inputs
    using Raymer's GA hydraulic system mass estimating function.

    Args:
        mdg (float): Design gross mass.
        mhyd (float): hydraulic system mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mhyd - 0.001*mdg"]
    original_units = {'mdg': 'lb', 'mhyd': 'lb'}
    default_units = {'mdg': 'kg', 'mhyd': 'kg'}
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


def ga_avionics_system_raymer(muav=None, mav=None,
                              units={'muav': 'kg', 'mav': 'kg'},
                              calc_mode='values'):
    """ Returns all avionics system properties for any given set of inputs
    using Raymer's GA avionics system mass estimating function.

    Args:
        muav (float): uninstalled avionics mass.
        mav (float): installed avionics mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mav - 2.117*muav**0.933"]
    original_units = {'muav': 'lb', 'mav': 'lb'}
    default_units = {'muav': 'kg', 'mav': 'kg'}
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


def ga_avionics_system_nicolai(muav=None, mav=None,
                               units={'muav': 'kg', 'mav': 'kg'},
                               calc_mode='values'):
    """ Returns all avionics system properties for any given set of inputs
    using Nicolai's GA avionics system mass estimating function.

    Args:
        muav (float): uninstalled avionics mass.
        mav (float): installed avionics mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mav - 2.117*muav**0.933"]
    original_units = {'muav': 'lb', 'mav': 'lb'}
    default_units = {'muav': 'kg', 'mav': 'kg'}
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


def ga_electrical_system_raymer(mav=None, mfsy=None, mel=None,
                                units={'mav': 'kg', 'mfsy': 'kg', 'mel': 'kg'},
                                calc_mode='values'):
    """ Returns all electrical system properties for any given set of inputs
    using Raymer's GA electrical system mass estimating function.

    Args:
        mav (float): installed avionics mass.
        mfsy (float): flight control system mass.
        mel (float): electrical system mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mel - 12.57*(mfsy+mav)**0.51"]
    original_units = {'mav': 'lb', 'mfsy': 'lb', 'mel': 'lb'}
    default_units = {'mav': 'kg', 'mfsy': 'kg', 'mel': 'kg'}
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


def ga_electrical_system_nicolai(
        mav=None, mfsy=None, mel=None,
        units={'mav': 'kg', 'mfsy': 'kg', 'mel': 'kg'},
        calc_mode='values'):
    """ Returns all electrical system properties for any given set of inputs
    using Nicolai's GA electrical system mass estimating function.

    Args:
        mav (float): installed avionics mass.
        mfsy (float): flight control system mass.
        mel (float): electrical system mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mel - 12.57*(mfsy+mav)**0.51"]
    original_units = {'mav': 'lb', 'mfsy': 'lb', 'mel': 'lb'}
    default_units = {'mav': 'kg', 'mfsy': 'kg', 'mel': 'kg'}
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


def ga_air_conditioning_anti_ice_raymer(
        mach=None, mav=None, mdg=None, nocc=None, mac=None,
        units={'mach': None, 'mav': 'kg', 'mdg': 'kg',
               'nocc': None, 'mac': 'kg'},
        calc_mode='values'):
    """ Returns all air conditioning and anti-icing properties for any given
    set of inputs using Raymer's GA air conditioning and anti-icing mass
    estimating function.

    Args:
        mav (float): installed avionics mass.
        mdg (float): Design gross mass.
        mach (float): machach number.
        nocc (float): number of occupants.
        mac (float): Ac and anti-icing mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mac - 0.265*mdg**0.52*nocc**0.68*mav**0.17*mach**0.08"]
    original_units = {'mach': None, 'mav': 'lb', 'mdg': 'lb', 'nocc': None,
                      'mac': 'lb'}
    default_units = {'mach': None, 'mav': 'kg', 'mdg': 'kg', 'nocc': None,
                     'mac': 'kg'}
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


def ga_air_conditioning_anti_ice_nicolai(
        mach=None, mav=None, mdg=None, nocc=None, mac=None,
        units={'mach': None, 'mav': 'kg', 'mdg': 'kg',
               'nocc': None, 'mac': 'kg'},
        calc_mode='values'):
    """ Returns all air conditioning and anti-icing properties for any given
    set of inputs using Nicolai's GA air conditioning and anti-icing mass
    estimating function.

    Args:
        mav (float): installed avionics mass.
        mdg (float): Design gross mass.
        mach (float): machach number.
        nocc (float): number of occupants.
        mac (float): Ac and anti-icing mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mac - 0.265*mdg**0.52*nocc**0.68*mav**0.17*mach**0.08"]
    original_units = {'mach': None, 'mav': 'lb', 'mdg': 'lb', 'nocc': None,
                      'mac': 'lb'}
    default_units = {'mach': None, 'mav': 'kg', 'mdg': 'kg', 'nocc': None,
                     'mac': 'kg'}
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


def ga_furnishings_raymer(mdg=None, mfurn=None,
                          units={'mdg': 'kg', 'mfurn': 'kg'},
                          calc_mode='values'):
    """ Returns all furnishings properties for any given set of inputs using
       Raymer's GA furnishings mass estimating function.

    Args:
        mdg (float): Design gross mass.
        mfurn (float): furnishings mass.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mfurn - ((0.0582*mdg)-65)"]
    original_units = {'mdg': 'lb', 'mfurn': 'lb'}
    default_units = {'mdg': 'kg', 'mfurn': 'kg'}
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


def ga_furnishings_nicolai(ncrew=None, qh=None, mfurn=None,
                           units={'ncrew': None, 'qh': 'Pa', 'mfurn': 'kg'},
                           calc_mode='values'):
    """ Returns all furnishings properties for any given set of inputs using
    Nicolai's GA furnishings mass estimating function.

    Args:
        mfurn (float): furnishings mass.
        ncrew (float): number of crew.
        qh (float): dynamic pressure at max level airspeed
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.

    """
    eqs = ["mfurn - 34.5*ncrew*qh**0.25"]
    original_units = {'ncrew': None, 'qh': 'lbf/ft²', 'mfurn': 'lb'}
    default_units = {'ncrew': None, 'qh': 'Pa', 'mfurn': 'kg'}
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


def wing_mass_howe(mwing=None, mc=None, mr=None, ar=None, s=None, tr=None,
                   phi=None, tc=None, theta=None, fa=None, m0=None, n=None,
                   r=None, mzw=None, ni=None, conf=None, composite=False,
                   kcomp=None,
                   units={'mwing': 'kg', 'mc': 'kg', 'mr': 'kg', 'ar': None,
                          's': 'm²', 'tr': None, 'phi': 'rad', 'tc': None,
                          'theta': 'rad', 'fa': 'MPa', 'm0': None, 'n': None,
                          'r': None, 'mzw': 'kg', 'ni': None, 'kcomp': None},
                   calc_mode='values'):
    """Returns the mass of a wing based on the formula by Howe.

    Args:
        mwing (float): Wing mass.
        mc (float): Structural box covers mass.
        mr (float): Spanwise shear webs mass.
        ar (float): Aspect ratio.
        s (float): Wing area.
        tr (float): Taper ratio.
        phi (float): Quarter chord sweep.
        tc (float): Thickness to chord ratio.
        theta (float): Sweep of the structure.
        fa (float): Allowable working stress of the material.
        m0 (float): Take-off mass of the aircraft.
        n (float): Ultimate design factor.
        r (float): Factor which allows inertial relief dependant on wing
                   confuiguration.
        conf (float): '1' for no wing-mounted powerplant or stores.
                      '2' for two wing-mounted powerplants.
                      '3' for four wing-mounted powerplants.
        mzw (float): Design zero fuel mass.
        ni (float): Manoeuvre factor.
        kcomp (float): Factor for correction in case of composite material.
        composite (boolean): 'False': no composite. 'True': composite.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.
    """
    if conf == 1:
        eqs = ["mwing - kcomp*(mc+mr)*m0",
               "mc - 1920*ar**1.5*s**0.5*n*r*(1+tr)*(cos(phi)*cos(theta)*tc)"
               "**(-1)*fa",
               "mr - ((3*s**1.25*tc**0.5)/(m0*ar**0.25))*((1-0.34*tr+0.44*tr"
               "**2)+2.2*tc*(s/ar)**0.5*(1-tr+0.72*tr**2))",
               "fa - 1.12*((n*r*ar**1.75*m0)/(s**0.75*tc**1.5)*(1+tr)**2.5*"
               "(cos(phi)*cos(theta))**(-1))**0.5*10**5",
               "n - 1.65*ni",
               "r - (1-(0.12+(1-(mzw/m0))))"]
    elif conf == 2:
        eqs = ["mwing - kcomp*(mc+mr)*m0",
               "mc - 1920*ar**1.5*s**0.5*n*r*(1+tr)*(cos(phi)*cos(theta)*tc)"
               "**(-1)*fa"
               "mr - ((3*s**1.25*tc**0.5)/(m0*ar**0.25))*((1-0.34*tr+0.44*tr"
               "**2)+2.2*tc*(s/ar)**0.5*(1-tr+0.72*tr**2))",
               "fa - 1.12*((n*r*ar**1.75*m0)/(s**0.75*tc**1.5)*(1+tr)**2.5*"
               "(cos(phi)*cos(theta))**(-1))**0.5*10**5",
               "n - 1.65*ni",
               "r - (1-(0.2+(1-(mzw/m0))))"]
    elif conf == 3:
        eqs = ["mwing - kcomp*(mc+mr)*m0",
               "mc - 1920*ar**1.5*s**0.5*n*r*(1+tr)*(cos(phi)*cos(theta)*tc)"
               "**(-1)*fa"
               "mr - ((3*s**1.25*tc**0.5)/(m0*ar**0.25))*((1-0.34*tr+0.44*tr"
               "**2)+2.2*tc*(s/ar)**0.5*(1-tr+0.72*tr**2))",
               "fa - 1.12*((n*r*ar**1.75*m0)/(s**0.75*tc**1.5)*(1+tr)**2.5*"
               "(cos(phi)*cos(theta))**(-1))**0.5*10**5",
               "n - 1.65*ni",
               "r - (1-(0.22+(1-(mzw/m0))))"]
    else:
        raise ValueError('Unknown wing configuration ' + conf)
    if not composite:
        eqs += ["kcomp - 1"]
    elif composite:
        eqs += ["kcomp - 0.85"]
    original_units = {'mwing': 'kg', 'mc': 'kg', 'mr': 'kg', 'ar': None,
                      's': 'm²', 'tr': None, 'phi': 'rad', 'tc': None,
                      'theta': 'rad', 'fa': 'MPa', 'm0': None, 'n': None,
                      'r': None, 'mzw': 'kg', 'ni': None, 'kcomp': None}
    default_units = {'mwing': 'kg', 'mc': 'kg', 'mr': 'kg', 'ar': None,
                     's': 'm²', 'tr': None, 'phi': 'rad', 'tc': None,
                     'theta': 'rad', 'fa': 'MPa', 'm0': None, 'n': None,
                     'r': None, 'mzw': 'kg', 'ni': None, 'kcomp': None}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('conf', 'composite')
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


def structural_mass_torenbeek(ms=None, mtow=None, ks=None, nult=None, bf=None,
                              hf=None, lf=None, kcomp=None, composite=None,
                              units={'ms': 'kg', 'mtow': 'kg', 'nult': None,
                                     'bf': 'm', 'hf': 'm', 'lf': 'm',
                                     'kcomp': None},
                              calc_mode='values'):
    """Returns the structural weight of an aircraft according to Torenbeek.

    Args:
        ms (float): Structural weight.
        mtow (float): Maximum take-off weight.
        nult (float): Ultimate load factor.
        bf (float): Fuselage width.
        hf (float): Fuselage heigth.
        lf (float): Fuselage length.
        kcomp (float): Factor for correction in case of composite material.
        composite (boolean): 'False': no composite. 'True': composite.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.
    """
    eqs = ["ms - kcomp*mtow*(0.447*nult**0.5*(bf*hf*lf/mtow)**0.24)"]
    if not composite:
        eqs += ["kcomp - 1"]
    elif composite:
        eqs += ["kcomp - 0.85"]
    original_units = {'ms': 'kg', 'mtow': 'kg', 'nult': None, 'bf': 'm',
                      'hf': 'm', 'lf': 'm', 'kcomp': None}
    default_units = {'ms': 'kg', 'mtow': 'kg', 'nult': None, 'bf': 'm',
                     'hf': 'm', 'lf': 'm', 'kcomp': None}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('composite')
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


def wing_mass_torenbeek(mw=None, mtow=None, kw=None, bs=None, b=None,
                        nult=None, tr=None, s=None, ar=None, phi=None,
                        kcomp=None, composite=None,
                        units={'mw': 'kg', 'mtow': 'kg', 'kw': None, 'bs': 'm',
                               'b': 'm', 'nult': None, 'tr': 'm', 's': 'm²',
                               'phi': 'rad', 'kcomp': None},
                        calc_mode='values'):
    """Wing mass estimation according to Torenbeek.

    Args:
        mw (float): Wing mass.
        mtow (float): Maximum take-off weight.
        kw (float): Factor.
        bs (float): Structural wing span.
        b (float): Wing span.
        nult (float): Ultimate load factor.
        tr (float): Maximum root thickness.
        s (float): Surface area.
        ar (float): Aspect ratio.
        phi (float): Half chord sweep angle (structural sweep angle).
        kcomp (float): Factor for correction in case of composite material.
        composite (boolean): 'False': no composite. 'True': composite.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.
    """
    # TODO: Take units into account when deciding which equation to take.
    # TODO: Remove kcomp from input variables and substitute it before passing
    #     the equation string to the solver.
    # TODO: Substitute kw from the equations as well.
    # TODO: Add further factors as given in reference (e.g. 2% increase for
    #     spoilers and speed brakes, 5% decrease for two wing-mounted engines,
    #     10% decrease for 4 wing-mounted engines, 30% decrease for strutted
    #     wings).
    if mtow <= 5670:
        eqs = ["mw - kcomp*mtow*(kw*bs**0.75*(1+(1.905/bs)**0.5)*nult**0.55*"
               "((bs/tr)/(mtow/s))**0.3)",
               "bs - b/cos(phi)",
               "kw - (4.9*10**(-3))"]
    else:
        eqs = ["mw - kcomp*mtow*(kw*bs**0.75*(1+(1.905/bs)**0.5)*nult**0.55*"
               "((bs/tr)/(mtow/s))**0.3)",
               "bs - b/cos(phi)",
               "kw - (6.67*10**(-3))"]
    if not composite:
        eqs += ["kcomp - 1"]
    elif composite:
        eqs += ["kcomp - 0.85"]
    original_units = {'mw': 'kg', 'mtow': 'kg', 'kw': None, 'bs': 'm',
                      'b': 'm', 'nult': None, 'tr': 'm', 's': 'm²',
                      'phi': 'rad', 'kcomp': None}
    default_units = {'mw': 'kg', 'mtow': 'kg', 'kw': None, 'bs': 'm',
                     'b': 'm', 'nult': None, 'tr': 'm', 's': 'm²',
                     'phi': 'rad', 'kcomp': None}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('composite')
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


def tailplane_mass_torenbeek(mtail=None, nult=None, stail=None, kcomp=None,
                             composite=None,
                             units={'mtail': 'kg', 'nult': None, 'stail': 'm²',
                                    'kcomp': None},
                             calc_mode='values'):
    """Tailplane mass estimation according to Torenbeek.

    Args:
        mtail (float): Tailplane mass.
        nult (float): Ultimate load factor.
        stail (float): Surface area.
        kcomp (float): Factor for correction in case of composite material.
        composite (boolean): 'False': no composite. 'True': composite.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.
    """
    eqs = ["mtail - kcomp*0.64*(nult*stail**2)**0.75"]
    if not composite:
        eqs += ["kcomp - 1"]
    elif composite:
        eqs += ["kcomp - 0.85"]
    original_units = {'mtail': 'kg', 'nult': None, 'stail': 'm²',
                      'kcomp': None}
    default_units = {'mtail': 'kg', 'nult': None, 'stail': 'm²',
                     'kcomp': None}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('composite')
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


def fuselage_torenbeek(mf=None, vd=None, lt=None, bf=None, hf=None, sg=None,
                       kcomp=None, composite=None,
                       units={'mf': 'kg', 'vd': 'm/s', 'lt': 'm', 'bf': 'm',
                              'hf': 'm', 'sg': 'm²', 'kcomp': None},
                       calc_mode='values'):
    """Returns the estimated fuselage mass by Torenbeek.

    Args:
        mf (float): Fuselage mass.
        vd (float): Design dive speed.
        lt (float): Defined length (not the total length of the fuselage).
        bf (float): Fuselage width.
        hf (float): Fuselage height.
        sg (float): Gross shell area.
        kcomp (float): Factor for correction in case of composite material.
        composite (boolean): 'False': no composite. 'True': composite.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.
    """
    eqs = ["mf - kcomp*0.23*(vd*lt/(bf+hf))**0.5*sg**1.2"]
    if not composite:
        eqs += ["kcomp - 1"]
    elif composite:
        eqs += ["kcomp - 0.85"]
    original_units = {'mf': 'kg', 'vd': 'm/s', 'lt': 'm', 'bf': 'm',
                      'hf': 'm', 'sg': 'm²', 'kcomp': None}
    default_units = {'mf': 'kg', 'vd': 'm/s', 'lt': 'm', 'bf': 'm',
                     'hf': 'm', 'sg': 'm²', 'kcomp': None}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('composite')
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


def landing_gear_torenbeek(mlg=None, mtow=None, a=None, b=None, c=None,
                           d=None, conf=None, kcomp=None, composite=None,
                           units={'mlg': 'kg', 'mtow': 'kg', 'a': None,
                                  'b': None, 'c': None, 'd': None,
                                  'kcomp': None},
                           calc_mode='values'):
    """Returns the estimated landing gear weight by Torenbeek.

    Args:
        mlg (float): Landing gear mass.
        mtow (float): Maximum take-off weight.
        a (float): Factor given in a table.
        b (float): Factor given in a table.
        c (float): Factor given in a table.
        d (float): Factor given in a table.
        conf (float): 'low' for low-wing configuration. 'high' for high-wing
                      configuration.
        kcomp (float): Factor for correction in case of composite material.
        composite (boolean): 'False': no composite. 'True': composite.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.
    """
    if conf == 'low':
        eqs = ["mlg - kcomp*(a+b*mtow**0.75+c*mtow+d*mtow**1.5)"]
    elif conf == 'high':
        eqs = ["mlg - kcomp*1.08*(a+b*mtow**0.75+c*mtow+d*mtow**1.5)"]
    else:
        raise ValueError('Unknown wing configuration ' + conf)
    if not composite:
        eqs += ["kcomp - 1"]
    elif composite:
        eqs += ["kcomp - 0.85"]
    original_units = {'mlg': 'kg', 'mtow': 'kg', 'a': None, 'b': None,
                      'c': None, 'd': None, 'kcomp': None}
    default_units = {'mlg': 'kg', 'mtow': 'kg', 'a': None, 'b': None,
                     'c': None, 'd': None, 'kcomp': None}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('conf', 'composite')
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


def surface_controls_torenbeek(msc=None, mtow=None, ksc=None, kcomp=None,
                               composite=None,
                               units={'msc': 'kg', 'mtow': 'kg', 'ksc': None,
                                      'kcomp': None},
                               calc_mode='values'):
    """Returns estimated weight of the surface controls by Torenbeek.

    Args:
        msc (float): Surface controls mass.
        mtow (float): Maximum take-off weight.
        ksc (float): Factor.
        kcomp (float): Factor for correction in case of composite material.
        composite (boolean): 'False': no composite. 'True': composite.
        units (dict): Dictionary with units of every variable. Default value
            is all SI-units.
        calc_mode (str): Calculation mode. Either 'values' (to calculate
            missing numerical values) or 'sets' (to calculate valid input
            sets of variables). Default value is 'values'.
    """
    eqs = ["msc - kcomp*ksc*mtow**(2/3)"]
    if not composite:
        eqs += ["kcomp - 1"]
    elif composite:
        eqs += ["kcomp - 0.85"]
    original_units = {'msc': 'kg', 'mtow': 'kg', 'ksc': None, 'kcomp': None}
    default_units = {'msc': 'kg', 'mtow': 'kg', 'ksc': None, 'kcomp': None}
    used_units = {**default_units, **units}

    used_locals = locals()
    used_locals.pop('composite')
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
