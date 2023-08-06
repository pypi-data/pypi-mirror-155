import sympy as sym
import itertools as it
from sympy.parsing.sympy_parser import parse_expr as parse_expr
from unitc import unit_conversion
import warnings


def valid_inputs(eqs):
    """ Returns what variables of the system of equations _eqs_ can potentially
    be used to uniquely solve all equations.

    The function recursively searches for clusters of _n_ equations with the
    same _n_ unknown variables and marks their variables as solvable. If all
    variables of the system of equations can be marked as solvable the set is
    returned as a valid input. MATHEMATICALLY NOT STRICTLY CORRECT!

    Args:
        eqs (list): list of strings. Each string defines an equation and should
            be given in the form LHS-RHS

    Returns:
        set: Set of frozen sets. Each frozen set is a possible
            combination of input variables to solve the whole system of
            equations.
    """
    symbolic_eqs = [sym.parsing.sympy_parser.parse_expr(eq) for eq in eqs]

    equation_vars = [eq.free_symbols for eq in symbolic_eqs]
    unique_vars = set().union(*equation_vars)

    n_eqs = len(eqs)
    n_vars = len(unique_vars)

    potential_sets = set(map(frozenset, it.combinations(
        unique_vars, n_vars - n_eqs)))

    input_sets = []
    for s in potential_sets:
        known_vars = s
        while known_vars != unique_vars:
            unknown_vars = list(map(frozenset, [eq_vars.difference(known_vars)
                                                for eq_vars in equation_vars]))
            new_known_vars = [i for i in set(unknown_vars)
                              if unknown_vars.count(i) == len(i)]
            if new_known_vars:
                known_vars = known_vars.union(*new_known_vars)
            else:
                s = None
                break
        input_sets.append(s)
    input_sets = set(input_sets)-{None}
    return input_sets


def eqs_solver(eqs, **kwargs):
    """ Solves the system of equations eqs with the variables contained in kwargs

    Args:
        eqs (list): list of strings. Each string defines an equation and should
            be given in the form LHS-RHS

        **kwargs: Initial values for all variables contained in eqs. Unknown
            variables are None, all other should have their value specified.
            For a variable <x>, the initial variable should be specified as
            <x>_i.

    Returns:
        dict: Dictionary with the values of all variables in eqs.
            Both known variables and calculated ones are given.

    TODO: What should be done when several solutions exist? Take the one with
    positive or real values?
    """
    symbolic_eqs = [parse_expr(eq) for eq in eqs]
    symbols = set().union(*[x.free_symbols for x in symbolic_eqs])
    known_symbols_dict = {str(x): kwargs[str(x)+"_i"] for x in symbols
                          if kwargs[str(x)+"_i"] is not None}
    unknown_symbols = [x for x in symbols if kwargs[str(x)+"_i"] is None]

    symbolic_sol = sym.solve(symbolic_eqs, *unknown_symbols)
    if type(symbolic_sol) is list:
        symbolic_sol = {k: v for k, v in zip(unknown_symbols, symbolic_sol[0])}

    try:
        result_dict = {
            **known_symbols_dict,
            **{str(x): symbolic_sol[x].subs(known_symbols_dict).evalf()
               for x in unknown_symbols}}
    except KeyError:
        known_symbols = symbols - set(unknown_symbols)
        all_valid_input_sets = valid_inputs(eqs)
        valid_input_sets = [x for x in valid_inputs(eqs)
                            if known_symbols.issubset(x)]
        if not valid_input_sets:
            raise ValueError('Invalid combination of input values.')
        else:
            # Calculate missing var ans set to zero
            missing_vars = set(valid_input_sets[0] - known_symbols)
            known_symbols_dict = {
                **{str(x): 0 for x in missing_vars},
                **known_symbols_dict}
            new_unknown_symbols = set(unknown_symbols) - missing_vars
            symbolic_sol = sym.solve(symbolic_eqs, *new_unknown_symbols)
            warnings.warn(f'Variables {missing_vars} were not specified.'
                          + ' They are set to be 0.')
            result_dict = {
                **known_symbols_dict,
                **{str(x): symbolic_sol[x].subs(known_symbols_dict).evalf()
                   for x in new_unknown_symbols}}

    return result_dict


def status_changed(status, priority, valid_input_sets):
    """ Chooses a new valid set of inputs according to the given current status
    and priority.

    Args:
        status (dict): dictionary with the status (bool) of all variables
        priority (list): list with all variables. Keeping the status of the
            last elements in the list has priority.
        valid_input_sets (set): set of sets. Each subset is one of the allowed
            input sets

    Returns:
        new_status (dict): dictionary with the new status of the variables

    """
    prio_weights_dict = {sym.sympify(i): 2**priority.index(i)
                         for i in priority}
    all_symbols = set(priority)
    valid_input_dicts = [{**{x: True for x in y},
                          **{x: False for x in all_symbols - y}}
                         for y in valid_input_sets]
    new_input_set = max(valid_input_dicts,
                        key=lambda x: sum([
                            prio_weights_dict[i]
                            for i in x.keys() if x[i] == status[i]]))
    return new_input_set


def dict_conv(args_dict, input_units, original_units, calc_type):
    """ Converts the values given in <args_dict> from the units in
        <input_units> to the ones in <original_units> renaming the keys
        appending "_i"
    """
    if calc_type == 'input':
        suffix = '_i'
    elif calc_type == 'output':
        suffix = ''
    else:
        raise ValueError('Unknown calculation type: ' + calc_type + '.')

    for i in ['units', 'calc_mode']:
        try:
            args_dict.pop(i)
        except Exception:
            pass

    solver_input = {}
    for i in original_units.keys():
        if args_dict[i] is not None:
            solver_input[i+suffix] = unit_conversion(
                args_dict[i], input_units[i], original_units[i])
        else:
            solver_input[i+suffix] = None
    return solver_input
