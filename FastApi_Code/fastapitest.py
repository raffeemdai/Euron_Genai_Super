from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/sudh/kumar")
def test():
    print("this is my test fun")
    return {
        "message" : "this is my first api program"
    }
    


@app.get("/add")    
def add(a,b):
    
    return {
        "a" : a,
        "b" : b ,
        "result" : a+b
    }


@app.get("/claculator")
def calculator(a:float , b :float , operation:str):
    if operation=="add":
        result = a+ b
    elif operation == "sub":
        result = a-b
        
    elif operation == "mul":
        result = a*b
        
    elif operation == "div":
        result=  a/b
    else :
        return {"message " : "you have to pass the valid input"}
    return {"result":result}


@app.get("/time")
def curent_time():
    return {
        "server_time" : datetime.now()
    }
    
import socket
import platform
import os


@app.get("/sudh_server")
def sudh_server_details():
    return {
        "hostname" : socket.gethostname(),
        "local_ip" : socket.gethostbyname(socket.gethostname()),
        "os" : platform.system(),
        "os_version" : platform.version(),
        "machine" : platform.machine(),
        "processor" : platform.processor(),
        "python_version" : platform.python_version(),
        "current_direcotyr" : os.getcwd()
    }
    


from fastapi import Request


@app.get("/visitor")
def visitor(request : Request):
    return {
        "ip" : request.client.host,
        "port" : request.client.port
    }
    


@app.get("/who-is-hitting-me")
def who_is_hitting_me(request: Request):

    # Get IP from proxy/ngrok header
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        visitor_ip = forwarded_for.split(",")[0].strip()
    else:
        visitor_ip = request.client.host

    visitor_data = {
        "public_ip": visitor_ip,
        "source_port": request.client.port,
        "user_agent": request.headers.get("user-agent"),
        "language": request.headers.get("accept-language"),
        "referer": request.headers.get("referer"),
        "method": request.method,
        "url": str(request.url),
        "timestamp": datetime.now().isoformat()
    }

    # PRINT IN YOUR FASTAPI CONSOLE
    print("\n")
    print("=" * 60)
    print("NEW VISITOR HIT MY API")
    print("=" * 60)

    print("IP Address     :", visitor_data["public_ip"])
    print("Source Port    :", visitor_data["source_port"])
    print("User Agent     :", visitor_data["user_agent"])
    print("Language       :", visitor_data["language"])
    print("Referer        :", visitor_data["referer"])
    print("Method         :", visitor_data["method"])
    print("URL            :", visitor_data["url"])
    print("Timestamp      :", visitor_data["timestamp"])

    print("=" * 60)
    print("\n")

    return {
        "message": "Request received successfully"
    }
    
