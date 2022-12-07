from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is_customer', default=False)
    is_employee = models.BooleanField('Is employee', default=False)
    mobile = models.CharField(max_length=12)
    email = models.EmailField(unique=True,error_messages={'unique':"*Email Id is already taken."})

    # USERNAME_FIELD ='email'
    # REQUIRED_FIELDS = []

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)

class create_roadUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=100,unique=True,error_messages={'unique':"*Aadhar Number is already exists."})
    gender = models.CharField(max_length=100,choices=GENDER_CHOICES, default=False)
    mobile_number = models.CharField(max_length=12,unique=True,error_messages={'unique':"*Phone Number is already exists."})
    email = models.EmailField(unique=True,error_messages={'unique':"*Email Id is already taken."})
    license_number = models.CharField(max_length=100,unique=True,error_messages={'unique':"*License Number Is already exists."})
    profile = models.ImageField(upload_to='media/',default= 'profile.png')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    class Meta:  
        db_table = "add_road_user"  
        
    def __str__(self):
        return f" {self.first_name} {self.last_name} profile"


class OffenceList(models.Model):
    offence = models.CharField(max_length=100)
    offence_fine = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    

class Crime(models.Model):
    challan = models.ForeignKey("Challan",on_delete=models.CASCADE)
    offence =  models.ForeignKey("OffenceList",on_delete=models.CASCADE)
    penalty = models.IntegerField()
   
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    
class Challan(models.Model):  
    refrence = models.CharField(max_length=100,null=True)
    vehicle_number = models.CharField(max_length=100,null=True)
    offender = models.ForeignKey("create_roadUser",on_delete=models.CASCADE)
    total_penalty = models.IntegerField()
    officer = models.ForeignKey("User",on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return f" {self.offender.first_name} made offence on {self.created_at} with  {self.total_penalty} rs"
 
    