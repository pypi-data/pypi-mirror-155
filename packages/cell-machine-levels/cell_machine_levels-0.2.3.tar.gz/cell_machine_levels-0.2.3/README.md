# Cell Machine Levels

A library for manipulating modded cell machine level codes.

## Level class

Level creation example:

```py
from cell_machine_levels import level
test = level.Level(10, 10, "test", level.WallEffect.wrap)
print(test.save("V1"))
```

Level importing example:

```py
from cell_machine_levels import level
test = level.open("V1;10;10;;;test;2")
print(f"{test.name}: {test.size}, {test.wall_effect}")
```
