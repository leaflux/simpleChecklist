from __future__ import unicode_literals

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from simpleChecklist.models import TodoList, Task


class TodoListMethodTests(TestCase):

    def test_list_char_limit(self):
        """
        Tests the character limit on TodoList names, which should be 35.
        """
        thirtyFiveChars = "testtesttesttesttesttesttesttesttet"
        thirtySixChars = "testtesttesttesttesttesttesttesttest"
        user = User.objects.create_user('tester', 'tester@gmail.com', 'testerrrr')

        todolist1 = TodoList(name=thirtyFiveChars, user=user)
        todolist1.save()
        todolist2 = TodoList(name=thirtySixChars, user=user)
        todolist2.save()
        self.assertEqual((len(todolist1.name) <= 35), True)
        self.assertEqual((len(todolist2.name) <= 35), True)

class TaskMethodTests(TestCase):

    def test_task_char_limits(self):
        """
        Tests the character limits on Task names and notes, which should be 35 and 40 respectively.
        """
        thirtyFiveChars = "testtesttesttesttesttesttesttesttet"
        thirtySixChars = "testtesttesttesttesttesttesttesttest"
        fortyChars = "testtesttesttesttesttesttesttesttestTEST"
        fortyOneChars = "testtesttesttesttesttesttesttesttestTETST"

        user = User.objects.create_user('tester', 'tester@gmail.com', 'testerrrr')

        todolist = TodoList(name=thirtyFiveChars, user=user)
        todolist.save()

        task1 = Task(todolist=todolist, name=thirtyFiveChars, note=fortyChars, priority='1')
        task1.save()
        task2 = Task(todolist=todolist, name=thirtySixChars, note=fortyOneChars, priority='1')
        task2.save()

        self.assertEqual((len(task1.name) <= 35), True)
        self.assertEqual((len(task2.name) <= 35), True)
        self.assertEqual((len(task1.note) <= 40), True)
        self.assertEqual((len(task2.note) <= 40), True)
