from django.urls import path
from . import views

urlpatterns = [
    # page
    path('', views.index, name="index"),
    path('questions_detail/<qid>/', views.qustions_detail),
    path('question_vote/<qid>/', views.question_vote),
    path('success/', views.success),


    # CUAD
    path('api/questions_lists/', views.questions_lists),
    path('api/question_list_detail/<qid>/', views.question_list_detail),
    path('api/problem/<pid>/', views.getProblemById),
    # path('api/get_csrf/', views.get_csrf),
    path('api/problem/', views.add_problem),
    path('api/edit/problem/', views.edit_problem),
    path('api/delete/problem/<pid>/', views.delete_problem),
    path('api/user_vote/', views.user_vote),
]
