
from setuptools import setup


setup(
    description="Apple Music Python Client",
    install_requires=['cryptography', 'PyJWT', 'requests'],
    keywords="apple music api wrapper",
    license="MIT",
    name="apple-music-py",
    packages=["applemusicpy"],
    # TODO:
    # test_suite="tests",
    url='https://github.com/rcrdclub/apple-music-py',
    version='0.2.0',
)
