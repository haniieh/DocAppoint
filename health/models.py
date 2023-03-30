from django.db import models
from django.contrib.auth.models import User

# Create your models here.
blood_group=[('-A','-A'),
('+A','+A'),
('-B','-B'),
('+B','+B'),
('-AB','-AB'),
('+AB','+AB'),
('-O','-O'),
('+O','+O'),
]

gender=[('Male','Male'),
('Female','Female'),
('Other','Other'),
]

class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    blood_group = models.CharField(max_length=10,choices=blood_group,null=True, blank=True)
    health_uid = models.CharField(max_length=16,null=True, blank=True)
    ex_year= models.CharField(max_length=10,null=True, blank=True)
    ex_month= models.CharField(max_length=10,null=True, blank=True)
    cvv = models.CharField(max_length=10,null=True, blank=True)
    mobile_no = models.CharField(max_length=10,null=True, blank=True)
    addr = models.CharField(max_length=100,null=True, blank=True)
    card_status = models.CharField(max_length=100,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Doctor(models.Model):
    status = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile_no = models.CharField(max_length=10, null=True, blank=True)
    addr = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    specialist = models.CharField(max_length=100, null=True, blank=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    clinic = models.CharField(max_length=100, null=True, blank=True)
    cl_address = models.CharField(max_length=100, null=True, blank=True)
    daystiming = models.CharField(max_length=100, null=True, blank=True)
    timing = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100,choices=gender,null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)



    def __str__(self):
        return self.user.username

class Medical(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=True)
    status = models.CharField(max_length=100,null=True, blank=True)
    days_time = models.CharField(max_length=100, null=True, blank=True)
    timing = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    foundation_date = models.CharField(max_length=100, null=True, blank=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)
    addr = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True, blank=True)

    def _str_(self):
        return self.name

class Appointment(models.Model):
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    medical=models.ForeignKey(Medical, on_delete=models.CASCADE, null=True)
    a_date=models.DateField(null=True)
    status=models.CharField(max_length=100,null=True)
    p_status=models.CharField(max_length=100,null=True)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)

    def _str_(self):
        return self.doctor.user.username+" "+self.patient.user.username

class Doctors_Invoice(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    medicine = models.CharField(max_length=100,null=True)
    prescription = models.CharField(max_length=100,null=True)
    price = models.CharField(max_length=100,null=True)

    def _str_(self):
        return self.apponitment.doctor.user.username + " " + self.apponitment.patient.user.username + " " + self.medicine


class Adminstration(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    mobile_no = models.CharField(max_length=10,null=True,blank=True)
    addr = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.user.username

class Prescription(models.Model):
    appoint = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.CharField(max_length=100,null=True,blank=True)
    days = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    price = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.appoint.doctor.user.username+" "+self.appoint.patient.user.username

class Medical_Record(models.Model):
    appoint = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    disc = models.CharField(max_length=100,null=True,blank=True)
    file = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.appoint.doctor.user.username+" "+self.appoint.patient.user.username

class Billing_Record(models.Model):
    appoint = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.appoint.doctor.user.username+" "+self.appoint.patient.user.username