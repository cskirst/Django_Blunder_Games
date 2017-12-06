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
        self.currentUser = user
        command = parsedText[0].upper() # commands should be toUpper
        userobj = User.objects.get(name=self.currentUser)
        if self.currentUser != "admin":
            self.Game = getattr(userobj , 'game')
            self.createlandmarklist()
        '''
        if self.Game != None:
          team = None
          i = 0
          for i in range(len(self.Game.teams)):
            if self.currentUser == self.Game.teams[i].getName():
              team = self.Game.teams[i]
              break
        
        if command == 'LOGIN':
          self.login(parsedText[1], parsedText[2])
        elif command == 'LOGOUT':
          self.logout()
        '''
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
          '''
          if team.currentLandmark > len(self.Game.landmarkList):
            print('Hunt complete!')
            self.Game.toggleActive()
          '''
        elif command == 'GET' and parsedText[1].upper() == 'STATUS':
          if self.Game.isActive == False:
              return "Game is not active"
          team.get_status()
        elif command == 'GET' and parsedText[1].upper() == 'CLUE':
          if self.Game.isActive == False:
              return "Game is not active"
          if len(self.LandmarkList) == userobj.currentLandmark:
              return "You have already won!"
          cl = getattr(userobj, 'currentLandmark')
          return(self.LandmarkList[cl].getClue())

        elif command == 'GET' and parsedText[1].upper() == 'QUESTION':
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
        '''
        if landmark is None or teams is None:
            print("Landmarks or teams must not be null: Needs to be in format: landmark1,landmark2 teamA,teamB")
            return
        lmstrings = landmark.split(",")
        tmstrings = teams.split(",")
        self.Game = Game(self.System)
        lm = []
        for l in lmstrings:
            returnedLandmark = self.System.getLandmark(l)
            if returnedLandmark is None:
                print("Could not add " + l + " as it does not exist in system!")
                return
            else:
              lm.append(returnedLandmark)
        self.Game.setLandmarkList(lm)

        for t in tmstrings:
            returnedTeamName = self.System.getTeam(t)
            if returnedTeamName is None:
                print("Could not add " + t + "as it does not exist in system!")
            else:
              password = self.System.getTeamPassword(t)
              self.Game.addTeamToGame(t, password)
        '''
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
            return 'You win!'
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



'''
class TestAcceptanceLogin(unittest.TestCase):
    def setUp(self):
        self.con = Controller()
        self.Interface = Interface()
    def test_NormalLogin(self):
        self.Interface.command("LOGIN admin kittens")
        self.assertEqual(self.con.currentUser, "admin", "Current user is not admin")
    def test_LoginWithOtherUser(self):
        self.con.currentUser = "admin"
        self.con.System.teams = {"admin":"kittens","other":"otherpass"}
        self.Interface.command("LOGIN other otherpass")
        self.assertEqual(self.con.currentUser, "admin", "Current user should not be changed when call to login while there is a current user")
    def test_BadLogin(self):
        self.Interface.command("LOGIN badname badpass")
        self.assertEqual(self.con.currentUser, None, "Incorrect username & password should fail")
        self.Interface.command("LOGIN admin badpass")
        self.assertEqual(self.con.currentUser, None, "Incorrect password should fail")
        self.Interface.command("LOGIN baduser kittens")
        self.assertEqual(self.con.currentUser, None, "Incorrect username should fail")

class TestAcceptanceLogout(unittest.TestCase):
    def setUp(self):
      self.con = Controller()
      self.Interface = interface.Interface()
    def test_NormalLogout(self):
      self.con.currentUser = "admin"
      self.Interface.command("LOGOUT")
      self.assertEqual(self.con.currentUser, None, "Logout was unsuccessful")
    def test_LogoutOnNoCurrentUser(self):
      self.Interface.command("LOGOUT")
      self.assertEqual(self.con.currentUser, None, "Logout on no current user should not change anything")
      
class TestAcceptanceCreateGame(unittest.TestCase):
    def setUp(self):
      self.con = Controller()
      self.Interface = interface.Interface()
    def test_NormalCreateGame(self):
      self.Interface.command("CREATE GAME landmark1,landmark2 teamA,teamB")
      self.assertEquals(self.con.Game.landmarkList, [landmark1,landmark2], "Landmarks not created correctly")
      self.assertEquals(self.con.Game.teams, [teamA,teamB], "Teams not created correctly")
    def test_noLandmarks(self):
      self.Interface.command("CREATE GAME teamA,teamB")
      self.assertEquals(self.con.Game.landmarkList, [], "No landmarks should be created")
      self.assertEquals(self.con.Game.teams, [], "No teams should be created")
    def test_createEmptyGame(self):
      self.Interface.command("CREATE GAME")
      self.assertEquals(self.con.Game.landmarkList, [], "No landmarks should be created")
      self.assertEquals(self.con.Game.teams, [], "No teams should be created")

class TestAcceptanceCreateLandmark(unittest.TestCase):
    def setUp(self):
      self.con = Controller()
      self.Interface = interface.Interface()
    def test_NormalCreateLandmark(self):
      self.Interface.command("CREATE LANDMARK newplace this,is,a,clue this,is,a,question answer")
      self.assertEquals(self.con.System.landmarks[0].getName(), "newplace", "Name not set corectly")
      self.assertEquals(self.con.System.landmarks[0].getClue(), "this is a clue", "Clue not set correctly")
      self.assertEquals(self.con.System.landmarks[0].getQuestion(), "this is a question", "Question not set correctly")
      self.asswerEquals(self.con.System.landmarks[0].getAnswer(), "answer", "Answer not set correctly")
    def test_badCreateLandmark(self):
      self.Interface.command("CREATE LANDMARK")
      self.assertRaises(ValueError, self.con.System.landmarks[0], "Nothing at index 0 of landmarks")
      
class TestAcceptanceEnd(unittest.TestCase):
    def setUp(self):
      self.con = Controller()
      self.Interface = interface.Interface()
      self.Game = game.Game(self.con.System)
    def test_NormalEndGame(self):
      self.Game.isActive = True
      self.Interface.command("END")
      self.assertFalse(self.Game.isActive, "Game's isActive should be set to False after call to end game")
    def test_EndGameWhileNoActiveGame(self):
      self.Game.isActive = False
      self.Interface.command("END")
      self.assertFalse(self.Game.isActive, "Game's isActive should be False after call to end game when there is no active game")
      
class TestAcceptanceAnswerQuestion(unittest.TestCase):
    def setUp(self):
      self.con = Controller()
      self.con.currentUser = "name"
      self.Interface = interface.Interface()
      self.Game = game.Game(self.con.System)
      self.Game.teams = [User("name","pass")]
      self.Game.landmarkList = [Landmarks("name", "clue", "question", "answer")]
    def test_CorrectAnswer(self):
      self.Interface.command("ANSWER QUESTION answer")
      assertEquals(self.Game.teams[0].currentLandmark, 1, "CurrentLandmark should be incremented")
    def test_BadAnswer(self):
      self.Interface.command("ANSWER QUESTION badanswer")
      assertEquals(self.Game.teams[0].currentLandmark, 1, "CurrentLandmark should be incremented")
      
class TestAcceptanceGetStatus(unittest.TestCase):
    def setUp(self):
      self.con = Controller()
      self.Interface = interface.Interface()

class TestGMCreateGame(unittest.TestCase): # Chris Kirst tests
    def setUp(self):
        self.con = Controller()
        self.con.currentUser = "admin"
        self.con.System.teams = {"admin": "kitten", "teamA": "passwordA", "teamB": "passwordB"}
        x = landmarks.Landmarks("park", "", "", "")
        y = landmarks.Landmarks("lab", "", "", "")
        z = landmarks.Landmarks("library", "", "", "")
        self.con.System.landmarks = [x, y, z]

    def test_createGame(self):
        listoflandmarks = ["park", "lab", "library"]
        teamnames = ["teamA", "teamB"]
        self.con.create_game("park,lab,library", "teamA,teamB")
        self.assertEquals(self.con.Game.getLandmarkList(), listoflandmarks, "Assigned landmarks in game not correct")
        self.assertIn(teamnames, self.con.Game.getTeams(), "Assigned teams in game not correct")
        self.assertEqual(self.con.Game.clock, 0, "Clock should not be started until Game maker initiates game")
        self.assertFalse(self.con.Game.isActive, "Game should not be active until started.")


class TestGMAddLandmark(unittest.TestCase):  # Chris Kirst
    def setUp(self):
        self.con = Controller()
        self.con.currentUser = "admin"

    def test_AddLandMark(self):
        self.con.create_landmark("park", "there are benches", "who is fountain dedicated to?", "St. Python")
        landmark = self.con.System.getLandmark("park")
        self.assertEquals(landmark.name, "park", "Landmark name is not correct")
        self.assertEquals(landmark.clue, "there are benches", "Landmark question is not correct")
        self.assertEquals(landmark.question, "who is the fountain dedicated to?",
                          "Landmark question is not correct")
        self.assertEquals(landmark.answer, "St. Python", "Landmark answer is not correct")

    def test_AddBadLandmark(self):
        self.assertEquals(self.con.create_landmark("", "", "", ""), "Invalid landmark argument(s)",
                          "Adding blank landmark should fail")


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.con = Controller()

    def test_badlogin(self):
        self.con.login("cheater", "sargreat")
        self.assertEqual(self.con.currentUser, None, "Nice try, User scum. Bad username test.")
        self.con.login("admin", "sarpoo")
        self.assertEqual(self.con.currentUser, None, "Nice try, User scum. Bad password test.")

    def test_goodlogin(self):
        self.con.login("admin", "kittens")
        self.assertEqual(self.con.currentUser, "admin", "Admin not successfully logged in.")


class LogoutTest(unittest.TestCase):
    def setUp(self):
        self.con = Controller()
        self.con.username = "admin"

    def test_goodlogout(self):
        self.con.logout()
        self.assertEqual(self.con.currentUser, None, "Current user should be null after logout")


class TestStartGame(unittest.TestCase):
    def setUp(self):
        self.con = Controller()
        self.User = user.User()
        self.User.name = "admin"
        self.Game = game.Game(self.con.System)

    def test_goodstart(self):
        self.con.start_game()
        self.assertTrue(self.Game.isActive, "Game not begun successfully!")

    def test_badStart(self):
        self.Game.isActive = True
        self.con.start_game()
        self.assertTrue(self.Game.isActive, "Calling start game on an active game should do nothing")


class TestEndGame(unittest.TestCase):
    def setUp(self):
        self.con = Controller()
        self.User = user.User()
        self.User.name = "admin"
        self.Game = game.Game(self.con.System)
        self.Game.isActive = True

    def test_endGame(self):
        self.con.end_game()
        self.assertFalse(self.Game.isActive, "End game did not successfully stop the game")

    def test_endGameOnAlreadyEndedGame(self):
        self.Game.isActive = False
        self.con.end_game()
        self.assertFalse(self.Game.isActive, "End game on a non-active game should stay non-active")'''
        
