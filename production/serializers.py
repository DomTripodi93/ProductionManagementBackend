from .models import ProUser, Production, Machine, HourlyProduction, Part, ChangeLog
from rest_framework import serializers


class ProUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ProUser
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = ProUser(
            email = validated_data['email'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, validated_data):
        user = ProUser

class ProductionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Production
        fields = ('id', 'user_id', 'machine', 'shift', 'job', 'quantity','date', 'in_question')
        extra_kwargs = {'user_id' : {'read_only': True}}

class MachineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ('id', 'user_id', 'machine', 'current_job',)
        extra_kwargs = {'user_id' : {'read_only': True}}

class PartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Part
        fields = (
            'id', 
            'user_id', 
            'machine', 
            'job', 
            "cycle_time", 
            "part", 
            'order_quantity',
            'possible_quantity',
            'remaining_quantity',
            'weight_recieved',
            'weight_length',
            'weight_quantity',
            'oal',
            'cut_off',
            'main_facing',
            'sub_facing',
            'heat_lot',
            "bars",
        )
        extra_kwargs = {'user_id' : {'read_only': True}}

class StartTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Part
        fields = (
            'id', 
            'user_id', 
            'machine', 
            "date", 
            "time"
        )
        extra_kwargs = {'user_id' : {'read_only': True}}




class HourlyProductionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HourlyProduction
        fields = (
            'id', 
            'user_id', 
            "hard_quantity", 
            "counter_quantity", 
            'machine', 
            'job', 
            "time", 
            "date",
        )
        extra_kwargs = {'user_id' : {'read_only': True}}

class ChangeLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChangeLog
        fields = ('id', 'user_id', "old_values", "change_type", "changed_id", "changed_model", "timestamp",)
        extra_kwargs = {'user_id' : {'read_only': True}}

        