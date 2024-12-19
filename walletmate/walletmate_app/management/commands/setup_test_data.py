import random

from django.db import transaction
from django.core.management.base import BaseCommand

from walletmate_app.models import *
from walletmate_app.factory import *

NUM_USERS = 10
NUM_EXPENSE_CATEGORIES = 5
NUM_TRANSACTIONS = 50
NUM_USER_PROFILES = 10
NUM_BUDGETS = 20

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")

        models = [User, ExpenseCategory, Transaction, UserProfile, Budget]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_USERS):
            user = UserFactory()

        for _ in range(NUM_EXPENSE_CATEGORIES):
            category = ExpenseCategoryFactory()

        for _ in range(NUM_TRANSACTIONS):
            transaction = TransactionFactory()

        for _ in range(NUM_USER_PROFILES):
            user_profile = UserProfileFactory()

        for _ in range(NUM_BUDGETS):
            budget = BudgetFactory()

        self.stdout.write(self.style.SUCCESS('Successfully created test data!'))