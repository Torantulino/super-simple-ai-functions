import ast
import copy
import traceback


def convertExpr2Expression(Expr):
    Expr.lineno = 0
    Expr.col_offset = 0
    result = ast.Expression(Expr.value, lineno=0, col_offset=0)

    return result


def exec_with_return(code):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        expression = convertExpr2Expression(last_ast.body[0])
        compliedExpr = compile(expression, "<ast>", "eval")
        return eval(compliedExpr, globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"), globals())


def getSmallTrace() -> str:
    lines = traceback.format_exc().splitlines()
    return "\n".join(lines[-2:])
