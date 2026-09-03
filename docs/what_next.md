# Resources

## Before the training course

We would recommend reading at least the first few chapters of this book so you are comfortable and familiar with Python before your Python Charmers training course.

If you have read this book thoroughly till now and practiced writing some
Python code, then you will be very well-placed to get the most out of the
course.

We're sure you'll enjoy the course and learn a lot. Meanwhile, please <a href="mailto:help@pythoncharmers.com">get in touch</a> if you have any questions!

## After the training course

Here are some project suggestions and further resources for after the course.

## Projects

If you have a work-related project, we recommend that you try applying Python to solve it as soon as possible after the course.

If you would like other project ideas, try these lists:

* [Mega Project List](https://github.com/karan/Projects#mega-project-list)
* [Exercises for Programmers: 57 Challenges to Develop Your Coding Skills](https://pragprog.com/titles/bhwb/exercises-for-programmers/)

## Example Code

The best way to learn a programming language is to write a lot of code and read a lot of code:

* [Python Module of the Week](https://pymotw.com/3/) is an excellent guide to the [Standard Library](stdlib.md#stdlib), with worked examples for module after module.
* [Real Python](https://realpython.com/) publishes a large library of practical tutorials, many of them free.

## Advice

* [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
* [The Elements of Python Style](https://github.com/amontalenti/elements-of-python-style)
* [PEP 8](https://peps.python.org/pep-0008/), the official Python style guide

## Videos

* [PyVideo](https://pyvideo.org) indexes talks from Python conferences worldwide.
* [PyCon AU](https://www.youtube.com/@PyConAU) publishes recordings of the Australian conference.

## Questions and Answers

* [Official Python FAQ](https://docs.python.org/3/faq/)
* [Norvig's list of Infrequently Asked Questions](https://norvig.com/python-iaq.html)
* [Stack Overflow questions tagged with python](https://stackoverflow.com/questions/tagged/python)

## Discussion

If you are stuck with a Python problem and don't know whom to ask, the [Python Discourse forum](https://discuss.python.org/) is a good place to start, and its Users category welcomes beginners.

Make sure you do your homework by trying to solve the problem yourself first and [ask smart questions](http://www.catb.org/~esr/faqs/smart-questions.html).

## News

If you want to keep up with the world of Python, follow [Planet Python](https://planetpython.org) or the [Real Python newsletter](https://realpython.com/newsletter/).

## Installing libraries

There are a huge number of open source libraries at the [Python Package Index](https://pypi.org) which you can use in your own programs.

A nice human-curated list of Python packages is here: [Awesome-Python](https://awesome-python.com).

To install and use these libraries, you can use [pip](https://pip.pypa.io/en/stable/). Newer tools such as [uv](https://docs.astral.sh/uv/) can do the same job considerably faster, and also manage your Python versions and virtual environments for you.

## Creating a Website

Learn [Flask](https://flask.palletsprojects.com/) to create your own website. Some resources to get started:

* [Flask Official Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
* [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

[Django](https://www.djangoproject.com/) is the other main choice, and takes a batteries-included approach where Flask stays minimal. If you are building an API rather than a website, [FastAPI](https://fastapi.tiangolo.com/) is worth a look.

## Graphical Software

Suppose you want to create your own graphical programs using Python. This can be done using a GUI (Graphical User Interface) library with their Python bindings. Bindings are what allow you to write programs in Python and use the libraries which are themselves written in C or C++ or other languages.

There are lots of choices for GUI using Python:

* [Tkinter](https://docs.python.org/3/library/tkinter.html)
  * Part of the standard library, so there is nothing to install. It looks dated next to the others and is awkward for large applications, but for a small tool it is the quickest way to put a window on the screen.
* [PySide6 / Qt for Python](https://doc.qt.io/qtforpython/)
  * The official Python binding for the Qt toolkit, released by the Qt Company under the LGPL, so you can use it in both open source and proprietary software. Qt is powerful and well documented, and Qt Designer lets you lay out interfaces visually. [PyQt](https://www.riverbankcomputing.com/software/pyqt/) is an alternative binding for the same toolkit, but it is GPL or commercial only.
* [Kivy](https://kivy.org)
  * Aimed at multi-touch applications and the only option here that also targets Android and iOS.
* [wxPython](https://wxpython.org)
  * Python bindings for the wxWidgets toolkit. It uses the native widgets of each platform, so applications look at home on Windows, macOS and Linux.

If you want a browser-based interface rather than a desktop one, [Streamlit](https://streamlit.io), [Dash](https://dash.plotly.com) and [Gradio](https://www.gradio.app) let you build a usable interface from a Python script with very little code. For data-focused work these are often a faster route than a desktop GUI, and we cover dashboards in our [Creating Dashboards in Python](https://pythoncharmers.com/training/creating-dashboards-python/) course.

### Summary of GUI Tools

For more choices, see the [GUI Programming page on the Python wiki](https://wiki.python.org/moin/GuiProgramming).

There is no one standard GUI tool for Python, so choose based on your situation. Is the interface for you alone or for other people? Does it need to run on one platform or several, or on mobile? And would a web page in the browser serve your users better than a desktop window?

## Various Implementations

There are usually two parts a programming language - the language and the software. A language is _how_ you write something. The software is _what_ actually runs our programs.

We have been using the _CPython_ software to run our programs. It is referred to as CPython because it is written in the C language and is the _Classical Python interpreter_.

There are also other software that can run your Python programs:

* [PyPy](https://pypy.org)
  * A Python implementation written in Python, with a just-in-time compiler that can make long-running programs several times faster than CPython.
* [Jython](https://www.jython.org)
  * A Python implementation that runs on the Java platform. This means you can use Java libraries and classes from within Python language and vice-versa. Note that it targets Python 2 only, so it is of limited use for new work.
* [IronPython](https://ironpython.net)
  * A Python implementation that runs on the .NET platform. This means you can use .NET libraries and classes from within Python language and vice-versa.

There are also others such as [Brython](https://brython.info) and [Pyodide](https://pyodide.org), which run Python inside a web browser, letting you use Python instead of JavaScript for browser programs.

Each of these implementations have their specialized areas where they are useful.

## Functional Programming (for advanced readers) <a id="functional-programming"></a>

When you start writing larger programs, you should definitely learn more about a functional approach to programming as opposed to the class-based approach to programming that we learned in the [object-oriented programming chapter](oop.md#oop):

* [Functional Programming HOWTO by A.M. Kuchling](https://docs.python.org/3/howto/functional.html)
* [The `functools` module](https://docs.python.org/3/library/functools.html) and [`itertools`](https://docs.python.org/3/library/itertools.html) in the standard library
* [Funcy library](https://github.com/Suor/funcy)
* [PyToolz library](https://toolz.readthedocs.io/en/latest/)

## Summary

We have now come to the end of this book but, as they say, this is the _beginning of the end_! You are now an avid Python user and you are no doubt ready to solve many problems using Python. You can start automating your computer to do all kinds of previously unimaginable things or write your own games and much much more. So, get started!

Do <a href="mailto:help@pythoncharmers.com">keep in touch</a> to let us know how you go!
