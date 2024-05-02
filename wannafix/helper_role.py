from flask import current_app
from flask_login import current_user
from flask_principal import identity_loaded, identity_changed, ActionNeed, RoleNeed, Permission, Identity, AnonymousIdentity
from enum import Enum

class Role(str, Enum):
    wanner    = "wanner"
    moderator = "moderator"
    admin     = "admin"

class Action(str, Enum):
    services_list     = "list services"
    services_create   = "create services"
    services_read     = "view services"
    services_update   = "edit services"
    services_delete   = "delete services"
    # services_moderate = "moderate services"
# Wanners poden visualitzar i crear productes
# Wanners poden editar i eliminar els seus productes
# Moderators poden visualitzar i moderar productes
# Admins poden fer de tot
_permissions = {
    Role.wanner: [
        Action.services_list,
        Action.services_create,
        Action.services_read,
        Action.services_update,
        Action.services_delete
    ],
    Role.moderator: [
        Action.services_list,
        Action.services_read,
        # Action.services_moderate
        Action.services_delete # si s'implementa la moderació es treu aquesta línia
    ],
    Role.admin: [
        Action.services_list,
        Action.services_read,
        Action.services_update,
        Action.services_delete,
        # Action.products_moderate,
    ],
}

def load_identity_permissions(identity):
    # Afegir rol
    role = identity.user.role
    identity.provides.add(RoleNeed(role))
    # Afegir permisos
    if (_permissions[role]):
        for action in _permissions[role]:
            identity.provides.add(ActionNeed(action))

###########################
# Mètodes Flask-Principal #
###########################

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    # current_user podria ser anonim!
    if hasattr(identity.user, 'role'):
        load_identity_permissions(identity)

def notify_identity_changed():
    # current_user podria ser anonim!
    if hasattr(current_user, 'email'):
        identity = Identity(current_user.email)
    else:
        identity = AnonymousIdentity()
        
    identity_changed.send(current_app._get_current_object(), identity = identity)

##################
# Routes helpers #
##################

# Usage example: 
# @role_required(Role.admin)
def role_required(*roles):
    needs = [RoleNeed(role) for role in roles]
    return Permission(*needs).require(http_exception=403)

# Usage example: 
# @perm_required(Action.products_create)
def perm_required(action):
    return Permission(ActionNeed(action)).require(http_exception=403)