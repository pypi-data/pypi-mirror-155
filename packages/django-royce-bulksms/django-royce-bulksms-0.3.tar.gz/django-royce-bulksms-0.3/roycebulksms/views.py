from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime 
from django.utils import timezone

from .forms import ContactForm, ContactsTextForm, GroupsTextForm, PhoneTextForm, SenderIdForm,ApiKeyForm,GroupForm
from .models import SenderId, ApiKey,Group,Contact, SentText
import requests
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
   
    return render(request, 'roycebulksms/index.html', {})

def outbox(request):
    texts= SentText.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(texts, 25)
    try:
        texts = paginator.page(page)
    except PageNotAnInteger:
        texts = paginator.page(1)
    except EmptyPage:
        texts = paginator.page(paginator.num_pages)
   
    return render(request, 'roycebulksms/outbox.html', {'texts':texts})
def senderIdDl(request,question_id):
    SenderId.objects.filter(id=question_id).delete()

    return HttpResponseRedirect('/bulksms/sender-id')
def ContactDl(request,question_id):
    Contact.objects.filter(id=question_id).delete()

    return HttpResponseRedirect('/bulksms/contacts')
def groupDl(request,question_id):
    Group.objects.filter(id=question_id).delete()

    return HttpResponseRedirect('/bulksms/groups')

def ApiKeyDl(request,question_id):
    ApiKey.objects.filter(id=question_id).delete()

    return HttpResponseRedirect('/bulksms/api-key')
   
    # return HttpResponseRedirect('/bulksms/sender-id')

def sendToNumbers(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhoneTextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # SenderId.objects.create(sender_id=form.cleaned_data['sender_id'])
            # print (form.cleaned_data)
            # redirect to a new URL:

            
            # print('+++++++++++++++++++++')
            # print(list2)
            message=form.cleaned_data['text']
            aphanumberic= SenderId.objects.get(pk=4)

          



            numbers=form.cleaned_data['phone_nubers'].splitlines()
            # print (numbers)
            list2 = [x for x in numbers if x]
            for number in list2:


                # print (number)
                # print(form.cleaned_data['sender_id'])
                # print(form.cleaned_data['text'])
                sendText(number,message,aphanumberic.sender_id)

            return HttpResponseRedirect('/bulksms/send-to-numbers')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PhoneTextForm()

    return render(request, 'roycebulksms/sendtonumbers.html', {'form': form})
def sendToContacts(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactsTextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            message=form.cleaned_data['text']
            aphanumberic= SenderId.objects.get(pk=4)

            numbers=form.cleaned_data['phone_nubers']
            # print (numbers)
            list2 = [x for x in numbers if x]
            for number in list2:
                
                sendText(number,message,aphanumberic.sender_id)

                raise ValidationError(
                    _('Invalid value: %(value)s'),
                    params={'value': '42'},
                )

            return HttpResponseRedirect('/bulksms/send-to-contacts')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactsTextForm()

    return render(request, 'roycebulksms/sendtocontacts.html', {'form': form})
def sendToGroups(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GroupsTextForm (request.POST)
        # check whether it's valid:
        if form.is_valid():

            message=form.cleaned_data['text']
            aphanumberic= SenderId.objects.get(pk=4)

            numbers=form.cleaned_data['phone_nubers']
            # print (numbers)
            list2 = [x for x in numbers if x]
            for number in list2:
                # print(number)
                # print(message)
                contacts= Contact.objects.filter(group_id=number)
                # print(contacts)
                for contact in contacts:
                    # print(contact.phone_number)
                
                    sendText(contact.phone_number,message,aphanumberic.sender_id)

                # raise ValidationError(
                #     _('Invalid value: %(value)s'),
                #     params={'value': '42'},
                # )

            return HttpResponseRedirect('/bulksms/send-to-groups')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GroupsTextForm()

    return render(request, 'roycebulksms/sendtogroups.html', {'form': form})
def sendText(number, message,sender_id):
    aphanumberic= SenderId.objects.get(sender_id=sender_id)
    save_text= SentText.objects.create(
        text_message=message,
        sender_id=aphanumberic,
        phone_number=number,
        status='Draft'
        )

    print(save_text)
    apikey= ApiKey.objects.order_by('-id').first()

    # print(apikey.api_key)


    
    endpoint = "https://bulksms.roycetechnologies.co.ke/api/sendmessage"
    data = {

    'sender_id': sender_id, 'text_message': message, 'phone_number': number
    }

    headers = {

    "Authorization": "Bearer "+apikey.api_key
    }

    response=requests.post(endpoint, data=data, headers=headers)

    api_response=response.json()
    SentText.objects.filter(id=save_text.id).update(
        message_id=api_response['message_id'],
        status=api_response['status'],
        # status=api_response.status

        )

    # print(response.json())
def SenderIdFn(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SenderIdForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            SenderId.objects.create(sender_id=form.cleaned_data['sender_id'])
            # print (form.cleaned_data)
            # redirect to a new URL:

            return HttpResponseRedirect('/bulksms/sender-id')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SenderIdForm()
        senderids= SenderId.objects.all()

        

    return render(request, 'roycebulksms/senderid.html', {'form': form,'senderids':senderids})
def ApiKeyFn(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ApiKeyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            ApiKey.objects.create(api_key=form.cleaned_data['api_key'])
            # print (form.cleaned_data)
            # redirect to a new URL:

            return HttpResponseRedirect('/bulksms/api-key')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ApiKeyForm()
        apikeys= ApiKey.objects.all()

        

    return render(request, 'roycebulksms/apikey.html', {'form': form,'apikeys':apikeys})

def groupFn(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            Group.objects.create(group_name=form.cleaned_data['group_name'])
            # print (form.cleaned_data)
            # redirect to a new URL:

            return HttpResponseRedirect('/bulksms/groups')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GroupForm()
        groups= Group.objects.all()

        

    return render(request, 'roycebulksms/groups.html', {'form': form,'groups':groups})

def contactFn(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            mygroup = Group.objects.filter(id=form.cleaned_data['group_name']).first()
            print('mygroup')
            print(mygroup)
            Contact.objects.create(
                group_id=mygroup,
                first_name=form.cleaned_data['first_name'],
                other_name=form.cleaned_data['other_names'],
                phone_number=form.cleaned_data['phone_number'],
                alt_phone_number=form.cleaned_data['alt_phone_number'],
                email=form.cleaned_data['email'],
   
                )
            # print (form.cleaned_data)
            # redirect to a new URL:

            return HttpResponseRedirect('/bulksms/contacts')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
        contacts= Contact.objects.all()

    return render(request, 'roycebulksms/contacts.html', {'form': form,'contacts':contacts})