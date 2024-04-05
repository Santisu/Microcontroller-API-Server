from django.urls import path
from .views import NewCommandView, CommandListView, CommandEditView

urlpatterns = [
    path('new/', NewCommandView.as_view(), name="nuevo-comando"),
    path('', CommandListView.as_view(), name="lista-comando"), 
    path('<str:cmd_id>/', CommandEditView.as_view(), name='editar-comando'),
]