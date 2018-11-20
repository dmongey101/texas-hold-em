from django.urls import path
from poker.views import create_table, find_table, view_table

urlpatterns = [
    path('create_table/', create_table, name="create_table"),
    path('find_table/', find_table, name="find_table"),
    path('table/<str:name>', view_table, name="get_table"),
]