# Generated by Django 3.1.1 on 2020-09-11 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_auto_20200908_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionlist',
            name='question_title',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='questionproblem',
            name='problem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vote.problem'),
        ),
    ]