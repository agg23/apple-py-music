
from setuptools import setup


setup(
    description="Apple Music Python Client",
    install_requires=['cryptography', 'PyJWT', 'requests'],
    keywords="apple music api wrapper",
    license="MIT",
    name="apple-py-music",
    packages=["applepymusic"],
    # TODO:
    # test_suite="tests",
    url='https://github.com/rcrdclub/apple-py-music',
    version='0.6.0',
)
