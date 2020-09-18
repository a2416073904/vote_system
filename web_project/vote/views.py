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

# show questionList page
def index(request):
    return render(request, 'index.html')


# show questionsList datail page
def qustions_detail(request, qid):
    return render(request, 'questionsDetail.html')



def questions_lists(request):
    questionLists = list(models.QuestionList.objects.all())

    questionLists = serializers.serialize("json", questionLists)

    logger.info(questionLists)

    return HttpResponse(questionLists)

# 
def question_list_detail(request, qid):
    questionList = models.QuestionList.objects.get(qid = qid)
    question_problems = questionList.questionproblem_set.all()  #h获取问卷关联问题ID
    
    result = {}
    problems = []
    problem_options = []
    for x in question_problems:
        p = models.Problem.objects.get(pid = x.problem.pid)
        tmep_list = p.option_set.all()
        logger.info(tmep_list)
        temp_dict = {}
        for o in tmep_list:
            logger.info(o)
            o.__dict__.pop("_state")
            temp_dict["problem_option"+ str(o.oid)] = o.__dict__
        problem_options.append(temp_dict)

        x.problem.__dict__.pop("_state")
        problems.append(x.problem.__dict__)

    result['problems'] = problems
    questionList.__dict__.pop("_state")
    result['questionList'] = questionList.__dict__
    result['problem_options'] = problem_options

    return JsonResponse(result, safe=False)
    

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
    if request.method == 'PUT':
        pid = request.POST.get('pid')

    problem = models.Problem.objects.get(pid = pid)
    problem.end_time = '2020-09-22 20:00:00'
    problem.save()

    logger.info(problem)
    return HttpResponse('问题{0}修改成功'.format(problem.pid))

# delete problem
def delete_problem(request):
    if request.method == 'DELEDE':
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

