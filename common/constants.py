East = 'E'
North = 'N'
South = 'S'
West = 'W'
Northeast = 'NE'
Northwest = 'NW'
Southwest = 'SW'
Southeast = 'SE'
Forward = 'F'
Left = 'L'
Right = 'R'
Backward = 'B'

D2D4 = ((1, 0), (0, 1), (-1, 0), (0, -1))
D2D8 = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
D3D6 = {(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)}
Dnames = (East, Northeast, North, Northwest, West, Southwest, South, Southeast)

NSEW_8 = {key: val for key, val in zip(Dnames, D2D8)}
NSEW = {key: val for key, val in NSEW_8.items() if abs(sum(val)) == 1}
NSEW_YINV = {key: (vx, -vy) for key, (vx, vy) in NSEW.items()}
NSEW_8_YINV = {key: (vx, -vy) for key, (vx, vy) in NSEW_8.items()}

HEX_N = {'N': (0, 1), 'S': (0, -1), 'NE': (1, 0), 'SE': (1, -1), 'NW': (-1, 1), 'SW': (-1, 0)}
HEX_E = {'E': (1, 0), 'W': (-1, 0), 'NE': (0, 1), 'NW': (-1, 1), 'SE': (1, -1), 'SW': (0, -1)}

Headings = {'E': 0, 'NE': 45, 'N': 90, 'NW': 135, 'W': 180, 'SW': 225, 'S': 270, 'SE': 315}
Headings.update({val: key for key, val in Headings.items()})

origin2 = (0, 0)
origin3 = (0, 0, 0)
origin4 = (0, 0, 0, 0)
