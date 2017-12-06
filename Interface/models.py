from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    isActive = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def checkIfWin(self, x):
        #TODO
        pass
    def toggleActive(self):
        if (self.isActive):
        ##THE ~FUTURE~  self.stopClock()
            self.isActive = False
        else:
            ##THE ~FUTURE~   self.startClock()
            self.isActive = True

class User(models.Model):
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    currentLandmark = models.IntegerField(default=0)
    game = models.ForeignKey(Game)
    def __str__(self):
        return self.name
    def getName(self):
        return self.name
    def getPassword(self):
        return self.password
    def get_status(self):
        # returns current time, location (penalties accounted for in later iteration)
        # implement gm total status sprint 2 - can probably just call this for each team
        print("Stats for " + self.name)
        # print("Current time: %d", self.Game.clock)  # TODO: need to fix this line
        print("You are on landmark " + self.currentLandmark)  # Prints name of landmark




class Landmarks(models.Model):
    name = models.CharField(max_length=100)
    clue = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    game = models.ForeignKey(Game)
    position = models.IntegerField()

    class Meta:
        verbose_name_plural = "Landmarks"
        
    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def setClue(self, clue):  # to be called by gamemaker
        self.clue = clue

    def getClue(self):
        return self.clue

    def setQuestion(self, question):  # to be called by gamemaker
        self.question = question

    def getQuestion(self):
        return self.question

    def setAnswer(self, answer):  # to be called by gamemaker
        self.answer = answer

    def getAnswer(self):
        return self.answer


class HuntCommand(models.Model):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User)
# Create your models here.
