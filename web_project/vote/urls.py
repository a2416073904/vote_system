from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),

    path('index/', views.index),
    path('manage/', views.manage),
    path('add_problem/', views.add_problem),
    path('edit_problem/<pid>/', views.edit_problem),
    path('delete_problem/<pid>/', views.delete_problem),
    path('user_vote/<pid>/<oid>/<content>/', views.user_vote),
]
