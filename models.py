from django.db import models

# Create your models here.

class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)


class securityperson(models.Model):
    security_name = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    id_proof = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    post = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    LOGIN = models.ForeignKey(login,on_delete=models.CASCADE)


class alert(models.Model):
    alert_msg = models.CharField(max_length=200)
    alert_status = models.CharField(max_length=200)
    alert_date = models.DateField(max_length=20)
    alert_time = models.CharField(max_length=20)


class survillancetask(models.Model):
    survilance_task = models.CharField(max_length=200)
    assign_date = models.CharField(max_length=20)
    assing_day = models.CharField(max_length=50)
    SECURITY_PERSON = models.ForeignKey(securityperson,on_delete=models.CASCADE)


class report(models.Model):
    report = models.CharField(max_length=200)
    SURVILANCE_TASK = models.ForeignKey(survillancetask,on_delete=models.CASCADE)
    report_date = models.CharField(max_length=20)
    report_time = models.CharField(max_length=20)


class complaint(models.Model):
    complaint = models.CharField(max_length=200)
    complaint_date = models.CharField(max_length=50)
    complaint_rply = models.CharField(max_length=200)
    reply_date = models.CharField(max_length=20)
    SECURITY_PERSON = models.ForeignKey(securityperson,on_delete=models.CASCADE)


class sec_entry(models.Model):
    SECURITY_PERSON = models.ForeignKey(securityperson,on_delete=models.CASCADE)
    date=models.CharField(max_length=200)
    image=models.CharField(max_length=200)

