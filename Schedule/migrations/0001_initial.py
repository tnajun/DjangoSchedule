# Generated by Django 3.2.4 on 2024-05-04 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(0, '月曜日'), (1, '火曜日'), (2, '水曜日'), (3, '木曜日'), (4, '金曜日'), (5, '土曜日'), (6, '日曜日')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TherapistGoogleCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_calendar_id', models.CharField(blank=True, max_length=255, null=True)),
                ('google_access_token', models.CharField(blank=True, max_length=255, null=True)),
                ('google_refresh_token', models.CharField(blank=True, max_length=255, null=True)),
                ('google_token_expiry', models.DateTimeField(blank=True, null=True)),
                ('google_credentials', models.TextField(blank=True, null=True)),
            ],
            options={
                'permissions': [('is_therapist', 'Can access therapist features')],
            },
        ),
    ]
