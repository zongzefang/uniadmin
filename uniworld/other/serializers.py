from rest_framework import serializers
from other.models import *

class LabelInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Label
        exclude=('description_ch','description_en','parent','tree_id','lft','rght','level')

class LabelDetailSerializer(serializers.ModelSerializer):
    father=LabelInfoSerializer(read_only=True)

    class Meta:
        model=Label
        fields='__all__'

class TitleLabelSerializer(serializers.ModelSerializer):

    class Meta:
        model=TitleLabel
        fields='__all__'

class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model=University
        fields='__all__'