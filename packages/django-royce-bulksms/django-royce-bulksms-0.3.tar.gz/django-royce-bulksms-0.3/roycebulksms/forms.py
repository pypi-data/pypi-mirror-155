from django import forms
# from bulksms.roycebulksms.models import Contact

from roycebulksms.models import Group, SenderId,Contact

class SenderIdForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SenderIdForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    sender_id = forms.CharField(label='Sender Id' )
class ApiKeyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ApiKeyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    api_key = forms.CharField(label='Sender Id' )

class GroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    group_name = forms.CharField(label='Group Name' )

class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    contacts= Group.objects.values_list('id','group_name')
    group_name=forms.ChoiceField(choices=contacts )       
    first_name = forms.CharField(label='First Name'  )
    other_names = forms.CharField(required=False )
    phone_number = forms.CharField()
    alt_phone_number = forms.CharField(required=False)
    email = forms.CharField(required=False)

class PhoneTextForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PhoneTextForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    senderids= SenderId.objects.values_list('id','sender_id')
    sender_id=forms.ChoiceField(choices=senderids )  
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Text message'}) )
    phone_nubers = forms.CharField( widget=forms.Textarea(attrs={'placeholder': '0712345678\n0112345678'}))
class ContactsTextForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(ContactsTextForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'


    senderids= SenderId.objects.values_list('id','sender_id')
    contacts= Contact.objects.values_list('phone_number','phone_number')
    sender_id=forms.CharField(widget=forms.widgets.Select(attrs={'placeholder': 'Text message','class':'form-control'},choices=senderids ) )  
    # favorite_colors=forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=contacts)
    phone_nubers=forms.MultipleChoiceField(
                required=True,
        
            widget = forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
            choices = contacts
    )
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Text message','class':'form-control'}) )
    # phone_nubers = forms.CharField( widget=forms.Textarea(attrs={'placeholder': '0712345678\n0112345678'}))
class GroupsTextForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(GroupsTextForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'


    senderids= SenderId.objects.values_list('id','sender_id')
    groups= Group.objects.values_list('id','group_name')
    sender_id=forms.CharField(widget=forms.widgets.Select(attrs={'placeholder': 'Text message','class':'form-control'},choices=senderids ) )  
    # favorite_colors=forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=contacts)
    phone_nubers=forms.MultipleChoiceField(
                required=True,
        
            widget = forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
            choices = groups
    )
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Text message','class':'form-control'}) )
    # phone_nubers = forms.CharField( widget=forms.Textarea(attrs={'placeholder': '0712345678\n0112345678'}))