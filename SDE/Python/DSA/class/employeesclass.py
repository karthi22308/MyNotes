


class employee:
    totalemployees=0
    idcounter=1000
    def __init__ (self,name, age):
        self.name = name
        self.age = age
        self.id = employee.idcounter
        employee.idcounter+=1
        employee.totalemployees+=1
    def introduce(self):
        print("hi, Im {}, im {} years old and my Id is {}".format(self.name,self.age,self.id))

class programmer(employee):
    def __init__ (self, name,age):
        super().__init__(name, age)   #
    def introduce(self):
        print("hi, Im {}, im {} years old and my Id is {} and im a Programmer".format(self.name,self.age,self.id))



