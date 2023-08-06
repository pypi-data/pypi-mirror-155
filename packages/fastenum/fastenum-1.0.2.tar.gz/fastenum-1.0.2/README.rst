fastenum
========

A roughly 3x faster drop-in replacement of Python's ``enum``.


Why
----
Python's `enum <https://docs.python.org/3/library/enum.html>`_ type is a useful building block for creating
semantic types and constants in your programs.

The problem is, if you're doing millions and millions of enum lookups (even simple expressions like
``Color.BLUE``) it's a little bit slow.

``fastenum`` is a stripped-down enum implementation that's up to 3.5x faster than the standard library
implementation. At `Quantlane <https://quantlane.com>`_ we use it in production code as a drop-in
replacement. Read more, including benchmarks, on our blog:
`A 3x faster enum type for Python <https://quantlane.com/blog/fastenum/>`_.


Installation
-------------
``fastenum`` is `available on PyPI <https://pypi.org/project/fastenum/>`_ and you can install it with:

::

	pip install fastenum

or

::

	poetry add fastenum


How to use it
--------------
Simply use ``fastenum.Enum`` instead of ``enum.Enum``:

.. code:: python

	import fastenum

	class Color(fastenum.Enum):
		RED = 0
		BLUE = 1
		GREEN = 2

	assert isinstance(Color.RED, Color)
	assert Color.RED is Color['RED']
	assert Color.BLUE != 1
	assert Color.GREEN.value == 2

	def is_red(c: Color) -> bool:
		return c is Color.RED

There is also a mypy plugin that you'll want to enable in ``mypy.ini`` to help mypy understand ``fastenum``
just like it understands ``enum``:

::

	[mypy]
	plugins = fastenum.mypy_plugin:plugin

Note you may experience odd mypy crashes relating to the mypy cache when using this plugin.
It's an unfortunate bug we have not yet tracked down. If you run into it, it is unfortunately necessary
to disable the mypy cache by setting ``cache_dir = /dev/null`` 🤦‍♂️


Tradeoffs and disadvantages
----------------------------
There is no support for automatic
values, unique value checks, aliases, custom ``__init__`` implementations on members, ``IntEnum``, ``Flag``,
or the functional API. If you require any of these features it's probably best to just use ``enum``.

``fastenum``'s mypy plugin may cause issues with your mypy cache (see above).


Running tests & benchmarks
---------------------------

::

	pip install -r dev-requirements.txt
	PYTHONPATH=. cq && pytest


Contributing
-------------
Pull requests are welcome! Especially if you know how to fix that pesky mypy cache bug 🙈

We will accept pull requests adding missing functionality *provided* they do not impact base ``fastenum``
performance (it's best to verify that with benchmarks).

****

	.. image:: quantlane.png

	``fastenum`` was made by `Quantlane <https://quantlane.com>`_, a systematic trading firm.
	We design, build and run our own stock trading platform.
