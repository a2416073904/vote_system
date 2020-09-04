from django.db import models

# Create your models here.

class Problem(models.Model):
    pid = models.AutoField(primary_key=True)  # 问题主键唯一
    description = models.CharField(max_length=200) # 设置问题描述
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)  # 问题创建时间
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False) # 设置结束时间
    problem_type = models.IntegerField()  # 设置问题类型 0:单选 1：多选 2：问答
    problem_state = models.IntegerField() # 设置问题状态 0：创建 1：发布 2：结束

    def __str__(self):  # 重写直接输出类的方法
        return '<Problem:{{pid={0}, description={1}, create_time={2}, end_time={3}, problem_type={4}, \
        problem_state={5} }}>\n'.format(self.pid, self.description, self.create_time, self.end_time, self.problem_type, self.problem_state)


class Option(models.Model):
    oid = models.AutoField(primary_key=True) # 选项主键唯一
    problem_ofield = models.ForeignKey("Problem", on_delete=models.CASCADE) # 设置关联问题
    option = models.CharField(max_length=50, null=True) # 设置选项内容

    def __str__(self):
        return '<Option:{{ oid={0}, pid={1}, option={2} }}>\n'.format(self.oid, self.pid, self.option)
        

class Vote(models.Model):
    vid = models.AutoField(primary_key=True)  # 投票主键唯一
    uid = models.CharField(max_length=32) # 设置投票用户
    problem_vfield = models.ForeignKey("Problem", on_delete=models.CASCADE) # 设置投票问题 
    option_vfield  = models.ForeignKey("Option", on_delete=models.CASCADE, null=True) # 设置投票选项（仅选择题有，其余时候为空）
    content = models.CharField(max_length=300, null=True) # 设置问题回答内容（仅问答题有，其余时候为空）

    def __str__(self):
        return '<Vote:{{ vid={0}, uid={1}, pid={2}, oid={3}, content={4} }}>\n'.format(self.vid, self.uid, self.pid, 
        self.oid, self.content)




