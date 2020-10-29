
from django.urls import path
from adminext.views import handleExcelFile

urls = [
        path("uploadexcel/",handleExcelFile)
    ]
