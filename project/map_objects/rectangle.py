"""
Coordinate system starts at top right corner of map. Going right increases x, going down increases y:

                0 1 2 3 4
                1 . . . .
                2 . . . .
                3 . . . .
                4 . . . .

"""


#  Coded by Philip Hofman, Copyright (c) 2020.

class Rect:
    """A helper class for working with rectangles."""

    def __init__(self, x, y, w, h):
        """Inits top left corner and bottom right corner coordinates.

        Args:
            x(int): x coordinate of top left corner.
            y(int): y coordinate of top left corner.
            w(int): Width of rectangle.
            h(int): Height of rectangle.
        """

        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        """Return the center coordinates of this rectangle.

        Returns:
            center_x(int): x coordinate of this rectangle's center.
            center_y(int): y coordinate of this rectangle's center.
        """

        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        """Returns true if this rectangle intersects with another one.

        Args:
            other(Rect): A Rect object representing the other room.

        Returns:
            (bool): Does this rectangle intersect with another one?
        """

        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
