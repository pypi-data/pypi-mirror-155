# Declarative Argparse

This project introduces a wrapper argound the built-in `argparse` module that permits one to make a declarative parser for options.

[[_TOC_]]

## Example

```python
import argparse
from declarative_argparse import DeclarativeOptionParser
from declarative_argparse.options.int import IntDO
from declarative_argparse.options.str import StrDO
class DAPExample(DeclarativeOptionParser):
    def __init__(self) -> None:
        super().__init__(argp=argparse.ArgumentParser())
        self.x: IntDO = self.addInt('--x', '-x', description='X coordinate')
        self.y: IntDO = self.addInt('--y', '-y', description='Y coordinate')
        self.name: StrDO = self.addStr('--name', description='Change tile name').setNArgs('?')
        self.id: StrDO = self.addStr('id', description='specify tile ID')

# ...

args = DAPExample()
args.parseArguments(['--x=0', '-y', '1', 'abc1'])
assert args.x.get_value() == 0
assert args.y.get_value() == 1
assert args.name.get_value() is None
assert args.id.get_value() == 'abc1'
```

## License

MIT