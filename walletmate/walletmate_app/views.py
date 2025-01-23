from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import *
from django.urls import reverse, reverse_lazy
from rest_framework.viewsets import ModelViewSet
from walletmate_app.serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

### LIST VIEWS ###

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
        created_at = self.request.GET.get('created_at')
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


### DETAIL VIEWS ###

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

### REGISTRATION/LOGIN ###

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


### ADD ###

def add_budget(request):
    if request.method == "POST":
        user_id = request.POST.get('user')
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not all([user_id, category_id, amount, start_date, end_date]):
            return render(request, 'add/add_budget.html', {
                'error': 'Sva polja su obavezna.',
                'users': User.objects.all(),
                'categories': ExpenseCategory.objects.all(),
            })

        try:
            user = get_object_or_404(User, pk=user_id)
            category = get_object_or_404(ExpenseCategory, pk=category_id)

            budget = Budget.objects.create(
                user=user,
                category=category,
                amount=amount,
                start_date=start_date,
                end_date=end_date,
            )
            return redirect('budget_detail', pk=budget.pk)
        except Exception as e:
            return render(request, 'add/add_budget.html', {
                'error': f'Greška prilikom dodavanja budžeta: {str(e)}',
                'users': User.objects.all(),
                'categories': ExpenseCategory.objects.all(),
            })

    return render(request, 'add/add_budget.html', {
        'users': User.objects.all(),
        'categories': ExpenseCategory.objects.all(),
    })


def add_transaction(request):
    if request.method == "POST":
        user_id = request.POST.get('user')
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        description = request.POST.get('description', '')
        date = request.POST.get('date')

        if not all([user_id, category_id, amount, transaction_type, date]):
            return render(request, 'add/add_transaction.html', {
                'error': 'Sva polja su obavezna.',
                'users': User.objects.all(),
                'categories': ExpenseCategory.objects.all(),
            })

        try:
            user = get_object_or_404(User, pk=user_id)
            category = get_object_or_404(ExpenseCategory, pk=category_id)

            transaction = Transaction.objects.create(
                user=user,
                category=category,
                amount=amount,
                transaction_type=transaction_type,
                description=description,
                date=date,
            )

            return redirect('transaction_detail', pk=transaction.pk)

        except Exception as e:
            return render(request, 'add/add_transaction.html', {
                'error': f'Greška prilikom dodavanja transakcije: {str(e)}',
                'users': User.objects.all(),
                'categories': ExpenseCategory.objects.all(),
            })

    return render(request, 'add/add_transaction.html', {
        'users': User.objects.all(),
        'categories': ExpenseCategory.objects.all(),
    })

def add_category(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if not name.strip():
            return render(request, 'add/add_expenseCategory.html',{
                'error': 'Naziv kategorije je obavezan!'
            })
        
        expenseCategory = ExpenseCategory.objects.create(
            name = name,
            description = description
        )
        
        return redirect(reverse('expenseCategory_detail', args=[expenseCategory.id]))
    return render(request, 'add/add_expenseCategory.html')

### UPDATE ###


class TransactionUpdate(UpdateView):
    model = Transaction
    template_name = 'update/update_transaction.html'
    fields = ['user', 'category', 'amount', 'description', 'date']
    
    def get_success_url(self):
        return reverse('transaction_detail', kwargs={'pk': self.object.pk})
    
class BudgetUpdate(UpdateView):
    model = Budget
    template_name = 'update/update_budget.html'
    fields = ['user', 'category', 'amount', 'end_date']
    
    
    def get_success_url(self):
        return reverse('budget_detail', kwargs={'pk': self.object.pk})
    
class ExpenseCategoryUpdate(UpdateView):
    model = ExpenseCategory
    template_name = 'update/update_category.html'
    fields = ['name', 'description']
    
    def get_success_url(self):
        return reverse('expenseCategory_detail', kwargs={'pk': self.object.pk})
    

class UserUpdate(UpdateView):
    model = UserProfile
    template_name = 'update/update_category.html'
    fields = ['user', 'currency']
    
    def get_success_url(self):
        return reverse('userProfile_detail', kwargs={'pk': self.object.pk})

### DELETE ###

class TransactionDelete(DeleteView):
    model = Transaction
    success_url = reverse_lazy('transaction_list')
    
class BudgetDelete(DeleteView):
    model = Budget
    success_url = reverse_lazy('budget_list')
    

class ExpenseCategoryDelete(DeleteView):
    model = ExpenseCategory
    success_url = reverse_lazy('expenseCategory_list')
    
class UserDelete(DeleteView):
    model = UserProfile
    success_url = reverse_lazy('userProfile_list')


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

class TransactionList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)