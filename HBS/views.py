from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import patient,invoice1,prescription, doctor
from datetime import date
from HBS.models import *
from . import models


# Create your views here.

def home(request):
    if request.method == 'POST':
        prescription_counter = 0
        while request.POST.get(f'predes{prescription_counter}', None) is not None:
            prescription_counter += 1
        doc_id = request.POST.get("dnum")
        if(int(doc_id)<1):
            return render(request, "html/error.html", {"error": "Invalid Doctor I'd."})


        doctorss = doctor.objects.all()
        k = None
        for s in doctorss:
            k = s.id  # this will give us id of last doctor
        if int(doc_id) < 1 or int(doc_id) > k:
            return render(request, "html/error.html", {"error": "Invalid Doctor I'd."})

        p = patient(name=request.POST.get('pname'), contact=request.POST.get('number'),
                     disease=request.POST.get('disease'),
                     cnic=request.POST.get('cnic'), doc=doctor.objects.all()[int(doc_id) - 1],operation=request.POST.get('operat'),
                    nursing=request.POST.get('nurse'),room=request.POST.get('room'),food=request.POST.get('food'))

        if len(p.contact) != 11 and len(p.contact) != 14 and len(p.contact) and 13:
            return render(request, "html/error.html", {"error": "Invalid Contact Number."})
        if len(p.cnic) != 13:
            return render(request, "html/error.html", {"error": "Invalid CNIC."})

        else:
            p.save()

        for k in range(prescription_counter):
            prescription(name=request.POST.get(f'prename{k}'), desc=request.POST.get(f'predes{k}'),
                          price=request.POST.get(f'preprice{k}'),
                          number=request.POST.get(f'prequan{k}'), patient=p).save()
        inv = invoice1.objects.create(date=date.today(), patient=p)
        allpres = prescription.objects.all()

        return render(request, 'html/invoice.html',
                      {"id": inv.id, "dte": inv.date, "pname": p.name, "contact": p.contact, "disease": p.disease,
                       "cnic": p.cnic,
                       "dname": p.doc.name, "dId": p.doc_id, "pres": allpres, "plast": p, "room" : p.room,"food":p.food
                       , "operation": p.operation,"nursing": p.nursing,"dfee":p.doc.fee})
    doc = doctor.objects.all()

    return render(request, 'html/home.html', {"docs": doc})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/')

    else:
        return render(request, 'html/login.html')


def invoice(request):
    if request.method == 'POST':

        inv_num = request.POST["num_inv"]
        invoices = invoice1.objects.all()
        patients = patient.objects.all()
        prescriptions = prescription.objects.all()
        doctors = doctor.objects.all()
        dte = None
        p = None
        flag = 0;
        for inv in invoices:
            if int(inv_num) == int(inv.id):
                p = inv.patient
                dte = inv.date
                flag = 1;
        if flag == 1:
            return render(request, 'html/invoice.html',
                          {"id": inv_num, "dte": inv.date, "pname": p.name, "contact": p.contact, "disease": p.disease,
                           "cnic": p.cnic,
                           "dname": p.doc.name, "dId": p.doc_id, "pres": prescriptions, "plast": p,"room" : p.room,"food":p.food
                       , "operation": p.operation,"nursing": p.nursing,"dfee":p.doc.fee })
        else:
            return render(request, "html/error.html", {"error": "Invoice does not exist."})

    return render(request, 'html/invoice.html')


def doc(request):
    if request.method == "POST":
        docc = doctor(name=request.POST.get("name_doc"), speciality=request.POST.get("spec_doc"),fee=request.POST.get('fee'))
        if docc.name == "" and docc.speciality == "":
            return render(request, "html/error.html", {"error": "Doctor name and Speciality are EMPTY."})
        if docc.name == "":
            return render(request, "html/error.html", {"error": "Doctor name is EMPTY."})
        if docc.speciality == "":
            return render(request, "html/error.html", {"error": "Doctor's speciality is EMPTY."})
        if docc.name != "" and docc.speciality != "":
            docc.save()
            return redirect("home")
    if request.method == "Get":
        return redirect("home")


def error(request):
    return render(request, "html/error.html")
