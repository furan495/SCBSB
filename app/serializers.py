from app.models import *
from rest_framework import serializers


class ProblemSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    def get_key(self, obj):
        return obj.id

    class Meta:
        model = Problem
        fields = ('id', 'key', 'theme', 'number', 'promoter', 'receiver', 'carbonCopy', 'createTime', 'expectTime',
                  'endTime', 'status', 'description', 'promAdvice', 'receAdvice', 'appendix', 'read', 'updateCount')


class ProjectSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()
    sections = serializers.StringRelatedField(many=True, read_only=True)
    progresses = serializers.StringRelatedField(many=True, read_only=True)
    """ status = serializers.ChoiceField(
        choices=PROJECT_STATUS, source='get_status_display', read_only=True) """
    persons = serializers.StringRelatedField(many=True, read_only=True)

    def get_key(self, obj):
        return obj.id

    class Meta:
        model = Project
        fields = ('id', 'name', 'key', 'status', 'owner',
                  'startTime', 'endTime', 'number', 'sections', 'progresses', 'persons')


class DepartmentSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'members')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'time')


class BomAnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomAna
        fields = ('time', 'operator', 'target', 'result')


class UserSerializer(serializers.ModelSerializer):

    key = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_key(self, obj):
        return str(obj.id)

    def get_title(self, obj):
        return obj.name

    class Meta:
        model = User
        fields = ('id', 'department', 'role', 'projects',
                  'name', 'phone', 'gender', 'password', 'key', 'title')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'authority')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'project', 'name', 'time',
                  'description')


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('id', 'project', 'name', 'time',
                  'description', 'creator')
