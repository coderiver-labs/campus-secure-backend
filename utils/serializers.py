from rest_framework import serializers



# create serializer hare


class DummySerializer(serializers.Serializer):
    pass



READ_ONLY_FIELDS = ["uuid", "created_at", "updated_at"]