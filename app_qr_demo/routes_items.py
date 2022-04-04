from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Optional, List
#from starlette.responses import FileResponse
from fastapi.responses import FileResponse
import re
import qrcode
import qrcode.image.svg
import tempfile
import base64
from PIL import Image

from . import models_io

router = APIRouter()

IBAN = 'CZ4655000000006026919979'

def create_demo_qr(qr: models_io.QR_INPUT) -> str:
    return f"SPD*1.0*ACC:{IBAN}*AM:500.00*CC:CZK*X-VS:{qr.X_VS}*MSG:{qr.MSG}"

@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.post("/qr/")
async def get_qr(qr: models_io.QR_INPUT):
    return create_demo_qr(qr) 

@router.post("/qr_image/")
async def get_qr_image(qr: models_io.QR_INPUT):
    qr_text = create_demo_qr(qr)  
    # qr_text = 'SPD*1.0*ACC:CZ7801000000000000000123*AM:799.50*CC:CZK*DT:20170701*X-VS:9562231077'
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(qr_text)   
    # qr.make(fit=True)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    # img = img.resize((135, 135), Image.NEAREST)    

    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=True) as FOUT:
        img.save(FOUT, format='PNG')
        FOUT.seek(0)
        return FileResponse(FOUT.name, media_type="image/png")
        # When we need a base64 string from png image file
        # encoded_string = base64.b64encode(FOUT.read())
        # return encoded_string 


@router.post("/qr_image_png_as_base64/{img_res}")
async def get_qr_image_png_as_base64(img_res: int, qr: models_io.QR_INPUT):
    qr_text = create_demo_qr(qr)  
    # qr_text = 'SPD*1.0*ACC:CZ7801000000000000000123*AM:799.50*CC:CZK*DT:20170701*X-VS:9562231077'
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(qr_text)   
    # qr.make(fit=True)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((img_res, img_res), Image.NEAREST)    

    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=True) as FOUT:
        img.save(FOUT, format='PNG')
        FOUT.seek(0)
        encoded_string = base64.b64encode(FOUT.read())
        return encoded_string    




