from django.contrib import admin
from .models import *


admin.site.register(RequestLogs)

admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker Admin Portal"

class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "current_balance",
        "amount",
        "expense_type",
        "description",  
        "created_at",
        "display_cashFlow",
    )
    search_fields = (
        'expense_type',
        'description'
    )
    ordering = (
        '-created_at',
        )
    # list_filter = (
    #     "expense_type",
    # )

    def display_cashFlow(self, obj):
        if obj.amount > 0:
            return "Positive"
        return "Negative"
    
    actions = ['make_credit', 'make_debit']

    @admin.action(description="Make Seleceted Expenses as Credited")
    def make_credit(modeladmin, request, queryset):
        for q in queryset:
            obj = TrackingHistory.objects.get(id = q.id)
            if obj.amount < 0:
                obj.amount = obj.amount * -1
                obj.save()
        queryset.update(expense_type='CREDIT')

    @admin.action(description="Make Seleceted Expenses as Debited")
    def make_debit(modeladmin, request, queryset):
        for q in queryset:
            obj = TrackingHistory.objects.get(id = q.id)
            if obj.amount > 0:
                obj.amount = obj.amount * -1
                obj.save()
        queryset.update(expense_type='DEBIT')

admin.site.register(TrackingHistory, TrackingHistoryAdmin)


class CurrentBalanceAdmin(admin.ModelAdmin):
    list_display =(
        "user",
        "current_balance",
    )
admin.site.register(CurrentBalance, CurrentBalanceAdmin)






