# HR Service Request Portal

A full-stack app modeled on the `tickets_app` sample (React + Vite frontend,
FastAPI + MongoDB backend), adapted for HR service requests instead of IT
tickets.

## Structure

```
hr_service_request_portal/
├── client/     # React (Vite) frontend
│   └── src/
│       ├── App.jsx          # routes + nav
│       ├── Login.jsx        # login form
│       ├── Register.jsx     # create user (role: Employee/HR Exec/HR Manager/Admin)
│       ├── RequestList.jsx  # list + delete service requests
│       ├── RequestForm.jsx  # create/edit a service request
│       └── api.js           # axios instance (baseURL: http://localhost:8000)
└── server/     # FastAPI backend
    └── main.py               # auth (JWT) + CRUD for /requests, /users, /login
```

## Roles

1 = Employee, 2 = HR Executive, 3 = HR Manager, 4 = Admin
(update/delete permissions on requests follow this same tiering as the
original ticket app: create = any logged-in user, update = role 2+, delete = role 4 only)

## Categories

Payroll, Leave, Onboarding, IT Access, Benefits, Grievance
(edit the `<option>` list in `RequestForm.jsx` to match your project's actual categories)

## Run it

### Server
```
cd server
pip install -r requirements.txt
# make sure MongoDB is running locally on mongodb://127.0.0.1:27017
uvicorn main:app --reload
```

### Client
```
cd client
npm install
npm run dev
```

Then open the Vite dev URL (usually http://localhost:5173), register a user,
log in, and start creating requests.

## Notes / things to change for your project

- `SECRET_KEY` in `server/main.py` is a placeholder — change it before any real use.
- Database name is `hr_service_request_db`, collections are `requests` and `users`.
- Add more fields to a request (e.g. `assigned_to`, `priority`, `due_date`) by
  extending `RequestCreate`/`RequestResponse` in `main.py` and the form in
  `RequestForm.jsx`.
