from django.contrib import admin
from .models import CurrentBalance, TrackingHistory, RequestLogs

admin.site.register(CurrentBalance)
admin.site.register(TrackingHistory)
admin.site.register(RequestLogs)


