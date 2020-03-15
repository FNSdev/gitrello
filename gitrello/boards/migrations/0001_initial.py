# Generated by Django 3.0.3 on 2020-03-14 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BoardMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.Board')),
                ('organization_membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.OrganizationMembership')),
            ],
            options={
                'unique_together': {('board', 'organization_membership')},
            },
        ),
        migrations.AddField(
            model_name='board',
            name='members',
            field=models.ManyToManyField(related_name='boards', through='boards.BoardMembership', to='organizations.OrganizationMembership'),
        ),
        migrations.AddField(
            model_name='board',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='organizations.Organization'),
        ),
        migrations.AlterUniqueTogether(
            name='board',
            unique_together={('name', 'organization')},
        ),
    ]
