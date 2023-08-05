# Contributing

# Initial settings - How to run the program with python
A virtual environment is not strictly needed but recommended. The default path for the virtual environment is `.\venv-unitc`.

## Linux

1. Create environment: `python3 -m venv venv-unitc`
2. Activate environment: `source venv-unitc/bin/activate` 
3. Install usage dependencies: `python3 -m pip install -r requirements/req.txt`
4. If you want regenerate the documentation, generate wheels or publish on pypi, install further dependencies: `python3 -m pip install -r requirements/dev.txt`

# Coding style
For the coding style, [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines should be used. This includes, among others, the following:

- maximum line length of 79 characters

# Testing
The following checks are run every time commits are pushed to the Gitlab server:

- `pylint`
- `pytest`
- `flake8`

## Flake8
**Flake8** checks if the code complies with [PEP 8](https://www.python.org/dev/peps/pep-0008/). To run it locally:

    python3 -m flake8 ./src/unitc

If it doesn't find any errors, the output should be empty. In certain files (see for example `__init__.py`) it can be of interest to skip the checks. This can be made adding a line stating `# flake8: noqa` somewhere at the beginnig of the file.

Flake8 should always run without errors.

## Pylint
**Pylint** is another code syntax checker. According to their own [definition](https://github.com/PyCQA/pylint), it is a *Python static code analysis tool which looks for programming errors, helps enforcing a coding standard, sniffs for code smells and offers simple refactoring suggestions.*

Before commiting and pushing any changes you should run it and fix the code if necessary.


## Pytest
Testing the functionality of the program is performed using the module `pytest`. For each module file `<file>.py` in `~/src/unitc/` a script named `~/tests/test_<file>.py` should be created. This script tests the functions defined in `<file>.py`.

To run all module tests, the following command should be executed from the upper directory:

    python3 -m pytest tests

A single file (e.g. `test_unitc.py`) with tests can be executed in a similar way:

    python -m pytest tests/test_unitc.py


# Documentation
The documentation is created with [Sphinx](http://www.sphinx-doc.org/en/master/contents.html).

`Sphinx` is a documentation generator for python which converts [reStructuredText](http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) into a user defined format such as *PDF* or *HTML*.

To generate the documentation, enter the doc folder and run `make`

    cd ./doc && make clean && make html
	
The generated html documentation can be read opening the file `./doc/_build/index.html`.


# Docstrings
Google style doctrings should be used. Example taken from the [docs](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html):

    # -*- coding: utf-8 -*-
    """Example Google style docstrings.
    
    This module demonstrates documentation as specified by the `Google Python
    Style Guide`_. Docstrings may extend over multiple lines. Sections are created
    with a section header and a colon followed by a block of indented text.
    
    Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::
    
    $ python example_google.py
    
    Section breaks are created by resuming unindented text. Section breaks
    are also implicitly created anytime a new section starts.
    
    Attributes:
    module_level_variable1 (int): Module level variables may be documented in
    either the ``Attributes`` section of the module docstring, or in an
    inline docstring immediately following the variable.
    
    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.
    
    Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension
    
    .. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html
    
    """
    
    module_level_variable1 = 12345
    
    module_level_variable2 = 98765
    """int: Module level variable documented inline.
    
    The docstring may span multiple lines. The type may optionally be specified
    on the first line, separated by a colon.
    """
    
    
    def function_with_types_in_docstring(param1, param2):
    """Example function with types documented in the docstring.
    
    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:
    
    Args:
    param1 (int): The first parameter.
    param2 (str): The second parameter.
    
    Returns:
    bool: The return value. True for success, False otherwise.
    
    .. _PEP 484:
    https://www.python.org/dev/peps/pep-0484/
    
    """
    
    
    def function_with_pep484_type_annotations(param1: int, param2: str) -> bool:
    """Example function with PEP 484 type annotations.
    
    Args:
    param1: The first parameter.
    param2: The second parameter.
    
    Returns:
    The return value. True for success, False otherwise.
    
    """
    
    
    def module_level_function(param1, param2=None, *args, **kwargs):
    """This is an example of a module level function.
    
    Function parameters should be documented in the ``Args`` section. The name
    of each parameter is required. The type and description of each parameter
    is optional, but should be included if not obvious.
    
    If \*args or \*\*kwargs are accepted,
    they should be listed as ``*args`` and ``**kwargs``.
    
    The format for a parameter is::
    
    name (type): description
    The description may span multiple lines. Following
    lines should be indented. The "(type)" is optional.
    
    Multiple paragraphs are supported in parameter
    descriptions.
    
    Args:
    param1 (int): The first parameter.
    param2 (:obj:`str`, optional): The second parameter. Defaults to None.
    Second line of description should be indented.
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.
    
    Returns:
    bool: True if successful, False otherwise.
    
    The return type is optional and may be specified at the beginning of
    the ``Returns`` section followed by a colon.
    
    The ``Returns`` section may span multiple lines and paragraphs.
    Following lines should be indented to match the first line.
    
    The ``Returns`` section supports any reStructuredText formatting,
    including literal blocks::
    
    {
    'param1': param1,
    'param2': param2
    }
    
    Raises:
    AttributeError: The ``Raises`` section is a list of all exceptions
    that are relevant to the interface.
    ValueError: If `param2` is equal to `param1`.
    
    """
    if param1 == param2:
    raise ValueError('param1 may not be equal to param2')
    return True
    
    
    def example_generator(n):
    """Generators have a ``Yields`` section instead of a ``Returns`` section.
    
    Args:
    n (int): The upper limit of the range to generate, from 0 to `n` - 1.
    
    Yields:
    int: The next number in the range of 0 to `n` - 1.
    
    Examples:
    Examples should be written in doctest format, and should illustrate how
    to use the function.
    
    >>> print([i for i in example_generator(4)])
    [0, 1, 2, 3]
    
    """
    for i in range(n):
    yield i
    
    
    class ExampleError(Exception):
    """Exceptions are documented in the same way as classes.
    
    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.
    
    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.
    
    Note:
    Do not include the `self` parameter in the ``Args`` section.
    
    Args:
    msg (str): Human readable string describing the exception.
    code (:obj:`int`, optional): Error code.
    
    Attributes:
    msg (str): Human readable string describing the exception.
    code (int): Exception error code.
    
    """
    
    def __init__(self, msg, code):
    self.msg = msg
    self.code = code
    
    
    class ExampleClass(object):
    """The summary line for a class docstring should fit on one line.
    
    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).
    
    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.
    
    Attributes:
    attr1 (str): Description of `attr1`.
    attr2 (:obj:`int`, optional): Description of `attr2`.
    
    """
    
    def __init__(self, param1, param2, param3):
    """Example of docstring on the __init__ method.
    
    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.
    
    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.
    
    Note:
    Do not include the `self` parameter in the ``Args`` section.
    
    Args:
    param1 (str): Description of `param1`.
    param2 (:obj:`int`, optional): Description of `param2`. Multiple
    lines are supported.
    param3 (:obj:`list` of :obj:`str`): Description of `param3`.
    
    """
    self.attr1 = param1
    self.attr2 = param2
    self.attr3 = param3  #: Doc comment *inline* with attribute
    
    #: list of str: Doc comment *before* attribute, with type specified
    self.attr4 = ['attr4']
    
    self.attr5 = None
    """str: Docstring *after* attribute, with type specified."""
    
    @property
    def readonly_property(self):
    """str: Properties should be documented in their getter method."""
    return 'readonly_property'
    
    @property
    def readwrite_property(self):
    """:obj:`list` of :obj:`str`: Properties with both a getter and setter
    should only be documented in their getter method.
    
    If the setter method contains notable behavior, it should be
    mentioned here.
    """
    return ['readwrite_property']
    
    @readwrite_property.setter
    def readwrite_property(self, value):
    value
    
    def example_method(self, param1, param2):
    """Class methods are similar to regular functions.
    
    Note:
    Do not include the `self` parameter in the ``Args`` section.
    
    Args:
    param1: The first parameter.
    param2: The second parameter.
    
    Returns:
    True if successful, False otherwise.
    
    """
    return True
    
    def __special__(self):
    """By default special members with docstrings are not included.
    
    Special members are any methods or attributes that start with and
    end with a double underscore. Any special member with a docstring
    will be included in the output, if
    ``napoleon_include_special_with_doc`` is set to True.
    
    This behavior can be enabled by changing the following setting in
    Sphinx's conf.py::
    
    napoleon_include_special_with_doc = True
    
    """
    pass
    
    def __special_without_docstring__(self):
    pass
    
    def _private(self):
    """By default private members are not included.
    
    Private members are any methods or attributes that start with an
    underscore and are *not* special. By default they are not included
    in the output.
    
    This behavior can be changed such that private members *are* included
    by changing the following setting in Sphinx's conf.py::
    
    napoleon_include_private_with_doc = True
    
    """
    pass
    
    def _private_without_docstring(self):
    pass



## Testing
Testing is performed using the module `pytest`. For each module file `<file>.py` in `~/src/unitc` a script named `~/tests/test_<file>.py` should be created. This script tests the functions defined in `<file>.py`.

To run all module tests, the following command should be executed from the upper directory:

    python -m pytest tests

A single file (e.g. `test_unitc.py`) with tests can be executed in a similar way:

    python -m pytest tests/test_unitc.py

## Upload to Pypi
In order to upload changes to pypi, the following steps have to be followed:

1. Run tests to check if everything works: `python3 -m pytest tests`. Before proceeding with the next steps, all tests should pass.
2. Check data in `./setup.py` and correct if necessary (e.g. for a new upload a new version number should be defined)
3. Update `build` and `twine`: `python3 -m pip install --upgrade build` and `python3 -m pip install --upgrade twine`
4. Create build files: `python3 -m build`
5. Upload files: `python3 -m twine upload --repository pypi dist/*`. Make sure you have a `.pypirc` file with an access token or an alternative identification method.

