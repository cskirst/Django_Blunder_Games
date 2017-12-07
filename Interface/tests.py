from django.test import TestCase
from Interface.models import Game, Landmarks, User
from .controller import Controller
'''
from .Interface import Interface
from .controller import Controller
'''

# Create your tests here.

class TestStartGame(TestCase):
    def setUp(self):
        Game.objects.create(name="game1")
        self.g1 = Game.objects.get(name="game1")
        User.objects.create(name="user1", password="pass1", currentLandmark=0, game=self.g1)
        u1 = User.objects.get(name="user1")
        self.controller = Controller()
        self.controller.currentUser = "user1"
        self.controller.Game = self.g1
    def test_beforeStart(self):
        self.assertFalse(self.g1.isActive, "Game should be inactive before start")
    def test_badStartGame(self):
        self.controller.start_game("game1")
        self.assertFalse(self.g1.isActive, "Game should not be toggled on non-admin user")
    def test_normalStartGame(self):
        self.controller.currentUser = "admin"
        self.controller.start_game("game1")
        self.assertTrue(self.controller.Game, "Game should be active after admin calls start game")

class TestEndGame(TestCase):
    def setUp(self):
        Game.objects.create(name="game1", isActive=True)
        self.g1 = Game.objects.get(name="game1")
        Landmarks.objects.create(name="landmark1", question="question1", clue="clue1", answer="answer1", position=0,game=self.g1)
        l1 = Landmarks.objects.get(name="landmark1")
        Landmarks.objects.create(name="landmark2", question="question2", clue="clue2", answer="answer2", position=1,game=self.g1)
        l2 = Landmarks.objects.get(name="landmark2")
        User.objects.create(name="user1", password="pass1", currentLandmark=0, game=self.g1)
        u1 = User.objects.get(name="user1")
        self.controller = Controller()
        self.controller.currentUser = "user1"
        self.controller.Game = self.g1
        self.controller.LandmarkList = [l1, l2]
        self.g1.isActive = True
    def test_beforeEnd(self):
        self.assertTrue(self.g1.isActive, "Game should be active before calling end game")
    def test_badEndGame(self):
        self.controller.end_game("game1")
        self.assertTrue(self.g1.isActive, "Game should still be active after non-admin user calls end game")
    def test_normalEndGame(self):
        self.controller.currentUser = "admin"
        self.controller.end_game("game1")
        self.assertFalse(self.controller.Game.isActive, "Game should be inactive after admin calls end game")

class TestGMCreateGame(TestCase):
    def setUp(self):
        self.con = Controller()
        Game.objects.create(name="game1")
        g1 = Game.objects.get(name="game1")
        self.con.currentUser = "admin"

    def test_createGame(self):

        print(self.con.create_game("game2"))
        g2 = Game.objects.get(name="game2")
        Landmarks.objects.create(name="landmark1", question="question1", clue="clue1", answer="answer1", position=0,game=g2)
        User.objects.create(name="user1", password="pass1", currentLandmark=0, game=g2)
        lm = Landmarks.objects.get(name="landmark1")
        self.con.Game = g2
        self.con.createlandmarklist()
        self.assertEquals(len(self.con.LandmarkList), 1, "Assigned landmarks in game not correct")
        self.assertEqual(self.con.LandmarkList[0], lm, "Landmark in Landmark List not correct!")
        #FUTURE: self.assertEqual(self.con.Game.clock, 0, "Clock should not be started until Game maker initiates game")
        self.assertFalse(self.con.Game.isActive, "Game should not be active until started.")
        self.con.Game.toggleActive()
        self.assertTrue(self.con.Game.isActive, "Game should be active!")

class TestCreateLandmarkList(TestCase):
    def setUp(self):
        Game.objects.create(name="game1")
        Game.objects.create(name="game2")
        g1 = Game.objects.get(name="game1")
        g2 = Game.objects.get(name="game2")
        Landmarks.objects.create(name="landmark2", question="question2", clue="clue2", answer="answer2", position=0,
                                 game=g2)
        Landmarks.objects.create(name="landmark1", question="question1", clue="clue1", answer="answer1", position=0,
                                 game=g1)
        self.con = Controller()
        self.con.Game = g1
        self.con.currentUser = User.objects.get(name="admin")

    def test_LandmarkList(self):
        l1 = Landmarks.objects.get(name="landmark1")
        self.con.createlandmarklist()
        self.assertEqual(len(self.con.LandmarkList), 1, "Landmark List not created correctly!")
        self.assertEqual(self.con.LandmarkList[0], l1, "Landmark List not correct!")

    def test_BadLandmarkList(self):
        l2 = Landmarks.objects.get(name="landmark2")
        self.con.createlandmarklist()
        self.assertNotEqual(self.con.LandmarkList[0], l2, "Landmark in Landmark List should be wrong!")


class TestCreateLandmarkList(TestCase):
    def setUp(self):
        Game.objects.create(name="game1")
        Game.objects.create(name="game2")
        g1 = Game.objects.get(name="game1")
        g2 = Game.objects.get(name="game2")
        Landmarks.objects.create(name="landmark2", question="question2", clue="clue2", answer="answer2", position=0,game=g2)
        Landmarks.objects.create(name="landmark1", question="question1", clue="clue1", answer="answer1", position=0,game=g1)
        self.l1 = Landmarks.objects.get(name="landmark1")
        self.l2 = Landmarks.objects.get(name="landmark2")
        self.con = Controller()
        self.con.Game = g1
        self.con.currentUser = "admin"

    def test_LandmarkList(self):
        #l1 = Landmarks.objects.get(name="landmark1")
        self.con.createlandmarklist()
        self.assertEqual(len(self.con.LandmarkList), 1, "Landmark List not created correctly!")
        self.assertEqual(self.con.LandmarkList[0], self.l1, "Landmark List not correct!")

    def test_BadLandmarkList(self):
        #l2 = Landmarks.objects.get(name="landmark2")
        self.con.createlandmarklist()
        self.assertNotEqual(self.con.LandmarkList[0], self.l2, "Landmark in Landmark List should be wrong!")


class TestCreateLandmark(TestCase):
    def setUp(self):
        Game.objects.create(name="game1")
        self.g1 = Game.objects.get(name="game1")
        User.objects.create(name="admin", password="kittens", currentLandmark=0, game=self.g1)
        self.a1 = User.objects.get(name="admin")
        User.objects.create(name="u1", password="cats", currentLandmark=0, game=self.g1)
        self.u1 = User.objects.get(name="u1")
        self.list1 = []
        self.controller1 = Controller()
        self.controller1.currentUser = "admin"
        self.controller1.Game = self.g1
        self.controller1.LandmarkList = self.list1

    def test_createLandmarkBadArgs(self):
        self.assertEqual(self.controller1.check(["create", "landmark", "badlm1"], "admin"), "Bad landmark credentials","Create landmark not recognizing bad input")

    def test_createLandmarkGood(self):
        self.controller1.create_landmark("l1", "c1", "q1", "a1", self.g1, 0)
        l1 = Landmarks.objects.get(name="l1")
        self.assertEqual(l1.name, "l1","Incorrectly creating landmark")

    def test_badUserCreate(self):
        self.controller1.currentUser = self.u1
        self.assertEqual(self.controller1.create_landmark("l1", "c1", "q1", "a1", self.g1, 0),"Must be admin to create landmark", "Must be admin to create")


class TestAnswerQuestion(TestCase):
    def setUp(self):
        Game.objects.create(name="game1")
        self.g1 = Game.objects.get(name="game1")
        Landmarks.objects.create(name="l1", clue="c1", question="q1", answer="a1", game=self.g1, position=0)
        Landmarks.objects.create(name="l2", clue="c2", question="q2", answer="a2", game=self.g1, position=1)
        self.l1 = Landmarks.objects.get(name="l1")
        self.l2 = Landmarks.objects.get(name="l2")
        self.list1 = [self.l1, self.l2]
        User.objects.create(name="u1", password="p1", currentLandmark=0, game=self.g1)
        self.u1 = User.objects.get(name="u1")
        self.controller1 = Controller()
        self.controller1.currentUser = "u1"
        self.controller1.Game = self.g1
        self.controller1.LandmarkList = self.list1

    def test_rightAnswer(self):
        self.assertEqual(self.controller1.answer_question("a1"), "Correct! Your next clue is: c2", "Answer Question not working")

    def test_incrementLandmark(self):
        self.controller1.answer_question("a1")
        desubaka = User.objects.get(name=self.controller1.currentUser)
        self.assertEqual(desubaka.currentLandmark, 1, "Not incrementing users position")

    def test_winGame(self):
        #setattr(self.u1,"currentLandmark",1)
        self.controller1.answer_question("a1")
        #self.u1.currentLandmark = 1
        self.assertEqual(self.controller1.answer_question("a2"), "You finished!","Answering last question not registering win game.")

class TestGetClue(TestCase):
    def setUp(self):
        game1 = Game.objects.create(name="game1")
        User.objects.create(name= "u1", password="p1", currentLandmark=0, game=game1)
        l1 = Landmarks.objects.create(name="name1", clue="clue1", question="question1", answer="answer1", position=0, game=game1)
        l2 = Landmarks.objects.create(name="name2", clue="clue2", question="question2", answer="answer2", position=1, game=game1)
        self.controller = Controller()
        self.controller.LandmarkList = [l1, l2]

    def test_clue(self):
        landmark = Landmarks.objects.get(name="name1")
        self.assertEqual(self.controller.LandmarkList[0].clue, landmark.clue, "Clue mismatch")

    def test_getclue(self):
        landmark = Landmarks.objects.get(name="name1")
        self.assertEqual(self.controller.LandmarkList[0].getClue(), landmark.clue, "GetClue incorrect")


class TestGetQuestion(TestCase):
    def setUp(self):
        game1 = Game.objects.create(name="game1")
        User.objects.create(name= "u1", password="p1", currentLandmark=0, game=game1)
        l1 = Landmarks.objects.create(name="name1", clue="clue1", question="question1", answer="answer1", position=0, game=game1)
        l2 = Landmarks.objects.create(name="name2", clue="clue2", question="question2", answer="answer2", position=1, game=game1)
        self.controller = Controller()
        self.controller.LandmarkList = [l1, l2]

    def test_question(self):
        landmark = Landmarks.objects.get(name="name1")
        self.assertEqual(self.controller.LandmarkList[0].question, landmark.question, "Clue mismatch")

    def test_getquestion(self):
        landmark = Landmarks.objects.get(name="name1")
        self.assertEqual(self.controller.LandmarkList[0].getQuestion(), landmark.question, "GetClue incorrect")

class TestCreateUser(TestCase):
    def setUp(self):
        self.game = Game.objects.create(name = "game1")
        User.objects.create(name="u1", password="p1", currentLandmark=0, game=self.game)
        self.u1 = User.objects.get(name="u1")
        self.con = Controller()
        self.con.currentUser = "admin"

    def test_create_user_success(self):
        self.assertEqual(self.u1.name, User.objects.get(name="u1").name)

    def test_createUserCredFailure(self):
        self.assertEqual("Invalid team credentials.", self.con.create_team("", "", self.game), "Team should not be created")


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

