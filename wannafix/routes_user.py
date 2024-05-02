from flask import Blueprint, render_template, abort, Response, request, redirect, url_for, flash, current_app
from flask_login import logout_user
from .models import User, Role
from .helper_role import Role, role_required
from flask_login import current_user
from wannafix import db_manager as db
import csv, io

# Blueprint
user_bp = Blueprint("user_bp", __name__)
@user_bp.route('/user')
@role_required(Role.admin, Role.moderator, Role.wanner)
def user_index():
    user = current_user
    return render_template('user/index.html', user=user)


@user_bp.route('/user/download/<int:user_id>')
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


@user_bp.route('/user/delete/<int:user_id>', methods=["GET", "POST"])
@role_required(Role.admin, Role.moderator, Role.wanner)
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    if request.method == "POST":
        confirmation_phrase = request.form.get("confirmation_phrase")
        if confirmation_phrase == current_app.config.get("FRASE_CONFIRMACION"):
            return render_template('user/delete_confirm.html', user=user)
        else:
            flash("La frase de confirmación es incorrecta", "error")

    return render_template('user/delete.html', user=user)


@user_bp.route('/user/delete_confirm/<int:user_id>', methods=["POST"])
@role_required(Role.admin, Role.moderator, Role.wanner)
def confirm_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    if request.method == "POST":
        user.delete()

        # Cerrar la sesión del usuario
        logout_user()

        flash("Tus datos han sido eliminados correctamente", "success")
        return redirect(url_for("index")) 

    return render_template('user/delete.html', user=user)