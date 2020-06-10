from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def create_error_message(self, label, message):
        error = {}
        error["label"] = label
        error["message"] = message
        return error, False
        
    def validate(self, form_data):
        data_is_valid = True
        errors = []

        if len(form_data['first_name']) < 2:
            error, data_is_valid = self.create_error_message(
                "first_name",
                "First name required ( 2 character minimum )"
            )
            errors.append(error)
        if len(form_data['last_name']) < 2:
            error, data_is_valid = self.create_error_message(
                "last_name",
                "Last name required ( 2 character minimum )"
            )
            errors.append(error)
        if not EMAIL_REGEX.match(form_data['email']):
            error, data_is_valid = self.create_error_message(
                "email",
                "Invalid format for email"
            )
            errors.append(error)
        for instance in User.objects.all():
            if instance.email == form_data['email']:
                error, data_is_valid = self.create_error_message(
                    "email",
                    "email already in use"
                )
                errors.append(error)

        if len(form_data['password']) < 8:
            error, data_is_valid = self.create_error_message(
                "password",
                "Password required ( 8 character minimum )"
            )
            errors.append(error)
        if(form_data['confirm']) != (form_data['password']):
            error, data_is_valid = self.create_error_message(
                "confirm",
                "Passwords must match"
            )   
            errors.append(error)
        return data_is_valid, errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["name"]) == 0:
            errors["name"] = "* Title is required"
        if len(postData["network"]) == 0:
            errors["network"] = "* Network is required"
        return errors

class Show(models.Model):
    name = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

class Rating(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="user_ratings")
    show = models.ForeignKey(Show, related_name="show_ratings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)