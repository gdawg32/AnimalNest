from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def generate_id(model_class, prefix, id_field='id'):
    if not hasattr(model_class, id_field):
        raise ValueError(f"The field '{id_field}' does not exist in {model_class.__name__}")

    max_id = model_class.objects.filter(**{f"{id_field}__startswith": prefix}).order_by(id_field).last()

    if max_id:
        last_number = int(getattr(max_id, id_field)[len(prefix):])
        new_number = last_number + 1
    else:
        new_number = 1
    return f"{prefix}{str(new_number).zfill(3)}"


class Adopter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Ensure the user has a unique username if not already set
        if not self.user.username:
            self.user.username = generate_id(Adopter, 'A', 'user__username')
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.user.pk:
            self.user.username = generate_id(Employee, 'E')
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Pet(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    date_of_arrival = models.DateField(default=timezone.now)
    adoption_status = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='pets/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate a new ID if not already set
        if not self.id:
            self.id = generate_id(Pet, 'P', 'id')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class VeterinaryRecord(models.Model):
    record_id = models.CharField(max_length=50, primary_key=True, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    checkup_date = models.DateField()
    health_issues = models.TextField(blank=True, null=True)
    treatment_given = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.record_id:
            self.record_id = generate_id(VeterinaryRecord, 'R', 'record_id')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Record {self.record_id} for Pet {self.pet}"

class Adoption(models.Model):
    adoption_id = models.CharField(max_length=50, primary_key=True, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter = models.ForeignKey(Adopter, on_delete=models.SET_NULL, null=True, blank=True)
    adoption_date = models.DateField()
    adoption_fee = models.FloatField()

    def save(self, *args, **kwargs):
        # Generate a new ID if not already set
        if not self.adoption_id:
            self.adoption_id = generate_id(Adoption, 'D', 'adoption_id')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Adoption {self.adoption_id} - Pet {self.pet.name} by Adopter {self.adopter.user.username}"

class Appointment(models.Model):
    appointment_id = models.CharField(max_length=50, primary_key=True, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    adopter = models.ForeignKey('Adopter', on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Generate a new ID if not already set
        if not self.appointment_id:
            self.appointment_id = generate_id(Appointment, 'A', 'appointment_id')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment {self.appointment_id} for Pet {self.pet.name}"

