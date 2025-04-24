from flask import Blueprint, render_template, request, redirect, session, url_for
from admin.models.model_request import CustomerRequest,UpdateCustomerRequest
from admin.presentation.repository import CustomerRepository
from flask import Blueprint, render_template
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'customer')
customer_route = Blueprint('customer_route', __name__, template_folder=template_dir)
    
#---------------------------------------Get all customer-------------------------------# 
    
@customer_route.route("/customer")
# @admin_required
def customer_management():
    customers = CustomerRepository.get_customer()
    return render_template("customer_management.html" , customers = customers)

#---------------------------------------Render add customer----------------------------#

@customer_route.route("/add_customer")
def add_customer():
    return render_template("add_new_customer.html")
    
#---------------------------------------Add customer-----------------------------------#

@customer_route.route("/add_new_customer", methods=["GET","POST"])
# @admin_required
def add_new_customer():
    
    name = request.form.get("name")
    
    code = CustomerRequest(code = request.form.get("code"))
    name = CustomerRequest(name = request.form.get("name"))
   
    response = CustomerRepository.add_customer_action(code, name)
   
    if response.status_code == 200:
        return redirect(request.referrer or url_for("customer_route.customer_management"))
    else:
        return render_template("add_new_customer.html", error=f"Lỗi khi thêm khách hàng: {response.text}")
    
#---------------------------------------Detail customer -------------------------------#
    
@customer_route.route("/detail_customer/<code>")
def detail_customer(code):
    customer = CustomerRepository.get_customer_by_code(code)
    return render_template("detail_customer.html", customer=customer)

#---------------------------------------Update customer action--------------------------#

@customer_route.route("/update_info_customer/<code>", methods=["GET","POST"])
# @admin_required
def update_customer(code):
    code = request.form.get("code")
    name = UpdateCustomerRequest(name=request.form.get("name"))
    
    response = CustomerRepository.update_customer_action(code, name)
   
    if response.status_code == 200:
        return redirect(url_for("admin_route.customer_route.customer_management"))
    else:
        customer = CustomerRepository.get_customer_by_code(code)
        return render_template("detail_customer.html", customer = customer , error=f"Lỗi khi thêm khách hàng: {response.text}")