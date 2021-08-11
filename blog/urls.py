from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [   
    path('postcomment', views.postcomment, name='PostComments'), 

    path('', views.bloghome, name='BlogHome'),
    path('<str:slug>', views.blogpost, name='BlogPost')
    
    
]
