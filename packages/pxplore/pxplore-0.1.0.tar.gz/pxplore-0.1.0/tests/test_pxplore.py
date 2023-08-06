
from io import StringIO
from inspect import currentframe
import pxplore
help(pxplore)

def test_pxplore_print_symbols():
    pxplore.print_symbols(file=StringIO())


def test_pxplore_print_symbols_custom_frame():
    pxplore.print_symbols(file=StringIO(), frame=currentframe())


def test_pxplore_print_symbols_hidden():
    pxplore.print_symbols(file=StringIO(), show_hidden=True)


def test_pxplore_print_symbols_locals_only():
    pxplore.print_symbols(file=StringIO(), show_globals=False)


def test_pxplore_print_symbols_hidden_and_builtins():
    pxplore.print_symbols(file=StringIO(), show_hidden=True, show_builtins=False)


def test_pxplore_print_module_symbols():
    pxplore.print_module_symbols(pxplore, file=StringIO())


def test_pxplore_print_module_symbols_hidden():
    pxplore.print_module_symbols(pxplore, file=StringIO(), show_hidden=True)
