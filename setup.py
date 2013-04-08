#!/usr/bin/env python
from distutils.core import setup

setup(name='mpris2-fork',
      version='0.0.1',
      description='Python MPRIS2 wrapper',
      author='hugosenari / K900',
      author_email='hugosenari@gmail.com / k0009000@gmail.com',
      url='https://github.com/K900/mpris2',
      keywords = ["dbus", "mpris2"],
      packages=('mpris2',),
      license = "GPL",
      classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: X11 Applications",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Programming Language :: Python :: 3.3",
            "Topic :: Software Development :: Libraries :: Python Modules",
      ]
)