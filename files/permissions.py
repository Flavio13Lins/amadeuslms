from rolepermissions.permissions import register_object_checker
from amadeus.roles import SystemAdmin

@register_object_checker()
def edit_file(role, user, file):
    if (role == SystemAdmin):
        return True

    if (user in file.topic.subject.professors.all()):
        return True

    return False

@register_object_checker()
def delete_file(role, user, file):
    if (role == SystemAdmin):
        return True

    if (user in file.topic.subject.professors.all()):
        return True

    return False