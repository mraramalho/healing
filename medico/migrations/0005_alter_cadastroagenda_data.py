# Generated by Django 5.0.4 on 2024-04-20 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0004_rename_horariosdisponiveis_cadastroagenda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadastroagenda',
            name='data',
            field=models.DateTimeField(),
        ),
    ]