from django.db import models


class Correctpic(models.Model):
    uid = models.AutoField(primary_key=True)
    picturefilename = models.CharField(db_column='pictureFileName', max_length=255)  # Field name made lowercase.
    doctorid = models.ForeignKey('Doctor', models.DO_NOTHING, db_column='doctorId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'correctPic'


class Doctor(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    id = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=50)
    doctornum = models.IntegerField(db_column='doctorNum', unique=True)  # Field name made lowercase.
    hospitalname = models.CharField(db_column='hospitalName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'doctor'


class Doctorcomment(models.Model):
    uid = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    doctorid = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctorId')  # Field name made lowercase.
    pictureid = models.ForeignKey('Patientpic', models.DO_NOTHING, db_column='pictureId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'doctorComment'


class Manage(models.Model):
    uid = models.AutoField(primary_key=True)
    doctorid = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctorId')  # Field name made lowercase.
    patientid = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patientId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'manage'


class Patient(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    id = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'patient'


class Patientpic(models.Model):
    uid = models.AutoField(primary_key=True)
    picturefilename = models.CharField(db_column='pictureFileName', max_length=255)  # Field name made lowercase.
    score = models.IntegerField(blank=True, null=True)
    correctpicid = models.ForeignKey(Correctpic, models.DO_NOTHING, db_column='correctPicId')  # Field name made lowercase.
    patientid = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patientId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'patientPic'
