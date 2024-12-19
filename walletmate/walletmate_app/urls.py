from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),

    path('transactions/', TransactionList.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionDetail.as_view(), name='transaction_detail'),

    path('budget/', BudgetList.as_view(), name='budget_list'),
    path('budget/<int:pk>/', BudgetDetail.as_view(), name='budget_detail'),

    path('expensecategory/', ExpenseCategoryList.as_view(), name='expenseCategory_list'),
    path('expensecategory/<int:pk>/', ExpenseCategoryDetail.as_view(), name='expenseCategory_detail'),


    path('userprofile/', UserProfileList.as_view(), name='userProfile_list'),
    path('userprofile/<int:pk>/', UserProfileDetail.as_view(), name='userProfile_detail'),
        
    path('admin/', admin_view, name='admin_view'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]