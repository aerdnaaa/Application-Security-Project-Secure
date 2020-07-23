from flask import Blueprint, render_template
import sqlite3, os, requests
from flaskr import file_directory

admin_blueprint = Blueprint('admin', __name__)


# ============================================= Admin Dashboard =============================================#
@admin_blueprint.route("/Admin")
def admin():
    return render_template("admin/Admin.html", title="Dashboard")


@admin_blueprint.route("/Admin/add_product")
def add_product():
    category_list = ['barbell', 'bench', 'racks', 'plates']
    return render_template("admin/Products/Add_Product.html", title="Add Product", category_list=category_list)


@admin_blueprint.route("/Admin/show_product")
def show_product():
    return render_template("admin/Products/Show_Product.html", title="Products")


@admin_blueprint.route("/Admin/show_voucher")
def show_voucher():
    return render_template("admin/Vouchers/Show_Voucher.html", title="Vouchers")


@admin_blueprint.route("/Admin/add_voucher")
def add_voucher():
    return render_template("admin/Vouchers/Add_Voucher.html", title="Add Voucher")


@admin_blueprint.route("/Admin/add_user_voucher")
def add_user_voucher():
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()

    c.execute("SELECT username FROM users WHERE admin <> 'y'")
    users = c.fetchall()
    return render_template("admin/Vouchers/Add_User_Voucher.html", title="Add User Voucher", users=users)


@admin_blueprint.route("/manage_user")
def manage_user():
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template("admin/Manage_Users/manage_user.html", title="users", users=users)


@admin_blueprint.route("/Queries")
def Queries():
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM query")
    query = c.fetchall()
    conn.close()
    return render_template("admin/Query/Queries.html", title="query", query=query)


@admin_blueprint.route("/logs")
def logs():
    token = "e96e83862dab40a0ad31c8c9caa963b8741acd8ee1304f1b9d2e37776d78c27f"
    url = "https://sentry.io/api/0/projects/indirect-bi/indirect-bi/issues/"
    header = {"Authorization": f"Bearer {token}"}
    my_response = requests.get(url, headers=header)
    data = my_response.json()
    return render_template("admin/Logging/log.html", title="Logs", data=data)
