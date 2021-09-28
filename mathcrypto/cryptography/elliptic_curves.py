"""This module wouldn't be possible to be created this fast
    if I didn't leverage the code that was written by xnomas and Baka-Git in their repository at:

    https://github.com/Baka-Git/Crypto_Math

    I want to thank them for allowing me to use their code.
"""


class EllipticCurve:
    """Elliptic curve objects

    Args:
        a0-a6 (int): Curve attributes (using the equation a0*y^2 + a1*y + a2*y*x = a3*x^3 + a4*x^2 + a5*x+a6)
        field (int, optional): The curves field
        point_px (int, optional): X coordinate of point P
        point_py (int, optional): Y coordinate of point P"""

    def __init__(
        self,
        a0: int,
        a1: int,
        a2: int,
        a3: int,
        a4: int,
        a5: int,
        a6: int,
        field: int = None,
        point_px: int = None,
        point_py: int = None,
    ):
        self.attributes = [a0, a1, a2, a3, a4, a5, a6]
        self.point_p = [point_px, point_py]
        self.field = field

    @classmethod
    def _divisors(cls, number: int):
        list_of_divisors = []
        for num in range(1, int(number) + 1):
            if int(number) % num == 0:
                list_of_divisors.append(num)
        return list_of_divisors

    @classmethod
    def _find_point(self, x, x_side, y_2_points, f):
        for y in range(0, len(y_2_points)):
            if x_side == y_2_points[y]:
                if y_2_points[y] == 0:
                    return [[x, self._find_sqrt_ec(y_2_points[y], f)]]
                return [[x, self._find_sqrt_ec(y_2_points[y], f)], [x, -self._find_sqrt_ec(y_2_points[y], f)]]
        return False

    @classmethod
    def _find_sqrt_ec(self, x, field):
        for i in range(0, field):
            result = (i * i) % field
            if result == x:
                return i

    @classmethod
    def _find_inverse(cls, num, mod):
        for i in range(1, int(mod)):
            if (i * num) % mod == 1:
                return i
        return False

    def is_elliptic_curve(self):
        """Checks if the curve is elliptic

        Returns:
            bool: True if curve with these attributes is elliptic
        """
        if self.attributes[0] != 1 or self.attributes[3] != 1:
            return False
        else:
            return True

    def get_curve_order(self, get_points: bool = False):
        """Gets the order of the curve.

        Args:
            get_points (bool, optional): Whether or not to return the curve points as well. Defaults to False.

        Raises:
            ValueError: If curve field is not set or the curve is not elliptic.

        Returns:
            bool: False if this EC is not supported.
            int: Elliptic curve order if get_points is not set to True
            (tuple):If get_points is set to true, returns a tuple containing:

                - int: Elliptic curve order
                - list: List of points on curve
        """
        if self.field is None:
            raise ValueError("Field is needed for this.")
        if not self.is_elliptic_curve():
            raise ValueError("This is not an elliptic curve!")
        if self.attributes[2] != 0:
            print("Not supported type of EC")
            return False

        line_points = []
        y_2_points = []

        for y in range(0, int(self.field / 2) + 1):
            y_2_points.append((y ** 2) % self.field)

        x_points = []
        x_side_points = []

        for x in range(0, self.field):
            x_points.append(x)
            x_side_points.append(
                (x ** 3 + x ** 2 * self.attributes[4] + x * self.attributes[5] + self.attributes[6])
                % self.field
            )

        for x in range(0, self.field):
            x_side = x_side_points[x]
            points = self._find_point(x, x_side, y_2_points, self.field)

            if points is False:
                y_2 = "-"
                y = "-"
                points = "-"
            else:
                y_2 = points[0][1] ** 2
                y = "+-" + str(points[0][1])

            line_points.append([x, x_side, y_2, y, points])

        line_points.append(["∞", "-", "-", "∞", "[∞,∞]"])
        order = 0
        list_of_points = []

        for line in line_points:
            if line[4] == "[∞,∞]":
                list_of_points.append(line[4])
                order += 1
            elif line[4] != "-":
                if line[2] == 0:
                    order += 1
                    list_of_points.append(line[4][0])
                else:
                    list_of_points.append(line[4][0])
                    list_of_points.append(line[4][1])
                    order += 2

        if not get_points:
            return order
        else:
            return order, list_of_points

    def is_point_on_elliptic_curve(self, x: int, y: int):
        """Checks if point of given coordinates is on the curve.

        Args:
            x (int): X coordinate of the point
            y (int): Y coordinate of the point

        Raises:
            ValueError: If curve field is not set or the curve is not elliptic.

        Returns:
            bool: True if point is on the curve
        """
        if self.field is None:
            raise ValueError("Field is needed for this.")
        if not self.is_elliptic_curve():
            raise ValueError("This is not an elliptic curve!")

        a = (y ** 2 + self.attributes[1] * y + self.attributes[2] * x * y) % self.field
        b = (x ** 3 + self.attributes[4] * x ** 2 + self.attributes[5] * x + self.attributes[6]) % self.field

        if a == b:
            return True
        return False

    def add_point(self, point_qx: int, point_qy: int):
        """Adds point P and point Q (of given coordinates) on the curve.

        Args:
            point_qx (int): X coordinate of point Q
            point_qy (int): Y coordinate of point Q

        Raises:
            ValueError: If curve field is not set.
            ValueError: If the curve is not elliptic.
            ValueError: If point P is not set.
            ValueError: If one or both poits are not on the curve.

        Returns:
            list: Resulting point coordinates
        """
        if self.field is None:
            raise ValueError("Field is needed for this.")
        if self.point_p is None:
            raise ValueError("Point P is needed for this.")
        point_p = [self.point_p[0] % self.field, self.point_p[1] % self.field]
        point_q = [point_qx % self.field, point_qy % self.field]

        if not (
            self.is_point_on_elliptic_curve(point_p[0], point_p[1])
            and self.is_point_on_elliptic_curve(point_q[0], point_q[1])
        ):
            raise ValueError(f"One or Two points, which were given, are not on E[F{str(self.field)}].")

        if point_p[0] != point_q[0]:
            a = point_q[1] - point_p[1]
            b = self._find_inverse(point_q[0] - point_p[0], self.field)

            lambdas = a * b % self.field

            x_r = (lambdas ** 2 - point_q[0] - point_p[0]) % self.field
            r = [x_r, (lambdas * (point_p[0] - x_r) - point_p[1]) % self.field]

        elif point_p[0] == point_q[0] and point_p[1] == point_q[1] and point_p[1] != 0:
            a = (3 * point_p[0] ** 2 + self.attributes[5]) % self.field
            b = self._find_inverse(2 * point_p[1], self.field)

            lambdas = a * b % self.field
            x_r = (lambdas ** 2 - 2 * point_p[0]) % self.field
            r = [x_r, (lambdas * (point_p[0] - x_r) - point_p[1]) % self.field]

        else:
            r = "[∞,∞]"

        return r

    def get_point_order(self, point_x: int = None, point_y: int = None):
        """Gets the order of point of given coordinates or point P if set. Given coordinates take precedence.

        Args:
            point_x (int, optional): X coordinate of the point
            point_y (int, optional): Y coordinate of the point

        Raises:
            ValueError: Neither valid parameters were passed and point P was not set

        Returns:
            int: Order of the point
        """
        if point_x is not None and point_y is not None:
            point = [point_x, point_y]
        elif self.point_p is None:
            raise ValueError(
                "Either provide the X and Y coordinates of the point to this method or create the EllipticCurve object with the point_px and point_py parameters."
            )
        else:
            point = self.point_p

        order = 1
        help_point = [point[0], point[1]]
        while True:
            help_curve = EllipticCurve(*self.attributes, self.field, *help_point)
            help_point = help_curve.add_point(*point)
            order += 1
            if help_point == "[∞,∞]":
                return order

    def get_all_point_order(self):
        """Gets orders of all points on the curve

        Raises:
            ValueError: If field is not set

        Returns:
            list of lists: list of lists[order, point]
        """
        if self.field is None:
            raise ValueError("Field is needed for this.")
        order_of_ec, points = self.get_curve_order(get_points=True)

        if order_of_ec is False:
            return False

        list_of_orders = self._divisors(order_of_ec)
        list_of_point_orders = []

        for order in list_of_orders:
            list_of_point_orders.append([order])

        for point in points:
            if point == "[∞,∞]":
                order = 1
            else:
                order = self.get_point_order(*point)
            for i in range(0, len(list_of_point_orders)):
                if list_of_point_orders[i][0] == order:
                    list_of_point_orders[i].append(point)
                    break

        return list_of_point_orders

    @classmethod
    def get_possible_orders(cls, order: int, new_order: int = None):
        """Gets the possible orders of points on a curve of certain order or if a curves order was changed to a given value.

        Args:
            order (int): Order of the curve
            new_order (int, optional): New order of the curve. Defaults to None.

        Returns:
            list: List of possible orders
        """

        if new_order is not None:
            order_of_curve = order
            new_field = new_order
        else:
            order_of_curve = order
            new_field = order

        possible_orders_old = cls._divisors(order_of_curve)
        possible_orders_field = cls._divisors(new_field)
        possible_orders_new = []

        for order_old in possible_orders_old:
            for order_field in possible_orders_field:
                if order_old == order_field:
                    possible_orders_new.append(order_field)

        return possible_orders_new
