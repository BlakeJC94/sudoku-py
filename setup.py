from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="sudoku_py",
    version='1.0.0',
    description="A sudoku generator and solver implmented in Python",
    long_description=long_description,
    author='BlakeJC94',
    author_email='blakejamescook@gmail.com',
    url='https://github.com/BlakeJC94/sudoku-py',
    python_requires=">=3.7",
    entry_points={
        'console_scripts': ['sudoku=sudoku_py.__main__:main'],
    }
)

