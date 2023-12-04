from abc import ABC, abstractmethod


class Shape(ABS):
    @abstractmethod
    def fuzzification(self):
        pass

    @abstractmethod
    def getCentroid(self):
        pass
