import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "prentr",
    version = "0.0.1",
    author = "Hamad Alafefi",
    author_email = "hamad@alafeefi.com",
    description = ("A tool made for the brave and the lazy alike, some say "
                   "it's a super tool, while others just can't withstand "
                   "it's humongous powers."),
    license = "The Unlicense",
    keywords = "python",
    url = "https://github.com/DmarZX2/prentr",
    packages=['prentr'],
    long_description_content_type="text/markdown",
    long_description=read('README.md')
)