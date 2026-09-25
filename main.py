from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone


app = FastAPI(
    title="HR Employee Service Portal",
    description="API for managing employee HR service requests",
    version="1.0.0"
)


# MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["hr_employee_service_db"]

request_collection = db["requests"]
user_collection = db["users"]


# Security
password_hash = PasswordHash.recommended()
SECRET_KEY = "HRServicePortalSecurityKey"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# ---------------- MODELS ----------------

class ServiceRequestCreate(BaseModel):
    employee_id: str
    category: str
    description: str


class ServiceRequestUpdate(BaseModel):
    status: str
    description: str


class ServiceRequestResponse(ServiceRequestCreate):
    request_id: str
    status: str


class UserCreate(BaseModel):
    username: str
    password: str
    role: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# ---------------- HELPERS ----------------

def request_helper(request):
    return {
        "request_id": str(request["_id"]),
        "employee_id": request["employee_id"],
        "category": request["category"],
        "description": request["description"],
        "status": request["status"]
    }


def user_helper(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }


# ---------------- JWT ----------------

def create_token(username, role):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINS
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(token=Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise HTTPException(401, "Invalid token")

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    user = user_collection.find_one(
        {"username": username}
    )

    if user is None:
        raise HTTPException(404, "User not found")

    return user


def require_roles(*roles):

    def check_role(user=Depends(get_current_user)):

        if user["role"] not in roles:
            raise HTTPException(
                403,
                "Permission denied"
            )

        return user

    return check_role


# ---------------- USERS ----------------

@app.post("/users", status_code=201)
def create_user(user: UserCreate):

    if user_collection.find_one(
        {"username": user.username}
    ):
        raise HTTPException(
            409,
            "Username already exists"
        )

    data = {
        "username": user.username,
        "password": password_hash.hash(user.password),
        "role": user.role
    }

    result = user_collection.insert_one(data)

    return user_helper(
        user_collection.find_one(
            {"_id": result.inserted_id}
        )
    )


# ---------------- LOGIN ----------------

@app.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = user_collection.find_one(
        {"username": form_data.username}
    )

    if not user or not password_hash.verify(
        form_data.password,
        user["password"]
    ):
        raise HTTPException(
            401,
            "Invalid username or password"
        )

    token = create_token(
        user["username"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ---------------- REQUESTS ----------------

# Create
@app.post(
    "/requests",
    status_code=201,
    response_model=ServiceRequestResponse
)
def create_request(
    request: ServiceRequestCreate,
    user=Depends(require_roles(1, 2, 3, 4))
):

    data = request.model_dump()
    data["status"] = "NEW"

    result = request_collection.insert_one(data)

    return request_helper(
        request_collection.find_one(
            {"_id": result.inserted_id}
        )
    )


# Get all
@app.get(
    "/requests",
    response_model=list[ServiceRequestResponse]
)
def get_requests(
    user=Depends(require_roles(1, 2, 3, 4))
):

    return [
        request_helper(r)
        for r in request_collection.find()
    ]


# Get by ID
@app.get(
    "/requests/{request_id}",
    response_model=ServiceRequestResponse
)
def get_request(
    request_id: str,
    user=Depends(require_roles(1, 2, 3, 4))
):

    if not ObjectId.is_valid(request_id):
        raise HTTPException(
            400,
            "Invalid request ID"
        )

    request = request_collection.find_one(
        {"_id": ObjectId(request_id)}
    )

    if not request:
        raise HTTPException(
            404,
            "Request not found"
        )

    return request_helper(request)


# Update
@app.put(
    "/requests/{request_id}",
    response_model=ServiceRequestResponse
)
def update_request(
    request_id: str,
    request: ServiceRequestUpdate,
    user=Depends(require_roles(1, 2, 3, 4))
):

    if not ObjectId.is_valid(request_id):
        raise HTTPException(
            400,
            "Invalid request ID"
        )

    result = request_collection.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": request.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            404,
            "Request not found"
        )

    return request_helper(
        request_collection.find_one(
            {"_id": ObjectId(request_id)}
        )
    )


# Delete
@app.delete("/requests/{request_id}")
def delete_request(
    request_id: str,
    user=Depends(require_roles(4))
):

    if not ObjectId.is_valid(request_id):
        raise HTTPException(
            400,
            "Invalid request ID"
        )

    result = request_collection.delete_one(
        {"_id": ObjectId(request_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            404,
            "Request not found"
        )

    return {
        "message": "Request deleted successfully"
    }