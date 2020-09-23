from django.shortcuts import render     # 可以用来返回我们渲染的html文件
from django.http import HttpResponse    # 可以返回渲染的页面
from . import models             # 导入我们的模型类
import logging
import uuid
from django.http import JsonResponse
import json
from django.core import serializers
from django.template.context_processors import csrf

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


# def get_csrf(request):
#         #生成 csrf 数据，发送给前端
#     x = csrf(request)
#     csrf_token = x['csrf_token']
#     return HttpResponse('{} ; {}'.format(str(re), csrf_token))

# select all questionList 
def questions_lists(request):
    questionLists = list(models.QuestionList.objects.all())

    questionLists = serializers.serialize("json", questionLists)

    logger.info(questionLists)

    return HttpResponse(questionLists)

# select questionList detail
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

#select problem by id
def getProblemById(request, pid):
    if request.method != "GET":
        return HttpResponse('403')

    result = {}
    problem_options = []

    problem = models.Problem.objects.get(pid=pid)
    tmep_list = problem.option_set.all()
    logger.info(tmep_list) 
    for o in tmep_list:
        logger.info(o)
        o.__dict__.pop("_state")
        problem_options.append(o.__dict__)
    problem.__dict__.pop("_state")
    result['problem'] = problem.__dict__
    result['problem_options'] = problem_options

    return JsonResponse(result, safe=False)


# add problem
def add_problem(request):
    if request.method != 'PUT':
         return HttpResponse('403')
    
    logger.info(request.body)
    
    data = request.PUT.get('notedata')
    problem_type = request.PUT.get('problem_type')
    qid = request.PUT.get('qid')
    logger.info(problem_type)
    logger.info(data)

    problem_options = data.split('\n\n')
    
    for x in problem_options:
        problem_option = x.split('\n')
        problem = models.Problem(description=problem_option[0], problem_type=problem_type)
        problem.save()
        question_problem = models.QuestionProblem(problem=problem, question_list=models.QuestionList.objects.get(qid=qid))
        question_problem.save()
        
        for i in range(1, len(problem_option)):
            if problem_option[i] != None and problem_option[i] != '':
                option = models.Option(problem=problem, option=problem_option[i])
                option.save()
    
    logger.info(problem.pid)  
    logger.info(problem)

    return HttpResponse('问题：{0}\n添加成功'.format(problem.description))

# edit problem
def edit_problem(request):
    if request.method != 'POST':
        return HttpResponse('403')

    pid = request.POST.get("editProblem[pid]")
    edit_options = request.POST.get('editOptions')

    problem = models.Problem.objects.get(pid=pid)
    problem.description = request.POST.get("editProblem[description]")
    
    problem.save()

    count = 0
    for x in edit_options:
        option = models.Option.objects.get(oid=x.oid)
        if x.option == None or x.option == "":
            option.delete
        else:
            option.option = x.option
            option.save()
        count += 1

    logger.info(problem)
    return HttpResponse('问题{0}修改成功'.format(problem.pid))

# delete problem
def delete_problem(request, pid):
    if request.method != 'DELETE':
        return HttpResponse('403')

    pid2 = request.GET.get('pid')
    problem = models.Problem.objects.get(pid = pid)
    problem.delete()
    
    return HttpResponse('问题{0}删除成功'.format(pid))

# vote 
def user_vote(request):
    if request.method == 'PUT':
        pid = request.POST.get('pid')
        oid = request.POST.get('oid')
        content = request.POST.get('content')
    
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    vote = models.Vote(uid = suid, problem_vfield = models.Problem.objects.get(pid = pid), option_vfield = models.Option.objects.get(oid = oid), content = content)
    vote.save()

    return HttpResponse('{0}投票问题{1}成功'.format(suid, pid))

