from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.index, name="panel-home"),
    path('show_tlg/<int:i>', views.show_tlg, name='show-tlg'),
    path('add_tlg/',views.add_tlg, name='add-tlg'),

]