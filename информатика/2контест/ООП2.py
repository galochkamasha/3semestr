class Car:
    def __init__(self, capacity, speed, number):
        self.capacity = capacity
        self.speed = speed
        self.number = number

class RaceCar(Car):
    def __init__(self, speed):
        super().__init__(capacity=0, speed=speed, number=None)


    

        

c = Car(1000, 100, "a720po")
print(c.capacity, c.speed, c.number)
r = RaceCar(300)
print(r.capacity, r.speed, r.number)
