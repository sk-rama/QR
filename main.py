import uvicorn
from functools import lru_cache
from fastapi import FastAPI, Request, Depends, Header, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

import forms


import app_qr_demo.routes_items

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(app_qr_demo.routes_items.router, prefix="/qr_demo")

def get_segment( request ): 
    try:
        segment = request.url.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment    
    except:
        return None  


@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    # Detect the current page
    segment = get_segment(request=request)
    return templates.TemplateResponse("dashboard.html", {"request": request, "segment":segment})

@app.get("/my-qr-demo-form.html", response_class=HTMLResponse)
async def get_qr_demo_form(request: Request):
#    try:
        form = await forms.BankTransfer.from_formdata(request)
        # Detect the current page
        segment = get_segment(request=request)
        return templates.TemplateResponse("my-qr-demo-form.html", {"request":request, "segment":segment, "form":form})
#    except:
#        return RedirectResponse(app.url_path_for('get_page_404'))

@app.post("/my-qr-demo-form")
async def post_qr_demo_form(request: Request):
#    try:
        form = await forms.BankTransfer.from_formdata(request)        
        # Detect the current page
        segment = get_segment(request=request)
        if await form.validate_on_submit():
            return PlainTextResponse('SUCCESS')
        return templates.TemplateResponse("my-qr-demo-form.html", {"request":request, "segment":segment, "form":form})
#    except:
        return RedirectResponse(app.url_path_for('get_page_404'))            

@app.get("/page-404/", response_class=HTMLResponse)
async def get_page_404(request: Request):
    # Detect the current page
    segment = get_segment(request=request)
    return templates.TemplateResponse("page-404.html", {"request": request, "segment":segment})    

@app.get("{file_path:path}", response_class=HTMLResponse)
async def get_ui_forms(file_path: str, request: Request):
    try:
        # Detect the current page
        segment = get_segment(request=request)
        return templates.TemplateResponse(file_path, {"request": request, "segment" :segment})
    except:
        return RedirectResponse(app.url_path_for('get_page_404'))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)