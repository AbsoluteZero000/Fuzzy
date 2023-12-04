import Shape


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3, tmp):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.tmp = tmp

    def fuzzification(self):
        # y = ax + b
        # b = y - ax
        slope = 0.0
        b = 0
        if self.tmp > self.x1 and self.tmp <= self.x2:
            if self.x1 == self.x2:
                slope = 1
            else:
                slope = (self.y2 - self.y1) / (self.x2 - self.x1)
            b = self.y1 - (slope * self.x1)
        else:
            if self.x2 == self.x3:
                slope = 1
            else:
                slope = (self.y3 - self.y2) / (self.x3 - self.x2)
            b = self.y2 - (slope * self.x2)
        return (slope * self.tmp) + b

    def getCentroid(self):
        centroid_x = (self.x1 + self.x2 + self.x3) / 3
        return centroid_x
