from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_medico/', views.cadastro_medico, name='cadastro_medico'),
    path('cadastro_agenda/', views.cadastro_agenda, name="cadastro_agenda"),
    path('consultas_medico/', views.consultas_medico, name="consultas_medico"),
    path('consulta_area_medico/<int:id_consulta>/', views.consulta_area_medico, name="consulta_area_medico"),
    path('finalizar_consulta/<int:id_consulta>/', views.finalizar_consulta, name="finalizar_consulta"),
    path('add_documento/<int:id_consulta>/', views.add_documento, name="add_documento"),
]