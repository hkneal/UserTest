from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def register(self, postData):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
        #First User to Register is Admin Level, else Normal level
        if len(UserName.objects.all()) < 1:
            thisAdminlvl = 2
        else:
            thisAdminlvl = 1
        user = UserName.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_pw,
            admin_level = thisAdminlvl
        )
        return {
            'user':user
            # 'message': "Thank You For Registering!"
            }

    def signin(self, postData):
        password = postData['password']
        user = UserName.objects.get(email = postData['email'])
        return {
            'user':user
            # 'message' : "You Have Successfully Logged In!"
            }

    def update_info(self, postData):
        if postData['admin_level'] == 'Admin':
            admin_level = 2
        else:
            admin_level = 1
        user = UserName.objects.filter(email= postData['email']).update(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData ['email'],
            admin_level = admin_level
        )
        return {
            'user' :user
        }

    def change_password(self, postData):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
        user = UserName.objects.filter(id= postData['id']).update(
            password = hashed_pw
        )
        return {
            'user' :user
        }

# Create your models here.
class UserName(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    admin_level = models.PositiveIntegerField(validators=[MaxValueValidator(2),], default=1)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField(max_length=2000)
    user = models.ForeignKey(UserName, related_name="users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    message = models.ForeignKey(Message, related_name="message_commentss")
    user = models.ForeignKey(UserName, related_name="comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
