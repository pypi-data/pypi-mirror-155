from setuptools import setup

setup(
    name="pytest-cython-collect",
    classifiers=["Framework :: Pytest"],
    version='v0.2',
    author="Mads Ynddal",
    author_email="mads@ynddal.dk",
    url="https://github.com/Baekalfen/pytest-cython-collect",
    py_modules=["cython_collect"],
    install_requires=[
        'pytest',
    ],
    entry_points={
        'pytest11': [
            'pytest_cython_collect = cython_collect',
        ],
    },
)
