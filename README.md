# Django Modular App

A Django-based modular app engine that enables dynamic installation, upgrading, and uninstallation of modules. Each module has a landing page and role-based access rights.(`manager`, `user`, `public`).

---

## Fitur Utama

- **Modular Engine** (core) (Superuser only: admin):

  - List all modules `/module/`.
  - Install / Upgrade / Uninstall button per module.
  - Auto register module when first run if not yet registered.

- **Product Module** (product_module):
  - Providing a landing page `/products/`.
  - Model `Product`: name, barcode, price, stock.
  - Role:
    - `manager`: CRUD.
    - `user`: CRU.
    - `public`: R (read only).
  - Popup validation when deleting data.
  - Uninstall module = landing page disabled.
  - Validation module access with middleware.

## Instalation & Setup

### 1. Clone Project

```bash
git clone <repo_url>
cd modular_app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

### 4. Migrate DB

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Groups, Permissions, Modules, Users and Superuser using Django Command

```bash
python manage.py init_groups        # Create grup: manager, user, public
python manage.py init_permissions   # Create grup permissions for product module
python manage.py init_modules       # Add default product_module to ModuleRegistry
python manage.py init_users         # Create superuser, manager, and user default.

or
python manage.py setup_project    # with 1 function command to setup all initial data + migrate DB
```

### 6. Run Server

```bash
python manage.py runserver
```

## Pages

- Admin Panel: http://127.0.0.1:8000/admin/

- Module Dashboard: http://127.0.0.1:8000/module/

- Product Landing Page (active when the module is installed): http://127.0.0.1:8000/products/

## Users

1. Admin

```bash
username: admin
password: admin123
```

2. Manager

```bash
username: manager
password: manager123
```

3. User

```bash
username: user
password: user123
```
