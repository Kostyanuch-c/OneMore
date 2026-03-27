from apps.access.entities import TutorStudentMembershipEntity


def assert_membership_entity(entity, *, student_id, tutor_id, is_active=True):
    assert isinstance(entity, TutorStudentMembershipEntity)
    assert entity.id is not None
    assert entity.student_id == student_id
    assert entity.tutor_id == tutor_id
    assert entity.is_active is is_active


def assert_membership_model(model, *, student_id, tutor_id, is_active=True):
    assert model.id is not None
    assert model.student_id == student_id
    assert model.tutor_id == tutor_id
    assert model.is_active is is_active
    assert model.created_at is not None
    assert model.updated_at is not None


def assert_membership_matches_db_model(entity, model):
    assert entity.id == model.id
    assert entity.student_id == model.student_id
    assert entity.tutor_id == model.tutor_id
    assert entity.is_active == model.is_active
    assert entity.created_at == model.created_at
    assert entity.updated_at == model.updated_at
