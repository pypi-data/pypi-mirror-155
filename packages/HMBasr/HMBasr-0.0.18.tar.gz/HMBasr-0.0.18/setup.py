from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.18'
DESCRIPTION = 'Automatic Speech Recognition'
LONG_DESCRIPTION = 'A package that allows to transcript french speech to text.'

# Setting up
setup(
    name="HMBasr",
    version=VERSION,
    author="Lou Lély",
    author_email="<loulely34@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['torch', 'transformers', 'librosa', 'pyctcdecode'],
    keywords=['python', 'transcription', 'speech', 'speech to text', 'speech recognition', 'fr', 'asr'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ])
