# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from simpleChecklist.models import TodoList, Task

class TodoListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Task, TaskAdmin)
