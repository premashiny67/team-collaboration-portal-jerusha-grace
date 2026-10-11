<<<<<<< HEAD
# Team Collaboration Portal — Jerusha Grace

A full-stack task collaboration application built with Python, Django, Django Templates, Bootstrap, and PostgreSQL support.

## Features

- Login and logout using Django's secure authentication system
- Admin and Member roles
- Admin dashboard with task statistics
- Admin can create, edit, assign, filter, and delete tasks
- Admin can create member accounts
- Members can view only their assigned tasks and update their task status
- Server-side role and ownership checks
- Search and status filtering
- Responsive interface
- PostgreSQL support in production; SQLite by default for local development
- Environment-based configuration for deployment

## Technology

- Python 3.12+
- Django 5.1/5.2
- Django ORM
- PostgreSQL (production) / SQLite (local)
- Bootstrap 5 via CDN
- Gunicorn and WhiteNoise
- Render deployment configuration included

## Run locally

1. Install Python 3.12 or newer.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows PowerShell
   .venv\\Scripts\\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and set a strong `SECRET_KEY`. Django reads environment variables from your shell; if you use a local `.env` file, export its values in your terminal or use your preferred environment-variable loader. The app works without `.env` for local development, using a development-only fallback secret.

5. Run migrations and create an admin account:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the app:

   ```bash
   python manage.py runserver
   ```

7. Open http://127.0.0.1:8000/ and log in with your superuser account. Django superusers are automatically treated as Admins.

## Create an Admin or Member

- Django superusers are Admins.
- In the portal, an Admin can use **Team Members → Add Member** to create a Member account.
- To create a non-superuser Admin, use Django Admin at `/django-admin/`, create a user, then set their profile role to `ADMIN`. The profile is created automatically for normal users; if needed, create the profile from the Django admin interface.

## PostgreSQL

Set `DATABASE_URL` to a PostgreSQL connection string, for example:

`postgresql://USER:PASSWORD@HOST:5432/DATABASE`

Do not commit production credentials to GitHub. Use your hosting provider's environment-variable settings.

## Deploy to Render

1. Push this repository to GitHub.
2. Create a PostgreSQL database with your chosen provider (for example, Neon or Render PostgreSQL).
3. In Render, create a new Web Service from the GitHub repository. You can use the included `render.yaml` blueprint or configure the service manually.
4. Set `DATABASE_URL` to your PostgreSQL connection string.
5. Set `SECRET_KEY` to a unique random secret, `DEBUG=False`, and `ALLOWED_HOSTS` to your deployed hostname (for example `your-service.onrender.com`).
6. Deploy. The build command installs dependencies, collects static files, and applies migrations.
7. Create the first superuser from the Render Shell:

   `python manage.py createsuperuser`

8. Open the deployed URL and log in.

**Note:** A deployed application is not live until you create the hosting service, configure its database/environment variables, run migrations, create an Admin account, and verify the deployment.

## Push to GitHub

Create an empty repository named `team-collaboration-portal-jerusha-grace` on GitHub, then run from this project directory:

```bash
git init
git add .
git commit -m "Initial Team Collaboration Portal"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/team-collaboration-portal-jerusha-grace.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with the account that will own the repository.

## Security notes

- Passwords are stored using Django's password hashers, not plaintext.
- Authorization is checked on the server for every task operation.
- Members can only update tasks assigned to them and cannot assign tasks or change other task fields.
- Use HTTPS and strong environment secrets in production.
- Before production use, configure email-based password reset, monitoring, backups, and a custom domain if required.
=======
# team-collaboration-portal-jerusha-grace
>>>>>>> 30ffcd6823215a428a8e2471528393431fda568d
