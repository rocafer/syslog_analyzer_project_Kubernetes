# analyzer/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_action, name='upload'),
    path('results/<int:file_id>/', views.show_results, name='show_results'),
    path('consulta/', views.consulta_registros, name='consulta_registros'),
    path('chat_consulta/', views.hola, name='hola'),
    path('un_registro/', views.ver_un_registro, name='ver_un_registro'),
    path('chat_gpt/', views.chat_gpt, name='chat_gpt'),  # Nueva ruta para la vista de Chat-GPT
    path('seleccionar_registro/', views.seleccionar_registro, name='seleccionar_registro'),
]
