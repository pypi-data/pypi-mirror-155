
from io import StringIO
from inspect import currentframe
import pxplore

def test_pxplore_print_names():
    pxplore.print_names(file=StringIO())


def test_pxplore_print_names_custom_frame():
    pxplore.print_names(file=StringIO(), frame=currentframe())


def test_pxplore_print_names_hidden():
    pxplore.print_names(file=StringIO(), show_hidden=True)


def test_pxplore_print_names_locals_only():
    pxplore.print_names(file=StringIO(), show_globals=False)


def test_pxplore_print_names_hidden_and_builtins():
    pxplore.print_names(file=StringIO(), show_hidden=True, show_builtins=False)


def test_pxplore_print_module_names():
    pxplore.print_module_names(pxplore, file=StringIO())


def test_pxplore_print_module_names_hidden():
    pxplore.print_module_names(pxplore, file=StringIO(), show_hidden=True)
