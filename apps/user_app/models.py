from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models
import bcrypt

class MessageManager(models.Manager):
    def verify(self, postData):
        if postData['title'] < 1:
            return { 'error' : 'Title cannot be empty'}
        else:
            book = Book.objects.create(
                title = postData['title'],
                author = postData['author']
            )
            return {
                'book' : book
            }

class CommentManager(models.Manager):
    def verify(self, postData):
        print "in ReviewManager"
        if postData['review'] < 1:
            return { 'error' : 'Review cannot be empty'}
        else:
            print "creating Review"
            review = Review.objects.create(
                review = postData['review'],
                book = postData['book'],
                user = postData['user'],
                rating_whole = postData['rating_whole'],
                rating_remainder = postData['rating_remainder']
            )
            return {
                'review' : review
            }

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
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField(max_length=2000)
    user = models.ForeignKey(UserName, related_name="users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    message = models.ForeignKey(Message, related_name="message_commentss")
    user = models.ForeignKey(UserName, related_name="comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()
