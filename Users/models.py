from django.db import models
from django.contrib.auth.models import AbstractUser

#models.

class User(AbstractUser):
	pass

class UserData(models.Model):
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.BinaryField()

	# def __repr__(self):
	# 	return "{}".format(self.__dict__)