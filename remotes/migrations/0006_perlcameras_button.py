# Generated by Django 4.0.5 on 2022-07-04 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0005_perlcameras_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='perlcameras',
            name='button',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='remotes.perlbuttons'),
            preserve_default=False,
        ),
    ]