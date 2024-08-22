# Generated by Django 4.2 on 2024-08-15 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adopter',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('position', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('species', models.CharField(max_length=50)),
                ('breed', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('date_of_arrival', models.DateField(default=django.utils.timezone.now)),
                ('adoption_status', models.CharField(max_length=20)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pets/')),
            ],
        ),
        migrations.CreateModel(
            name='VeterinaryRecord',
            fields=[
                ('record_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('checkup_date', models.DateField()),
                ('health_issues', models.TextField(blank=True, null=True)),
                ('treatment_given', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('appointment_date', models.DateField()),
                ('purpose', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.employee')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Adoption',
            fields=[
                ('adoption_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('adoption_date', models.DateField()),
                ('adoption_fee', models.FloatField()),
                ('adopter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.adopter')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
            ],
        ),
    ]
