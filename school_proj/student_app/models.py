from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False) 
    student_email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    personal_email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    locker_number = models.IntegerField(null=False, blank=False, unique=True, default=110)
    locker_combination = models.CharField(max_length=20, null=False, blank=False, default="12-12-12")
    good_student = models.BooleanField(null=False, default=True)

    def __str__(self):
        return f"{self.name} - {self.student_email} - {self.locker_number}"
    
    def locker_reassignment(self, number):
        self.locker_number = number

    def student_status(self, status):
        self.good_student = status