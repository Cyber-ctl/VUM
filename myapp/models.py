#from django.db import models

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=500)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.email}"
    
    def __str__(self):
        return self.name
    
    def delete_student(self):
        self.delete()


class quotes(models.Model):
    quotes_a = models.CharField(max_length=5000)
    author = models.CharField(max_length=100, null=True, blank=True)
    active = models.IntegerField() 
    createdat = models.CharField(max_length=100, null=True, blank=True)
    modifiedat = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.quotes_a

    def delete_quotes(self):
        self.delete()


class Sabhasad(models.Model):
    reg_no = models.IntegerField()
    name = models.CharField(max_length=500, null=True, blank=True)
    division = models.CharField(max_length=100)
    contact_no = models.BigIntegerField()
    reg_date = models.DateField()
    dob = models.DateField()
    active = models.IntegerField() 
    email_id = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    createdat = models.CharField(max_length=100, null=True, blank=True)
    modifiedat = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.reg_no} ({self.email_id})"

    def delete_quotes(self):
        self.delete()


    
class Div(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class Admin_reg(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    password= models.CharField(max_length=255, null=True, blank=True)
    status= models.CharField(max_length=50, null=True, blank=True)
    email= models.CharField(max_length=50, null=True, blank=True)
    createdat = models.CharField(max_length=100, null=True, blank=True)
    modifiedat = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

