# Generated by Django 3.1.4 on 2021-01-01 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perseptivTest', '0002_auto_20201228_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonnalInfos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=25)),
                ('age', models.IntegerField(default=20)),
                ('email', models.EmailField(default='', max_length=45)),
                ('musician', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='answers',
            name='age',
        ),
        migrations.RemoveField(
            model_name='answers',
            name='email',
        ),
        migrations.RemoveField(
            model_name='answers',
            name='musician',
        ),
        migrations.RemoveField(
            model_name='answers',
            name='name',
        ),
    ]
