from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
import re

from schwifty import IBAN


class Iban(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        return IBAN(v)
        

class QR_INPUT(BaseModel):
    SPD: Optional[str] = '2.0'
    ACC: Iban = 'CZ4655000000006026919979' 
    AM: Optional[float] = 100.00
    CC: Optional[str] = 'EUR'
    X_VS: Optional[str] = '0000045'
    MSG: Optional[str] = 'platba QR kodem'

    @validator('X_VS', pre=True, always=True)
    def is_variable_symbol(cls, v):
        if len(v) != len(re.match('[0-9]*', v).group(0)):
            raise ValueError('Tel. Number must contain only numbers')
        if len(v) > 11:
            raise ValueError('must contain max 10 numbers')
        return v



class QR_OUTPUT(BaseModel):
    SPD: str = '4.0'
    ACC: Optional[str] = None 
    AM: Optional[float] = None
    X_VS: Optional[str] = '000001'
    MSG: Optional[str] = 'platba QR kodem'


class IMG_RES(BaseModel):
    img_res: int = 125 

    @validator('img_res', pre=True, always=True)
    def is_img_resolution(cls, v):
        if len(v) != len(re.match('[0-9]*', v).group(0)):
            raise ValueError('image resolution must contain only numbers')
        if v > 512:
            raise ValueError('max supported image resolution is 512 pixels')
        if v < 85:
            raise ValueError('min supported image resolution is 85 pixels')
        return v   

    
