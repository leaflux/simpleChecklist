from django.conf.urls import url
from simpleChecklist import views


urlpatterns = [
    # The main four URLs that show what I intend the user to see
    url(r'^$', views.index, name='index'),
    url(r'^create_todolist/$', views.create_todolist, name='create_todolist'),
    url(r'^todolist/(?P<user_name>[\w.@+-]+)/(?P<todolist_name_slug>[\w\-]+)/$', views.todolist, name='todolist'),
    url(r'^todolist/(?P<user_name>[\w.@+-]+)/(?P<todolist_name_slug>[\w\-]+)/create_task/$', views.create_task, name='create_task'),
    # These three URLs don't have actual templates of their own. Instead they work off of the Index and Todolist templates
    url(r'^delete_todolist/$', views.delete_todolist, name="delete_todolist"),
    url(r'^delete_task/$', views.delete_task, name="delete_task"),
    url(r'^sort_tasks/$', views.sort_tasks, name="sort_tasks"),
]
