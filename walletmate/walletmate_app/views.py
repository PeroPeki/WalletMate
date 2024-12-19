from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Transaction, ExpenseCategory, UserProfile, Budget

homepage_text = "Promijeni!"

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def index(request):
    global homepage_text

    if request.method == "POST" and is_admin(request.user):
        new_text = request.POST.get("homepage_text")
        if new_text.strip():
            homepage_text = new_text
        return redirect('index')

    context = {
        'homepage_text': homepage_text,
        'is_admin': is_admin(request.user),
    }
    return render(request, 'walletmate_app/index.html', context)

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_page.html')

### LIST VIEWS

class TransactionList(ListView):
    model = Transaction
    template_name = 'walletmate_app/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = Transaction.objects.all()
        amount = self.request.GET.get('amount')
        if amount:
            try:
                amount = int(amount)
                queryset = queryset.filter(amount=amount)
            except ValueError:
                pass
        return queryset

class ExpenseCategoryList(ListView):
    model = ExpenseCategory
    template_name = 'walletmate_app/expenseCategory_list.html'
    context_object_name = 'expenseCategories'

    def get_queryset(self):
        created_at = self.kwargs.get('created_at')
        queryset = ExpenseCategory.objects.all()
        if created_at:
            try:
                created_at_date = timezone.datetime.strptime(created_at, "%Y-%m-%d").date()
                queryset = queryset.filter(created_at__date=created_at_date)
            except ValueError:
                pass
        return queryset

class UserProfileList(ListView):
    model = UserProfile
    template_name = 'walletmate_app/userProfile_list.html'
    context_object_name = 'userProfiles'

    def get_queryset(self):
        created_at = self.kwargs.get('created_at')
        queryset = UserProfile.objects.all()
        if created_at:
            try:
                created_at_date = timezone.datetime.strptime(created_at, "%Y-%m-%d").date()
                queryset = queryset.filter(created_at__date=created_at_date)
            except ValueError:
                pass
        return queryset

class BudgetList(ListView):
    model = Budget
    template_name = 'walletmate_app/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        queryset = Transaction.objects.all()
        amount = self.kwargs.get('amount')
        if amount:
            try:
                amount = int(amount)
                queryset = queryset.filter(amount=amount)
            except ValueError:
                pass
        
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(user__username__icontains=search_query)
        return queryset #tu


### DETAIL VIEWS

class TransactionDetail(DetailView):
    model = Transaction
    template_name = 'walletmate_app/transaction_detail.html'
    context_object_name = 'transactions'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    
class ExpenseCategoryDetail(DetailView):
    model = ExpenseCategory
    template_name = 'walletmate_app/expenseCategory_detail.html'
    context_object_name = 'expenseCategories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context   

class UserProfileDetail(DetailView):
    model = UserProfile
    template_name = 'walletmate_app/userProfile_detail.html'
    context_object_name = 'userProfiles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    
class BudgetDetail(DetailView):
    model = Budget
    template_name = 'walletmate_app/budget_detail.html'
    context_object_name = 'budgets'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

### REGISTRATION/LOGIN

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user_group, created = Group.objects.get_or_create(name='Korisnik')
            user.groups.add(user_group)

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')
