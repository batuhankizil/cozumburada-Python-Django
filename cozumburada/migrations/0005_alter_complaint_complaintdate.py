# Generated by Django 4.1.6 on 2023-04-19 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cozumburada', '0004_alter_complaint_title_delete_complaints'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='complaintDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]