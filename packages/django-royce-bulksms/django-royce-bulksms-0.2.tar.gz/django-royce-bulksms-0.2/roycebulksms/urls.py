from django.urls import path

from . import views

urlpatterns = [
    path('', views.outbox, name='index'),
    path('outbox', views.outbox, name='outbox'),
    path('send-to-numbers', views.sendToNumbers, name='send-to-numbers'),
    path('send-to-contacts', views.sendToContacts, name='send-to-contacts'),
    path('send-to-groups', views.sendToGroups, name='send-to-groups'),
    path('sender-id', views.SenderIdFn, name='sender-id'),
    path('senderid-delete/<int:question_id>/', views.senderIdDl, name='dl-sender-id'),

    path('api-key', views.ApiKeyFn, name='api-key'),
    path('api-key-delete/<int:question_id>/', views.ApiKeyDl, name='dl-api-key'),

    path('groups', views.groupFn, name='groups'),
    path('group-delete/<int:question_id>/', views.groupDl, name='dl-group'),

    path('contacts', views.contactFn, name='contacts'),
    path('contact-delete/<int:question_id>/', views.ContactDl, name='dl-contact'),
    # path('specifics/<int:question_id>/', views.detail, name='detail'),
]