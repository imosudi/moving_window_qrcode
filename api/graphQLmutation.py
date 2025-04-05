

from.graphQLquery import *

# ===========================================
# GRAPHQL MUTATIONS
# ===========================================
class GenerateQRCode(graphene.Mutation):
    class Arguments:
        instructor_id = graphene.String(required=True)
        course_code = graphene.String(required=True)

    Output = QRCodePayload

    def mutate(self, info, instructor_id, course_code):
        """Fetch course details from the database and generate a secure QR code payload."""
        course = Course.query.filter_by(instructor_id=instructor_id, course_code=course_code).first()
        if not course:
            raise Exception("Course not found or unauthorized instructor.")

        current_time = get_current_server_time()
        print("current_time: ", current_time)
        window_start = (current_time // TIME_WINDOW_DURATION) * TIME_WINDOW_DURATION
        nonce = generate_random_nonce()

        # Check for nonce reuse (security)
        if is_nonce_used(nonce):
            raise Exception("Nonce already used. Possible replay attack detected.")

        payload = {
            "instructor_id": course.instructor_id,
            "course_code": course.course_code,
            "course_level": course.course_level,
            "lecture_start": course.lecture_start.isoformat(),
            "lecture_end": course.lecture_end.isoformat(),
            "window_start": window_start,
            "nonce": nonce
        }
        print(payload, SECRET_KEY)
        enc_payload = hmac_sha256(payload, SECRET_KEY) + " | " + str(payload)

        # Mark nonce as used
        #mark_nonce_as_used(nonce)

        # Log event
        log_event("QR Generation", payload, enc_payload, current_time)

        expiry_time=window_start + TIME_WINDOW_DURATION
        print("expiry_time: ", expiry_time, "window_start: ", window_start, "TIME_WINDOW_DURATION: ", TIME_WINDOW_DURATION)
        
        return QRCodePayload(qr_code_payload=enc_payload,
                              payload=MessageField(
                                    instructor_id = course.instructor_id,
                                    course_code = course.course_code,
                                    course_level = course.course_level,
                                    lecture_start = course.lecture_start.isoformat(),
                                    lecture_end = course.lecture_end.isoformat(),
                                    window_start = window_start,
                                    nonce = nonce
                              ),
                                expiry_time=expiry_time)

# ===========================================
# SERVER-SIDE: Attendance Validation
# ===========================================
class ValidateAttendance(graphene.Mutation):
    class Arguments:
        encrypted_payload = graphene.String(required=True)
        student_id = graphene.String(required=True)

    Output = graphene.JSONString

    def mutate(self, info, encrypted_payload, student_id):
        print("\n", "validate_attendance Mutation", "\n")
        return validate_attendance(encrypted_payload, student_id)

class Mutation(graphene.ObjectType):
    generate_qr_code = GenerateQRCode.Field()
    validate_attendance = ValidateAttendance.Field()

#schema_mutation = graphene.Schema(query=Query, mutation=Mutation)

