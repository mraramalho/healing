# Generated by Django 5.0.4 on 2024-04-20 21:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0003_alter_dadosmedico_crm_alter_dadosmedico_rg_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HorariosDisponiveis',
            new_name='CadastroAgenda',
        ),
    ]
