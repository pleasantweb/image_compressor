# Generated by Django 3.2.7 on 2021-10-13 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compressor', '0008_upload_orignal_size_x_y'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Compressed',
        ),
    ]
