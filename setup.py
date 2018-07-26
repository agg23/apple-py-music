
from setuptools import setup

import applymusicpy


setup(
    description="Apple Music Python Client",
    install_requires=['PyJWT', 'requests'],
    keywords="apple music api wrapper",
    license="MIT",
    name="apple-music-py",
    packages=["applemusicpy"],
    # TODO:
    # test_suite="tests",
    url='https://github.com/rcrdclub/apple-music-py',
    version=applymusicpy.VERSION,
)
