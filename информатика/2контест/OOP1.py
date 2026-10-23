class Car:
    def __init__( self, capacity, speed, number):
        self.capacity = capacity
        self.speed = speed
        self.number = number


c = Car(1000, 100, "a720po")
print(c.capacity, c.speed, c.number)