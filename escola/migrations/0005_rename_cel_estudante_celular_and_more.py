# Generated by Django 5.1.4 on 2024-12-19 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0004_alter_curso_codigo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estudante',
            old_name='cel',
            new_name='celular',
        ),
        migrations.RenameField(
            model_name='estudante',
            old_name='data_nasciemtno',
            new_name='data_nascimento',
        ),
    ]
