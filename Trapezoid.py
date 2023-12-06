class Triangle:
    def __init__(self, x_points, y_points, tmp):
        self.x_points = x_points
        self.y_points = y_points
        self.tmp = tmp

    def fuzzification(self):
        # y = ax + b
        # b = y - ax
        slope = 0.0
        b = 0
        if self.tmp > self.x_points[0] and self.tmp <= self.x_points[1]:
            if self.x_points[0] == self.x_points[1]:
                slope = 1
            else:
                slope = (self.y_points[1] - self.y_points[0]) / (
                    self.x_points[1] - self.x_points[0]
                )
            b = self.y_points[0] - (slope * self.x_points[0])
            return (slope * self.tmp) + b
        elif self.tmp > self.x_points[1] and self.tmp <= self.x_points[2]:
            if self.x_points[1] == self.x_points[2]:
                slope = 1
            else:
                slope = (self.y_points[2] - self.y_points[1]) / (
                    self.x_points[2] - self.x_points[1]
                )
            b = self.y_points[1] - (slope * self.x_points[1])
            return (slope * self.tmp) + b
        elif self.tmp > self.x_points[2] and self.tmp <= self.x_points[3]:
            if self.x_points[2] == self.x_points[3]:
                slope = 1
            else:
                slope = (self.y_points[3] - self.y_points[2]) / (
                    self.x_points[3] - self.x_points[2]
                )
            b = self.y_points[2] - (slope * self.x_points[2])
            return (slope * self.tmp) + b
        else:
            return 0

    def getCentroid(self):
        centroid_x = sum(self.x_points) / len(self.x_points)
        return centroid_x
