
from setuptools import setup

setup(name="Stravamous",
      version="0.2",
      author="Bryce",
      author_email="bjasmer@gmail.com",
      url="http://www.github.com/b-jazz/stravamous",
      scripts=["src/stravamous"],
      install_requires=['configurati>=0.2.2', 'gpxpy>=0.9.5'],
      )
