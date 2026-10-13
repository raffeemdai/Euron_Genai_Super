# FastAPI Authentication Using JWT — Simple Explanation

This note is based on the provided `login.py` script and the class transcript.

---

## 1. What are Authentication and Authorization?

### Authentication
Authentication means:

> **Who are you?**

The user provides:

- Username
- Password

The application checks whether those credentials are valid.

Example:

```text
Username: sudh
Password: sudh123
```

If the credentials are correct, the user is authenticated.

### Authorization
Authorization means:

> **What are you allowed to access after login?**

After successful login, the application generates an **access token**.

That token is then used to access protected APIs such as:

```text
/access_profile
/access_course
```

The transcript explains this using an office ID-card example:

```text
Login once
    ↓
Receive an access token
    ↓
Use that token like an office ID card
    ↓
Access allowed resources without entering password again
```

---

# 2. Overall JWT Authentication Flow

The complete flow in the script is:

```text
User Registration
      ↓
Hash Password
      ↓
Store Username + Hashed Password in Supabase
      ↓
User Login
      ↓
Read User from Database
      ↓
Verify Entered Password Against Stored Hash
      ↓
Generate JWT Access Token
      ↓
Return Token to User
      ↓
User Sends Bearer Token to Protected Endpoint
      ↓
FastAPI Reads Token using HTTPBearer
      ↓
JWT is Decoded and Validated
      ↓
User Gets Access
```

The class transcript describes the same sequence:

```text
1. Register
2. Login
3. Generate access token
4. Send token with protected requests
5. Validate token
6. Allow access
```

---

# 3. Required Imports

The final JWT-based section of the script uses:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from supabase import create_client
from pwdlib import PasswordHash
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import jwt
import os
```

### What each import is used for

| Import | Purpose |
|---|---|
| `FastAPI` | Creates the API application |
| `Depends` | Injects security dependencies into protected endpoints |
| `HTTPBearer` | Reads Bearer tokens from HTTP requests |
| `BaseModel` | Validates request JSON |
| `create_client` | Connects to Supabase |
| `PasswordHash` | Hashes and verifies passwords |
| `load_dotenv` | Loads values from `.env` |
| `datetime`, `timedelta`, `timezone` | Creates JWT expiration time |
| `jwt` | Creates and validates JWT tokens |
| `os` | Reads environment variables |

---

# 4. Loading Environment Variables

The script loads values such as the Supabase URL, Supabase key, and JWT secret from environment variables.

```python
load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

client = create_client(SUPABASE_URL, SUPABASE_KEY)
```

Later the JWT secret is also read from the environment:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

A sample `.env` file could look like:

```text
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key
```

The transcript first demonstrates a hardcoded secret for learning and then moves the secret into `.env`.

---

# 5. User Request Model

The script defines:

```python
class User(BaseModel):
    username: str
    password: str
```

This tells FastAPI that the request body should contain:

```json
{
  "username": "sudh",
  "password": "sudh123"
}
```

FastAPI automatically converts the JSON request into a `User` object.

Then you can use:

```python
user.username
user.password
```

---

# 6. First Version — Plain Password Registration

The script first demonstrates an insecure version:

```python
@app.post("/register")
def register_user(user: User):
    response = client.table("users").insert({
        "username": user.username,
        "password": user.password
    }).execute()

    return response
```

This stores the password directly.

Example:

```text
username = sudh
password = sudh123
```

The database would contain:

```text
sudh | sudh123
```

The transcript explains why this is unsafe: anyone with database access could see the real password.

Therefore, the later version uses password hashing.

---

# 7. Password Hashing

The final version uses:

```python
password_hash = PasswordHash.recommended()
```

During registration:

```python
hashed_password = password_hash.hash(user.password)
```

Example:

```text
User enters:
sudh123

Database stores something similar to:
$argon2id$v=19$...
```

So the real password is not stored directly.

The registration endpoint in the script is:

```python
@app.post("/register_hashed_pwdlib")
def register_user_hashed(user: User):

    hashed_password = password_hash.hash(user.password)

    response = client.table("users").insert({
        "username": user.username,
        "password": hashed_password
    }).execute()

    return response
```

### Flow

```text
User sends username/password
        ↓
password_hash.hash()
        ↓
Hashed password generated
        ↓
Username + hashed password stored in Supabase
```

---

# 8. Login

The login endpoint is:

```python
@app.post("/login_hashed_pwdlib")
def login_user_hashed_pwdlib(user: User):

    response = (
        client
        .table("users")
        .select("*")
        .eq("username", user.username)
        .execute()
    )

    if response.data and password_hash.verify(
        user.password,
        response.data[0]["password"]
    ):

        access_token = jwt.encode(
            {
                "sub": user.username,
                "exp": datetime.now(tz=timezone.utc)
                       + timedelta(minutes=30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "status": "success",
            "access_token": access_token
        }

    return {"status": "failure"}
```

Let us understand this step by step.

---

# 9. Find the User in Supabase

This code:

```python
response = (
    client
    .table("users")
    .select("*")
    .eq("username", user.username)
    .execute()
)
```

means:

```text
Go to users table
      ↓
Find record where username matches
      ↓
Return that record
```

For example:

```text
username entered = sudh
```

Supabase searches for:

```text
username = sudh
```

The important point is that the password is **not** compared directly in the database query because the database contains a hashed password.

---

# 10. Verify the Password

This code performs password verification:

```python
password_hash.verify(
    user.password,
    response.data[0]["password"]
)
```

Think of it as:

```text
Plain password entered by user
              +
Hashed password from database
              ↓
       password_hash.verify()
              ↓
          True / False
```

Example:

```text
Entered password: sudh123
Stored hash:      $argon2id$...
```

If they match:

```python
True
```

Otherwise:

```python
False
```

The transcript demonstrates the same behavior: a wrong password produces failure and the correct password produces success.

---

# 11. Generate the JWT Access Token

After password verification succeeds:

```python
access_token = jwt.encode(
    {
        "sub": user.username,
        "exp": datetime.now(tz=timezone.utc)
               + timedelta(minutes=30)
    },
    SECRET_KEY,
    algorithm="HS256"
)
```

The JWT payload contains:

```python
{
    "sub": user.username,
    "exp": expiration_time
}
```

### `sub`

`sub` means **subject**.

In this script:

```python
"sub": user.username
```

So if the user is:

```text
sudh
```

the token contains a subject identifying that user.

### `exp`

`exp` means **expiration time**.

The code:

```python
datetime.now(tz=timezone.utc) + timedelta(minutes=30)
```

means:

```text
Current UTC time + 30 minutes
```

Therefore this access token expires after 30 minutes.

The transcript also explains adding an expiration time so the access token does not remain valid indefinitely.

---

# 12. What is `SECRET_KEY`?

The script uses:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

This secret is used when creating and validating the token.

JWT creation:

```python
jwt.encode(
    payload,
    SECRET_KEY,
    algorithm="HS256"
)
```

JWT validation:

```python
jwt.decode(
    token.credentials,
    SECRET_KEY,
    algorithms=["HS256"]
)
```

The same secret must be available when encoding and decoding an HS256 token.

For learning, the earlier section of the script used:

```python
SECRET_KEY = "euron123"
```

The later version moves it to `.env`.

---

# 13. What is HS256?

The script uses:

```python
algorithm="HS256"
```

`HS256` is the JWT signing algorithm used by this example.

Simplified view:

```text
Payload
   +
SECRET_KEY
   +
HS256
   ↓
JWT token
```

A useful conceptual representation is:

```text
HEADER.PAYLOAD.SIGNATURE
```

Example shape:

```text
xxxxx.yyyyy.zzzzz
```

> Note: the transcript sometimes describes the JWT as "encrypted." More precisely, the JWT used here is **signed** with HS256. Its payload can be decoded, so sensitive data such as passwords should not be placed inside it.

---

# 14. JWT Login Response

After successful login, the endpoint returns:

```python
{
    "status": "success",
    "access_token": access_token
}
```

Example:

```json
{
  "status": "success",
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

The client now keeps this token and sends it when calling protected APIs.

This is why the user does not need to send the username and password again for every request.

---

# 15. HTTPBearer

The script creates:

```python
security = HTTPBearer()
```

This tells FastAPI:

> Protected APIs expect an HTTP Bearer token.

A normal HTTP request will look like:

```text
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

The transcript explains that the token is carried with requests to protected endpoints.

---

# 16. Protecting an API with `Depends`

The profile endpoint is:

```python
@app.get("/access_profile")
def access_profile(token=Depends(security)):

    decoded = jwt.decode(
        token.credentials,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    return {
        "status": "success",
        "username": decoded["sub"]
    }
```

The important part is:

```python
token = Depends(security)
```

This means the endpoint depends on the security mechanism.

Without the Bearer token, the protected endpoint should not be accessed successfully.

The transcript describes this as making the function depend on authorization before it can execute.

---

# 17. What is `token.credentials`?

When FastAPI receives:

```text
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

`HTTPBearer()` separates the request into roughly:

```text
scheme      = Bearer
credentials = eyJhbGciOiJIUzI1NiIs...
```

Therefore:

```python
token.credentials
```

gives only the JWT token.

---

# 18. Decode the JWT

The script uses:

```python
decoded = jwt.decode(
    token.credentials,
    SECRET_KEY,
    algorithms=["HS256"]
)
```

If the token is valid, `decoded` contains the payload.

For example:

```python
{
    "sub": "sudh",
    "exp": 1790000000
}
```

Then:

```python
decoded["sub"]
```

returns:

```text
sudh
```

The API responds:

```json
{
  "status": "success",
  "username": "sudh"
}
```

---

# 19. Another Protected Endpoint

The script has another endpoint:

```python
@app.get("/access_course")
def access_course(token=Depends(security)):

    decoded = jwt.decode(
        token.credentials,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    return {
        "status": "success",
        "username": decoded["sub"]
    }
```

The same JWT token can therefore be used to access multiple protected resources.

Conceptually:

```text
                     ┌──> /access_profile
JWT Bearer Token ────┤
                     └──> /access_course
```

The transcript explains this as logging in once and then using the token to access different authorized parts of the system.

---

# 20. Simple Real-World Analogy

The transcript gives an office ID-card analogy.

Think of JWT like this:

```text
Office Security                       FastAPI

Show identity + credentials           Username + Password
          ↓                                  ↓
Security verifies you                 Login verifies user
          ↓                                  ↓
Receive ID card                       Receive JWT token
          ↓                                  ↓
Carry ID card                         Send Bearer token
          ↓                                  ↓
Enter allowed rooms                   Access protected APIs
```

You do not show your original identity documents every time you enter another room.

Similarly:

```text
You do not send username/password
for every protected API request.

You send the JWT token.
```

---

# 21. Complete Flow with Example

Assume a user registers:

```json
{
  "username": "raffee",
  "password": "fastapi123"
}
```

### Step 1 — Register

Request:

```text
POST /register_hashed_pwdlib
```

FastAPI:

```python
hashed_password = password_hash.hash(user.password)
```

Supabase stores:

```text
username = raffee
password = <hashed value>
```

---

### Step 2 — Login

Request:

```text
POST /login_hashed_pwdlib
```

Body:

```json
{
  "username": "raffee",
  "password": "fastapi123"
}
```

Application:

```text
Find raffee in Supabase
        ↓
Read hashed password
        ↓
Verify fastapi123
        ↓
Password correct
        ↓
Generate JWT
```

Response:

```json
{
  "status": "success",
  "access_token": "eyJ..."
}
```

---

### Step 3 — Access Profile

Request:

```text
GET /access_profile
```

Header:

```text
Authorization: Bearer eyJ...
```

FastAPI executes:

```python
decoded = jwt.decode(
    token.credentials,
    SECRET_KEY,
    algorithms=["HS256"]
)
```

Then reads:

```python
decoded["sub"]
```

Response:

```json
{
  "status": "success",
  "username": "raffee"
}
```

---

# 22. Swagger `/docs` Testing Flow

The transcript tests the APIs using FastAPI Swagger UI.

Run the app and open:

```text
http://localhost:8000/docs
```

A simple testing order is:

```text
1. Call /register_hashed_pwdlib
2. Enter username and password
3. Execute

4. Call /login_hashed_pwdlib
5. Enter same username and password
6. Copy returned access_token

7. Use the Authorize/Bearer option in Swagger
8. Paste token

9. Call /access_profile
10. Call /access_course
```

If the token is missing or invalid, the protected endpoint should not allow normal access.

---

# 23. Authentication vs Authorization in This Project

### Authentication happens here

```python
password_hash.verify(
    user.password,
    response.data[0]["password"]
)
```

This answers:

```text
Is this really the user?
```

### Authorization/protected access happens here

```python
token = Depends(security)
```

and:

```python
jwt.decode(...)
```

This answers:

```text
Does this request have a valid token?
```

In a larger application, the decoded token can also be used to check roles such as:

```text
admin
manager
student
premium_user
```

---

# 24. Why Not Send Username and Password Every Time?

Without JWT:

```text
Request 1 → username/password
Request 2 → username/password
Request 3 → username/password
Request 4 → username/password
```

With JWT:

```text
Login once → username/password
              ↓
          receive JWT

Request 1 → JWT
Request 2 → JWT
Request 3 → JWT
Request 4 → JWT
```

This is the main idea demonstrated in the transcript.

---

# 25. Important Code Explained in One Place

## Register

```python
hashed_password = password_hash.hash(user.password)
```

Meaning:

```text
Plain password → hashed password
```

---

## Find user

```python
client.table("users").select("*").eq(
    "username",
    user.username
).execute()
```

Meaning:

```text
Search Supabase users table for username
```

---

## Verify password

```python
password_hash.verify(
    user.password,
    response.data[0]["password"]
)
```

Meaning:

```text
Compare entered password with stored hash
```

---

## Generate token

```python
jwt.encode(
    {
        "sub": user.username,
        "exp": datetime.now(tz=timezone.utc)
               + timedelta(minutes=30)
    },
    SECRET_KEY,
    algorithm="HS256"
)
```

Meaning:

```text
Create JWT for this user
Valid for 30 minutes
```

---

## Require Bearer token

```python
token = Depends(security)
```

Meaning:

```text
This endpoint requires authentication credentials
```

---

## Validate token

```python
jwt.decode(
    token.credentials,
    SECRET_KEY,
    algorithms=["HS256"]
)
```

Meaning:

```text
Check token signature/validity
and retrieve its payload
```

---

# 26. Final Simplified Code

The core example from the provided script can be understood as:

```python
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from supabase import create_client
import jwt
import os

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

security = HTTPBearer()
password_hash = PasswordHash.recommended()


class User(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(user: User):

    hashed_password = password_hash.hash(user.password)

    response = client.table("users").insert({
        "username": user.username,
        "password": hashed_password
    }).execute()

    return response


@app.post("/login")
def login(user: User):

    response = (
        client
        .table("users")
        .select("*")
        .eq("username", user.username)
        .execute()
    )

    if response.data and password_hash.verify(
        user.password,
        response.data[0]["password"]
    ):

        token = jwt.encode(
            {
                "sub": user.username,
                "exp": datetime.now(timezone.utc)
                       + timedelta(minutes=30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "status": "success",
            "access_token": token
        }

    return {"status": "failure"}


@app.get("/profile")
def profile(token=Depends(security)):

    decoded = jwt.decode(
        token.credentials,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    return {
        "status": "success",
        "username": decoded["sub"]
    }
```

---

# 27. Easy Interview Explanation

You can explain the project like this:

> In my FastAPI application, users first register with a username and password. Instead of storing the plain password, I hash it using `PasswordHash` and store the hash in Supabase. During login, I fetch the user by username and verify the entered password against the stored hash. If authentication succeeds, I generate a JWT access token containing the username in the `sub` claim and an expiration time of 30 minutes. Protected endpoints use FastAPI's `HTTPBearer` with `Depends` to receive the Bearer token. The API decodes and validates the JWT using the secret key and then allows the user to access protected resources such as profile or course APIs.

---

# 28. One-Line Memory Trick

Remember:

```text
REGISTER → HASH → STORE
LOGIN → VERIFY → TOKEN
REQUEST → BEARER TOKEN → DECODE → ACCESS
```

Or even shorter:

```text
Password proves who you are.
JWT proves you already logged in.
```

---

# 29. Files Used

This note was prepared from:

- `login(1).py`
- `transcript (7).txt`

The explanation follows the same learning progression used in the source material:

```text
Plain password
    ↓
Hashed password
    ↓
Login verification
    ↓
JWT generation
    ↓
Bearer token
    ↓
Protected APIs
    ↓
Token expiration
```
