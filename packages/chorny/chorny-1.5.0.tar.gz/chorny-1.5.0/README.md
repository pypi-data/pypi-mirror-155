# chorny

Chorny (russian: чёрный) is a loader of [Black](https://github.com/psf/black) that patches code on the fly to change the formatting to satisfy Athenian's conventions.

So far, the only difference with the original rules is how magic trailing commas work. Chorny
prevents new line expansion by the magic trailing comma for parentheses unless the code is
a function signature. Example:

```python
async def foo(self, arg, other,):
    pass
```

becomes

```python
async def foo(
    self,
    arg,
    other,
):
    pass
```

However,

```python
foo(
    1, "one,
)
```

stays intact.

## Installation

```
pip install chorny
```

## Usage

`chorny` patches and launches `black` and should be used the same way.

## License

MIT, see [LICENSE](LICENSE).
