from pydantic import BaseModel
from typing import Optional
from datetime import date

class PaymentMethodBase(BaseModel):
    mode_name: str
    pay_date: Optional[date] = None

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    mode_name: Optional[str] = None
    pay_date: Optional[date] = None

class PaymentMethodResponse(PaymentMethodBase):
    payment_method_id: int

    model_config = {
        "from_attributes": True
    }