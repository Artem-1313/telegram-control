from django.urls import path, include
from . import views
from .views import TelegramsListView, TelegramDetailView
urlpatterns = [

    path('', TelegramsListView.as_view(), name="panel-home"),
    # path('show_tlg/<int:i>', views.show_tlg, name='show-tlg'),
    path('add_tlg/', views.add_tlg, name='add-tlg'),
    path('telegram/<int:pk>/', TelegramDetailView.as_view(), name='telegram-detail'),

]