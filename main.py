from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.api import router
from fastapi.middleware.cors import CORSMiddleware

templates=Jinja2Templates(directory="templates")
app=FastAPI(title="backend for sim")
app.include_router(router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get('/',response_class=HTMLResponse)
def home(request: Request):
     return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome to FastAPI!"})





if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
