from datetime import datetime

from django.contrib import messages
from django.shortcuts import render

from KeyLogger.models import Keys, Person, AssignedKeys


def base(request):
    return render(request, template_name="base/base.html")


def save_new_key(request):
    key = None
    if request.method == "POST":
        key = Keys.objects.create(
            key_title=request.POST.get("key_title"),
            key_notes=request.POST.get("key_notes"),
        )
        messages.success(request, "Key added successfully!")
    context = {
        "key": key
    }
    return render(request, template_name="save_new_key.html", context=context)


def add_new_person(request):
    person = None
    if request.method == "POST":
        person = Person.objects.create(
            full_name=request.POST.get("full_name"),
            email_address=request.POST.get("email_address"),
            phone_number=request.POST.get("phone_number"),
        )
        messages.success(request, "Person added successfully!")
    context = {
        "person": person
    }
    return render(request, template_name="add_person.html", context=context)


def assign_key(request):
    persons = Person.objects.all()
    keys = Keys.objects.filter(status="Available")
    if request.method == "POST":
        key = Keys.objects.get(key_qr=request.POST.get("key"))
        person = Person.objects.get(person_qr=request.POST.get("person"))

        assigned = AssignedKeys.objects.create(
            key=key,
            person=person,
        )
        assigned.save()
        key.status = "Assigned to "+person.full_name
        key.save()
        messages.success(request, "Key assigned successfully!")
    context = {
        "persons": persons,
        "keys": keys,
    }
    return render(request, template_name="assign_key.html", context=context)


def return_key(request):
    keys = Keys.objects.filter(status__contains="Assigned")
    if request.method == "POST":
        key = Keys.objects.get(key_qr=request.POST.get("key"))
        assigned_key = AssignedKeys.objects.get(key=key, returned=False)
        assigned_key.returned = True
        assigned_key.returned_at = datetime.now()
        assigned_key.save()
        key.status = "Available"
        key.save()
        messages.success(request, "Key returned successfully!")
    context = {
        "keys": keys,
    }
    return render(request, template_name="return_key.html", context=context)


def dashboard(request):
    keys = AssignedKeys.objects.all()
    context = {
        "keys": keys,
    }
    return render(request, template_name="dashboard.html", context=context)

def all_keys(request):
    keys = Keys.objects.all()
    context = {
        "keys": keys,
    }
    return render(request, template_name="all_keys.html", context=context)