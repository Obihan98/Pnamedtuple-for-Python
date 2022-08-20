# Pnamedtuple-for-Python
Pnamedtuple function to create a class to construct instances of a specified namedtuple.

• Initial function call constructs a class that we can use to define objects
```
>>> Point = pnamedtuple('Point', ['x','y'], mutable=False)
```
• Equivilant to:
```
>>> Point = pnamedtuple('Point', 'x y')
>>> Point = pnamedtuple('Point', 'x, y')
```

• Constructed the class named 'Point'
```
>>> type(Point)
<class 'type'>
>>> Point._fields
['x', 'y']
```

• Use this class to create new objects
```
>>> origin = Point(0, 0)
>>> origin
Point(x=0,y=0)
```

# Methods
• _asdict: Return the pnamedtuple as a dict
```
>>> origin._asdict()
{'x': 0, 'y': 0}
```

• _make: Take one iterable, and return a new object
```
>>> Point._make((1, 1))
Point(x=1,y=1)
```

• _replace: Take keyword arguments as parameters, changes the values in the nametuple
```
>>> origin._replace(y = 5)
Point(x=0,y=5)
```
