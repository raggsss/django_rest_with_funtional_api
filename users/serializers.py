from rest_framework import serializers

from users.models import DUser


class DUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DUser
        # fields = ['id', 'first_name', 'last_name', 'address', 'contact', 'email_id', 'website', 'is_active']
        fields = "__all__"
