# Generated by Django 2.0.7 on 2018-08-06 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20180806_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.Slot'),
        ),
    ]
