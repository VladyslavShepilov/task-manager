# Generated by Django 5.0.2 on 2024-02-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0006_alter_employee_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="type",
            field=models.CharField(
                choices=[
                    ("bug", "Bug"),
                    ("New feature", "new_feature"),
                    ("Change", "change"),
                    ("Refactor", "refactor"),
                    ("QA", "qa"),
                ],
                max_length=20,
            ),
        ),
    ]