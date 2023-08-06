from setuptools import setup

with open("README.md", 'r') as file:
    long_description = file.read()

setup(name = 'minitk',
      version = '0.3.3',
      author = 'Jean-Luc Déziel',
      author_email = 'jluc1011@hotmail.com',
      url = 'https://gitlab.com/jldez/minitk',
      description = 'Minimalist non blocking control panel for parameters',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      packages = ['minitk'],
      install_requires = ['Tk', 'pynput'],
    )