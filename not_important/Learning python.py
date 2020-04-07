# python as a language is quite easy straight forward, and not so complicated
# It's actually both OOP and functional based program
# it is a dynamic language and no need to specify the dtypes and variable allocation is done internal itself


# The first thing that we learn is going to be OOP:
"""
So this is a doc string for just explanation:
What is Object oriented programming, it basically just tells us how do we relate to real life examples:
so suppose I have a laptop say it is a Macbook air I am using, So this Macbook has certain features, now these features
are further classified into 2 types: Attributes, Behaviour,

Now guys what does those words mean actually ???
Attributes describe more like appearance, and the attributes of a laptop can be described as:
        Length, Weight, Width, Make, Brand
so the above are the general attributes of a laptop.

i.e. class Laptop{
    name:
    make:
    brand:
    dimensions:
    weight:
    year:
    keyboard:
    mouse:
    power button:
}

These are the attributes now what are the behaviours ???
so behaviours generally mean what you can do using the attributes or what are the actions that can be done by our object
( here it is Macbook)

The behaviors are :
        Power: on, off; Typing; Scrolling; Brightness: dim, bright ( can also be a range from 0 to 100); Browse; code

these are called functions in programming terms:

class Laptop{
    Power():
        # this will actually on the laptop if it is off, and vice versa
        so it is literally just changing the state at which laptop is, i.e off to on, or on to off
    Brightness(value):
        currentBrightness = value
        # it takes the input from the User interface( button over here) and executes it.

}

So now we have an idea that class is an abstract idea like it is a type system based on which we have several instances
of that type

Like we have a type called Laptop and in this we have a instance called Macbook air

OOP is based on Objects.
Water Bottle - 15rs kenley: object
class - blueprint of an object.
object to be created a class.
Water Bottle - 15rs kenley
Mould - class, Mould - dimensions(length, width)
                    -   size
                    -   volume

Attributes and behaviour.


Jimmy dog: nose, eyes, 4 legs, shape, height, weight
         : barking, eating, sleep,

dog is a class, JImmy is an object of class Dog
Office bag: Attributes: zip, Pocket, length, width, volume
            behaviours: openClosingZip, put, take

class,

10 objects, attributes, behaviours.


PATTERNS:
    GooglePay():
        App called Google Pay -
        Any no. of persons - 10
        One person to another some amount - Rs.100 /-


"""


def classes():
    class Customer:
        def __init__(self, name, id, age, amount):  # constructor
            self.name = name
            self.id = id
            self.age = age
            self.amount = amount

    x = Customer('karthick', 12345, 22, 10000)
    y = Customer('Jyo', 12354, 22, 10000)
    z = Customer('sashank', 1111, 22, 10000)

    class GooglePay:
        def __init__(self):
            self.customers = set()

        def register(self, customer):
            self.customers.add(customer)
            return self

        def send(self, sender, receiver, cash):
            p = {sender, receiver}
            if isinstance(sender, Customer) and isinstance(receiver, Customer):
                if p.issubset(self.customers):
                    if sender.amount > cash:
                        sender.amount = sender.amount - cash
                        receiver.amount = receiver.amount + cash
                        print("transaction successful")
                        print(str(sender.name) + " current account balance is " + str(sender.amount))
                        print(str(receiver.name) + " current account balance is " + str(receiver.amount))
                    else:
                        print("insufficient funds")
                else:
                    print("sender or receiver does not exist")
            else:
                print("either sender or receiver is not a real customer")
                # if receiver in self.customers and sender in self.customers :

    googlePay = GooglePay()
    googlePay.register(x).register(y).register(z)
    googlePay.send(x, z, 1000)


classes()


