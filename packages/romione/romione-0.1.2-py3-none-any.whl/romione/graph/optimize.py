import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


def get_stationary_data(fn, symbol="infer"):
    r"""Get stationary point of the fn w.r.t a symbol.
    If symbol is infer, fn should only contain one symbol."""

    if isinstance(fn, str):
        fn = parse_expr(fn)
    if symbol != "infer" and isinstance(symbol, str):
        symbol = sp.Symbol(symbol)

    symbols = fn.free_symbols
    if symbol == "infer":
        assert len(symbols) == 1, f"Multiple symbols ({symbols}) present in "\
            f"function ({fn}). Specify the symbol w.r.t which stationary "\
            "point is to be obtained."

        symbol = next(iter(symbols))

    stationary_fn = fn.diff(symbol)
    stationary_points = sp.solve(stationary_fn, symbol)

    return symbol, stationary_fn, stationary_points

def get_minima_or_maxima_data(fn, symbol="infer", allow_expr_return=True, for_minima=True):
    r"""Get points, fn values and condition for minima or maxima for the fn 
    w.r.t a symbol. If symbol is infer, fn should only contain one symbol.
    allow_expr_return is set to be True if the minima or maxima points are to be 
    left in terms of other symbols and the value of minima or maxima are to be 
    obtained by substituting their value by the caller."""

    if isinstance(fn, str):
        fn = parse_expr(fn)

    symbol, stationary_fn, stationary_points = get_stationary_data(fn, symbol)
    stationary_fn_diffs = [
        stationary_fn.diff(symbol).subs(symbol, p) for p in stationary_points
    ]

    relational_type = sp.core.relational.Relational

    points, fn_values, conditions = [], [], []
    for point, expr in zip(stationary_points, stationary_fn_diffs):
        
        check = expr > 0 if for_minima else expr < 0
        
        if ((allow_expr_return and isinstance(check, relational_type)) or 
            (not isinstance(check, relational_type) and check)):
            
            conditions.append(check)
            points.append(point)
            fn_values.append(fn.subs(symbol, point))

    return symbol, points, fn_values, conditions


def maximize(fn, symbol="infer", allow_expr_return=True):
    r"""Get maxima points, maxima and maxima conditions for the fn w.r.t a symbol. 
    If symbol is infer, fn should only contain one symbol.
    allow_expr_return is set to be True if the maxima points are to be 
    left in terms of other symbols and the value of the maxima are to be 
    obtained by substituting their value by the caller."""

    symbol, maxima_points, maxima, maxima_conditions = get_minima_or_maxima_data(
        fn, symbol, allow_expr_return, for_minima=False,
    )
    return symbol, maxima_points, maxima, maxima_conditions


def minimize(fn, symbol="infer", allow_expr_return=True):
    r"""Get minima points, minima and minima conditions for the fn w.r.t a symbol. 
    If symbol is infer, fn should only contain one symbol.
    allow_expr_return is set to be True if the minima points are to be 
    left in terms of other symbols and the value of the minima are to be 
    obtained by substituting their value by the caller."""

    symbol, minima_points, minima, minima_conditions = get_minima_or_maxima_data(
        fn, symbol, allow_expr_return, for_minima=True,
    )
    return symbol, minima_points, minima, minima_conditions