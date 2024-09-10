from rest_framework import serializers
from apps.stbs.models import Language, STBManufacture, Natco, NactoManufactureLanguage
import re


def non_number_validator(value):
    if value and not re.match(r'^[a-zA-Z/S]+$', value):
        raise serializers.ValidationError("Cannot Contain Numbers")
    return value


class LanguageSerializer(serializers.ModelSerializer):

    language_name = serializers.CharField(required=True, max_length=20)

    class Meta:
        fields = ('id', 'language_name',)
        model = Language

    def validate_language_name(self, value):
        if value is None:
            raise serializers.ValidationError("Language Field cannot be Empty")
        elif value and not re.match(r"^[a-zA-Z/S]+$", value):
            raise serializers.ValidationError("Language Cannot Contain Numbers and Symbols")
        return value


class STBManufactureSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', )
        model = STBManufacture

    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError("STB Manufacture Name Cannot be Empty")
        elif value and not re.match(r"^[a-zA-Z/S]+$", value):
            raise serializers.ValidationError("STB Manufacture Name Cannot Contain Numbers")
        return value
    
    def validate(self, attrs):
        if attrs['name']:
            if STBManufacture.objects.filter(name=attrs['name']).exists():
                raise serializers.ValidationError("STB Manufacture Already Exists")
            else:
                return attrs
        else:
            raise serializers.ValidationError("Name Field Cannot be Empty")


class NactoSerializer(serializers.ModelSerializer):

    country = serializers.CharField(required=True, validators=[non_number_validator])
    natco = serializers.CharField(required=True, validators=[non_number_validator])

    class Meta:
        fields = ('id', 'country', 'natco',)
        model = Natco

    def validate(self, attrs): 
        if attrs['country'] and attrs['natco']:
            if Natco.objects.filter(country=attrs['country'], natco=attrs['natco']).exists():
                raise serializers.ValidationError("Country or Nacto Already Present Please Check")
        return attrs
    

class NatcoLanguageSerializer(serializers.ModelSerializer):

    natco = serializers.PrimaryKeyRelatedField(queryset=Natco.objects.all(), required=True)
    device_name = serializers.PrimaryKeyRelatedField(queryset=Natco.objects.all(), required=True)
    language_name = serializers.PrimaryKeyRelatedField(queryset=Natco.objects.all(), required=True)

    class Meta:
        fields = ('id', 'natco', 'device_name', 'language_name',)
        model = NactoManufactureLanguage


class NatcoOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Natco
        fields = ('natco',)


class LanguageOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('language_name',)


class DeviceOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = STBManufacture
        fields = ('name',)


class ReportFilterSerializer(serializers.Serializer):

    device_name = serializers.CharField(source="device_name__name", required=False)
