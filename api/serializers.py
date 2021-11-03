from rest_framework import serializers

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):
        
        if "version" not in data:
            validated_data = latest_version(data["name"])

            if validated_data == None:
                raise serializers.ValidationError()

            return validated_data
        
        if not version_exists(data["name"], data["version"]):
            raise serializers.ValidationError()

        validated_data = {"name": data["name"], "version": data["version"]}
        return validated_data


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        
        project = Project(name=validated_data["name"])
        project.save()

        for package in validated_data["packages"]:
            exist = PackageRelease.objects.filter(name=package["name"], project_id=project.id)
                        
            if exist:
                continue

            package_release = PackageRelease(
                project_id=project.id, 
                name=package["name"], 
                version=package["version"]
            )
            package_release.save()
        
        return project
