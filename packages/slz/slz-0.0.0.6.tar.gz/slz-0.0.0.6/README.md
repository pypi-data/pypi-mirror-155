[![PyPI](https://img.shields.io/pypi/v/slz)](https://pypi.org/project/slz/)

## slz

a (light) binding for http://www.libslz.org/

```
o = slz.compressobj
o.compress('hello')
o.flush()
```

the stream is compatible with zlib deflate.

## tested versions

- Python 2.7
- Python 3.9
- PyPy [2.7] 7.3.3
- PyPy [3.7] 7.3.5
    - For PyPy2, pip needs to be 20.1.x cf https://github.com/pypa/pip/issues/8653
    - PyPy needs to be 7.3.1+ cf https://github.com/pybind/pybind11/issues/2436
- Pyston [3.8] 2.3

## Windows installation

Now sdist installation is possible.

## Apple M1 wheel

It will be considered after https://github.com/actions/python-versions/pull/114 is done.
