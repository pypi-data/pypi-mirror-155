from rest_framework import serializers

from leapchain.constants.network import MAX_POINT_VALUE, VERIFY_KEY_LENGTH


class AccountLockedSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    locked = serializers.IntegerField(min_value=0, max_value=MAX_POINT_VALUE)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
