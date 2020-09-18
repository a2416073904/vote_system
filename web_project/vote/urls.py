from django.urls import path
from . import views

urlpatterns = [
    # page
    path('', views.index, name="index"),
    path('qustions_detail/<qid>', views.qustions_detail),


    # data
    path('api/questions_lists/', views.questions_lists),
    path('api/question_list_detail/<qid>/', views.question_list_detail),
    path('api/problem/', views.add_problem),
    path('api/problem/<pid>/', views.edit_problem),
    path('api/problem/<pid>/', views.delete_problem),
    path('api/user_vote/<pid>/<oid>/<content>/', views.user_vote),
]
