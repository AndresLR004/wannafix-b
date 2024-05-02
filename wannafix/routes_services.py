from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from .models import Service, Category, Status
from . import db_manager as db
from .forms import ServiceForm, ConfirmForm
from .helper_role import Action, perm_required
import uuid
import os

# Blueprint
services_bp = Blueprint("services_bp", __name__)

# https://code.tutsplus.com/templating-with-jinja2-in-flask-advanced--cms-25794t
@services_bp.context_processor
def templates_processor():
    return {
        'Action': Action
    }

@services_bp.route('/services/list')
@perm_required(Action.services_list)
def services_list():
    # select amb join que retorna una llista de resultats
    services = Service.get_all()

    return render_template('services/list.html', services = services)

@services_bp.route('/services/read/<int:services_id>')
@perm_required(Action.services_read)
def services_read(services_id):
    result = (
        db.session.query(Service)
        .join(Category) 
        .join(Status)   
        .filter(Service.id == services_id)
        .options(joinedload(Service.category), joinedload(Service.status))
        .first()
    )
    
    if not result:
        abort(404)

    service = result
    
    if not current_user.is_action_allowed_to_service(Action.services_read, service):
        abort(403)
    
    return render_template('services/read.html', service=service)


@services_bp.route('/services/create', methods = ['POST', 'GET'])
@perm_required(Action.services_create)
def service_create(): 
    # selects que retornen una llista de resultats
    categories = Category.get_all()
    statuses = Status.get_all()
    # carrego el formulari amb l'objecte services
    form = ServiceForm()
    form.category_id.choices = [(category.id, category.name) for category in categories]
    form.status_id.choices = [(status.id, status.name) for status in statuses]

    if form.validate_on_submit(): # si s'ha fet submit al formulari
        new_service = Service()
        new_service.seller_id = current_user.id

        # dades del formulari a l'objecte product
        print("Datos del formulario antes de populate_obj:", form.data)
        form.populate_obj(new_service)
        print("Datos del objeto después de populate_obj:", new_service.__dict__)

        # si hi ha foto
        filename = __manage_photo_file(form.photo_file)
        if filename:
            new_service.photo = filename
        else:
            new_service.photo = "no_image.png"
            
        print(form.data)

        # insert!
        new_service.save()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        flash("Nou servei creat", "success")
        return redirect(url_for('services_bp.services_list'))
    else: # GET
        return render_template('services/create.html', form = form)


# @services_bp.route('/services/update/<int:product_id>',methods = ['POST', 'GET'])
# @perm_required(Action.services_update)
# def product_update(product_id):
#     # select amb 1 resultat
#     product = Product.get(product_id)
    
#     if not product:
#         abort(404)

#     if not current_user.is_action_allowed_to_product(Action.services_update, product):
#         abort(403)

#     # selects que retornen una llista de resultats
#     categories = Category.get_all()
#     statuses = Status.get_all()

#     # carrego el formulari amb l'objecte services
#     form = ProductForm(obj = product)
#     form.category_id.choices = [(category.id, category.name) for category in categories]
#     form.status_id.choices = [(status.id, status.name) for status in statuses]

#     if form.validate_on_submit(): # si s'ha fet submit al formulari
#         # dades del formulari a l'objecte product
#         form.populate_obj(product)

#         # si hi ha foto
#         filename = __manage_photo_file(form.photo_file)
#         if filename:
#             product.photo = filename

#         # update!
#         product.update()

#         # https://en.wikipedia.org/wiki/Post/Redirect/Get
#         flash("Producte actualitzat", "success")
#         return redirect(url_for('services_bp.product_read', product_id = product_id))
#     else: # GET
#         return render_template('services/update.html', product_id = product_id, form = form)

@services_bp.route('/services/delete/<int:service_id>',methods = ['GET', 'POST'])
@perm_required(Action.services_delete)
def service_delete(service_id):
    # select amb 1 resultat
    service = Service.get(service_id)

    if not service:
        abort(404)

    if not current_user.is_action_allowed_to_service(Action.services_delete, service):
        abort(403)

    form = ConfirmForm()
    if form.validate_on_submit(): # si s'ha fet submit al formulari
        # delete!
        service.delete()

        flash("Servei esborrat", "success")
        return redirect(url_for('services_bp.service_list'))
    else: # GET
        return render_template('services/delete.html', form = form, service = service)

__uploads_folder = os.path.abspath(os.path.dirname(__file__)) + "/static/services/"

def __manage_photo_file(photo_file):
    # si hi ha fitxer
    if photo_file.data:
        filename = photo_file.data.filename.lower()

        # és una foto
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # M'asseguro que el nom del fitxer és únic per evitar col·lissions
            unique_filename = str(uuid.uuid4())+ "-" + secure_filename(filename)
            photo_file.data.save(__uploads_folder + unique_filename)
            return unique_filename

    return None