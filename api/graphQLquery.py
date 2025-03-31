from .helpers import *
import graphene
from sqlalchemy.exc import IntegrityError

# ===========================================
# GRAPHQL OBJECT TYPES
# ===========================================
class RoleObject(graphene.ObjectType):
    class Meta:
        model = Role
        interfaces = (graphene.relay.Node,)

class UserObject(graphene.ObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)

class AttendanceObject(graphene.ObjectType):
    class Meta:
        model = Attendance
        interfaces = (graphene.relay.Node,)

# ===========================================
# GRAPHQL QUERY
# ===========================================
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = graphene.List(UserObject)
    all_roles = graphene.List(RoleObject)
    all_attendance = graphene.List(AttendanceObject)

    def resolve_all_users(self, info):
        return User.query.all()

    def resolve_all_roles(self, info):
        return Role.query.all()
    
    def resolve_all_attendance(self, info):
        return Attendance.query.all()

schema_query = graphene.Schema(query=Query)


COURSE_DETAILS = {
    "instructor_id": "INS123",
    "course_code": "SEN312",
    "course_level": "400",
    "lecture_start": "2025-04-01T08:00:00Z",
    "lecture_end": "2025-04-01T10:00:00Z"
}
