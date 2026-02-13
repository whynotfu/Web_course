import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, no):
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)

    def dot(self, no):
        return self.x * no.x + self.y * no.y + self.z * no.z

    def cross(self, no):
        return Point(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )

    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(a, b, c, d):
    ab = b - a
    bc = c - b
    cd = d - c
    x = ab.cross(bc)
    y = bc.cross(cd)
    cos_angle = x.dot(y) / (x.absolute() * y.absolute())
    cos_angle = max(-1, min(1, cos_angle))
    return math.degrees(math.acos(cos_angle))

if __name__ == '__main__':
    points = []
    for _ in range(4):
        coords = list(map(float, input().split()))
        points.append(Point(*coords))
    print(f"{plane_angle(*points):.2f}")
