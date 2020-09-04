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

# Query all questions with status 1 
def index(request):
    problems = list(models.Problem.objects.filter(problem_state=1))

    logger.info(*problems)

    problems = serializers.serialize("json", problems)
    data = {
        'problems': problems
    }
    return JsonResponse(data)

# manager page
def manage(request):
    problems = list(models.Problem.objects.all())

    logger.info(*problems)

    problems = serializers.serialize("json", problems)
    data = {
        'problems': problems
    }
    return JsonResponse(data)


# add problem
def add_problem(request):
    problem = models.Problem(description='你喜欢什么水果？', end_time='2020-09-22 16:00:00', problem_type = 0, problem_state=1)
    if problem is not None:
        problem.save()


    logger.info(problem.pid)
    option1 = models.Option(problem_ofield = problem, option = '苹果')
    option2 = models.Option(problem_ofield = problem, option = '香蕉')
    option3 = models.Option(problem_ofield = problem, option = '梨子')
    options = [option1, option2, option3]

    

    if options is not None:
        for x in options:
            x.save()

    logger.info(problem)
    logger.info(*options)
    return HttpResponse('问题：{0}\n添加成功'.format(problem.description))

# edit problem
def edit_problem(request, pid):
    problem = models.Problem.objects.get(pid = pid)
    problem.end_time = '2020-09-22 20:00:00'
    problem.save()

    logger.info(problem)
    return HttpResponse('问题{0}修改成功'.format(problem.pid))

# delete problem
def delete_problem(request, pid):
    problem = models.Problem.objects.get(pid = pid)
    problem.delete()
    
    return HttpResponse('问题{0}删除成功'.format(pid))

# vote 
def user_vote(request, pid, oid, content):
    
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    vote = models.Vote(uid = suid, problem_vfield = models.Problem.objects.get(pid = pid), option_vfield = models.Option.objects.get(oid = oid), content = content)
    vote.save()

    return HttpResponse('{0}投票问题{1}成功'.format(suid, pid))