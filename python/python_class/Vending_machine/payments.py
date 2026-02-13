from abc import ABC, abstractmethod

class Payments(ABC):
    def __str__(self):
        return(f"{self.name}")

class Cash(Payments):
    def __init__(self):
        self.name = "cash"

class Card(Payments):
    def __init__(self):
        self.name = "card"
