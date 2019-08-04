from django.contrib import admin
from . import models
from django.contrib.auth.backends import ModelBackend


Models = (
    models.Production, 
    models.ProUser,
    models.Machine,
    models.Part,
    models.HourlyProduction,
    models.ChangeLog
    )

admin.site.register(Models)
