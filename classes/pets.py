 #!/usr/bin/env python3

"""Script contains a task execution from Lecture 7.

Task. Create the Person class and the Owner class derived from it; 
class Animal and class Pet, which inherits from Animal; 
specific classes of animals inherited from Animal: Cat, Dog, Hamster, Parrot.
Also create an OwnedPets class that represents the pets that the owner has 
(the animals can be different). Each object of the Owner type (each Owner) 
must contain the pets attribute — an object of the OwnedPets class.

For the OwnedPets container, implement useful operations (add a new animal, 
find all animals of a certain type, remove from the container, etc.), as well 
as operations on sets (merge two containers, find elements included in one and 
not included in the other, etc.). Implement typical operations for containers 
(__getitem__, __setitem__, __len__, __iter__, __contains__, ...). Try to reload 
standard operations using magic methods (addition, subtraction, etc.).

In turn, in the Owner class using the container, implement higher-level methods 
(for example, add_pets, feed_pets, is_pets_hungry, etc.).

Under the if __name__ == '__main__' block: demonstrate how it works.
"""

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        clsname = self.__class__.__name__
        return f'{clsname} {self.name.title()}, age={self.age}'


class Owner(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.pets = OwnedPets(self.name)

    def __repr__(self):
        return f'{super().__repr__()}, has {len(self.pets)} pets'
        
    def add_pets(self, *animals):
        for animal in animals:
            self.pets.add_pet(animal)
        
    def feed_pets(self):
        self.pets.feed_all()
        
    def are_pets_hungry(self):
        return self.pets.is_any_hungry()
        

class Animal:
    def __init__(self, name, species, sound):
        self.name = name
        self.species = species
        self.sound = sound
        self.hungry = True

    def __repr__(self):
        return f'{self.name.title()}, species: {self.species}'
        
    def make_sound(self):
        print(self.sound)
        
    def eat(self):
        self.hungry = False
        

class Pet(Animal):
    def __init__(self, name, species, sound, owner=None):
        super().__init__(name, species, sound)
        self.owner = owner

    def __repr__(self):
        return f'{super().__repr__()}'
        

class Cat(Animal):
    def __init__(self, name, owner=None):
        super().__init__(name, 'Cat', 'Meow')
        self.owner = owner
        
class Dog(Animal):
    def __init__(self, name, owner=None):
        super().__init__(name, 'Dog', 'Woof')
        self.owner = owner
        
class Cow(Animal):
    def __init__(self, name, owner=None):
        super().__init__(name, 'Cow', 'Moo')
        self.owner = owner
        

class OwnedPets:
    def __init__(self, name=None):
        self.owner = name
        self.pets = []

    def __repr__(self):
        return f'{self.owner} is owner of such pets as: {self.pets}'
        
    def add_pet(self, pet):
        self.pets.append(pet)
        pet.owner = self.owner
        
    def remove_pet(self, pet):
        if pet in self.pets:
            self.pets.remove(pet)
        
    def feed_all(self):
        for pet in self.pets:
            pet.eat()
        print(f"\t- All {self.owner}'s pets are fed.\n")
        
    def is_any_hungry(self):
        return any(pet.hungry for pet in self.pets)
    
    def find_all_of_type(self, species):
        return [pet for pet in self.pets if pet.species == species]
    
    def __len__(self):
        return len(self.pets)
    
    def __getitem__(self, index):
        return self.pets[index]
    
    def __setitem__(self, index, value):
        self.pets[index] = value

    # preffered for iterator
    def __iter__(self):
        return iter(self.pets)

    # preffered for 'in'
    def __contains__(self, pet):
        return pet in self.pets
    
    def __add__(self, other):
        new_pets = OwnedPets()
        new_pets.pets = self.pets + other.pets
        return new_pets
    
    def __sub__(self, other):
        new_pets = OwnedPets()
        new_pets.pets = [pet for pet in self.pets if pet not in other.pets]
        return new_pets

    def union(self, other):
        new_pets = self.pets.copy()
        for pet in other:
            if pet not in new_pets:
                new_pets.append(pet)
        return new_pets

    def intersection(self, other):
        return [pet for pet in self.pets if pet in other]

    def difference(self, other):
        return [pet for pet in self.pets if pet not in other]


if __name__ == '__main__':
    
    marv = Owner("Marv", 30)
    bob = Owner("Bob", 45)
    steve = Owner("Steve", 27)

    print(f'{marv.name}, {bob.name} and {steve.name} are a pet owners.\n')

    tom = Cat("tom", marv)
    jack = Cat("Jack", bob)
    molly = Cat("Molly", steve)
    bond = Dog("Bond", bob)
    rex = Dog("Rex", steve)
    sundy = Dog("Sundy", bob)
    star = Cow("Star", marv)
    lola = Cow("Lola", marv)

    marv.add_pets(tom, star, lola)
    bob.add_pets(jack, bond, sundy)
    steve.add_pets(molly, rex)

    jusper = Pet('Jusper', 'Parrot', 'Good morning!!!')
    steve.pets.add_pet(jusper)

    print(f'\n{marv}:')
    for pet in marv.pets:
        print(f'\t{pet}')

    print(f'\n{bob}:')
    for pet in bob.pets:
        print(f'\t{pet}')

    print(f'\n{steve}:')
    for pet in steve.pets:
        print(f'\t{pet}')

    print(f"\n\nCheck if {steve.name}'s pets want some food.\n\t...checking...")
    if steve.are_pets_hungry:
        print('\t- They are hungry, feed them.\n\t...yum-yum...')
        steve.feed_pets()
    else:
        print('\t- Pets are not hungry!')

    print(f'\n- ({steve.name}){jusper.name}, can you speek?\n- ({jusper.name}){jusper.sound}\n')
    
    print(f'\nAdd pet ({jusper.name}) to {marv.name}:')
    marv.pets.add_pet(jusper)
    print(f'{marv}:')
    for pet in marv.pets:
        print(f'\t{pet}')

    print(f'\nRemove pet ({sundy.name}) from {bob.name}:')
    bob.pets.remove_pet(sundy)
    print(f'{bob}:')
    for pet in bob.pets:
        print(f'\t{pet}')

    print(f'\n\nHow many pets do you have, {marv.name}? - {len(marv.pets)}')
    print(f'Do you have some cows? - ', end="")
    for pet in marv.pets.find_all_of_type('Cow'):
        print(f'{pet.name} ', end="")

    print(f'\n\n\nSecond pet in Steve - {steve.pets[1]}. Change it to Sundy.')
    steve.pets[1] = sundy
    print(f'Sundy belongs to Steve? - {sundy in steve.pets}')
    print(f'{steve}:')
    for pet in steve.pets:
        print(f'\t{pet}')

    # pets addition
    print(f'\n\nBob pets + Steve pets =\n  {(bob.pets + steve.pets).pets}')
    # pets substruction
    print(f'\nMarv pets - Steve pets =\n  {(marv.pets - steve.pets).pets}')
    # pets union
    print(f'\n\nMarv pets | Steve pets =\n  {marv.pets.union(steve.pets)}')
    # pets intersection
    print(f'\nMarv pets & Steve pets =\n  {marv.pets.intersection(steve.pets)}')
    # pets difference
    print(f'\nMarv pets - Steve pets =\n  {marv.pets.difference(steve.pets)}')
    
