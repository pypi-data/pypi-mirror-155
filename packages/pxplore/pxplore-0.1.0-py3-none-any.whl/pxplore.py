"""
Various tools to explore hidden details of the Python code.
"""

from inspect import getframeinfo, currentframe

__version__ = "0.1.0"

# FIXME: Is there a less messy way how to print builtins?

# special which require special treatment when being printed
_BUILTINS_NONPRINTABLES = {
    "__builtins__",
    "quit",
    "exit",
    "copyright",
    "credits",
    "license",
    "help",
    "None",
    "Ellipsis",
    "NotImplemented",
    "False",
    "True",
}


def print_symbols(show_globals=True, show_hidden=False, show_builtins=False,
                  alignment="  ", frame=None, file=None):
    """ Print symbols of the callers frame and their values. """

    def _get_format_symbol(name):
        if name == "__builtins__":
            return _format_symbol_builtins
        return _format_symbol

    if not frame:
        frame = currentframe().f_back
    info = getframeinfo(frame)

    print(
        f"File \"{info.filename}\", line {info.lineno}, in {info.function}",
        file=file
    )

    if show_builtins:
        for name, value in frame.f_globals["__builtins__"].__dict__.items():
            if name in frame.f_locals or name in frame.f_globals:
                continue
            if not show_hidden and name.startswith("_"):
                continue
            print(f"{alignment}buildin: {_format_symbol_builtins(name, value)}", file=file)

    if show_globals:
        for name, value in frame.f_globals.items():
            if name in frame.f_locals:
                continue
            if not show_hidden and name.startswith("_"):
                continue
            format_symbol = _get_format_symbol(name)
            print(f"{alignment}global:  {format_symbol(name, value)}", file=file)

    for name, value in frame.f_locals.items():
        if not show_hidden and name.startswith("_"):
            continue
        format_symbol = _get_format_symbol(name)
        print(f"{alignment}local:   {format_symbol(name, value)}", file=file)


def print_module_symbols(module, show_hidden=False, alignment="  ", file=None):
    """ Print symbols of the given module and their values. """

    def _get_format_symbol(module_name, name):
        if module_name == 'builtins' or name == "__builtins__":
            return _format_symbol_builtins
        return _format_symbol

    print(module, file=file)
    module_name = module.__name__
    for name, value in module.__dict__.items():
        if not show_hidden and name.startswith("_"):
            continue
        format_symbol = _get_format_symbol(module_name, name)
        print(f"{alignment}{format_symbol(name, value)}", file=file)


def _format_symbol(name, value):
    return f"{name} = {value!r}"


def _format_symbol_builtins(name, value):
    if name in _BUILTINS_NONPRINTABLES:
        value = object.__repr__(value)
    else:
        value = repr(value)
    return f"{name} = {value}"
