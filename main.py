from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="HR Employee Service Portal",
    description="API for managing employee HR service requests",
    version="1.0.0"
)


# -------------------------
# Pydantic Models
# -------------------------

class ServiceRequestCreate(BaseModel):
    employee_id: str
    category: str
    description: str


class ServiceRequestUpdate(BaseModel):
    status: str
    description: str


class ServiceRequestResponse(ServiceRequestCreate):
    request_id: int
    status: str


# -------------------------
# Routes
# -------------------------

@app.get("/")
def home():
    return {
        "message": "HR Employee Service Portal API"
    }


# Get all requests
@app.get("/requests")
def get_requests():
    return {
        "message": "List of HR service requests"
    }


# Create a request
@app.post(
    "/requests",
    response_model=ServiceRequestResponse
)
def create_request(request: ServiceRequestCreate):

    new_request = ServiceRequestResponse(
        request_id=1,
        employee_id=request.employee_id,
        category=request.category,
        description=request.description,
        status="NEW"
    )

    return new_request


# Update a request
@app.put(
    "/requests/{request_id}",
    response_model=ServiceRequestResponse
)
def update_request(
    request_id: int,
    request: ServiceRequestUpdate
):

    updated_request = ServiceRequestResponse(
        request_id=request_id,
        employee_id="EMP101",
        category="PAYROLL_QUERY",
        description=request.description,
        status=request.status
    )

    return updated_request


@app.delete("/requests/{request_id}")
def delete_request(request_id: int):

    if request_id != 1:
        raise HTTPException(
            status_code=404,
            detail="HR service request not found"
        )

    return {
        "message": "HR service request deleted successfully",
        "request_id": request_id
    }