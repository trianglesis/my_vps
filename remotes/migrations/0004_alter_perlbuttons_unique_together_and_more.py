# Generated by Django 4.0.5 on 2022-07-04 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0003_perlbuttons_description_perlcameras_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='perlbuttons',
            unique_together={('dom', 'gate', 'mode')},
        ),
        migrations.AlterUniqueTogether(
            name='perlcameras',
            unique_together={('dvr', 'cam')},
        ),
    ]