import builtins

from pair import *

class SchemeError(Exception):
    """Exception indicating an error in a Scheme program."""

################
# Environments #
################

# 代表了一个环境帧 

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        # bindings字典,把一个scheme的symbo(py中是string表示)和value绑定起来
        self.bindings = {}
        # 父帧,全局帧的父帧是None
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    # bindings进行绑定,在我这个帧中
    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 1
        self.bindings[symbol] = value
        # END PROBLEM 1

    # 从我当前的这个frame开始往parent的frame进行查找,找到并且返回这个value
    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 1
        curr = self
        while curr != None:
            for key, value in curr.bindings.items():
                if key == symbol:
                    return curr.bindings[key]
            curr = curr.parent
        # END PROBLEM 1
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    # 创建一个子帧
    # 当调用一个用户定义的procedure的时候,创建一个frame
    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Both FORMALS and VALS are represented
        as Pairs. Raise an error if too many or too few vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        if len(formals) != len(vals):
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 8
        # 把创建的value和名称进行一一绑定即可
        child_frame = Frame(self)
        symbol = formals
        value = vals
        while symbol != nil:
            child_frame.define(symbol.first, value.first)
            symbol = symbol.rest
            value = value.rest
        return child_frame
        # END PROBLEM 8

##############
# Procedures #
##############

class Procedure:
    """The the base class for all Procedure classes."""

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, py_func, need_env=False, name='builtin'):
        self.name = name
        self.py_func = py_func
        self.need_env = need_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

# 用户自己定义的过程
class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))

class EnumerateProcedure(Procedure):
    """
    Returns the enumaration of a list...
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return '#[enumerate]'
    
    def __repr__(self):
        return 'EnumerateProcedure()'
    
