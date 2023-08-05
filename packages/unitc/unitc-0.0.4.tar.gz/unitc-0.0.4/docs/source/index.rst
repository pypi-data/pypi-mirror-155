.. unitc documentation master file, created by
   sphinx-quickstart on Tue Apr  5 13:18:12 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to unitc's documentation!
=================================

**unitc** is a simple Python 3 module to perform conversions between measurement units.


.. code:: python

    >>> from unitc import unit_conversion
    # Convert 1 kg to pounds
    >>> unit_conversion(1, 'kg', 'lb')
    2.204623
    >>> unit_conversion(1, from_unit='kg', to_unit='lb')
    2.204623
    
    # If the conversion is done to or from SI units, they don't need to be specified explicitely
    >>> unit_conversion(1, 'ft')  # Converts 1 ft to m
    0.3047999902464003
    >>> unit_conversion(1, to_unit='HP') # Converts 1 W to horse power (HP)
    0.001341022

    # Unit conversion works also with lists and arrays
    >>> a = [1, 2, 3, 4, 5]
    >>> unit_conversion(a, 'kPa', 'lbf/ft²')
    array([ 20.88543648,  41.77087296,  62.65630944,  83.54174592, 104.42718239])

    >>> b = np.array([2, 5, 8, 7])
    >>> unit_conversion(b, 'kt', 'm/s')
    array([1.02888947, 2.57222367, 4.11555787, 3.60111313])
    
    # Input units can be specified in the input value as a string
    >>> unit_conversion('4 g/cm³', to_unit='lb/in³')
    0.14450917891460638


   
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   units
   avail


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
