from app.models import *
from app.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProgressesViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def membersFormat(self, memberList, key):
        members = []
        for ind, member in zip(range(len(memberList)), memberList):
            members.append(
                {'key': '%s-%s' % (key, ind+1), 'title': member.name, 'value': member.name})
        return members

    def list(self, request, *args, **kwargs):
        departments = []
        queryset = self.filter_queryset(self.get_queryset())

        for ind, department in zip(range(len(queryset)), queryset):
            members = department.members.all()
            departments.append(
                {'key': '1-%s' % (ind+1), 'title': department.name, 'value': department.name,  'children': self.membersFormat(members, '1-%s' % (ind+1))})

        tree = [
            {'key': '1', 'title': '北京华晟智造科技有限公司',
                'value': '北京华晟智造科技有限公司', 'children': departments}
        ]

        return Response(tree)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class BomAnaViewSet(viewsets.ModelViewSet):
    queryset = BomAna.objects.all()
    serializer_class = BomAnaSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
