from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse, resolvers


class Manager(models.Model):
    PORTIFOLIO = (
        ('Programmes', 'Programmes'),
        ('Administration', 'Admininstration'),
    )

    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=50, choices=PORTIFOLIO, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class HOD(models.Model):
    DEPARTMENT = (
        ('TVSTP', 'TVSTP'),
        ('CDP', 'CDP'),
        ('APB', 'APB'),
    )

    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT)

    def __str__(self):
        return str(self.name)

class FinanceOfficer(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)


class Budget(models.Model):
    funder = models.CharField(max_length=100, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.funder


class BudgetLine(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, default=None)
    code = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=255, default=None, null=True, blank=True)
    total_allocation = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.code


class Requisition(models.Model):
    PAYMENTMODE = (
        ('USD Cash', 'USD Cash'),
        ('ZWL Cash', 'ZWL Cash'),
        ('USD Bank Transfer', 'USD Bank Transfer'),
        ('ZWL Bank Transfer', 'ZWL Bank Transfer')
    )

    STATUS = (
        ('Pending', 'Pending'),
        ('Recommended', 'Recommended'),
        ('Authorised', 'Authorised'),
        ('Processed', 'Processed'),
        ('Rejected', 'Rejected'),
        ('Paid', 'Paid'),
        ('Confirmed', 'Confirmed')
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True)
    payment_type = models.CharField(max_length=30, choices=PAYMENTMODE, default='ZWL Bank Transfer')
    payee = models.CharField(max_length=255, null=True, blank=True)
    payee_details = models.CharField(max_length=255, null=True, blank=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True)
    justification_for_cash_payment = models.CharField(max_length=255, null=True, blank=True)
    requested_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    date_requested = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS, default='Pending', null=True)
    recommended_by = models.ForeignKey(HOD, on_delete=models.CASCADE,null=True, blank=True, default=None)
    authorized_by = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True, default=None)
    processed_by = models.ForeignKey(FinanceOfficer, on_delete=models.CASCADE, null=True, blank=True, default=None)
    reason_for_rejection = models.CharField(max_length=255, default=None, null=True, blank=True)
    quotation = models.FileField(default=None, storage='media/attachments', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("requisition", kwargs={"id": self.id})


class BudgetedExpense(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, default=None, null=True, blank=True)
    budget_line = models.ForeignKey(BudgetLine, on_delete=models.CASCADE, default=None, null=True, blank=True)
    description = models.CharField(max_length=150, default=None, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("landing", kwargs={"id": self.id})


class Liquidation(models.Model):
    PAYMENTMODE = (
        ('USD Cash', 'USD Cash'),
        ('ZWL Cash', 'ZWL Cash'),
        ('USD Bank Transfer', 'USD Bank Transfer'),
        ('ZWL Bank Transfer', 'ZWL Bank Transfer')
    )

    STATUS = (
        ('Pending', 'Pending'),
        ('Processed', 'Processed'),
        ('Rejected', 'Rejected'),
        ('Updated', 'Updated'),
    )
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, default=None)
    total_requested = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    compiled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(default=timezone.now)
    processed_by = models.ForeignKey(FinanceOfficer, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    process_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    reason_for_rejection_by_Finance = models.TextField(default=None, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS, default="Pending")
    receipts = models.FileField(default=None, storage='media/attachments', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("liquidation", kwargs={"id": self.id})


class ActualExpense(models.Model):
    liquidation = models.ForeignKey(Liquidation, on_delete=models.CASCADE, default=None, null=True, blank=True)
    budget_line = models.ForeignKey(BudgetLine, on_delete=models.CASCADE, default=None, null=True, blank=True)
    description = models.CharField(max_length=150, default=None, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("landing", kwargs={"id": self.id})
