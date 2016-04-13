import time
import ast
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython.core.magics.execution import _format_time
from IPython.utils.timing import clock


@magics_class
class MyTimeitMagics(Magics):
    @line_cell_magic
    def timeit2(self, line='', cell=None):

        import timeit

        opts, stmt = self.parse_options(line, 'n:r:gtcp:',
                                        posix=False, strict=False)
        if stmt == "" and cell is None:
            return

        timefunc = timeit.default_timer
        number = int(getattr(opts, "n", 0))
        repeat = int(getattr(opts, "r", timeit.default_repeat))
        precision = int(getattr(opts, "p", 3))
        if hasattr(opts, "t"):
            timefunc = time.time
        if hasattr(opts, "c"):
            timefunc = clock

        if hasattr(opts, "g"):
            timer = timeit.Timer(timer=timefunc, setup='gc.enable()')
        else:
            timer = timeit.Timer(timer=timefunc)
        # this code has tight coupling to the inner workings of timeit.Timer,
        # but is there a better way to achieve that the code stmt has access
        # to the shell namespace?
        transform = self.shell.input_splitter.transform_cell

        if cell is None:
            # called as line magic
            ast_setup = ast.parse("pass")
            ast_stmt = ast.parse(transform(stmt))
        else:
            ast_setup = ast.parse(transform(stmt))
            ast_stmt = ast.parse(transform(cell))

        ast_setup = self.shell.transform_ast(ast_setup)
        ast_stmt = self.shell.transform_ast(ast_stmt)

        # This codestring is taken from timeit.template - we fill it in as an
        # AST, so that we can apply our AST transformations to the user code
        # without affecting the timing code.
        timeit_ast_template = ast.parse('def inner(_it, _timer):\n'
                                        '    setup\n'
                                        '    _t0 = _timer()\n'
                                        '    for _i in _it:\n'
                                        '        stmt\n'
                                        '    _t1 = _timer()\n'
                                        '    return _t1 - _t0\n')

        class TimeitTemplateFiller(ast.NodeTransformer):
            "This is quite tightly tied to the template definition above."

            def visit_FunctionDef(self, node):
                "Fill in the setup statement"
                self.generic_visit(node)
                if node.name == "inner":
                    node.body[:1] = ast_setup.body

                return node

            def visit_For(self, node):
                "Fill in the statement to be timed"
                if getattr(getattr(node.body[0], 'value', None), 'id', None) == 'stmt':
                    node.body = ast_stmt.body
                return node

        timeit_ast = TimeitTemplateFiller().visit(timeit_ast_template)
        timeit_ast = ast.fix_missing_locations(timeit_ast)

        # Track compilation time so it can be reported if too long
        # Minimum time above which compilation time will be reported
        tc_min = 0.1

        t0 = clock()
        code = compile(timeit_ast, "<magic-timeit>", "exec")
        tc = clock() - t0

        ns = {}
        exec code in self.shell.user_ns, ns
        timer.inner = ns["inner"]

        if number == 0:
            # determine number so that 0.2 <= total time < 2.0
            number = 1
            for i in range(1, 10):
                if timer.timeit(number) >= 0.2:
                    break
                number *= 10

        result = timer.repeat(repeat, number)
        best = min(result) / number
        worst = max(result) / number
        avg = sum(result) / number / float(len(result))

        print u"{0} loops" \
              u"\n   AVG of {1}: {2:>5} per loop" \
              u"\n  BEST of {1}: {3:>5} per loop" \
              u"\n WORST of {1}: {4:>5} per loop".format(
                number, repeat,
                _format_time(avg, precision),
                _format_time(best, precision),
                _format_time(worst, precision)
        )
        if tc > tc_min:
            print "Compiler time: %.2f s" % tc


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(MyTimeitMagics)
