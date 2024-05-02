from flask import Blueprint, render_template, abort, Response
from flask_principal import RoleNeed
from .models import User, DownloadInfo, Role
from .helper_role import Role, role_required
from flask_login import current_user
from wannafix import db_manager as db
import csv, io


# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = User.get_all() 
    return render_template('admin/users/list.html', users=users)


# # Admin para descargar datos del usuario
@admin_bp.route('/admin/users/<int:user_id>/download', methods=["GET"])
def download_info_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'verified': user.verified,
        'category_id': user.category_id,
    }
    
    # Obtener los IDs de los servicios asociados al usuario
    service_ids = [service.id for service in user.services]

    # Agregar los IDs de los servicios al diccionario de datos del usuario
    user_data['service_ids'] = service_ids

    service_data = []
    # Obtener la información de cada servicio asociado al usuario
    for service in user.services:
        service_info = {
            'service_id': service.id,
            'description': service.description,
            'price': service.price
            # Agregar más campos según sea necesario
        }
        service_data.append(service_info)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=user_data.keys())
    writer.writeheader()
    writer.writerow(user_data)
    for service_info in service_data:
        writer.writerow(service_info)

    csv_data = output.getvalue()

    response = Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=user_info.csv"}
    )

    return response