from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from .forms import RequisitionForm, ActualExpenseForm, CloseLiquidationForm, ProcessLiquidationForm, ConfirmPaymentForm, LiquidationForm, ProcessRequisitionForm ,BudgetedExpenseForm, AuthoriseRequisitionForm, RecommendRequisitionForm
from .filters import RequisitionFilter, LiquidationFilter
from expenses.models import Requisition, Liquidation, BudgetedExpense, ActualExpense, Budget
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users, unauthenticated_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# ******************* AllCreate Views ***********************

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 'Finance Officer', 'Director', 'Admin Staff'])
def requisitionCreate(request):
    form = RequisitionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.requested_by = request.user
        instance.save() 

        return redirect('/requisitions')

    context = {'form': form}

    return render(request, 'expenses/requisition_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 'Finance Officer', 'Director', 'Admin Staff'])
def liquidationCreate(request, pk):
    requisition = Requisition.objects.get(id=pk)
    form = LiquidationForm(initial={'requisition': requisition})

    if request.method == 'POST':
        form = LiquidationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liquidations')

    context = {'form': form}
    return render(request, 'expenses/liquidation_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 'Finance Officer', 'Director', 'Admin Staff'])
def budgetedExpenseCreate(request, pk):
    BudgetedExpenseFormSet = inlineformset_factory(Requisition,
                                                 BudgetedExpense,
                                                 fields=(
                                                     'requisition',
                                                     'budget_line',
                                                     'description',
                                                     'quantity',
                                                     'unit_cost',
                                                     'total'),
                                                 extra=5)
    requisition = Requisition.objects.get(id=pk)
    formset = BudgetedExpenseFormSet(queryset=BudgetedExpense.objects.none(), instance=requisition)

    if request.method == 'POST':
        formset = BudgetedExpenseFormSet(request.POST, instance=requisition)
        if formset.is_valid():
            formset.save()
            return redirect('/requisitions' )

    context = {'formset': formset, 'requisition': requisition}
    return render(request, 'expenses/budgetedExpense_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 'Finance Officer', 'Director', 'Admin Staff'])
def actualExpenseCreate(request, pk):
    ActualExpenseFormSet = inlineformset_factory(Liquidation,
                                                 ActualExpense,
                                                 fields=(
                                                        'liquidation',
                                                        'budget_line',
                                                        'description',
                                                        'quantity',
                                                        'unit_cost',
                                                        'total'),
                                                 extra=5)
    liquidation = Liquidation.objects.get(id=pk)
    formset = ActualExpenseFormSet(queryset=ActualExpense.objects.none(), instance=liquidation)

    if request.method == 'POST':
        formset = ActualExpenseFormSet(request.POST, instance=liquidation)
        if formset.is_valid():
            formset.save()
            return redirect('/liquidations')

    context = {'formset': formset, 'liquidation': liquidation}
    return render(request, 'expenses/actualExpense_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officers', 'Head of Department','Manager', 'Finance Officer', 'Director', 'Admin Staff'])
def updateActualExpense(request, pk):
    actualExpense = ActualExpense.objects.get(id=pk)
    ActualExpenseFormSet = inlineformset_factory(Liquidation, ActualExpense, fields=(
                                                        'liquidation',
                                                        'budget_line',
                                                        'description',
                                                        'quantity',
                                                        'unit_cost',
                                                        'total'),
                                                 extra=5)
    formset = ActualExpenseFormSet(instance=actualExpense)

    context = {'formset': formset, 'actualExpense':actualExpense}
    return render(request, 'expenses/actualExpense_form.html', context)



# ************************* List Views *****************************

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def requisitionsDashboard(request):
    requisitions = Requisition.objects.all()
    pending = requisitions.filter(status='Pending').count()
    recommended = requisitions.filter(status='Recommended').count()
    authorised = requisitions.filter(status='Authorised').count()
    rejected = requisitions.filter(status='Rejected').count()
    processed = requisitions.filter(status='Processed').count()
    paid = requisitions.filter(status='Paid').count()
    confirmed = requisitions.filter(status='Confirmed').count()

    myFilter = RequisitionFilter(request.GET, queryset=requisitions)
    requisitions = myFilter.qs
   
    context = {
            'requisitions': requisitions,
            'pending': pending,
            'recommended': recommended,
            'authorised': authorised,
            'rejected': rejected,
            'processed': processed,
            'paid': paid, 
            'confirmed': confirmed,
            'myFilter': myFilter,
           }

    return render(request, 'expenses/requisitions.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def liquidationsDashboard(request):
    liquidations = Liquidation.objects.all().order_by('-date_submitted')
    pending = liquidations.filter(status='Pending').count()
    rejected = liquidations.filter(status='Rejected').count()
    processed = liquidations.filter(status='Processed').count()
    closed = liquidations.filter(status='Closed').count()

    myFilter = LiquidationFilter(request.GET, queryset=liquidations)
    liquidations = myFilter.qs

    context = {'liquidations': liquidations, 'pending': pending,
               'rejected': rejected, 'processed': processed, 'closed': closed, 'myFilter': myFilter}

    return render(request, 'expenses/liquidations.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Finance officer', 'Manager', ])
def landing(request):
    budgetedExpenses = BudgetedExpense.objects.all()
    actualExpenses = ActualExpense.objects.all()
    context = {'budgetedExpenses': budgetedExpenses, 'actualExpenses': actualExpenses}
    return render(request, 'expenses/landing.html', context)


# ************************ Detail Views *************************

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def requisition(request, pk):
    requisition = Requisition.objects.get(id=pk)
    budgetedExpenses = BudgetedExpense.objects.all().order_by('-id').filter(requisition=requisition)
    liquidations = requisition.liquidation_set.all()

    context = {'requisition': requisition, 'liquidations': liquidations, 'budgetedExpenses': budgetedExpenses}
    return render(request, 'expenses/requisition.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def liquidation(request, pk):
    liquidation = Liquidation.objects.get(id=pk)
    actualExpenses = ActualExpense.objects.all().order_by('-id').filter(liquidation=liquidation)

    context = {'liquidation': liquidation, 'actualExpenses': actualExpenses}
    return render(request, 'expenses/liquidation.html', context)


######################## Update Views ####################################

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department', 'Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def updateRequisition(request, pk):
    requisition = Requisition.objects.get(id=pk)
    form = RequisitionForm(instance=requisition)

    if request.method == 'POST':
        form = RequisitionForm(request.POST, instance= requisition)
        if form.is_valid():
            form.save() 
            return redirect('/requisitions')

    context = {'form': form}
    return render(request, 'expenses/requisition_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def updateLiquidation(request, pk):
    liquidation = Liquidation.objects.get(id=pk)
    form = LiquidationForm(instance=liquidation)

    if request.method == 'POST':
        form = LiquidationForm(request.POST, instance= liquidation)
        if form.is_valid():
            form.save() 
            return redirect('/liquidations')

    context = {'form': form}
    return render(request, 'expenses/liquidation_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def updateBudgetedExpense(request, pk):
    budgetedExpense = BudgetedExpense.objects.get(id=pk)
    form = BudgetedExpenseForm(instance=budgetedExpense)

    if request.method == 'POST':
        form = BudgetedExpenseForm(request.POST, instance= budgetedExpense)
        if form.is_valid():
            form.save() 
            return redirect('/requisitions')

    context = {'form': form}
    return render(request, 'expenses/budgetedExpense_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Projects Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def updateActualExpense(request, pk):
    actualExpense = ActualExpense.objects.get(id=pk)
    form = ActualExpenseForm(instance=actualExpense)

    if request.method == 'POST':
        form = ActualExpenseForm(request.POST, instance= actualExpense)
        if form.is_valid():
            form.save() 
            return redirect('/requisitions')

    context = {'form': form}
    return render(request, 'expenses/actualExpense_form.html', context)

# ************************** Requisition Approval *****************************

@login_required(login_url='login')
@allowed_users(allowed_roles=['Head of Department','Manager', 'Director'])
def recommendRequisition(request, pk):
    requisition = Requisition.objects.get(id=pk)
    form = RecommendRequisitionForm(instance=requisition)

    if request.method == 'POST':
        form = RecommendRequisitionForm(request.POST, instance=requisition)
        if form.is_valid():
            
            form.save()
            return redirect('/requisitions')

    context = {'form': form}
    return render(request, 'expenses/recommendationForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Manager', 'Director'])
def authoriseRequisition(request, pk):
    requisition = Requisition.objects.get(id=pk)
    form = AuthoriseRequisitionForm(instance=requisition)

    if request.method == 'POST':
        form = AuthoriseRequisitionForm(request.POST, instance=requisition)
        if form.is_valid():
            form.save()
            return redirect('/requisitions')

    context = {'form': form}
    return render(request, 'expenses/authoriseRequisition.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Finance Officer'])
def processRequisition(request, pk):
    requisition = Requisition.objects.get(id=pk)
    form = ProcessRequisitionForm(instance=requisition)

    if request.method == 'POST':
        form = ProcessRequisitionForm(request.POST, instance=requisition)
        if form.is_valid():
            form.save()
            return redirect('/requisitions')

    context = {'form': form}
    return render(request, 'expenses/processRequisition.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def confirmPayment(request, pk):
    requisition = Requisition.objects.get(id=pk)
    form = ConfirmPaymentForm(instance=requisition)

    if request.method == 'POST':
        form = ConfirmPaymentForm(request.POST, instance=requisition)
        if form.is_valid():
            form.save()
            return redirect('/requisitions')

    context = {'form': form}
    return render(request, 'expenses/paymentConfirmation.html', context)


# ********************* Liquidation Approval **********************

@login_required(login_url='login')
@allowed_users(allowed_roles=['Finance Officer'])
def processLiquidation(request, pk):
    liquidation = Liquidation.objects.get(id=pk)
    form = ProcessLiquidationForm(instance=liquidation)

    if request.method == 'POST':
        form = ProcessLiquidationForm(request.POST, instance=liquidation)
        if form.is_valid():
            form.save()
            return redirect('/liquidations')

    context = {'form': form}
    return render(request, 'expenses/processLiquidation.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Manager', 'Director', ])
def closeLiquidation(request, pk):
    liquidation = Liquidation.objects.get(id=pk)
    form = CloseLiquidationForm(instance=liquidation)

    if request.method == 'POST':
        form = CloseLiquidationForm(request.POST, instance=liquidation)
        if form.is_valid():
            form.save()
            return redirect('/liquidations')

    context = {'form': form}
    return render(request, 'expenses/closeLiquidation.html', context)


####################### Delete Views ##############################

@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def deleteRequisition(request, pk):
    requisition = Requisition.objects.get(id=pk)
    if request.method == "POST":
        requisition.delete()
        return redirect('/requisitions')

    context = {'item': requisition}
    return render(request, 'expenses/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def deleteLiquidation(request, pk):
    liquidation = Liquidation.objects.get(id=pk)
    if request.method == "POST":
        liquidation.delete()
        return redirect('/liquidations')

    context = {'item': liquidation}
    return render(request, 'expenses/deleteLiquidation.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def deleteBudgetedExpense(request, pk):
    budgetedExpense = BudgetedExpense.objects.get(id=pk)
    if request.method == "POST":
        budgetedExpense.delete()
        return redirect('/requisitions')

    context = {'item': budgetedExpense}
    return render(request, 'expenses/deleteBudgetedExpense.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Officer', 'Head of Department','Manager', 
'Finance Officer', 'Director', 'Admin Staff'])
def deleteActualExpense(request, pk):
    actualExpense = ActualExpense.objects.get(id=pk)
    if request.method == "POST":
        actualExpense.delete()
        return redirect('/liquidations')
    context = {'item': actualExpense}
    return render(request, 'expenses/deleteActualExpense.html', context)
