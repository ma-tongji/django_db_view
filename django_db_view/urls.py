
from django.urls import path
from django_db_view import views

app_name = 'django_db_view'
urlpatterns = [
    #path('home/', views.home, name='home'),
    path('<str:app_name>/<str:model_name>/show/', views.show, name='show'),
    path('<str:app_name>/<str:model_name>/edit/<int:obj_id>/', views.edit, name='edit'),
    path('<str:app_name>/<str:model_name>/delete/<int:obj_id>/', views.delete, name='delete'),
]
