from django.db import models



# Create your models here.
class SenderId(models.Model):
    sender_id = models.CharField(max_length=200)
    created_at = models.DateTimeField('date created',auto_now_add=True)

class ApiKey(models.Model):
    api_key = models.CharField(max_length=250)
    created_at = models.DateTimeField('date created',auto_now_add=True)

class Group(models.Model):
    group_name = models.CharField(max_length=250)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    

class Contact(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    other_name = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=250)
    alt_phone_number = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField('date created',auto_now_add=True)

class SentText(models.Model):
    class Meta:
        ordering = ('-id',)
    text_message = models.TextField()
    sender_id = models.ForeignKey(SenderId, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    created_at = models.DateTimeField('date created',auto_now_add=True)
    message_id = models.CharField(max_length=250,null=True, blank=True)
    response_code = models.CharField(max_length=250, null=True, blank=True)
    response_description = models.CharField(max_length=250, null=True, blank=True)
    network_id = models.CharField(max_length=250, null=True, blank=True)
    delivery_status = models.CharField(max_length=250, null=True, blank=True)
    delivery_description = models.CharField(max_length=250, null=True, blank=True)
    delivery_tat = models.CharField(max_length=250, null=True, blank=True)
    delivery_network_id = models.CharField(max_length=250, null=True, blank=True)
    delivery_time = models.CharField(max_length=250, null=True, blank=True)
    delivery_response_description = models.CharField(max_length=250, null=True, blank=True)
    
    

