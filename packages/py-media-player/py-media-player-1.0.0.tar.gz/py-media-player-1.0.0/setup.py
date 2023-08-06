from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = "1.0.0"
DESCRIPTION = "Media player library"
LONG_DESCRIPTION = "A cross platform audio and video player Python library"

# Setting up
setup(
    name="py-media-player",
    version=VERSION,
    author="Wallee (Red-exe-Engineer)",
    #author_email="<>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "audio", "audio player", "video", "video player", "cross platform"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)