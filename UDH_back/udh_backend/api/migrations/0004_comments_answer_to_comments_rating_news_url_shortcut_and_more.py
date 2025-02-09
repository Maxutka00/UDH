# Generated by Django 4.2.10 on 2024-03-26 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_users_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='answer_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.comments'),
        ),
        migrations.AddField(
            model_name='comments',
            name='rating',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='url_shortcut',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articles',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='comments',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.articles'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='edit_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.news'),
        ),
        migrations.AlterField(
            model_name='news',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='topics',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
