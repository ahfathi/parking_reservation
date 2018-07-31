# Generated by Django 2.0.7 on 2018-07-31 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=32)),
                ('floor', models.IntegerField()),
                ('segment', models.IntegerField()),
            ],
        ),
        migrations.AddIndex(
            model_name='slot',
            index=models.Index(fields=['building', 'floor', 'segment'], name='management__buildin_7d8ace_idx'),
        ),
    ]