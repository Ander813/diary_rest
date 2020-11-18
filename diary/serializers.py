from rest_framework import serializers
from .models import Record, RecordType, AbstractRecordType, CustomUser
from .entity_fields_validators import AbstractEntityValidator, EntityValidator


class RecordSerializer(serializers.ModelSerializer):
    children = serializers.DictField(source='children_dict', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context['request'].method != 'GET':
            self.fields['children'] = serializers.ListField(source='children_list', required=False)

    class Meta:
        model = Record
        fields = ['id', 'create_date', 'edit_date', 'name',
                  'text', 'is_important', 'content', 'children']

    def create(self, validated_data):
        if validated_data.get('children_list'):
            children = validated_data.pop('children_list')
        else:
            children = []

        record = Record.objects.create(**validated_data)
        record.children_list = children
        return record

    def update(self, instance, validated_data):
        if validated_data.get('children_list'):
            children = validated_data.pop('children_list')
        else:
            children = []

        for name, value in validated_data.items():
            setattr(instance, name, value)
        instance.children_list = children

        return instance


class RecordTypeSerializer(serializers.ModelSerializer):
    entity_validator = EntityValidator

    class Meta:
        model = RecordType
        fields = ('name', 'entity', 'parents')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields', '')
        if fields:
            fields = fields.split(',')
            requested = set(fields)
            existing = set(self.fields.keys())

            for drop in existing - requested:
                self.fields.pop(drop)

    def validate(self, attrs):
        for parent in attrs['parents']:
            if parent.name in attrs['entity']:
                self.entity_validator().validate(parent.entity, attrs['entity'][parent.name])
            else:
                raise serializers.ValidationError(f'No data for "{parent.name}" in entity')

        return attrs


class AbstractRecordTypeSerializer(serializers.ModelSerializer):
    entity_validator = AbstractEntityValidator

    class Meta:
        model = AbstractRecordType
        fields = ('name', 'entity')

    def validate(self, attrs):
        self.entity_validator().validate(attrs['entity'])

        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
