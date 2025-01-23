from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('', index, name='index'),

    path('transactions/', TransactionList.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionDetail.as_view(), name='transaction_detail'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('transaction/<int:pk>/update/', TransactionUpdate.as_view(), name='update_transaction'),
    path('transaction/<int:pk>/delete/', TransactionDelete.as_view(), name='delete_transaction'),

    path('budget/', BudgetList.as_view(), name='budget_list'),
    path('budget/<int:pk>/', BudgetDetail.as_view(), name='budget_detail'),
    path('add-budget/', add_budget, name='add_budget'),
    path('budget/<int:pk>/update/', BudgetUpdate.as_view(), name='update_budget'),
    path('budget/<int:pk>/delete/', BudgetDelete.as_view(), name='delete_budget'),

    path('expensecategory/', ExpenseCategoryList.as_view(), name='expenseCategory_list'),
    path('expensecategory/<int:pk>/', ExpenseCategoryDetail.as_view(), name='expenseCategory_detail'),
    path('add-category/', add_category, name='add_category'),
    path('expensecategory/<int:pk>/update/', ExpenseCategoryUpdate.as_view(), name='update_category'),
    path('expensecategory/<int:pk>/delete/', ExpenseCategoryDelete.as_view(), name='delete_category'),
    
    path('userprofile/', UserProfileList.as_view(), name='userProfile_list'),
    path('userprofile/<int:pk>/', UserProfileDetail.as_view(), name='userProfile_detail'),
    path('userprofile/<int:pk>/update/', UserUpdate.as_view(), name='update_user'),
    path('userprofile/<int:pk>/delete/', UserDelete.as_view(), name='delete_user'),
        
    path('admin/', admin_view, name='admin_view'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]



router = DefaultRouter()
router.register(r'api/transactions', TransactionViewSet, basename='transaction')

# Add router-generated URLs to urlpatterns
urlpatterns += router.urls

urlpatterns += [
    path('api/token/', ObtainAuthToken.as_view(), name='api_token_auth'),
]