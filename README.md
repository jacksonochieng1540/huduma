# 🏢 Huduma Center Ticketing System

A modern, full-featured Django-based service request and queue management system for Huduma Centers in Kenya. Staff can manage citizen service requests, monitor queues, and process tickets in real-time, while citizens can submit requests, track their status, and upload required documents.

---

## 🚀 Features

### 👥 User Roles
- **Citizens**: Submit service requests, upload documents, and track ticket progress.
- **Staff**: View and manage tickets, mark tickets as processing/completed, view analytics.
- **Admin**: Full control over the system.

### 🎫 Ticket Management
- Create tickets based on service.
- Auto-generated unique ticket numbers (e.g. `T00001`).
- Track statuses: `Pending`, `Processing`, `Completed`.
- Progress bar and timestamps (created, processing start, completion).

### 📊 Staff Dashboard
- View all pending and processing tickets.
- Filter by priority (`High`, `Normal`).
- Start and complete tickets.
- View real-time clock.

### 📁 Document Upload
- Citizens or staff can upload service-specific documents.
- List uploaded files with status badges (`Uploaded`, `Pending`, `Missing`).
- Auto-display file names.

### 📄 Ticket Detail View
- View service description, customer details, ticket status.
- Auto-refresh for real-time updates.
- Print-friendly layout and PDF generation.

### 📈 Analytics 
- Ticket volume by status
- Service usage breakdown
- Staff performance metrics

  
###📸 Screenshots

🧾 Ticket Detail View
<img width="1281" height="681" alt="image" src="https://github.com/user-attachments/assets/e88a9b9e-59dc-40a7-ae86-4d33423465fd" />


🧑‍💼 Staff Dashboard
<img width="1275" height="677" alt="image" src="https://github.com/user-attachments/assets/da159d6b-1633-464c-829b-1a812fdf5923" />

<img width="1271" height="616" alt="image" src="https://github.com/user-attachments/assets/df3482e4-01ee-474d-91d3-8cc6b8e510e9" />
---

## 🧱 Tech Stack

| Layer        | Technology               |
|--------------|--------------------------|
| Backend      | Django 5.x + SQLite/PostgreSQL |
| Frontend     | Django Templates + Bootstrap 5 |
| Styling      | CSS3, FontAwesome Icons  |
| Auth         | Django auth (custom user model) |
| File Uploads | Django Media Storage     |
| CI/CD        | GitHub Actions           |
| Deployment   | Docker + Nginx + Gunicorn |
| Containerization | Docker Compose       |

---

## 📂 Project Structure

```bash
huduma/
├── core/           # User management (Citizen, Staff, Admin)
├── services/       # Services offered by Huduma
├── queue1/         # Ticket management & dashboards
├── analytics/      # Admin insights & metrics
├── templates/      # HTML templates (bootstrap themed)
├── static/         # CSS, JS, Images
├── media/          # Uploaded documents
├── manage.py
└── Dockerfile, docker-compose.yml

⚙️ Installation
##1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/huduma-center.git
cd huduma-center
##2. Create Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
##3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
##4. Apply Migrations
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
##5. Run the Development Server
bash
Copy
Edit
python manage.py runserver

🤝 Contribution
Want to contribute? Great!

1.Fork the project

2.Create your feature branch: git checkout -b feature/awesome-feature

3.Commit changes: git commit -m 'Add awesome feature'

4.Push to branch: git push origin feature/awesome-feature

5.Open a Pull Request

🙌 Acknowledgements
1.Kenya eCitizen for Huduma Center inspiration

2.Django Project Community

3.FontAwesome & Bootstrap Teams

🔐 User Roles Setup
Use Django admin or fixtures to create:

Citizens (role='C')

Staff members (role='S')

Superusers/Admins
