from django.test import TestCase

from Interface.models import Game, Landmarks, User
'''
from .Interface import Interface
from .controller import Controller
'''

# Create your tests here.

'''
CreateGame - Chris
StartGame - Derek
EndGame - Derek
CreateLandmark - Thomas
CreateUser - David
AnswerQuestion (and win game) - Thomas
CreateLandmarkList - Chris
Testing views? - Derek
Acceptance Test Document - Thomas
GetClue/GetQuestion - David
'''

'''
CONTROLLER TESTS
'''

class TestGMCreateGame(TestCase):
    def setUp(self):
        Game.objects.create(name="game1")
        Game.objects.create(name="game2")

    def test_createGame(self):
        #listoflandmarks = "park,c,q,a"
        #teamnames = "teamA,passwordA"#user.User
        #realteam = user.User("teamA","passwordA")
        #self.con.create_game(listoflandmarks, teamnames)
        self.con.create_game("park","teamA")
        self.assertEquals(len(self.con.Game.landmarkList), 1, "Assigned landmarks in game not correct")
        self.assertEquals(len(self.con.Game.teams),1, "Assigned teams in game not correct")
        #FUTURE: self.assertEqual(self.con.Game.clock, 0, "Clock should not be started until Game maker initiates game")
        self.assertFalse(self.con.Game.isActive, "Game should not be active until started.")


class TestGMAddLandmark(TestCase):
    def setUp(self):
        self.con = controller.Controller()
        self.con.currentUser = "admin"

    def test_AddLandMark(self):
        self.con.create_landmark("park", "there are benches", "who is fountain dedicated to?", "St. Python")
        landmark = self.con.System.getLandmark("park")
        self.assertEquals(landmark.name, "park", "Landmark name is not correct")
        self.assertEquals(landmark.clue, "there are benches", "Landmark question is not correct")
        self.assertEquals(landmark.question, "who is fountain dedicated to?","Landmark question is not correct")
        self.assertEquals(landmark.answer, "St. Python", "Landmark answer is not correct")

    def test_AddBadLandmark(self):
        self.con.create_landmark("", "", "", "")
        self.assertEquals(len(self.con.System.landmarks), 0,"Adding blank landmark should fail")


class LoginTest(TestCase):
    def setUp(self):
        self.con = controller.Controller()

    def test_badlogin(self):
        self.con.login("cheater", "sargreat")
        self.assertEqual(self.con.currentUser, None, "Nice try, User scum. Bad username test.")
        self.con.login("admin", "sarpoo")
        self.assertEqual(self.con.currentUser, None, "Nice try, User scum. Bad password test.")

    def test_goodlogin(self):
        self.con.login("admin", "kittens")
        self.assertEqual(self.con.currentUser, "admin", "Admin not successfully logged in.")


class LogoutTest(TestCase):
    def setUp(self):
        self.con = controller.Controller()
        self.con.username = "admin"

    def test_goodlogout(self):
        self.con.logout()
        self.assertEqual(self.con.currentUser, None, "Current user should be null after logout")


class TestStartGame(TestCase):
    def setUp(self):
        self.con = controller.Controller()
        self.con.currentUser = "admin"
        self.con.Game = game.Game(self.con.System)

    def test_goodstart(self):
        self.con.start_game()
        self.assertTrue(self.con.Game.isActive, "Game not begun successfully!")

    def test_badStart(self):
        self.con.Game.isActive = True
        self.con.start_game()
        self.assertTrue(self.con.Game.isActive, "Calling start game on an active game should do nothing")


class TestEndGame(TestCase):
    def setUp(self):
        self.con = controller.Controller()
        self.con.currentUser = "admin"
        self.con.Game = game.Game(self.con.System)
        self.con.Game.isActive = True

    def test_endGame(self):
        self.con.end_game()
        self.assertFalse(self.con.Game.isActive, "End game did not successfully stop the game")

    def test_endGameOnAlreadyEndedGame(self):
        self.con.Game.isActive = False
        self.con.end_game()
        self.assertFalse(self.con.Game.isActive, "End game on a non-active game should stay non-active")


'''
GAME TESTS
'''


class TestAddTeamsToGame(TestCase):  # Thomas
    def setUp(self):
        self.con = controller.Controller()
        self.con.currentUser = "admin"
        self.System = system.System()
        self.Game = game.Game(self.con.System)
        self.con.System.teams = {"username": "password", "TeamB": "otherpass", "TeamC": "Lincoln"}

    def test_AddUser(self):
        self.Game.addTeamToGame("TeamB", "bpass")
        self.assertEquals(self.Game.teams[0].name, "TeamB", "TeamB should be first in currentTeams")
        self.Game.addTeamToGame("TeamC", "cpass")
        self.assertEquals(len(self.Game.teams), 2, "Should have two teams in the game")



class TestGetLandmarkList(TestCase):
    def setUp(self):
        self.System = system.System()
        self.Game = game.Game(self.System)
        self.Game.landmarkList = ["Road", "Park"]

    def test_normalGetLandmark(self):
        self.assertEqual(self.Game.getLandmarkList(), ["Road", "Park"], "Return of getLandmarkList() not accurate")
        self.Game.landmarkList = ["Apartment", "The Alamo"]
        self.assertEqual(self.Game.getLandmarkList(), ["Apartment", "The Alamo"], "LandmarkList incorrect after change")

    def test_emptyGetLandmark(self):
        self.Game.landmarkList = []
        self.assertEqual(self.Game.getLandmarkList(), [],
                         "Call to getLandmarkList() when list is empty should return an empty list")


class TestToggleActive(TestCase):
    def setUp(self):
        self.System = system.System()
        self.Game = game.Game(self.System)

    def test_normalToggle(self):
        self.assertFalse(self.Game.isActive, "Game starting out active")
        self.Game.toggleActive()
        self.assertTrue(self.Game.isActive, "Game is not active after call to toggleActive()")


'''
LANDMARKS TESTS
'''
class TestSetClue(TestCase):
    def setUp(self):
        self.Landmark = landmarks.Landmarks("Central Park", "Near the dumpster", "What is the meaning of the universe?",
                                  "The guy right behind you")

    def test_normalSetClue(self):
        self.assertEqual(self.Landmark.clue, "Near the dumpster", "Clue is incorrect to start")
        self.Landmark.setClue("So many tests")
        self.assertEqual(self.Landmark.clue, "So many tests", "Clue not changed on call to setClue()")


class TestGetClue(TestCase):
    def setUp(self):
        Game.objects.create(name="game1")
        g1 = Game.objects.get(name="game1")
        Landmarks.objects.create(name="landmark1", question="question1", clue="clue1", answer="answer1", position=0, game=g1)

    def test_getClue(self):
        landmark = Landmarks.objects.get(name="landmark1")
        self.assertEqual(landmark.getClue(), "clue1", "Clue is not correct!")


class TestGetQuestion(TestCase):
    def setUp(self):
        self.Landmark = landmarks.Landmarks("Central Park", "Near the dumpster", "What is the meaning of the universe?",
                                  "The guy right behind you")

    def test_getQuestion(self):
        self.assertEqual(self.Landmark.getQuestion(), "What is the meaning of the universe?",
                         "GetQuestion() returns incorrect question")


class TestSetQuestion(TestCase):
    def setUp(self):
        self.Landmark = landmarks.Landmarks("Central Park", "Near the dumpster", "What is the meaning of the universe?",
                                  "The guy right behind you")

    def test_normalSetQuestion(self):
        self.Landmark.setQuestion("Who wrote the declaration of independence?")
        self.assertEqual(self.Landmark.question, "Who wrote the declaration of independence?",
                         "Question not set correctly after call to setQuestion()")


class TestSetAnswer(TestCase):
    def setUp(self):
        self.Landmark = landmarks.Landmarks("Central Park", "Near the dumpster", "What is the meaning of the universe?",
                                  "The guy right behind you")

    def test_normalSetAnswer(self):
        self.Landmark.setAnswer("Bologna")
        self.assertEqual(self.Landmark.answer, "Bologna", "Answer not set correctly after call to setAnswer()")


'''
USER TESTS
'''

class TestAcceptanceQuestions(TestCase):
    def setUp(self):
        self.con = controller.Controller()
        self.Interface = interface.Interface(self.con)
        self.con.Game = game.Game(self.con.System)
        self.system = system.System()
        self.user = user.User("newuser","newpass")
        self.con.currentUser = "newuser"
        self.con.Game.teams.append(self.user)
        # self.controller = controller.Controller()
        river = landmarks.Landmarks("River", "test1", "test2", "test3")
        tree = landmarks.Landmarks("Tree", "blah1", "blah2", "blah3")
        self.system.landmarks = [tree, river]
        self.con.Game.landmarkList = [river, tree]

    def test_answer_question_correct(self):
        self.user.currentLandmark = 0
        self.Interface.command("ANSWER QUESTION test3")
        self.assertEquals(self.user.currentLandmark, 1, "Current landmark not incremented after correct answer")

    def test_answer_question_wrong(self):
        self.user.currentLandmark = 0
        self.Interface.command("ANSWER QUESTION badanswer")
        self.assertEquals(self.user.currentLandmark, 0, "Current landmark was incremented after bad answer")

'''
class TestAcceptanceUserStatus(unittest.TestCase):
    def setUp(self):
        self.con = controller.Controller()
        self.game = game.Game(self.con.System)
        self.user = user.User("user","pass")

    def test_userStatusCurrent(self):
        self.game.isActive = True
        self.game.clock = 5
        self.user.currentLandmark = 1
        self.assertEquals(self.user.get_status(), "Time: 5, Landmark: 2","User cannot access current status during game")
'''


class TestAcceptanceGMStatus(TestCase):  # TODO
    def setup(self):
        self.con = controller.Controller()
        self.game = game.Game(self.con.System)

    def test_gm_status_current(self):
        pass


'''
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestGMCreateGame))
suite.addTest(unittest.makeSuite(TestGMAddLandmark))
suite.addTest(unittest.makeSuite(LoginTest))
suite.addTest(unittest.makeSuite(LogoutTest))
suite.addTest(unittest.makeSuite(TestStartGame))
suite.addTest(unittest.makeSuite(TestEndGame))

#Game tests
suite.addTest(unittest.makeSuite(TestAddTeamsToGame))
suite.addTest(unittest.makeSuite(TestGetLandmarkList))
suite.addTest(unittest.makeSuite(TestToggleActive))

#Landmarks tests
suite.addTest(unittest.makeSuite(TestSetClue))
suite.addTest(unittest.makeSuite(TestGetClue))
suite.addTest(unittest.makeSuite(TestGetQuestion))
suite.addTest(unittest.makeSuite(TestSetQuestion))
suite.addTest(unittest.makeSuite(TestSetAnswer))

#System tests
suite.addTest(unittest.makeSuite(TestAddTeam))
suite.addTest(unittest.makeSuite(TestAddTeamAcceptance))

#User tests
suite.addTest(unittest.makeSuite(TestAcceptanceQuestions))
#suite.addTest(unittest.makeSuite(TestAcceptanceUserStatus))
suite.addTest(unittest.makeSuite(TestAcceptanceGMStatus))

runner = unittest.TextTestRunner()
res = runner.run(suite)
print(res)
print("*" * 20)
for i in res.failures: print(i[1])
'''