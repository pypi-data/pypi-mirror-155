# pytcm

A Python Terminal Commands Manager

## Installation

```
$ pip install pytcm
```

## Usage

### Using execute directly

``` python
import pytcm

binary = 'python'
opts = [
    pytcm.Flag('--version', True)
]

result = pytcm.execute(binary, opts)

print(result.out)  # "Python 3.9.7"
print(result.err)  # ""
print(result.returncode)  # 0
```

### Using a Command object that holds the context

``` python
import pytcm

binary = 'python'
opts = [
    pytcm.Flag('--version', True)
]

cmd = pytcm.Command(binary, opts)
cmd.execute()

print(cmd.out)  # "Python 3.9.7"
print(cmd.err)  # ""
print(cmd.returncode)  # 0
```

## Options

### Flag

A boolean option

```python
import pytcm

flag = pytcm.Flag("--verbose", True)
opt = flag.parse()

print(opt)  # "--verbose"
```

### Explicit

An option with an equal sign

```python
import pytcm

explicit = pytcm.Explicit("--age", 12)
opt = explicit.parse()

print(opt)  # "--age=12"
```

### Implicit

An option separated by a space character

```python
import pytcm

implicit = pytcm.Implicit("--age", 12)
opt = implicit.parse()

print(opt)  # "--age 12"
```

### Positional

A simple inline option

```python
import pytcm

positional = pytcm.Positional("test.txt")
opt = positional.parse()

print(opt)  # "test.txt"
```

## Contributing

Thank you for considering making pytcm better.

Please refer to [docs](docs/CONTRIBUTING.md).

## Change Log

See [CHANGELOG](CHANGELOG.md)

## License

MIT