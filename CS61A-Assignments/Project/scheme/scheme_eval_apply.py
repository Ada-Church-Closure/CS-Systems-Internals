import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

# 在给定的环境下计算表达式
# expr就是string已经被解析成了pair对象
def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        # 找到和这个名称对应的value
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    # 把第一个元素拿出来查找看是不是特殊的形式
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        # 怎么实现调用一个本地的方法
        # 先获取操作符
        procedure = scheme_eval(expr.first, env)
        
        # 对于剩下的操作数进行求值
        # 就是说我想用map创建expr的深拷贝,用lambda函数
        args = expr.map(lambda x : x)
        args = args.rest
        curr_arg = args
        while curr_arg != nil:
            # 对于每个operand都要进行循环的eval求值
            curr_arg.first = scheme_eval(curr_arg.first, env)
            curr_arg = curr_arg.rest

        # 最后用apply求值
        result = scheme_apply(procedure, args, env)
        return result
        # END PROBLEM 3

# 把过程应用于一些参数
# 用户定义的procedure要创建新的frame,但是built-in的不需要
# 用户定义的还要计算body中的多余的表达式
def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
       # 如果是内置的过程
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        arg_list = []
        curr = args
        while curr != nil:
            arg_list.append(curr.first)
            curr = curr.rest

        if procedure.need_env:
            arg_list.append(env)
        
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            result = procedure.py_func(*arg_list)
            return result
            # 如果参数的数量发生错误,就raise下面的Error
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # 我们怎么调用我们定义的lambda来计算
        # 注意这里的调用一定是用procedure的env来调用,而不是我们当前的env,否则绑定到全局帧了就是扯淡
        child_frame = procedure.env.make_child_frame(procedure.formals, args)
        result = eval_all(procedure.body, child_frame)
        return result
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        # 一个动态的作用域
        # 注意这个env就不是调用时候的procedure,而是我们当前的procedure
        child_frame = env.make_child_frame(procedure.formals, args)
        result = eval_all(procedure.body, child_frame)
        return result
        # END PROBLEM 11
    elif isinstance(procedure, EnumerateProcedure):
        index = len(args) - 1
        curr = []
        while args != nil:
            curr.append(args.first)
            args = args.rest
        
        curr.reverse()
        num = 0
        lst = nil
        while index >= 0:
            item = Pair(index, curr[num])
            lst = Pair(item, lst)
            index -= 1
            num += 1
        
        return lst

    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    # 主要是实现了begin语句的功能
    # 计算每个表达式.然后返回最后一个
    curr = expressions
    if curr == nil:
        return None
    while curr != nil:
        value = scheme_eval(curr.first, env)
        curr = curr.rest
    return value
    # END PROBLEM 6

################################
# Extra Credit: Tail Recursion #
################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
