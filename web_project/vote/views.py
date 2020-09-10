from django.shortcuts import render     # 可以用来返回我们渲染的html文件
from django.http import HttpResponse    # 可以返回渲染的页面
from . import models             # 导入我们的模型类
import logging
import uuid
from django.http import JsonResponse
import json
from django.core import serializers

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create your views here.

# test page
def test(request):
    return render(request, 'test.html', {})

# show questionList list
def index(request):
    questionLists = list(models.QuestionList.objects.all())

    questionLists = serializers.serialize("json", questionLists)
    data = {
        'questionLists': questionLists
    }
    return render(request, 'index.html', data)


def question_list_detail(request, qid):
    question_list = models.QuestionList.objects.get(qid)
    question_problem = models.QuestionProblem.objects.get()

    problmes = list()
    

# add problem
def add_problem(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        problem_type = request.POST.get('type')
        options = request.POST.get('options')
    
    problem = models.Problem(description = description, problem_type = problem_type)
    problem.save()


    logger.info(problem.pid)
    for option in options:
        models.Option(problem = problem, option = option)

    logger.info(problem)
    logger.info(*options)
    return HttpResponse('问题：{0}\n添加成功'.format(problem.description))

# edit problem
def edit_problem(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')

    problem = models.Problem.objects.get(pid = pid)
    problem.end_time = '2020-09-22 20:00:00'
    problem.save()

    logger.info(problem)
    return HttpResponse('问题{0}修改成功'.format(problem.pid))

# delete problem
def delete_problem(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
    problem = models.Problem.objects.get(pid = pid)
    problem.delete()
    
    return HttpResponse('问题{0}删除成功'.format(pid))

# vote 
def user_vote(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        oid = request.POST.get('oid')
        content = request.POST.get('content')
    
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    vote = models.Vote(uid = suid, problem_vfield = models.Problem.objects.get(pid = pid), option_vfield = models.Option.objects.get(oid = oid), content = content)
    vote.save()

    return HttpResponse('{0}投票问题{1}成功'.format(suid, pid))

