# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.template.defaultfilters import slugify
from datetime import datetime
from django.contrib.auth.models import User

# TodoLists are here to contain Tasks. When making one, the user can only control the Name field.
# TodoLists also have a User field, which is the user that created it. I use this to prevent
# users from editing other users' lists.
class TodoList(models.Model):
    # After testing with capital Ws, I can fit about 35 characters in the name field
    name = models.CharField(max_length=35)
    # Just a normal slug field to help make the URL
    slug = models.SlugField()

    created_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, default='')

    def save(self, *args, **kwargs):
        if len(self.name) > 35:
            self.name = self.name[:35]

        self.slug = slugify(self.name)
        super(TodoList, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    # With the name and user fields set to be unique in combination,
    # multiple todolists with the same name can be made by different users,
    # but multiple todolists with the same name can't be made by the same user.
    class Meta:
        unique_together = (("name", "user"),)

# Tasks are the actual content of the TodoLists. Aside from a Name, they have a Due Date
# (any date, even in the past), Priority (Low, Medium or High), and a Note (any extra text the user wants)
class Task(models.Model):
    # one-to-many relationship with TodoLists set up here
    todolist = models.ForeignKey(TodoList)
    name = models.CharField(max_length=35)
    slug = models.SlugField()

    note = models.TextField(max_length=40)
    date = models.DateField(blank=False, default=datetime.now)
    created_on = models.DateField(auto_now_add=True)

    LOW = "1"
    NORMAL = "2"
    HIGH = "3"
    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
    )
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default=NORMAL,
    )

    def save(self, *args, **kwargs):
        if len(self.name) > 35:
            self.name = self.name[:35]

        if len(self.note) > 40:
            self.note = self.note[:40]

        self.slug = slugify(self.name)
        super(Task, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
