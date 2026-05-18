from django.contrib import admin
from django.urls import path, include
from common.views import menu_view
from common.views.register.register_csv_view import RegisterCsvView

app_name = "common"
urlpatterns = [
    # メニュー表示
    path("main_menu", menu_view.main_menu, name="main_menu"),
    # CSV登録画面
    path("register_csv/", RegisterCsvView.as_view(), name="register_csv"),
]
