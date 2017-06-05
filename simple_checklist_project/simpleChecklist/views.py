# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from simpleChecklist.models import TodoList, Task
from simpleChecklist.forms import TodoListForm, TaskForm

from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse

@login_required
def index(request):

    # Queries the database for all of a user's Todo Lists
    todolist_list = TodoList.objects.filter(user=request.user)

    return render(request, 'simpleChecklist/index.html', {'todolists': todolist_list})

@login_required
def todolist(request, todolist_name_slug, user_name):

    context_dict = {}
    # Gathers all of the tasks' info for the todolist with the given slug,
    # to return as the context
    try:
        todolist = TodoList.objects.get(slug=todolist_name_slug, user=request.user)
        context_dict['todolist_name'] = todolist.name

        # Orders all of the tasks in the given todo list by their due date
        tasks = Task.objects.filter(todolist=todolist)
        context_dict['tasks'] = tasks

        # Used in the template to check whether the todolist exists or not
        context_dict['todolist'] = todolist

        # The username and slug are here to identify the specific todolist,
        # and are combined to make a unique URL.
        context_dict['user_name'] = user_name
        context_dict['todolist_name_slug'] = todolist_name_slug


    except TodoList.DoesNotExist:
        # There's no need to check whether the TodoList exists twice,
        # so I stop that error from raising an exception here.
        pass

    return render(request, 'simpleChecklist/todolist.html', context_dict)

@login_required
# Loads the todo list form from forms.py on GET, saves form info to the todo list data on POST
def create_todolist(request):

    if request.method == 'POST':
        form = TodoListForm(request.POST)

        if form.is_valid():
            todolist = form.save(commit=False)
            todolist.user = request.user
            todolist.save()
            # When a todolist is successfully created, redirects to the page that displays them all
            return redirect(index)

        else:
            print form.errors

    else:
        form = TodoListForm()

    return render(request, 'simpleChecklist/create_todolist.html', {'form': form})

# Basically the same as create_todolist, except with a couple of extra arguments to
# filter out the todo list being added to, and to provide info for the todo list template after
# successfully filling out the form
@login_required
def create_task(request, todolist_name_slug, user_name):

    try:
        currentList = TodoList.objects.get(slug=todolist_name_slug, user=request.user)
    except TodoList.DoesNotExist:
        currentList = None

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            if currentList:
                task = form.save(commit=False)
                task.todolist = currentList
                task.save()
                # Makes sure the todolist template has all the info it needs
                return redirect(todolist, todolist_name_slug=todolist_name_slug, user_name=request.user)

        else:
            print form.errors

    else:
        form = TaskForm()

    context_dict = {'form': form, 'todolist': currentList}
    return render(request, 'simpleChecklist/create_task.html', context_dict)


@login_required
def delete_todolist(request):
    context_dict = {}
    # I use a try/except statement here just in case some sneaky user decides to type in the URL manually
    # on the wrong page. Since this view doesn't have its own template, that causes errors.
    try:
        # How this data gets here:
        # data-listid (index template) -> listid (javascript) -> list_id (request)
        list_id = request.GET['list_id']

    except MultiValueDictKeyError:
        error_type = "Bad URL"
        context_dict['error_type'] = error_type

        error_message = "Did you get here on accident? Try going back to the home page."
        context_dict['error_message'] = error_message

        return render(request, 'simpleChecklist/error.html', context_dict)

    except UnboundLocalError:
        error_type = "Bad URL"
        context_dict['error_type'] = error_type

        error_message = "Something went horribly wrong with the URL. Go back to the home page and try again."
        context_dict['error_message'] = error_message

        return render(request, 'simpleChecklist/error.html', context_dict)

    # This 'should' always be true, since the delete buttons are hidden whenever their lists are
    if list_id:
        todolist = TodoList.objects.get(id=list_id)
        todolist.delete()

    # If something goes horribly wrong, sends the user back to the homepage before doing anything
    else:
        return redirect(index)

    # Lines up the context with what the original index page template displays, with
    # the deleted list now gone
    todolist_list = TodoList.objects.filter(user=request.user)
    context_dict['todolists'] = todolist_list

    # Sends template info to an alternate template, index_alt, which holds HTML
    # for the jQuery to load into the original template
    return render(request, 'simpleChecklist/index_alt.html', context_dict)

# Pretty much a rehash of the delete_todolist function, except it grabs the deleted task's
# todo list id in order to update the template's task list after a task is deleted
@login_required
def delete_task(request):
    context_dict = {}
    try:
        task_id = request.GET['task_id']
    except MultiValueDictKeyError:
        error_type = "Bad URL"
        context_dict['error_type'] = error_type

        error_message = "Did you get here on accident? Try going back to the home page."
        context_dict['error_message'] = error_message

        return render(request, 'simpleChecklist/error.html', context_dict)

    except UnboundLocalError:
        error_type = "Bad URL"
        context_dict['error_type'] = error_type

        error_message = "Something went horribly wrong with the URL. Go back to the home page and try again."
        context_dict['error_message'] = error_message

        return render(request, 'simpleChecklist/error.html', context_dict)

    if task_id:
        list_id = request.GET['list_id']

        if list_id:
            task = Task.objects.filter(id=task_id)
            task.delete()
            todolist = TodoList.objects.filter(id=list_id)[0]
            context_dict['todolist'] = todolist
            # Finds the new list of tasks here
            tasks = Task.objects.filter(todolist=todolist)
            context_dict['tasks'] = tasks

        else:
            return redirect(index)

    else:
        return redirect(index)

    return render(request, 'simpleChecklist/todolist_alt.html', context_dict)

# Sorts the task table by whatever data-sorttype specifies, with no need for branching if statements
def sort_tasks(request):
    context_dict = {}
    try:
        list_id = request.GET['list_id']

    except MultiValueDictKeyError:
        error_type = "Bad URL"
        context_dict['error_type'] = error_type

        error_message = "Did you get here on accident? Try going back to the home page."
        context_dict['error_message'] = error_message

        return render(request, 'simpleChecklist/error.html', context_dict)

    sort_type = request.GET['sort_type']


    if list_id and sort_type:
        todolist = TodoList.objects.filter(id=list_id)[0]
        context_dict['todolist'] = todolist

        tasks = Task.objects.filter(todolist=todolist).order_by(sort_type)
        context_dict['tasks'] = tasks

    else:
        return redirect(index)

    return render(request, 'simpleChecklist/todolist_alt.html', context_dict)
