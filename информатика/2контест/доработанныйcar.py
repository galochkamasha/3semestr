class Car:
    def __init__( self, capacity, speed, number):
        self.capacity = capacity
        self.speed = speed
        self.number = number

    def __str__(self):
        return f"<Car capacity:{self.capacity} speed:{self.speed} number:{self.number}>"

c = Car(1000, 100, "a720po")
print(c)