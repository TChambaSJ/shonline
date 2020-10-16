from django.contrib import admin
from .models import *


admin.site.register(Requisition)
admin.site.register(BudgetLine)
admin.site.register(Budget)
admin.site.register(Liquidation)
admin.site.register(BudgetedExpense)
admin.site.register(ActualExpense)
admin.site.register(Manager)
admin.site.register(HOD)
admin.site.register(FinanceOfficer)