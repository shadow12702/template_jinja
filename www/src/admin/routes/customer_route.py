# admin/routes/customer_route.py

from flask import Blueprint, render_template, request, redirect, url_for
from admin.model.request.customer_request import CustomerRequest
from admin.service import customer_service

from pathlib import Path
template_path = Path(__file__).resolve().parents[1] / 'templates/customer'

customer_route = Blueprint('customer', __name__, template_folder=template_path)

@customer_route.route('/list')
def list_customers():
    '''Get all customers.'''
    _list = customer_service.get_customer()
    return render_template('customer.html', customers=_list)

@customer_route.route('/add')
def add():
    '''Prompt to add a new customer.'''
    return render_template('add_customer.html')

@customer_route.route('/add_customer', methods=['POST'])
def add_customer():
    '''Add a new customer.'''
    if request.method == 'POST':

        _new_customer = CustomerRequest(**request.form)
        response = customer_service.add_customer(_new_customer)
        if response.status_code == 200:
            return redirect(url_for('customer.list_customers'))
        else:
            error_message = response.json().get('message', 'Failed to add customer')
            return render_template('add_customer.html', error=error_message)
    return render_template('add_customer.html')

@customer_route.route('/update/<code>')
def update(code):
    '''Prompt to update customer information.'''
    customer = customer_service.get_customer_by_code(code)
    if customer:
        return render_template('update_customer.html', customer=customer)
    else:
        return redirect(url_for('customer.list_customers'))

@customer_route.route('/update_customer', methods=['POST'])
def update_customer():
    '''Update customer information.'''
    if request.method == 'POST':
        _update_customer = CustomerRequest(**request.form)
        response = customer_service.update_customer(_update_customer)
        if response.status_code == 200:
            return redirect(url_for('customer.list_customers'))
        else:
            error_message = response.json().get('message', 'Failed to update customer')
            return render_template('update_customer.html', error=error_message)
    return redirect(url_for('customer.list_customers'))

@customer_route.route('/detail/<code>')
def detail(code):
    '''Get customer details.'''
    customer = customer_service.get_customer_by_code(code)
    if customer:
        return render_template('detail.html', customer=customer)
    else:
        return redirect(url_for('customer.list_customers'))