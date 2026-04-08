from pydantic import BaseModel, Field
from typing import List, Literal


class Observation(BaseModel):
    patient_message: str = Field(..., description="Initial patient complaint")
    patient_reply: str = Field(..., description="Reply from patient after agent action")
    asked: List[str] = Field(default_factory=list, description="Symptoms already checked")


class Action(BaseModel):
    action_type: Literal["check_symptom", "final"] = Field(
        ..., description="Type of action"
    )
    content: str = Field(
        ..., description="Symptom name or final decision"
    )

    # 👇 ADD IT HERE (inside class, same indentation level)
    def __str__(self):
        return f"{self.action_type}: {self.content}"