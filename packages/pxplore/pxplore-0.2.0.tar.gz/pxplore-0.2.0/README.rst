
::

  pip install pxplore

pxplore_ is a Python package providing a set of useful tools to explore
hidden details of the Python code.

.. _pxplore: https://github.com/pacesm/pxplore                                         

.. code-block:: python

 import pxplore

 # print names (variables, functions, classes ... etc.) in the current frame
 pxplore.print_names()

 # print names (variables, functions, classes ... etc.) contained by a module
 pxplore.print_module_names(pxplore)
