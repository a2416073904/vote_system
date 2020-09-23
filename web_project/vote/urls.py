from django.urls import path
from . import views

urlpatterns = [
    # page
    path('', views.index, name="index"),
    path('qustions_detail/<qid>/', views.qustions_detail),


    # CUAD
    path('api/questions_lists/', views.questions_lists),
    path('api/question_list_detail/<qid>/', views.question_list_detail),
    path('api/problem/<pid>/', views.getProblemById),
    # path('api/get_csrf/', views.get_csrf),
    path('api/problem/', views.add_problem),
    path('api/edit/problem/', views.edit_problem),
    path('api/delete/problem/<pid>/', views.delete_problem),
    path('api/user_vote/<pid>/<oid>/<content>/', views.user_vote),
]
