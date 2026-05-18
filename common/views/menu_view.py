from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest


# メインメニュー表示
def main_menu(request):
    return render(request, "common/main_menu.html")
