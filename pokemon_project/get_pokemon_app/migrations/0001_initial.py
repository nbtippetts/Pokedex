# Generated by Django 2.2.6 on 2019-10-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pokemon_id', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('sprites', models.CharField(max_length=100)),
                ('type1', models.TextField()),
                ('type2', models.TextField()),
            ],
        ),
    ]
