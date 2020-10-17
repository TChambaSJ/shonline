from django.forms import ModelForm
from .models import Requisition, Liquidation, Budget, BudgetedExpense, BudgetLine, ActualExpense 


class BudgetedExpenseForm(ModelForm):
    class Meta:
        model = BudgetedExpense
        fields = '__all__'


class RequisitionForm(ModelForm):
    class Meta:
        model = Requisition
        fields = ['budget', 'payee', 'payee_details', 'total', 'payment_type', 'justification_for_cash_payment', 'quotation']


class RecommendRequisitionForm(ModelForm):
    class Meta:
        model = Requisition
        fields = ['status', 'recommended_by', 'reason_for_rejection']


class AuthoriseRequisitionForm(ModelForm):
    class Meta:
        model = Requisition
        fields = ['status', 'authorized_by', 'reason_for_rejection']

class ProcessRequisitionForm(ModelForm):
    class Meta:
        model = Requisition
        fields = ['status', 'processed_by', 'reason_for_rejection']

class ConfirmPaymentForm(ModelForm):
    class Meta:
        model = Requisition
        fields = ['status', 'reason_for_rejection']


class CloseLiquidationForm(ModelForm):
    class Meta:
        model = Liquidation
        fields = ['status',]


class LiquidationForm(ModelForm):
    class Meta:
        model = Liquidation
        fields = ['requisition', 'compiled_by', 'total_requested', 'total_spent', 'balance','comments' ,'receipts' ]

class ProcessLiquidationForm(ModelForm):
    class Meta:
        model = Liquidation
        fields = ['status', 'processed_by', 'reason_for_rejection_by_Finance']


class ActualExpenseForm(ModelForm):
    class Meta:
        model = ActualExpense
        fields = '__all__'

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'

class BudgetLineForm(ModelForm):
    class Meta:
        model = BudgetLine
        fields = '__all__'
