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

## Contributing

Thank you for considering making pytcm better.

Please refer to [docs](docs/CONTRIBUTING.md).

## Change Log

See [CHANGELOG](CHANGELOG.md)

## License

MIT