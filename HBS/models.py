from django.db import models


# Create your models here.
class doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    fee = models.IntegerField()


class patient(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    disease = models.CharField(max_length=300)
    cnic = models.CharField(max_length=100)
    doc = models.ForeignKey(doctor, on_delete=models.CASCADE)
    operation = models.IntegerField()
    nursing = models.IntegerField()
    room = models.IntegerField()
    food = models.IntegerField()


class prescription(models.Model):
    name = models.CharField(max_length=300)
    desc = models.TextField()
    price = models.IntegerField()
    number = models.IntegerField()
    patient = models.ForeignKey(patient, on_delete=models.CASCADE)


class invoice1(models.Model):
    date = models.DateField()
    patient = models.ForeignKey(patient, on_delete=models.CASCADE)