# Flask Auth0 App

This Flask web application exemplifies Auth0 access control and secure login/logout. Third-party authentication and protected routes are being implemented as part of a CST8919 lab experiment.

---

## 🎯 Objective

- Connect Auth0 to a web application built with Flask.
- Permit users to access protected content by logging in using Auth0.
- To guarantee that only authorised users can access them, protect particular routes.
- Show off your ability to handle sessions and log out.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mishravaibhav0032/flask-auth0-app.git
cd flask-auth0-app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Auth0

Create a file named `.env` in the project root and add the following:

```env
AUTH0_CLIENT_ID=your-client-id-here
AUTH0_CLIENT_SECRET=your-client-secret-here
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CALLBACK_URL=http://localhost:3000/callback

FLASK_APP=server.py
FLASK_ENV=development
APP_SECRET_KEY=your-random-secret-key
PORT=3000
```

> 🔐 Generate a secure `APP_SECRET_KEY` using:  
> `python -c "import secrets; print(secrets.token_hex(32))"`

### 5. Set Allowed URLs in Auth0

In your Auth0 dashboard, configure your Application Settings:

- **Allowed Callback URLs**: `http://localhost:3000/callback`
- **Allowed Logout URLs**: `http://localhost:3000`
- **Allowed Web Origins**: `http://localhost:3000`

---

## ▶️ Running the App

```bash
python server.py
```

Visit [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔐 Protected Routes

- `/protected` — Only accessible to logged-in users. Redirects to `/login` if not authenticated.
- `/dashboard` — Displays user profile info (name/email) after login.

Example of `/protected` logic in `server.py`:

```python
@app.route("/protected")
def protected():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("protected.html", user=session["user"])
```

---

## 📺 Demo Video

🎥 https://drive.google.com/file/d/1uId360Oik0VOs3X5SG2vjUFleHEqzMOx/view?usp=drive_link


---

## 📘 Learnings

- How to incorporate Flask's secure session and route protection logic with third-party authentication (Auth0)
- Utilising environment variables to manage secrets
- Flask routeing, templates, and OAuth2 principles
---

## 📁 Project Structure

```
flask-auth0-app/
├── templates/
│   ├── home.html
│   ├── dashboard.html
│   └── protected.html
├── app.py
├── server.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── venv/
```
 
