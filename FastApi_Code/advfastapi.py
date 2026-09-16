from fastapi import FastAPI , Depends , Header , HTTPException , status 
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials , APIKeyHeader


app = FastAPI()

SECRET_KEY = "test123"

def verify_token(x_token: str = Header(...)):
    if x_token != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Token header",
        )
    return True


@app.get("/test")
def test(verify : bool = Depends(verify_token)):
    return {"message": "Token verified successfully"}



api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/test1")
def test1(api_key: str = Depends(api_key_header)):
    if api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return {"message": "API Key verified successfully"}



import time 
from  fastapi import Request

request_history  = {}


@app.get("/rate-limiting")
def rate_limiting(request: Request):
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in request_history:
        request_history[client_ip] = []
        
    request_history[client_ip] = [timestamp for timestamp in request_history[client_ip] if current_time - timestamp < 60]   
    
    
    if len(request_history[client_ip]) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.", 
        )
    request_history[client_ip].append(current_time)
    
    return {"message": "Request successful"}

from pydantic import BaseModel




class books(BaseModel):
    title: str
    author: str
    year: int

@app.post("/create_book")    
def create_book(book: books , x_Api_key: str = Depends(APIKeyHeader(name="X-API-Key"))):
    if x_Api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return {"message": "Book created successfully", "book": book.dict()}