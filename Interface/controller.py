import unittest
from .models import User, Landmarks, Game
from django.http import HttpResponse


class Controller:
    def __init__(self):
        self.currentUser = None
        self.Game = None
        self.LandmarkList = []

    def check(self, parsedText, user):  # where parsedText is a list of strings
        # if user=None, don't accept any method except login
        # elif tree of different methods depending on first index of parsedText
        # a = eval('A')
        self.currentUser = user.name
        command = parsedText[0].upper() # commands should be toUpper
        userobj = User.objects.get(name=self.currentUser)
        if self.currentUser != "admin":
            self.Game = getattr(userobj , 'game')
            self.createlandmarklist()
        if command == 'CREATE':
          if parsedText[1].upper() == 'GAME':
            return self.create_game(parsedText[2])
          elif parsedText[1].upper() == 'LANDMARK':
            if len(parsedText)!=8:
                return "Bad landmark credentials"
            return self.create_landmark(parsedText[2], parsedText[3], parsedText[4], parsedText[5], parsedText[6], parsedText[7])
          elif parsedText[1].upper() == 'USER':
            if len(parsedText)!=5:
                return "Bad user credentials"
            return self.create_team(parsedText[2], parsedText[3], parsedText[4])
          else:
            return("Invalid command")
        elif command == 'START':
            if len(parsedText) != 3:
                return "Invalid number of arguments!"
            return self.start_game(parsedText[2])
        elif command == 'END':
            if len(parsedText) != 3:
                return "Invalid number of arguments!"
            return self.end_game(parsedText[2])
        #User calls
        elif command == 'ANSWER' and parsedText[1].upper() == 'QUESTION':
          if self.currentUser == "admin":
              return "Cannot answer question as admin"
          if self.Game.isActive == False:
              return "Game is not active"
          j=2
          newAnswer = ""
          for i in range(2,(len(parsedText))):
            newAnswer += parsedText[j] + " "
            j+=1
          newAnswer = newAnswer.rstrip()
          return self.answer_question(newAnswer)
          #if that answer is the last one, they're done and it prints the end message
        elif command == 'GET' and parsedText[1].upper() == 'STATUS':
          if self.Game.isActive == False:
              return "Game is not active"
          team.get_status()
        elif command == 'GET' and parsedText[1].upper() == 'CLUE':
          if self.currentUser == "admin":
              return "No clue for admin user"
          if self.Game.isActive == False:
              return "Game is not active"
          if len(self.LandmarkList) == userobj.currentLandmark:
              return "You have already won!"
          cl = getattr(userobj, 'currentLandmark')
          return(self.LandmarkList[cl].getClue())

        elif command == 'GET' and parsedText[1].upper() == 'QUESTION':
          if self.currentUser == "admin":
              return "No question for admin user"
          if self.Game.isActive == False:
              return "Game is not active"
          if len(self.LandmarkList) == userobj.currentLandmark:
              return "You have already won!"
          cl = getattr(userobj, 'currentLandmark')
          return(self.LandmarkList[cl].getQuestion())
        else:
          return('Invalid command.')
        
        
    # def getInstance(self):
    # Game maker must be first to log in?
    def login(self, username, password):
        if self.currentUser is None:
          if self.System.getTeamPassword(username) == password:
            self.currentUser = username
            return "Successfully logged in"
          else:
            return "Username or password is incorrect"
        else:
          return "Another user is currently logged in."
    def logout(self):
        if self.currentUser == None:
          return "No user is logged in"
        else:
          self.currentUser = None
          return "User logged out"

    def create_game(self, name):
        # instantiates new game object and calls setLandmarkList & setTeams in Game class. Current user is admin
        if self.currentUser != "admin":
            return ("Cannot create game if not game maker")

        g = Game(name=name,isActive=False)
        g.save()
        self.Game=g
        return "Game created!"
        


    def start_game(self, name):
        # only accessible if game maker. This method calls startClock() in Game class
        if self.currentUser != "admin":
            return "Cannot start game if not game maker"
        else:
            try:
                self.Game = Game.objects.get(name=name)
                if self.Game.isActive:
                    return "Game is already active!"
                else:
                    self.Game.toggleActive()
                    self.Game.save()
                    return "Game started!"
            except Game.DoesNotExist:
                return "Game not found"

    def end_game(self, name):
        # only accessible if game maker
        if self.currentUser != "admin":
            return "Cannot end a game unless game maker"
        else:
            try:
                self.Game = Game.objects.get(name=name)
                if self.Game.isActive == False:
                    return "Game is already inactive!"
                else:
                    self.Game.toggleActive()
                    self.Game.save()
                    return "Game ended!"
            except Game.DoesNotExist:
                return "Game not found"

    def create_landmark(self, name, clue, question, answer, gamename, position):
        if self.currentUser != "admin":
            return "Must be admin to create landmark"
        if name == "" or clue == "" or question == "" or answer == "" or gamename=="" or position==None:
            return "Invalid landmark argument(s)"
        try:
            g = Game.objects.get(name=gamename)
        except Game.DoesNotExist:
            return "Game not found"
        l = Landmarks(name=name, clue=clue, question=question, answer=answer,game=g, position=int(position))
        l.save()
        self.LandmarkList.append(l)
        return "Landmark created"

    def create_team(self, username, password, gamename):
      if self.currentUser != "admin":
          return "Must be admin to create a user"
      if username == "" or password == "" or username =='admin' or gamename=="":
        return "Invalid team credentials."
      try:
        g = Game.objects.get(name=gamename)
      except Game.DoesNotExist:
        return "Game not found"
      t = User(name=username, password=password, currentLandmark=0, game=g)
      t.save()
      return "Team created"

      
    def answer_question(self, answer):
        userobj = User.objects.get(name=self.currentUser)
        cl = getattr(userobj, 'currentLandmark')
        if len(self.LandmarkList) == userobj.currentLandmark:
            return "You have already won!"
        if self.LandmarkList[cl].getAnswer() == answer:
          userobj.currentLandmark+=1
          userobj.save()
                # need to be able to print the clue
          if len(self.LandmarkList) == userobj.currentLandmark:
            return 'You finished!'
          else:
            return ("Correct! Your next clue is: " + self.LandmarkList[cl+1].getClue())
        else:
          return "Incorrect answer, try again."
                # Eventually add penalty.
                # if answer is correct: automatically provide next clue, increments currentLandmark if correct
    def createlandmarklist(self):
        if self.Game==None:
            return
        list = Landmarks.objects.filter(game = self.Game).order_by('position')
        self.LandmarkList = list
        return