from django.urls import path
from . import views

app_name='item'
urlpatterns = [
    path('items', views.items, name='items'),
    path('new', views.new, name='new'),
    path('item/<int:pk>',views.detail, name='detail'),
    path('item/delete/<int:pk>',views.delete, name='delete'),
    path('item/edit/<int:pk>',views.edit, name='edit'),
]
