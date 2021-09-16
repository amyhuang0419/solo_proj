from django.db import models
import re
# from datetime import datetime
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.utils import timezone

# Create your models here.
class UserManager(models.Manager):
    def register_validation(self,post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        #validate first name
        if post_data['first_name'] == '':
            errors['first_name_empty'] = "First name is required!!"
        elif len(post_data['first_name']) < 2 :
            errors['first_name_length'] = "First name has at least 2 characters."
        elif not FIRST_NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = "First name must be letters!"

        #validate last name
        if post_data['last_name'] == '':
            errors['last_name_empty'] = "Last name is required!!"
        elif len(post_data['last_name'])< 2:
            errors['last_name_length'] = "Last name has at least 2 characters."
        elif not LAST_NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = "Last name must be letters!"

        #validate email
        users = User.objects.filter(email = post_data['email'])
        if post_data['email'] == '':
            errors['email_empty'] = "Email is required!!"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        elif users:
            errors['email_used'] = "This emaill address has registered by someone else."

        #validate password
        if post_data['password'] == '':
            errors['password_empty'] = "Password is required!!"
        elif len(post_data['password']) < 8:
            errors['password_length'] = "Password has at least 8 characters."

        if post_data['password'] != post_data['confirm_password']:
            errors['password_not_match'] = "Password Not Match!!!"

        #validate birthdate
        if post_data['birthdate'] == '':
            errors['birthdate_empty'] = "Please select a birthdate"

        return errors

    def login_validation(self,post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        #validate login email address
        if post_data['email'] == '':
            errors['email_empty'] = "Please enter your Login Email!!"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"

        # password can not be empty
        elif post_data['password'] == '':
            errors['password_empty'] = "Password is required!"

        return errors

class SneakerManager(models.Manager):
    def sneaker_validation(self, post_data):
        errors = {}

        #validate sneaker name
        if post_data['sneaker_name'] == '':
            errors['sneaker_name_empty'] = "Please tell me the Sneaker Name!!!"
        elif len(post_data['sneaker_name']) <2 :
            errors['sneaker_name_length'] = "Sneaker name has at least 2 characters."

        #validate color
        if post_data['color'] == '':
            errors['color_empty'] = "Please tell me the Sneaker Color!!!"
        elif len(post_data['color']) < 3 :
            errors['color_length'] = "Sneaker color has at least 3 characters."

        #validate sku number
        if post_data['sku_number'] == '':
            errors['sku_number_empty'] = "Please tell me the Sneaker SKU Number!!!"
        elif len(post_data['sku_number']) < 4 :
            errors['sku_number_length'] = "Sneaker SKU has at least 4 characters."



        #validate release price
        if post_data['release_price'] == '':
            errors['release_price_empty'] = "Please tell me the release price!!!"
        elif int(post_data['release_price']) < 0:
            errors['release_price_nagative'] = "The release price can not be nagative"
        # if post_data['release_price'] is not IntegerField():
        #     errors['release_price_not_intger'] = "The release price must be integer"



        #validate release date
        if post_data['release_date'] == '':
            errors['release_date_empty'] = "Please select a release date"
        elif datetime.strptime(post_data['release_date'], '%Y-%m-%d') > datetime.now():
            errors['release_date'] = "Release Date must be in the past"
        
        #validate buy price
        if post_data['buy_price'] == '':
            errors['buy_price_empty'] = "Please tell me the purchase price!!!"
        elif int(post_data['buy_price']) < 0:
            errors['buy_price_nagative'] = "The purchase price can not be nagative"
        # if post_data['buy_price'] is not IntegerField():
        #     errors['buy_price_not_intger'] = "The purchase price must be integer"

        return errors

class CommentManager(models.Manager):
    def comment_validation(self, post_data):
        errors = {}

        #validate comment
        if post_data['comment'] == '':
            errors['comment_empty'] = "What is the Comment??"
        elif len(post_data['comment']) < 10 :
            errors['comment_length'] = "Comment has at least 10 characters."

        return errors
    


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    birthdate = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Sneaker(models.Model):
    sneaker_name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    sku_number = models.CharField(max_length=255)
    release_price = models.IntegerField()
    release_date = models.DateTimeField(default=timezone.now)
    sneaker_size = models.FloatField()
    buy_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    posted_by = models.ForeignKey(User, related_name="sneaker_posted", on_delete=models.CASCADE)

    users_who_like = models.ManyToManyField(User, related_name = "liked_sneakers")

    # users_who_comment = models.ManyToManyField(User, related_name = "commented_sneakers")

    objects = SneakerManager()


class Comment(models.Model):
    comment = models.TextField()

    posted_by = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE) # user and comment

    upload_on = models.ForeignKey(Sneaker, related_name="sneaker_comments", on_delete=models.CASCADE) #sneaker and comment

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()


class Image(models.Model):
    image = models.ImageField(upload_to='images', blank= True)
    posted_by = models.ForeignKey(User, related_name="user_images", on_delete=models.CASCADE)

    upload_on = models.ForeignKey(Sneaker, related_name="sneaker_images", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
