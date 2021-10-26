from rest_framework import serializers

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):
        # TODO
        # Validar o pacote, checar se ele existe na versão especificada.
        # Buscar a última versão caso ela não seja especificada pelo usuário.
        # Subir a exceção `serializers.ValidationError()` se o pacote não
        # for válido.
        print('primeiro com data %s' %data)
        
        if 'version' not in data:
            validated_data = latest_version(data['name'])

            if validated_data == None:
                serializers.ValidationError()

            return validated_data
        
        if not version_exists(data['name'], data['version']):
            serializers.ValidationError()

        validated_data = {'name': data['name'], 'version': data['version']}
        return validated_data


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        # TODO
        # Salvar o projeto e seus pacotes associados.
        #
        # Algumas referência para uso de models do Django:
        # - https://docs.djangoproject.com/en/3.2/topics/db/models/
        # - https://www.django-rest-framework.org/api-guide/serializers/#saving-instances

        print('terceiro com data %s' %validated_data)
        print(self)
        project = Project(name=validated_data['name'])
        print(project.id)
        project.save()
        
        print(project)

        for package in validated_data['packages']:
            package_release = PackageRelease(project_id=project.id, name=package['name'], version=package['version'])
            package_release.save()
        
        return project
