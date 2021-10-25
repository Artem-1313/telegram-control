from django.urls import path, include
from . import views
from .views import TelegramsListView, TelegramDetailView, TelegramsDeleteView, TelegramsUpdateView, CheckUnits, pdf_view
urlpatterns = [

    path('', TelegramsListView.as_view(), name="panel-home"),
    path('add_tlg/', views.add_tlg, name='add-tlg'),
    path('telegram/<int:pk>/', TelegramDetailView.as_view(), name='telegram-detail'),
    path('delete/<int:pk>/', TelegramsDeleteView.as_view(), name='telegram-delete'),
    path('update/<int:pk>/', TelegramsUpdateView.as_view(), name='telegram-update'),
    path('check/<int:pk>/', CheckUnits, name='check'),
    path('pdf_view/<int:pk>/', views.pdf_view, name='pdf-view'),
    path('unit_detail/<str:name>/', views.search_by_unit, name='unit-detail')

]