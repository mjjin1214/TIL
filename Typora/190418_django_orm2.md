```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py startapp manytomany
```



```settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'crud',
    'onetomany',
    'manytomany',
]
```



manytomany / models.py 수정

```python
class Doctor(models.Model):
    name = models.TextField()
    
# Doctor:Patient = 1:N
class Patient(models.Model):
    name = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
```



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py makemigrations
Migrations for 'manytomany':
  manytomany/migrations/0001_initial.py
    - Create model Doctor
    - Create model Patient
    
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, crud, manytomany, onetomany, sessions
Running migrations:
  Applying manytomany.0001_initial... OK
```



manytomany / models.py 수정

```python
class Patient(models.Model):
    name = models.TextField()
    
# Doctor:Reservation = 1:N
# Patient:Reservation = 1:N
class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py makemigrations
Migrations for 'manytomany':
  manytomany/migrations/0002_reservation.py
    - Create model Reservation
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, crud, manytomany, onetomany, sessions
Running migrations:
  Applying manytomany.0002_reservation... OK
  
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py shell_plus
```



```shell
>>> doctor1 = Doctor.objects.create(name='Kim')
>>> doctor2 = Doctor.objects.create(name='Kang')                              
>>> patient1 = Patient.objects.create(name='Tom')
>>> patient2 = Patient.objects.create(name='John')
>>> Reservation.objects.create(doctor=doctor1, patient=patient2)
<Reservation: Reservation object (1)>

>>> Reservation.objects.create(doctor=doctor1, patient=patient1)
<Reservation: Reservation object (2)>

>>> doctor1.reservation_set.all()
<QuerySet [<Reservation: Reservation object (1)>, <Reservation: Reservation object (2)>]>

>>> patient2.reservation_set.all()
<QuerySet [<Reservation: Reservation object (1)>]>

>>> for res in doctor1.reservation_set.all():
...     print(res.patient.name)
... 
John
Tom
	
>>> doctor1
<Doctor: Doctor object (1)>

>>> patient1 = Patient.objects.get(pk=1)
>>> patient1.doctors.all()
<QuerySet [<Doctor: Doctor object (1)>]>

>>> doctor2 = Doctor.objects.get(pk=2)
>>> doctor1.patient_set.all()
<QuerySet [<Patient: Patient object (2)>, <Patient: Patient object (1)>]>
```



manytomany / models.py 수정

```python
class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor, related_name='patients', through='Reservation')
    
# Doctor:Reservation = 1:N -> Reservation = N*Doctor
# Patient:Reservation = 1:N -> Reservation = M*Patient
# N*Doctor = M*Patient -> M:N = Doctor:Patient
# Doctor:Patient = M:N
class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
```



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ ./manage.py makemigrations
Migrations for 'manytomany':
  manytomany/migrations/0004_auto_20190418_0200.py
    - Alter field doctors on patient
    
(orm-venv) minjaejin:~/workspace/django/orm (master) $ ./manage.py migrateOperations to perform:
  Apply all migrations: admin, auth, contenttypes, crud, manytomany, onetomany, sessions
Running migrations:
  Applying manytomany.0004_auto_20190418_0200... OK
  
(orm-venv) minjaejin:~/workspace/django/orm (master) $ ./manage.py shell_plus
```



```shell
>>> doctor1 = Doctor.objects.first()
>>> doctor1.patients.all()
<QuerySet [<Patient: Patient object (2)>, <Patient: Patient object (1)>]>
```



manytomany / models.py 수정

```python
from django.db import models

# Create your models here.
# 병원에 오는 사람들을 기록하는 시스템을 만드려고 한다.
# 필수적인 모델은 환자와 의사이다.
# 어떠한 관계로 표현할 수 있을까?

class Doctor(models.Model):
    name = models.TextField()
    

class Patient(models.Model):
    name = models.TextField()
    doctors = models.ManyToManyField(Doctor, related_name='patients')
```



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py makemigrations
Migrations for 'manytomany':
  manytomany/migrations/0001_initial.py
    - Create model Doctor
    - Create model Patient

(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, crud, manytomany, onetomany, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying crud.0001_initial... OK
  Applying manytomany.0001_initial... OK
  Applying onetomany.0001_initial... OK
  Applying sessions.0001_initial... OK
  
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py shell_plus
```



```shell
>>> doctor1 = Doctor.objects.create(name='Kim')
>>> doctor2 = Doctor.objects.create(name='Kang')                             
>>> patient1 = Patient.objects.create(name='Tom')
>>> patient2 = Patient.objects.create(name='John')                           
>>> doctor1.patients.all()
<QuerySet []>

>>> patient2.doctors.all()
<QuerySet []>

>>> doctor1.patients.add(patient2)
>>> doctor1.patients.all()
<QuerySet [<Patient: Patient object (2)>]>

>>> patient2.doctors.all()
<QuerySet [<Doctor: Doctor object (1)>]>

>>> doctor1.patients.remove(patient2) # = patient2.doctors.remove(doctor1)
>>> doctor1.patients.all()
<QuerySet []>

>>> patient2.doctors.all()
<QuerySet []>
```

