from django.db import models

class Game(models.Model):
    isActive = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    currentLandmark = models.IntegerField(default=0)
    game = models.ForeignKey(Game)
    def __str__(self):
        return self.name

class Landmarks(models.Model):
    name = models.CharField(max_length=100)
    clue = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    game = models.ForeignKey(Game)
    def __str__(self):
        return self.name

class HuntCommand(models.Model):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User)
# Create your models here.
