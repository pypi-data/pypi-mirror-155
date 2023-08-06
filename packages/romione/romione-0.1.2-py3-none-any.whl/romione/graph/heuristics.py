import sympy as sp


def complexity(expr, tgt_symbols):
    r"""Heuristics based complexity estimation to prioritize equations for 
    solving in terms of target symbols."""

    value = 0
    if tgt_symbols:
        # represent tgt_symbols with a single identifier symbol x_
        # (Probably not a great heauristic for now)
        x_ = sp.Symbol("x_")
        if tgt_symbols != (x_,):
            expr = expr.subs({s: x_ for s in tgt_symbols})

        # collect powers of x_ in the polynomial terms in the eqn
        poly_terms = sp.collect(expr, x_, evaluate=False)
        
        # non_poly terms are gathered to 1
        expr = poly_terms.get(1)
        if expr:
            poly_terms.pop(1)

            if x_ in expr.free_symbols:
                # replace any function with an identity function
                # (Probably not a great heauristic for now)
                expr = expr.replace(
                    lambda expr: expr.is_Function, 
                    lambda expr: expr.args[0], # just take the argument and return it
                )

                value += complexity(expr, (x_,))

        if poly_terms:
            # get the highest polynomial power/exponent. 
            # args of a polynomial terms is of the form of (base, exponent)
            value += max(1 if term == x_ else term.args[1] for term in poly_terms)

    return value