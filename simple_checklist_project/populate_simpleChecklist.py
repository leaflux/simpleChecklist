import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_checklist_project.settings')

import django
django.setup()

from simpleChecklist.models import TodoList, Task
import datetime
from django.contrib.auth.models import User

def add_list(name, user):
    l = TodoList.objects.get_or_create(name=name, user=user)[0]
    return l

def add_task(todolist, name, note, priority, date):
    t = Task.objects.get_or_create(todolist=todolist, name=name)[0]
    t.note = note
    t.priority = priority
    t.date = date
    t.save()
    return t

def populate():
    user1 = User.objects.all()[0]
    user2 = User.objects.all()[1]
    prog_list = add_list(
        name='Programming',
        user=user2
    )

    add_task(todolist=prog_list,
        name="Skeleton Code",
        note="try to follow my flowchart better this time",
        priority="1",
        date=datetime.date(2017, 7, 30))

    add_task(todolist=prog_list,
        name="Population Script",
        note="write some clear comments",
        priority="2",
        date=datetime.date(2017, 6, 30))

    chore_list = add_list(
        name='Chores',
        user=user1,
    )

    add_task(todolist=chore_list,
        name="Clean the Kitchen",
        note="get underneath the counters",
        priority="2",
        date=datetime.date(2017, 7, 31))

    free_list1 = add_list(
        name='Free Time',
        user=user1,
    )

    add_task(todolist=free_list1,
        name="Gaming",
        note="set up the console",
        priority="3",
        date=datetime.date(2018, 7, 3))

    add_task(todolist=free_list1,
        name="Reading",
        note="search online for something new",
        priority="2",
        date=datetime.date(2017, 10, 31)
    )

    add_task(todolist=free_list1,
        name="Drinking",
        note="try something snobbish at the wine place",
        priority="1",
        date=datetime.date(2017, 11, 4)
    )

    # Tests whether list name and user are unique together by adding another list
    # with the same name.
    free_list2 = add_list(
        name='Free Time',
        user=user2,
    )

    add_task(todolist=free_list2,
        name="Gaming",
        note="set up the console",
        priority="3",
        date=datetime.date(2018, 7, 3))



    for l in TodoList.objects.all():
        for t in Task.objects.filter(todolist=l):
            print "{0}: {1}".format(str(l), str(t))

if __name__ == '__main__':
    print "Populating simpleChecklist with data..."
    populate()
