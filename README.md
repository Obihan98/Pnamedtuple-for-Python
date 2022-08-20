# Pnamedtuple-for-Python
Pnamedtuple function to create a class to construct instances of a specified namedtuple


Initial function call constructs a class that we can use to define objects
`Point = pnamedtuple('Point', ['x','y'], mutable=False)`
Equivilant to:
`Point = pnamedtuple('Point', 'x y')
Point = pnamedtuple('Point', 'x, y')`

Define objects
`origin = Point(0,0)`
