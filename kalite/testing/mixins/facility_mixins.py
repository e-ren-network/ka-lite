from kalite.facility.models import Facility, FacilityGroup, FacilityUser


class CreateFacilityMixin(object):
    DEFAULTS = {
        'id': 1,
        'name': 'facility0',
        'description': 'a default facility',
        'user_count': 1,
    }

    @classmethod
    def create_facility(cls, **kwargs):
        # we want this class's DEFAULTS, not whoever has inherited and thus overrided it!
        fields = CreateFacilityMixin.DEFAULTS.copy()
        fields.update(**kwargs)

        obj, created = Facility.objects.get_or_create(**fields)
        return obj


class CreateGroupMixin(CreateFacilityMixin):
    DEFAULTS = {
        'name': 'group0',
    }

    @classmethod
    def create_group(cls, **kwargs):
        fields = CreateGroupMixin.DEFAULTS.copy()
        fields.update(**kwargs)
        fields['facility'] = (fields.get('facility') or
                              cls.create_facility())
        return FacilityGroup.objects.create(**fields)


class CreateStudentMixin(CreateFacilityMixin):
    DEFAULTS = {
        'first_name': 'Cannon',
        'last_name': 'Fodder',
        'username': 'teststudent1',
        'password': 'password',
        'is_teacher': False
    }

    @classmethod
    def create_student(cls, password='password', **kwargs):
        fields = CreateStudentMixin.DEFAULTS.copy()
        fields.update(**kwargs)
        fields['facility'] = (fields.get('facility') or
                              cls.create_facility())
        user = FacilityUser(**fields)
        user.set_password(password)
        user.save()
        return user


class CreateTeacherMixin(CreateFacilityMixin):
    DEFAULTS = {
        'first_name': 'Teacher 1',
        'last_name': 'Sample',
        'username': 'teacher1',
        'password': 'password',
        'is_teacher': True
    }

    @classmethod
    def create_teacher(cls, **kwargs):
        fields = CreateTeacherMixin.DEFAULTS.copy()
        fields.update(**kwargs)
        fields['facility'] = (fields.get('facility') or
                              cls.create_facility())
        user = FacilityUser(**fields)
        user.set_password(fields['password'])
        user.save()
        return user


class FacilityMixins(CreateStudentMixin, CreateGroupMixin, CreateTeacherMixin, CreateFacilityMixin):
    '''
    Toplevel class that has all the mixin methods defined above
    '''
    pass
