import datetime
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
from SecureZone_app.models import *


def Login(request):
    return render(request,'index.html')


def Login_post(request):
    username1 = request.POST['textfield']
    password1 = request.POST['textfield2']

    lobj = login.objects.filter(username = username1,password=password1)
    if lobj.exists():
        lobj = lobj[0]
        request.session['lg'] = "lin"
        if lobj.usertype == 'admin':
            return HttpResponse("<script>alert('login successfull');window.location='/AdminHome'</script>")
        else:
            return HttpResponse("<script>alert('incorrect password');window.locatioin='/'</script>")

    else:
        return HttpResponse("<script>alert('invalid');window.locatioin='/'</script>")

def Logout(request):
    request.session['lg'] = ""
    return HttpResponse("<script>alert('logout successfull');window.location='/'</script>")


def AddSecurity(request):
    if request.session['lg']!="lin":
        return HttpResponse("<script>alert('logout successfull');window.location='/'</script>")

    return render(request,'admin/add_security.html')

def Addsecurity_post(request):
    name1 = request.POST['textfield']
    image1 = request.FILES['fileField']
    id1 = request.FILES['fileField2']
    email1 = request.POST['textfield2']
    pin1 = request.POST['textfield3']
    post1 = request.POST['textfield4']
    place1 = request.POST['textfield5']
    phone1 = request.POST['textfield6']

    fs = FileSystemStorage()
    d = datetime.datetime.now().strftime('%y%m%d-%H%M%S')
    fs.save(r"C:\Users\athul\PycharmProjects\SecureZone\SecureZone_app\static\\"+d+'.jpg',image1)
    path1 = '/static/'+d+'.jpg'

    fs.save(r"C:\Users\athul\PycharmProjects\SecureZone\SecureZone_app\static\\" + d + '.pdf',id1)
    path2 = '/static/' + d + '.pdf'

    ps=random.randint(0000,9999)

    i=login.objects.filter(username = email1)
    if i.exists():
        return HttpResponse("<script>alert('Already added');window.location='/ViewSecurity'</script>")
    else:
        obj = login()
        obj.username = email1
        obj.password = ps
        obj.usertype = 'security'
        obj.save()

        obj1 = securityperson()
        obj1.security_name = name1
        obj1.image = path1
        obj1.id_proof = path2
        obj1.email = email1
        obj1.pin = pin1
        obj1.post = post1
        obj1.place = place1
        obj1.phone = phone1
        obj1.LOGIN = obj
        obj1.save()

        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("securezonesentinel3@gmail.com", "xbmm dxjv wvqk blzm")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "securezonesentinel3@gmail.com"
        msg['To'] = email1
        msg['Subject'] = "USERNAME AND PASSWORD"
        body = "Your Password is:- - " + str(ps)+ "Your Username is:- - " + str(email1)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return HttpResponse("<script>alert('security added sucessfully');window.location='/ViewSecurity'</script>")


def ViewSecurity(request):
    data = securityperson.objects.all()
    return render(request,'admin/view_security.html',{'data':data})

def delete_security(request,id):
    securityperson.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/ViewSecurity'</script>")

def Edit(request,id):
    view=securityperson.objects.get(id=id)
    return render(request,'admin/edit.html',{'view':view})

def Edit_post(request,id):
    name2 = request.POST['textfield']
    if "fileField" in request.FILES:
        image2 = request.FILES['fileField']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime('%y%m%d-%H%M%S')
        fs.save(r"C:\Users\athul\PycharmProjects\SecureZone\SecureZone_app\static\\" + d + '.jpg', image2)
        path1 = '/static/' + d + '.jpg'
        securityperson.objects.filter(id=id).update(image=path1)
    if "proof" in request.FILES:
        id1 = request.FILES['proof']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime('%y%m%d-%H%M%S')
        fs.save(r"C:\Users\athul\PycharmProjects\SecureZone\SecureZone_app\static\\" + d + '.pdf', id1)
        path2 = '/static/' + d + '.pdf'
        securityperson.objects.filter(id=id).update(id_proof=path2)
    email2 = request.POST['textfield2']
    pin2 = request.POST['textfield3']
    post2 = request.POST['textfield4']
    place2 = request.POST['textfield5']
    phone2 = request.POST['textfield6']
    securityperson.objects.filter(id=id).update(security_name=name2,email=email2,pin=pin2,post=post2,place=place2,phone=phone2)

    return HttpResponse("<script>alert('Profile edited successfully');window.location='/ViewSecurity'</script>")



def Assign(request,id):
    return render(request,'admin/assign.html',{"id":id})


def Assign_post(request,id):
    task = request.POST['textarea']
    day = request.POST['select']
    i=survillancetask.objects.filter(survilance_task = task)
    if i.exists():
        return HttpResponse("<script>alert('Already assigned');window.location='/ViewSecurity'</script>")
    else:
        obj2 = survillancetask()
        obj2.survilance_task = task
        obj2.assign_date = datetime.datetime.now().strftime("%d-%m-%Y")
        obj2.assing_day = day
        obj2.SECURITY_PERSON_id = id
        obj2.save()
        return HttpResponse("<script>alert('Task assigned successfully');window.location='/ViewSecurity'</script>")

def ViewTask(request,id):
    data = survillancetask.objects.filter(SECURITY_PERSON_id=id)
    return render(request,'admin/view_task.html',{'data':data})


def SendAlert(request):
    return render(request,'admin/send_alert.html')

def SendAlert_post(request):
    alert1 = request.POST['textfield']
    obj = alert()
    obj.alert_msg = alert1
    obj.alert_status = 'pending'
    obj.alert_date = datetime.datetime.now().strftime("%Y-%m-%d")
    obj.alert_time = datetime.datetime.now().strftime("%H:%M:%S")
    obj.save()
    return HttpResponse("<script>alert('Alert send successfully');window.location='/ViewSecurity'</script>")

def ViewAlert(request):
    data = alert.objects.all()
    return render(request,'admin/view_alert.html',{'data':data})


def ViewCmplnt(request):
    data = complaint.objects.all()
    return render(request,'admin/view&respond_complaint.html',{'data':data})

def Reply(request,id):
    return render(request,'admin/reply.html',{"id":id})

def Reply_post(request,id):
    reply1 = request.POST['textarea']
    rd=datetime.datetime.now().strftime("%d-%m-%Y")
    complaint.objects.filter(id=id).update(complaint_rply=reply1,reply_date=rd)
    return HttpResponse("<script>alert('Replied successfully');window.location='/ViewCmplnt'</script>")

def AdminHome(request):
    return render(request,'admin/admin_index.html')

def ViewReport(request,id):
    data = report.objects.filter(SURVILANCE_TASK_id=id)
    return render(request,'admin/view_report.html',{'data':data})



# =========================================================================================================================================================================



def and_login(request):

    u=request.POST['username']
    p=request.POST['password']
    data=login.objects.filter(username=u,password=p)
    if data.exists():
        type=data[0].usertype
        lid=data[0].id
        return JsonResponse({"status":"ok","type":type,"lid":lid})
    else:
        return JsonResponse({"status": None})

def and_manage_profile(request):
    lid = request.POST['lid']
    data=securityperson.objects.get(LOGIN=lid)
    return JsonResponse({"status":"ok","security_id": data.id,
                         "security_name":data.security_name,
                         "image":data.image,
                         "id_proof": data.id_proof,
                         "email": data.email,
                         "pin": data.pin,
                         "post":data.post,
                         "place": data.place,
                         "phone": data.phone,
                         })


def and_view_task(request):
    lid=request.POST['lid']
    data = survillancetask.objects.filter(SECURITY_PERSON__LOGIN=lid)
    a = []
    for i in data:
        a.append({
            "task_id": i.id,
            "task": i.survilance_task,
            "date": i.assign_date,
            "day": i.assing_day,
            "security_name":i.SECURITY_PERSON.security_name,

        })
    return JsonResponse({"status": "ok", "users": a})

def and_view_response(request):
    lid=request.POST['lid']

    data=complaint.objects.filter(SECURITY_PERSON__LOGIN=lid)
    a=[]
    for i in data:
        a.append({
            "reply_id":i.id,
            "complaint":i.complaint,
            "date":i.complaint_date,
            "reply":i.complaint_rply,
            "rply_date":i.reply_date

        })
        print(a,"aaaaaaaaa")

    return JsonResponse({"status":"ok","users":a})

def and_alert(request):
    data=alert.objects.all()
    a=[]
    for i in data:
        a.append({
            "em_id":i.id,
            "alert":i.alert_msg,
            "date":i.alert_date,
            "time":i.alert_time,

        })
    print(a,"aaaaaaaaa")
    return JsonResponse({"status":"ok","users":a})

def index(request):
    return  render(request,"admin/admin_index.html")


def send_complaint_post(request):
    complaint1 = request.POST['textfield']
    lid = request.POST['lid']
    obj = complaint()
    obj.complaint = complaint1
    obj.complaint_date = datetime.datetime.now().strftime("%H:%M:%S")
    obj.complaint_rply = "pending"
    obj.reply_date = "pending"
    obj.SECURITY_PERSON =securityperson.objects.get(LOGIN=lid)
    obj.save()
    return JsonResponse({"status":"ok"})



def and_reply(request):
    lid=request.POST['lid']
    data=complaint.objects.filter(SECURITY_PERSON__LOGIN=lid)
    a=[]
    for i in data:
        a.append({
            "id":i.id,
            "complaint":i.complaint,
            "complaint_date":i.complaint_date,
            "complaint_rply":i.complaint_rply,
            "reply_date":i.reply_date,
        })
    return JsonResponse({"status":"ok","users":a})


def send_report_post(request):
    report1 = request.POST['textfield']
    lid = request.POST['tid']
    obj = report()
    obj.report = report1
    obj.SURVILANCE_TASK_id=lid
    obj.report_date = datetime.datetime.now().strftime("%Y%m%d")
    obj.report_time = datetime.datetime.now().strftime("%H%M%S")
    obj.save()
    return JsonResponse({"status": "ok"})


def update_post(request):
    name3 = request.POST['security_name']
    lid = request.POST['lid']

    if "fileField" in request.FILES:
        image2 = request.FILES['fileField']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime('%y%m%d-%H%M%S')
        fs.save(r"C:\Users\athul\PycharmProjects\SecureZone\SecureZone_app\static\\" + d + '.jpg', image2)
        path1 = '/static/' + d + '.jpg'
        securityperson.objects.filter(id=lid).update(image=path1)

    if "proof" in request.FILES:
        id1 = request.FILES['proof']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime('%y%m%d-%H%M%S')

        fs.save(r"C:\Users\athul\PycharmProjects\SecureZone\SecureZone_app\static\\" + d + '.pdf', id1)
        path2 = '/static/' + d + '.pdf'
        securityperson.objects.filter(id=lid).update(id_proof=path2)

    email3 = request.POST['email']
    pin3 = request.POST['pin']
    post3 = request.POST['post']
    place3 = request.POST['place']
    phone3 = request.POST['phone']
    securityperson.objects.filter(id=lid).update(security_name=name3, email=email3, pin=pin3, post=post3, place=place3,
                                                phone=phone3)
    return JsonResponse({"status": "ok"})

def notification(request):

    data = alert.objects.filter(id__gt=request.POST['lastid'],alert_date=datetime.datetime.now().date()).order_by('-id')
    ar =[]


    print(data,"iuytr",request.POST['lastid'])


    if data.exists():

        for i in data:
            ar.append({
                'id':i.id,
                'alert_msg':i.alert_msg,
                'alert_status':i.alert_status

            })
        return JsonResponse({"status": "ok",'ln':len(ar),"id":data[0].id})
    else:
        return JsonResponse({"status":""})
