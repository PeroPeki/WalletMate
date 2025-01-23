from rest_framework import serializers
from walletmate_app.models import *

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'