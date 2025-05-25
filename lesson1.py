from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import date
 
app = FastAPI()
 
#Enum for leave types
class LeaveType(str, Enum):
    sick = "Sick"
    casual = "Casual"
    earned = "Earned"
 
#Enum for status
class LeaveStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
 
#pydantic model for leave request input
class LeaveRequest(BaseModel):
    employee_name: str = Field(..., example= "John Doe")
    leave_type: LeaveType = Field(..., example = "Sick")
    start_date: date = Field(..., example="2025-06-01")
    end_date: date = Field(..., example="2025-06-05")
    reason: Optional[str] = Field(None, example= "Fever and rest")
 
#pydantic model for leave request stored (with ID and status)
class LeaveRequestInDB(LeaveRequest):
    id: int
    status: LeaveStatus
 
#Fake database
leave_db: List[LeaveRequestInDB] = []
current_id = 1
 
@app.post("/leave", response_model = LeaveRequestInDB)
def submit_leave_request(leave_request: LeaveRequest):
    global current_id
    leave = LeaveRequestInDB(
        id=current_id,
        status = LeaveStatus.pending,
        **leave_request.dict()
    )
    leave_db.append(leave)
    current_id +=1
    return leave
 
@app.get("/leave", response_model=List[LeaveRequestInDB])
def get_all_leave_request():
    return leave_db
 
@app.put("/leave/{leave_id}/approve", response_model=LeaveRequestInDB)
def approve_leave_request(leave_id: int):
    for leave in leave_db:
        if leave.id == leave_id:
            if leave.status != LeaveStatus.pending:
                raise HTTPException(status_code = 400, detail="Leave request already processed.")
            leave.status = LeaveStatus.approved
            return leave
        raise HTTPException(status_code=404, detail="Leave request not found.")
 
@app.put("/leave/{leave_id}/reject", response_model=LeaveRequestInDB)
def reject_leave_request(leave_id: int):
    for leave in leave_id:
        if leave.id == leave_id:
            if leave.status != LeaveStatus.pending:
                raise HTTPException(status_code=400, detail="Leave request already processed.")
            leave.status = LeaveStatus.rejected
            return leave
        raise HTTPException(status_code=404, detail="Leave request not found.")