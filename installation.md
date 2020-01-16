# Installation

If you have not used Python before and would like to start using Python before your Python Charmers course, this chapter describes how to get started.

## Overview

We recommend the latest Anaconda Python 3.x installer, which is available from
[here](https://www.anaconda.com/distribution#download-section). This comes with
Python and several hundred of the most important 3rd-party packages. To install
this, choose a folder name without a space in it. \(Examples: `C:\Python3`,
`/home/user/anaconda`.\)

## More details

Feel free to skip the rest of this chapter if the above instructions are enough. Otherwise, read on for more details about installing Python via Anaconda.

## Python 3.x

The latest version is Python 3.8. The Python 3.x series is the future of all development in the language. Python 2 is a dead end; it will not be developed further. We will use Python 3.7 as the default version for the training course.

When we refer to "Python 3" in this book, we will assume any version of Python equal to or greater than version 3.5.

## Older Python versions

Python 2 is now a "legacy" platform that has received no major updates since 2010.

The vast majority of Python's best packages now support Python 3.x \(see [http://py3readiness.org](http://py3readiness.org)\), so we highly recommend starting new projects in Python 3.7. Python 3.7 is also cleaner and more consistent and has a healthy number of new useful features versus 2.7.

However, note that Python 3.x is backwardly incompatible with the Python 2.x series. If you are developing an existing Python 2.x code base, you must update the code to support Python 3 idioms or stick with the older version.

It is now relatively easy to provide automatic forward compatibility for running Python 3-style code under Python 2 using the **python-future** project, which Python Charmers sponsors. See [http://python-future.org](http://python-future.org) for information on writing compatible code.

Your training course with Python Charmers will largely describe how to write code that is compatible with both Python 3.x and Python 2.x.

## Installation requirements

We highly recommend at least 8 GB of memory \(RAM\) and a 64-bit operating system. All of the 3 major operating systems are supported: Windows, macOS, and Linux.

## Anaconda Python

We recommend installing Python via the Anaconda distribution, because it:

* is free
* can be installed without Administrator / root privileges
* supports all three major platforms \(Windows, macOS, Linux\)
* is up-to-date
* can be upgraded easily
* provides **binaries** of many of the traditionally hardest-to-install
  packages, like SciPy, scikit-learn, Numba, PIL \(via Pillow\), lxml, and
  libraries for geospatial analysis.

The **Anaconda Python 3.x** installer is available [here](https://www.anaconda.com/distribution#download-section).

We highly recommend that you install Anaconda:

1. for your user account \(**not** for all users\). This way you can install and remove packages later without needing Administrator / root access privileges.

2. in a folder without spaces. For example: `C:\Python3` or `/home/user/anaconda` are good choices. Spaces in the Python path occasionally cause scripts to break.

## Summary

From now on, we will assume that you have Python installed on your system.

Next, we will write our first Python program.

