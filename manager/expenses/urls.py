from django.urls import path, re_path
from django.contrib.auth.models import User
from . import views


urlpatterns = [

# ******************************* List URLs *****************************
    
    path('requisitions/', views.requisitionsDashboard, name='requisitions'), # List Requisitions
    path('liquidations/', views.liquidationsDashboard, name='liquidations'), # List Liquidations
    path('landing/', views.landing, name='landing'),

 # ******************************* Create URLs ****************************

    path('create_requisition/', views.requisitionCreate, name='create_requisition'),
    path('create_budgetedExpense/<str:pk>', views.budgetedExpenseCreate, name='create_budgetedExpense'),
    path('create_liquidation/<str:pk>/', views.liquidationCreate, name='create_liquidation'),
    path('create_actualExpense/<str:pk>', views.actualExpenseCreate, name='create_actualExpense'),

# ******************************* Detail URLs ****************************


    path('liquidation/<str:pk>/', views.liquidation, name='liquidation'),
    path('requisition/<str:pk>/', views.requisition, name='requisition'),
    # re_path(r'requisition/(?P<pk>[0-9]+)/$', views.requisition, name='requisition'),
    


# ******************************* Update URLs ****************************
    
    path('update_budgetedExpense/<str:pk>/', views.updateBudgetedExpense, name='update_budgetedExpense'),
    path('update_actualExpense/<str:pk>/', views.updateActualExpense, name='update_actualExpense'),
    path('update_liquidation/<str:pk>/', views.updateLiquidation, name='update_liquidation'),
    path('update_requisition/<str:pk>/', views.updateRequisition, name='update_requisition'),

# ******************************* Approval Flow URLs ****************************

    path('recommend-requisition/<str:pk>/', views.recommendRequisition, name='recommend-requisition'),
    path('authorise-requisition/<str:pk>/', views.authoriseRequisition, name='authorise-requisition'),
    path('process-requisition/<str:pk>/', views.processRequisition, name='process-requisition'),
    path('confirm-payment/<str:pk>/', views.confirmPayment, name='confirm-payment'),

    path('process-liquidation/<str:pk>/', views.processLiquidation, name='process-liquidation'),
    path('close-liduidation/<str:pk>/', views.closeLiquidation, name='close-liquidation'),

# ******************************* Delete URLs *****************************

    path('delete_actualExpense/<str:pk>/', views.deleteActualExpense, name='delete_actualExpense'),
    path('delete_budgetedExpense/<str:pk>/', views.deleteBudgetedExpense, name='delete_budgetedExpense'),
    path('delete_requisition/<str:pk>/', views.deleteRequisition, name='delete_requisition'),
    path('delete_liquidation/<str:pk>/', views.deleteLiquidation, name='delete_liquidation')
]