# Generated by Django 4.2 on 2023-05-12 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Jobs', '0005_alter_applyjob_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='days',
        ),
        migrations.AddField(
            model_name='job',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Jobs.position'),
        ),
    ]
