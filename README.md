DOKUMENTASI Project Pangrango 3 Front Office

---

# 1. Database Setup

Bikin database di MariaDB:

```sql
CREATE DATABASE gp3_faculty_office;
```

# 2. Konfig Database

Edit `faculty_office/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gp3_faculty_office',
        'USER': 'root',              # sesuain
        'PASSWORD': '',              # sesuain
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 3. App yang udah ada

**staff/** - authentication

- `UserModel` - sistem login (username, nama, role: ADMIN/STAFF)

**hotel/** - models

- `Room` - kamar (room_number, status, price)
- `Guest` - tamu dan transaksi (nama, phone, room, check_in, check_out, total_price)
- `Report` - report (total_revenue, total_guests, date_from, date_to)

---

## cara jalanin:

```bash
# 1. Clone repo
git clone https://github.com/Dhannandist/GP3_faculty_office/

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

---

# STRUKTUR

```
faculty_office/  #  Root
 app/            #  core/base templates (On Progress)
 staff/          #  Authentication
 hotel/          #  Data models
 dashboard/      #  UI
 hardware/       #  IoT untuk tapping kartu di fo (Not Started)
 templates/      #  Html templates
```
