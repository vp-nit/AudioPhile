# Generated by Django 2.1.15 on 2021-02-08 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comfort', models.IntegerField(default=0)),
                ('performance', models.IntegerField(default=0)),
                ('durability', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Product')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Profile')),
            ],
        ),
    ]
