from flask import Blueprint, render_template, request, redirect, session, url_for
from admin.models.model_request import CustomerRequest,UpdateCustomerRequest
from apps.models.responses.user_model import UserModel
from core.request import RequestHandler  # Import RequestHandler
from src.admin.models.model_response import CustomerResponse # Import CustomerResponse
from flask import Blueprint, render_template
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'customer')

customer_route = Blueprint('customer_route', __name__, template_folder=template_dir)
    
def get_customer():
    response = RequestHandler.post("/customer/get-customer", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        customers = [CustomerResponse(**item) for item in response.json()]
        return customers
    return []

def get_customer_by_code(code):
    response = RequestHandler.get(f"/customer/show/{code}", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        customers = [CustomerResponse(**item) for item in response.json()]
        return customers
    return []

def add_customer_action(CustomerRequest : CustomerRequest):
    
    data = {
        "code": CustomerRequest.code,
        "name" : CustomerRequest.name,
    }
    response = RequestHandler.post(f"/customer/add" , data=data ,headers={"Content-Type": "application/json"})
    return response

def update_customer_action(code , UpdateCustomerRequest : UpdateCustomerRequest):
    data = {
        "name" : UpdateCustomerRequest.name,
    }
    response = RequestHandler.put(f"/customer/update/{code}" , data=data ,headers={"Content-Type": "application/json"})
    return response

def get_user_data():
    user_data = session.get('user')
    user = UserModel(**user_data)
    return user

@customer_route.route("/customer")
# @admin_required
def customer_management():
    customers = get_customer()
    return render_template("customer_management.html" , customers = customers , user = get_user_data())


# Route
@customer_route.route("/add_customer")
def add_customer():
    return render_template("add_new_customer.html" , user = get_user_data())

@customer_route.route("/add_new_customer", methods=["GET","POST"])
# @admin_required
def add_new_customer():
    
    name = request.form.get("name")
    
    code = CustomerRequest(code = request.form.get("code"))
    name = CustomerRequest(name = request.form.get("name"))
   
    response = add_customer_action(code, name)
   
    if response.status_code == 200:
        return redirect(request.referrer or url_for("customer_route.customer_management"))
    else:
        return render_template("add_new_customer.html", user=get_user_data(), error=f"Lỗi khi thêm khách hàng: {response.text}")
    
@customer_route.route("/detail_customer/<code>")
def detail_customer(code):
    customer = get_customer_by_code(code)
    return render_template("detail_customer.html", customer=customer, user=get_user_data())

@customer_route.route("/update_info_customer/<code>", methods=["GET","POST"])
# @admin_required
def update_customer(code):
    code = request.form.get("code")
    name = UpdateCustomerRequest(name=request.form.get("name"))
    
    response = update_customer_action(code, name)
   
    if response.status_code == 200:
        return redirect(url_for("admin_route.customer_route.customer_management"))
    else:
        customer = get_customer_by_code(code)
        return render_template("detail_customer.html", customer = customer , user=get_user_data(), error=f"Lỗi khi thêm khách hàng: {response.text}")