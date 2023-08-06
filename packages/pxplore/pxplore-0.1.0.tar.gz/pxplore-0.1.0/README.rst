
::

  pip install pxplore

pxplore_ is a Python package providing a set of useful tools to explore
hidden details of the Python code.

.. _pxplore: https://github.com/pacesm/pxplore                                         

.. code-block:: python

 import pxplore

 # print symbols in the current frame
 pxplore.print_symbols()

 # print symbols offered by a module
 pxplore.print_module_symbols(pxplore)
