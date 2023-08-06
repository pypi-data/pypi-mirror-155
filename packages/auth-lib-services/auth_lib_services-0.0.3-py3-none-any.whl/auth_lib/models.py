from django.contrib.auth.models import AbstractBaseUser

class CustomPermission():
    def __init__(self, id, codename):
        self.id = id
        self.codename = codename

class CustomGroup():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.permissions = []

class Program():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def from_json(self, json):
        self.id = json['id']
        self.name = json['name']
        return self

class TokenUser(AbstractBaseUser):
    def from_json(self, data):
        self.id = data['id']
        self.is_active = data['is_active']
        self.custom_permissions = data['user_permissions']
        self.program = Program().from_json(data['program'])
        self.custom_groups = []

        for group in data['groups']:
            group_model = CustomGroup(id=group['id'], name=group['name'])
            for permission in group['permissions']:
                permission_model = CustomPermission(id=permission['id'], codename=permission['codename'])
                group_model.permissions.append(permission_model)
        self.custom_groups.append(group_model)

    class Meta:
        managed = False

    def has_group(self, group):
        for g in self.custom_groups:
            if g.name == group:
                return True
        return False

    def has_permission(self, perm):
        for group in self.custom_groups:
            for permission in group.permissions:
                if permission.codename == perm:
                    return True
        for permission in self.custom_permissions:
            if permission.codename == perm:
                return True
        return False