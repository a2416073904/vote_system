from django.db import models

# Create your models here.

class Problem(models.Model):
    pid = models.AutoField(primary_key=True)  # 问题主键唯一
    description = models.CharField(max_length=200) # 设置问题描述
    problem_type = models.IntegerField()  # 设置问题类型 0:单选 1：多选 2：问答
    
    def __str__(self):  # 重写直接输出类的方法
        return '<Problem:{{pid={0}, description={1}, problem_type={2} }}>\n'.format(self.pid, self.description, self.problem_type)


class Option(models.Model):
    oid = models.AutoField(primary_key=True) # 选项主键唯一
    problem = models.ForeignKey("Problem", on_delete=models.CASCADE) # 设置关联问题
    option = models.CharField(max_length=50, null=True) # 设置选项内容

    def __str__(self):
        return '<Option:{{ oid={0}, problem={1}, option={2} }}>\n'.format(self.oid, self.problem, self.option)
        

class Vote(models.Model):
    vid = models.AutoField(primary_key=True)  # 投票主键唯一
    uid = models.CharField(max_length=32) # 设置投票用户
    problem = models.ForeignKey("Problem", on_delete=models.CASCADE) # 设置投票问题 
    option  = models.ForeignKey("Option", on_delete=models.CASCADE, null=True) # 设置投票选项（仅选择题有，其余时候为空）
    content = models.CharField(max_length=300, null=True) # 设置问题回答内容（仅问答题有，其余时候为空）

    def __str__(self):
        return '<Vote:{{ vid={0}, uid={1}, problem={2}, option={3}, content={4} }}>\n'.format(self.vid, self.uid, self.problem, 
        self.option, self.content)

class  QuestionList(models.Model):
    qid = models.AutoField(primary_key=True)  # 问卷ID
    question_title = models.CharField(max_length = 12)  # 问卷标题
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)  # 问卷创建时间
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True) # 设置开始时间
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)  # 设置结束时间
    answer_num = models.IntegerField()  # 答卷数量
    state = models.IntegerField()  # 设置问卷状态 0：草稿 1：发布 2：结束

    def __str__(self):
        return '<QuestionList:{{ qid={0}, question_title={1} create_time={2}, start_time={3}, end_time={4}, answer_num={5}, state={6} }}>\n'.format(self.qid,
        self.question_title, self.create_time, self.start_time, self.end_time, self.answer_num, self.state)

class QuestionProblem(models.Model):
    id = models.AutoField(primary_key=True)  # 问卷列表与问题关联表ID
    problem = models.OneToOneField("Problem", on_delete=models.CASCADE)    # 关联问题
    question_list = models.ForeignKey("QuestionList", on_delete=models.CASCADE)  # 关联问卷

    def __str__(self):
        return '<QuestionProblem:{{ id={0}, problem={1}, question_list={2} }}>\n'.format(self.id, self.problem, self.question_list)





