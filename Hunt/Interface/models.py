from django.db import models

class User(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    currentLandmark = models.IntegerField(default=0)

class Landmarks(models.Model):
    name = models.CharField(max_length=100)
    clue = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)

class Game(models.Model):
    isActive = models.BooleanField(default=False)
    landmarkList = models.ForeignKey() #NOT SURE WHAT TO PUT HERE
    System = models.ForeignKey() #NOT SURE WHAT TO PUT HERE
    teams = models.ForeignKey() #NOT SURE WHAT TO PUT HERE

class System(models.Model): #THIS CLASS MIGHT BE REPLACED BY THE ACTUAL DATABASE THUS MIGHT NOT BE NEEDED HERE
    landmarks = models.ForeignKey() #NOT SURE WHAT TO PUT HERE
    team = models.ForeignKey() #NOT SURE WHAT TO PUT HERE

class HuntCommand(models.Model):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User)
# Create your models here.
