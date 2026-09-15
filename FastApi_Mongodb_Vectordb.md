# FastAPI — The Story of How Your Click Talks to Code

*Notes written like a story, not a textbook. Read once to understand the "why", then use the interview Q&A section to revise. Based entirely on the two class sessions covering APIs and FastAPI.*

---

## 1. The Story — What Even Is an API?

Let's start with something you already do every day: sending money through Google Pay.

When you send ₹500 to a friend, Google Pay doesn't hold your money. It's just a *messenger*. It talks to your bank (say HDFC), your bank talks to the UPI server (owned by the Government of India), and UPI talks to your friend's bank (say ICICI) to credit the money there.

Now here's the interesting part: Google Pay's backend might be written in Java. HDFC's system might be in PHP. ICICI's might be in Scala. UPI's might be in Python. Nobody can force anybody to "please rewrite your whole backend in my language." That would be absurd.

Yet, all of them talk to each other flawlessly, every single day, millions of times. How?

> **This is the whole point of an API.** API = Application Programming Interface. It's a **bridge** between systems built in completely different languages/frameworks, so they can still call each other's functions using one common, neutral protocol — usually HTTP/HTTPS.

**The one-line theory to remember:** Every click you make on your phone — booking an Uber, ordering on Zomato, logging into Gmail — is silently calling one or more *functions* running on someone else's server. The API is simply the doorway that lets your click reach that function, regardless of what language the function was written in.

---

## 2. Your First API — Turning a Python Function into a Website

Here's the magic trick the class did live: take a normal Python function, and make it callable from *any* browser, *any* language, *any* machine on the internet — without that caller knowing a single line of Python.

### 2.1 Setup

```bash
pip install fastapi uvicorn
```

> Think of it like this: **FastAPI** is the framework that lets you *label* a Python function as "publicly callable." **Uvicorn** is the engine that actually turns your Python file into a running server — like plugging in a shop's shutter and switching the lights on.

### 2.2 The Simplest Possible API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/sudh/kumar")
def test():
    print("this is my test fun")
    return {
        "message": "this is my first api program"
    }
```

Run it with:

```bash
uvicorn fastapi_test:app --reload
```

- `fastapi_test` = your filename (without `.py`)
- `app` = the FastAPI object you created
- `--reload` = auto-restart the server every time you save a change

Once running, it prints something like:
```
Uvicorn running on http://127.0.0.1:8000
```

**Break that address down like a postal address:**

| Part | Meaning |
|---|---|
| `127.0.0.1` (localhost) | *Which machine* — "this machine right here" |
| `8000` | *Which door on that machine* — the port number |
| `/sudh/kumar` | *Which specific function* behind that door — the route |

Open `http://localhost:8000/sudh/kumar` in **any browser** (Chrome isn't written in Python!) — and you'll see your Python function's return value. That's the entire trick: your Pythonic function is now language-independent, reachable by literally anything that can speak HTTP.

> **The `@app.get("/route")` line is called a decorator** — think of it as a sticky note you paste on top of your function saying: "Hey world, if anyone knocks on this door (`/route`) with a GET request, run *this* function and hand them back what it returns."

---

## 3. Making the Whole World See It — ngrok

As of now, only people on your Wi-Fi can reach `127.0.0.1`. To let the *entire internet* — your classmates on Zoom, anyone — hit your local server, you need a tunnel.

```bash
ngrok http 8000
```

This gives you a public HTTPS URL (like `https://random-name.ngrok.io`) that forwards straight into your local port 8000. Anyone in the world hitting that URL is secretly hitting your laptop.

> **Analogy:** Imagine your house has no street address, but you set up a mail-forwarding service that gives you a real, public street address, and any letter sent there magically appears on your desk. That's exactly what ngrok does for your local server.

This is also how the instructor could see, in real time, students' IP addresses, browsers, and even locations hitting his server — because every request carries this metadata by default (more on this later).

---

## 4. Swagger UI — Your Free, Built-in API Testing Tool

FastAPI gives you something amazing for free: visit `/docs` on your running server (e.g. `http://localhost:8000/docs`) and you get an interactive UI listing every API you've created.

```
http://localhost:8000/docs
```

You can click **Try it out → Execute** on any endpoint and test it without writing a single `curl` command. This UI is called **Swagger UI**, and it's one of FastAPI's biggest advantages over other frameworks like Flask (which gives you *no* UI — you'd have to build your own documentation).

You can also test the same API from the command line using `curl`, which Swagger UI conveniently generates for you:

```bash
curl -X GET "http://localhost:8000/sudh/kumar"
```

---

## 5. Passing Data to a Function — Query Parameters

A function that takes no input is boring. Let's pass values.

```python
@app.get("/add")
def add(a, b):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }
```

Call it like:
```
http://localhost:8000/add?a=3&b=4
```

Everything after `?` is a **query parameter** — a way of passing data straight through the URL.

> **Gotcha demonstrated in class:** if `a` and `b` aren't typed as numbers, Python treats them as strings, so `a + b` becomes string concatenation ("3" + "4" = "34"), not addition (7). Fix it by adding type hints:

```python
@app.get("/calculator")
def calculator(a: float, b: float, operation: str):
    if operation == "add":
        result = a + b
    elif operation == "sub":
        result = a - b
    elif operation == "mul":
        result = a * b
    elif operation == "div":
        result = a / b
    else:
        return {"message": "you have to pass a valid input"}
    return {"result": result}
```

FastAPI automatically reads your type hints (`a: float`) and validates incoming data against them — reject bad input before your function even runs. This is a small taste of a bigger concept coming up: **Pydantic**.

---

## 6. The Five HTTP Methods — The Real Heart of REST APIs

REST stands for **Representational State Transfer** — a fancy name for a simple idea: *expose your data and functions over HTTP, using standard verbs that describe what action you're taking.*

Here's the story analogy that makes all five verbs click instantly — think of a **library with books**:

| Method | Library Analogy | What It Does |
|---|---|---|
| **GET** | Reading a book off the shelf | Fetch/read data. Never modifies anything. |
| **POST** | Donating a brand-new book to the library | Create new data. |
| **PUT** | Replacing an entire damaged book with a new full copy | Update/replace *all* fields of a record. |
| **PATCH** | Just fixing a torn page, not the whole book | Update *only* the specific fields you send. |
| **DELETE** | Removing a book from the shelf entirely | Delete data. |

### 6.1 GET — Reading, the Insecure Way

```python
books = {
    1: {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 10.99},
    2: {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 12.99},
    3: {"id": 3, "title": "1984", "author": "George Orwell", "price": 9.99}
}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = books.get(book_id)
    if book:
        return {"book": book}
    else:
        return {"message": "Book not found"}, 404
```

Notice `{book_id}` in the route — this is a **path parameter**. It's part of the URL structure itself: `/books/3` fetches book #3 directly.

**Why is GET called "insecure"?** Because whatever you pass through the URL is fully visible — in the browser's address bar, in server logs, in your browser history. Try Googling something: `google.com/search?q=data+science` — your search term sits right there in the URL. That's fine for a search, but terrible for a password. Which is exactly why Gmail's login page never shows your email/password in the URL — because login uses **POST**, not GET.

### 6.2 POST — Creating, the Secure Way

```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    price: float

@app.post("/books/")
def create_book(book: Book):
    new_id = max(books.keys()) + 1
    books[new_id] = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "price": book.price
    }
    return {"message": "Book created successfully", "book": books[new_id]}
```

With POST, data travels inside the **request body**, not the URL — invisible to anyone glancing at your browser bar. This is why every login form, every signup form, every "create" action uses POST.

> **Notice the auto-incrementing ID trick:** `max(books.keys()) + 1` — take whatever the highest existing key is, add 1. Simple, elegant, avoids the caller having to guess or clash IDs.

### 6.3 PUT — Full Replace

```python
@app.put("/books/{book_id}")
def replace_book(book_id: int, book: Book):
    if book_id in books:
        books[book_id] = {
            "id": book_id,
            "title": book.title,
            "author": book.author,
            "price": book.price
        }
        return {"message": "Book replaced successfully", "book": books[book_id]}
    else:
        return {"message": "Book not found"}, 404
```

You must send **every field** — title, author, price — even if only the price changed. PUT overwrites the whole record.

### 6.4 PATCH — Partial Update

But what if the book's price changed due to inflation, and you don't want to re-type the title and author? That's where PATCH shines.

```python
from typing import Optional

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None

@app.patch("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    update_data = book.model_dump(exclude_unset=True)  # only fields the caller actually sent
    books[book_id].update(update_data)
    return {"message": "Book updated successfully", "book": books[book_id]}
```

The key trick: `exclude_unset=True`. It tells Pydantic — "only give me back the fields the caller *actually provided*, ignore the ones left as default." That way, sending just `{"price": 15.5}` updates *only* the price, leaving the title and author untouched.

> **Analogy recap:** PUT = repaint the whole car. PATCH = just touch up the one scratch.

### 6.5 DELETE — Removing

```python
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id in books:
        del books[book_id]
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
```

Simple, does exactly what it says.

---

## 7. Pydantic — The Bouncer at the Door

Here's a real Python quirk: type hints are just *notes*, not *rules*.

```python
a: int = 5
a = "hello"   # Python won't stop you! It's just a suggestion, not a law.
```

That's dangerous for an API — you don't want someone submitting `name: 12345` when you expect a string. This is exactly the gap **Pydantic** fills. Pydantic classes *actually enforce* the rules, rejecting bad data before it ever reaches your function.

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import date
from typing import Optional

class User(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr                         # auto-validates proper email format
    age: int = Field(gt=0, le=100)           # must be > 0 and <= 100
    github_url: Optional[HttpUrl] = None     # auto-validates it's a real URL
    enrollment_date: Optional[date] = None
    full_name: Optional[str] = None
    skills: list[str] = Field(min_length=1, max_length=10)   # at least 1 skill required
```

```python
@app.post("/users/")
def create_user(user: User):
    return {"user": user}
```

If someone sends `age = -7` or `name = 12345` instead of a string, FastAPI automatically returns a `422 Unprocessable Entity` error with a clear message — *before* your function even runs. You never have to write manual `if` checks for basic validation again.

> **Theory in one line:** Pydantic is a *bouncer at the club entrance*. It checks everyone's ID card (data type, format, range) before letting them in. Your function only ever sees clean, valid data.

**Interesting library note:** Pydantic ships with pre-built validators for common patterns — `EmailStr` for emails, `HttpUrl` for URLs — so you don't hand-roll regex for these common cases. For something niche (like an Indian mobile number format), you'd write a **custom validator** yourself.

---

## 8. Securing Your API — Because Anyone Can Hit an Open Door

So far, *anyone* on the internet could call every function you exposed — no login, no permission. That's obviously dangerous for a real system. Let's lock the door.

### 8.1 The Basic Idea — A Secret Password

```python
from fastapi import FastAPI, Depends, Header, HTTPException, status

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
def test(verify: bool = Depends(verify_token)):
    return {"message": "Token verified successfully"}
```

The magic word here is **`Depends`**. It says: "Before you even run this function, first run `verify_token` and get its result." If `verify_token` raises an error (wrong key), the actual function `test()` never even executes.

> **Analogy:** `Depends()` is a security guard standing outside a meeting room. Before you're allowed to enter and speak (execute your function), the guard checks your badge (the token). No badge, no entry — you never even reach the conference table.

Call it with a header (a way of sending data alongside a request, invisible in the URL, unlike query parameters):

```bash
curl -H "x-token: test123" http://localhost:8000/test
```

### 8.2 A Cleaner Way — `APIKeyHeader`

FastAPI gives you a pre-built helper for exactly this "give me a secret key in the header" pattern:

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/test1")
def test1(api_key: str = Depends(api_key_header)):
    if api_key != SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return {"message": "API Key verified successfully"}
```

**The difference from a plain header, demonstrated in class:** Swagger UI shows a little 🔒 **lock icon** next to endpoints using `APIKeyHeader`. It knows this field is a *security credential*, not just random text — so it hides the value once entered, and gives you a proper "Authorize" popup to save your key across multiple test calls. A plain `Header()` is treated like any other string field, no special protection.

### 8.3 Protecting a POST Endpoint Too

```python
class Book(BaseModel):
    title: str
    author: str
    year: int

@app.post("/create_book")
def create_book(book: Book, x_api_key: str = Depends(APIKeyHeader(name="X-API-Key"))):
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return {"message": "Book created successfully", "book": book.dict()}
```

Same pattern: whatever HTTP method, whatever route — just add the `Depends(...)` bouncer and it applies.

---

## 9. Rate Limiting — Stopping Someone from Flooding Your Server

Imagine someone writes a script that hits your `/add` endpoint 10 million times a second. Your server has finite CPU and RAM — it'll choke. This is how basic (denial-of-service style) attacks work, even unintentionally from a buggy client script.

```python
import time
from fastapi import Request

request_history = {}

@app.get("/rate-limiting")
def rate_limiting(request: Request):
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in request_history:
        request_history[client_ip] = []

    # keep only requests from the last 60 seconds
    request_history[client_ip] = [
        timestamp for timestamp in request_history[client_ip]
        if current_time - timestamp < 60
    ]

    if len(request_history[client_ip]) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )

    request_history[client_ip].append(current_time)
    return {"message": "Request successful"}
```

**The logic, in plain words:**
1. Look up this visitor's IP.
2. Check their history of recent hit-timestamps, throw away anything older than 60 seconds.
3. If they've already hit you 5+ times in the last 60 seconds — reject them with a `429 Too Many Requests`.
4. Otherwise, log this hit and let it through.

> **Analogy:** It's like a bouncer at a buffet counter who says "you can only come back for a refill 5 times per hour" — after that, no more plates, no matter how much you insist.

This is a hand-rolled version of what production systems usually do via an **API Gateway** (a dedicated layer that handles rate limiting, authentication, and routing before requests even reach your actual server) — something to be covered in later, more advanced classes.

---

## 10. Reading Data *About* the Caller — Request Metadata

Every request that hits your server silently carries a lot of metadata — you don't have to ask for it, it's just there in the `Request` object.

```python
from fastapi import Request

@app.get("/visitor")
def visitor(request: Request):
    return {
        "ip": request.client.host,
        "port": request.client.port
    }
```

And going further — full visitor fingerprinting, exactly as demonstrated live in class:

```python
from datetime import datetime

@app.get("/who-is-hitting-me")
def who_is_hitting_me(request: Request):
    forwarded_for = request.headers.get("x-forwarded-for")
    visitor_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host

    visitor_data = {
        "public_ip": visitor_ip,
        "source_port": request.client.port,
        "user_agent": request.headers.get("user-agent"),   # browser/device info
        "language": request.headers.get("accept-language"),
        "referer": request.headers.get("referer"),
        "method": request.method,
        "url": str(request.url),
        "timestamp": datetime.now().isoformat()
    }
    print(visitor_data)   # logs on the server console in real time
    return {"message": "Request received successfully"}
```

This is exactly how every website on the internet quietly knows your browser, rough location (via IP), device, and preferred language — no special hacking involved, just reading what your own browser sends in its headers on every single request. This is also the technical seed of how ad-targeting and personalized recommendations begin.

---

## 11. Exposing System Info — Just Another Function

```python
import socket, platform, os

@app.get("/sudh_server")
def sudh_server_details():
    return {
        "hostname": socket.gethostname(),
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "current_directory": os.getcwd()
    }
```

Nothing new conceptually — same "write a Python function, decorate it with `@app.get`" pattern. The point here was to hammer home that *anything* a Python function can compute, an API can expose.

---

## 12. The Inspect Tool — Seeing APIs Everywhere

One final "aha" moment from class: open any website, right-click → **Inspect → Network tab**, then click around the site. You'll see a stream of requests firing — each with a URL, a method (GET/POST), and a response body.

That banner image on a homepage? An API call. The "recent courses" list? An API call — `?type=recent&page=1&limit=12` is literally a query-parameter-driven GET request, exactly like the `/add?a=3&b=4` you wrote yourself. There is **no website in existence that doesn't run on this exact same pattern** underneath its polished UI.

---

## 13. Q&A — Real Doubts Raised in Class

**Q: Is an API always real-time?**
A: No. That depends entirely on which protocol and design you choose. Some APIs are designed for batch processing, some for real-time — it's a choice, not a guarantee.

**Q: Why did we use a `.py` file instead of a Jupyter notebook (`.ipynb`) this time?**
A: A notebook is like a *form* — it never executes as a standalone file; it needs a kernel attached, and cells execute independently, not as one continuous sequential program. A server needs to run as one single continuous process, in order — which only a `.py` file (run via `python file.py` or `uvicorn file:app`) can do properly.

**Q: Does Swagger UI come from FastAPI specifically, or is it separate?**
A: Swagger UI is *built into* FastAPI by default — you get it for free at `/docs`. Flask (another Python API framework) doesn't include this; you'd have to add your own documentation tool, like Postman collections.

**Q: Is GET always insecure?**
A: Yes — anything passed via GET (query parameters) is visible in the URL, browser history, and server logs. That's why sensitive data (passwords, tokens) should always go through POST (request body), never GET.

**Q: What's the actual difference between passing data via a plain `Header()` versus `APIKeyHeader`?**
A: Functionally, both read a value from the request headers. But `APIKeyHeader` explicitly tells FastAPI (and Swagger UI) "this is a security credential" — so Swagger shows a 🔒 lock icon, provides an "Authorize" button, and hides the value visually. A plain header field is treated like any other piece of text data with no special protection semantics.

**Q: Do I need to implement rate limiting myself in every project?**
A: In production, you'd typically rely on an **API Gateway** to handle this centrally rather than hand-writing it into every endpoint. But understanding the underlying logic (as coded above) is important — it's exactly what such gateways do internally.

**Q: If my API is exposed over the internet (e.g. via ngrok), do people accessing it need ngrok installed too?**
A: No. ngrok is only needed on the *server* side to create the tunnel. Anyone hitting the resulting public HTTPS URL is just making a normal HTTPS request — no special tool needed on their end, just like visiting any website.

**Q: Can this same Python function be called from Java, JavaScript, or any other language?**
A: Yes — that's the entire point of exposing it via HTTP/REST. The moment a function is wrapped behind an API endpoint, it becomes language-independent. Any language capable of making an HTTP request (which is basically all of them) can call it.

---

## 14. Revision Points — Read the Night Before Your Exam / Interview

**Core Concept**
- API = a bridge that lets systems written in different languages/frameworks communicate, typically over HTTP/HTTPS.
- Every click in any app ultimately triggers one or more backend function calls — this is universal across the digital world.
- REST API (Representational State Transfer) = exposing functions/resources over standard HTTP verbs.

**Building Blocks**
- `FastAPI()` creates the app object; `@app.get("/route")` (or `.post`, `.put`, `.patch`, `.delete`) decorates a function to expose it at that route.
- Run with `uvicorn filename:app --reload`.
- Address = `host:port/route` (e.g. `127.0.0.1:8000/add`).
- `/docs` gives you Swagger UI automatically — test any endpoint without writing curl commands.
- `ngrok http <port>` exposes your local server to the public internet via a secure HTTPS tunnel.

**HTTP Methods — Library Analogy**
| Method | Purpose |
|---|---|
| GET | Read data (insecure — visible in URL) |
| POST | Create data (secure — sent in body) |
| PUT | Replace the *entire* record |
| PATCH | Update only *specific* fields (`exclude_unset=True`) |
| DELETE | Remove a record |

**Validation**
- Type hints in plain Python are just suggestions — they don't enforce anything.
- Pydantic (`BaseModel`) enforces real validation: data types, string length (`Field(min_length=..., max_length=...)`), numeric ranges (`Field(gt=0, le=100)`), and special formats (`EmailStr`, `HttpUrl`).
- Invalid data → automatic `422 Unprocessable Entity` before your function code even runs.

**Security**
- `Depends()` runs a dependency function *before* your endpoint executes — used to gate access.
- `Header(...)` reads a plain custom header value (e.g., `x-token`).
- `APIKeyHeader(name="X-API-Key")` is the FastAPI-native way to mark a header as a security credential — shows a 🔒 lock + Authorize button in Swagger UI.
- Rate limiting: track each client IP's recent request timestamps; reject with `429 Too Many Requests` once they exceed your threshold within a time window.

**Metadata**
- The `Request` object gives you IP, port, headers (`user-agent`, `accept-language`, `referer`) for free on every incoming call — this is the technical basis of analytics, personalization, and ad targeting across the web.

**Golden Takeaway**
- Every website you've ever used is, underneath the UI, just a continuous stream of exactly these API calls — GET to read, POST to create, PUT/PATCH to update, DELETE to remove — all secured, validated, and rate-limited the same way you just learned to do by hand.




# MongoDB & Vector Databases — The Story of Your Data

*Notes written like a story, not a textbook. Read it once for understanding, then use the revision points before your exam. Based entirely on the class session covering MongoDB and Vector (Qdrant) databases.*

---

## 1. The Story So Far

In the previous class, an API was built to talk to a SQL database — tables, rows, columns, a fixed schema you must follow every single time.

In this class, the story moves to two new kinds of databases:

1. **MongoDB** — a document-based NoSQL database.
2. **Vector Database (Qdrant)** — a database that stores the *meaning* of your data as numbers, not the data itself.

Both are things you will genuinely use once you start building real applications, because SQL alone can't handle every kind of data you'll meet in the real world.

---

## 2. MongoDB — The Flexible Database

### 2.1 Why MongoDB Exists

In SQL, before you store anything, you must first design a table: fixed column names, fixed data types. Every single row you insert **must** follow that exact structure. If tomorrow you want to add a new field, you have to change the whole table design.

MongoDB throws that rule away. It says: "Bring me your data in whatever shape it is today — I'll store it." It's called a **document-based database**, and the "document" it stores looks exactly like a Python dictionary — key and value pairs.

> **Theory line to remember:** MongoDB has no hard-and-fast schema rule. This time you might insert `{name, age, email}`. Next time you might insert only `{name, grade}`, or add something new like `{skills, project}` — same collection, no error. This flexibility is exactly why MongoDB, along with Cassandra and HBase, became so popular across the industry over the last 10–15 years.

### 2.2 The SQL vs MongoDB Mapping

| SQL World | MongoDB World |
|---|---|
| Database | Database (DB) |
| Table | Collection |
| Row / Record | Document (a dictionary) |
| Column + fixed data type | Key inside a document — flexible, can change any time |

### 2.3 Setting Up the Connection

The steps used in class, in order:

1. Log in to MongoDB Atlas and open your cluster.
2. Click **Connect → Driver → Python 3.12 or later**.
3. Copy the connection string it gives you.
4. Fill in your DB password inside that string.
5. Use it inside Python via `pymongo`.

```python
from pymongo import MongoClient

# the connection string you copied from MongoDB Atlas, with your password filled in
client = MongoClient("your-connection-string-here")

# creating (or selecting) a database — MongoDB creates it automatically if it doesn't exist
db = client["july_super_mongo"]

# creating (or selecting) a collection inside that database — same automatic creation
collection = db["student_collection"]
```

Only **three lines**, always in this order: create a `client`, pick a `database` from it, pick a `collection` from that database. You never run a "CREATE DATABASE" command like in SQL — it's created the moment you insert the first document into it.

You can verify all this visually too: go to your cluster → **Browse Collections** — this shows every database and collection you've created, and the actual documents stored inside.

---

## 3. CRUD in MongoDB — Insert, Find, Update, Delete

### 3.1 Insert — Adding Data

**Insert one record:**

```python
collection.insert_one({
    "id": 1,
    "name": "Anshu Kumar",
    "age": 30,
    "email": "anshu@example.com",
    "skills": ["Python", "SQL", "MongoDB"]
})
```

This one line does the whole job — create the collection (if it doesn't exist yet) and drop the data in.

**A key demonstration from class:** the *next* record you insert doesn't need to match the shape of the first one at all.

```python
collection.insert_one({
    "id": 2,
    "name": "Rahul",
    "age": 27,
    "skills": ["Python", "FastAPI"],
    "project": "Chatbot App"   # <- a brand-new field, never used before, and MongoDB accepts it without complaint
})
```

That's the exact moment SQL and MongoDB part ways — in SQL this would fail unless you redesigned the whole table. In MongoDB, it just works.

**Insert many records at once (bulk insert):**

```python
students = [
    {"id": 3, "name": "Rahul", "age": 27},
    {"id": 4, "name": "Neha", "age": 24},
    {"id": 5, "name": "Sudha", "age": 22},
]
collection.insert_many(students)
```

> **Common error to expect:** `DuplicateKeyError`. This happens when you reuse an `id`/`_id` value that already exists — MongoDB enforces uniqueness on it, exactly like a primary key in SQL.

### 3.2 Find — Reading Data

```python
# find_one -> gives you just the first matching document (a "sample")
student = collection.find_one({"name": "Rahul"})

# find -> gives you EVERYTHING that matches (or everything, if no filter)
all_students = collection.find()
```

**Filtering with conditions** — this is where MongoDB's query operators come in:

```python
# age greater than 25
collection.find({"age": {"$gt": 25}})

# age less than 25
collection.find({"age": {"$lt": 25}})

# age equal to 25
collection.find({"age": {"$eq": 25}})

# age greater than or equal to 25
collection.find({"age": {"$gte": 25}})

# age less than or equal to 25
collection.find({"age": {"$lte": 25}})

# find by an exact field value (no operator needed)
collection.find({"name": "Ranshu Kumar"})
```

**The operator cheat sheet from class:**

| Operator | Meaning |
|---|---|
| `$gt` | greater than |
| `$lt` | less than |
| `$gte` | greater than or equal to |
| `$lte` | less than or equal to |
| `$eq` | equal to |
| (implied `$ne` exists too) | not equal to |

### 3.3 Update — Changing Data

An update always needs **two parts**: a condition (who to update) and a `$set` (what to change).

```python
# update_one — updates the first match only
collection.update_one(
    {"name": "Amit"},
    {"$set": {"age": 26}}
)

# update_many — updates every matching document in one shot
collection.update_many(
    {"age": {"$lt": 25}},
    {"$set": {"age": 25}}
)
```

**A moment from class worth remembering:** after running `update_many` to bump everyone under 25 up to age 25, searching again for `{"age": {"$lt": 25}}` returned an *empty list* — because there genuinely was nobody left matching that old condition anymore. That's the update working correctly, not a bug.

### 3.4 Delete — Removing Data

```python
# delete_one — deletes the first match only
collection.delete_one({"name": "Amit"})

# delete_many — deletes every matching document
collection.delete_many({"age": 25})
```

> **Story recap:** Insert → Find → Update → Delete. Every single operation here is basically a one-liner. This ease of use, combined with the schema flexibility, is exactly why MongoDB (and databases like it) took over so much of the industry.

---

## 4. Vector Databases — Searching by Meaning, Not Keywords

### 4.1 The Story Behind Why Vector DBs Exist

Imagine you work in an HR department (or Finance, or Legal) with hundreds of thousands of documents. In the old world, you'd build a keyword-based search — it works, but it's dumb; it only finds exact word matches.

Generative AI changed this. The new idea:

1. Read all your documents.
2. Break them into small pieces — lines, paragraphs, or "chunks."
3. Convert each chunk into a **numerical representation** (a vector) using an embedding model.
4. Store that vector *along with* the original text.
5. When someone asks a question in plain English (or any language), convert their question into a vector too, and find the *nearest* stored vectors.

> **The core theory:** Computers don't understand English, Hindi, or Tamil — at the end of the day, everything is just numbers to them. An embedding model has been trained on huge amounts of data and understands semantic meaning — what tends to come after what, grammar, relationships between words — and it uses that understanding to represent any sentence as an array of numbers.

This is exactly why vector databases exploded in popularity once **RAG (Retrieval Augmented Generation)** became a big deal — before that, they were barely used.

### 4.2 Providers Mentioned in Class

Qdrant, FAISS, ChromaDB, Pinecone, Weaviate — and even general-purpose databases like Supabase and MongoDB itself have started offering vector storage and search as a built-in feature. Learning one vector DB well makes the others easy to pick up, since the core idea (store vector + do similarity search) is the same everywhere.

### 4.3 Setting Up Qdrant

1. Go to Qdrant's site and sign in with Google (takes under a minute).
2. Click **Cluster → Create Cluster** (first-time setup takes a few minutes).
3. Open **Cluster UI** to see your cluster's collections.
4. Go to **API Key → Create**, and copy both the **API Key** and the **Cluster Endpoint (URL)** — you need both.

```python
from qdrant_client import QdrantClient

client = QdrantClient(
    url="your-cluster-endpoint-url",
    api_key="your-qdrant-api-key"
)
```

> Qdrant gives a free instance that's more than enough for building and testing real applications — no card required unless you're scaling to a massive number of users.

### 4.4 Generating Embeddings (Converting Text to Numbers)

An embedding model is needed to do this conversion. Class used a model gateway (Euron/URI API) that gives access to many providers' models through one API key — because every model provider makes their models "OpenAI-compatible", so one single interface can call any of them: OpenAI, Gemini, Claude, Qwen, Kimi, and more.

```python
from openai import OpenAI
import os

os.environ["EURI_API_KEY"] = "your-euri-api-key"

client_openai = OpenAI(
    base_url="https://api.euron.one/euri",
    api_key=os.environ["EURI_API_KEY"]
)

def generate_embedding(text):
    response = client_openai.embeddings.create(
        model="gemini-embedding-2-preview",   # embedding model used in class
        input=text
    )
    return response.data[0].embedding
```

The result is a list of numbers — for the Gemini embedding model used in class, the vector had a length (dimension) of **3072**. Every embedding model has its own fixed output size, and you must match your vector DB's collection size to it.

### 4.5 Creating a Collection in Qdrant

```python
from qdrant_client.models import VectorParams, Distance

client.create_collection(
    collection_name="your_knowledge_base",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
)
```

- **size** — must match your embedding model's output length (3072, in this case).
- **distance** — the similarity metric. Class mentioned a few options: Euclidean distance, Manhattan distance, cosine similarity, and HNSW. **Cosine similarity** was the one used, since it's the most common choice for text embeddings.

### 4.6 Storing Data (Vector + Original Text)

Just storing the vector isn't enough — you also want the original text next to it, so when you find a match, you can actually read what it says. That original text is stored as a **payload**.

```python
from qdrant_client.models import PointStruct

text = "MongoDB is a document-oriented NoSQL database."
vector = generate_embedding(text)

point = PointStruct(
    id=1,
    vector=vector,
    payload={"text": text}
)

client.upsert(
    collection_name="your_knowledge_base",
    points=[point]
)
```

**Storing multiple documents in a loop** (this was the real demo in class — five documents about different topics):

```python
documents = [
    {"text": "MongoDB is a document-oriented NoSQL database.", "course": "Databases", "chapter": 1},
    {"text": "Docker packages an application together with its dependencies.", "course": "DevOps", "chapter": 2},
    # ... and so on
]

for i, doc in enumerate(documents):
    vector = generate_embedding(doc["text"])
    point = PointStruct(id=i, vector=vector, payload=doc)
    client.upsert(collection_name="your_knowledge_base", points=[point])
```

### 4.7 Searching by Meaning (Semantic Search)

This is the payoff moment — instead of matching exact keywords, you convert your *question* into a vector too, and ask the database for the nearest matches.

```python
query = "tell me about MongoDB"
query_vector = generate_embedding(query)

results = client.query_points(
    collection_name="your_knowledge_base",
    query=query_vector,
    limit=3   # top 3 results, i.e. "top K"
)

for point in results.points:
    print(point.score, point.payload["text"])
```

In class, asking "tell me about MongoDB" correctly returned the MongoDB document as the top hit, with the highest similarity score — followed by the Docker document as the next closest, purely because the model understood meaning, not exact word overlap.

> **The score:** with cosine similarity, the score always falls between 0 and 1. Closer to 1 means the two pieces of text are closer in meaning.

---

## 5. Q&A — The Actual Questions Asked in Class

**Q: Is MongoDB expensive for production use?**
A: No. It runs on a pay-as-you-go model and ends up similarly priced to Postgres-based databases (like Neon/PG).

**Q: When should I use MongoDB vs a SQL database like Postgres/Neon?**
A: Use MongoDB wherever your data's shape is flexible or unpredictable. Use SQL when the structure is fixed and strict rules matter.

**Q: I got a "duplicate key error" on insert — why?**
A: You reused an `id` value that already exists in the collection. Change it to a new, unused value.

**Q: I ran `find` with a filter and got an empty list — is something broken?**
A: Not necessarily. If you previously ran an `update_many` that changed every document matching that filter, there may genuinely be nothing left that matches the old condition anymore.

**Q: Are we only able to use Gemini's embedding model? What about OpenAI or others?**
A: No — the gateway makes *every* provider's models "OpenAI-compatible," so the same code style works for OpenAI, Gemini, Claude, Qwen, Kimi, and others. You just change the `model` name.

**Q: What does the vector's "size" (e.g. 3072) actually represent?**
A: It's how many numbers are used to represent one piece of text's meaning. Different embedding models output different sizes — your Qdrant collection's vector size must match your model's output size exactly, or inserts will fail.

**Q: What does the similarity "score" mean when searching?**
A: With cosine similarity, it's always between 0 and 1. It tells you how close in *meaning* two vectors are — higher score = closer semantic match.

**Q: Why does vector search matter — what's the real-world use?**
A: Search, recommendation systems, and knowledge-base Q&A across any domain — HR, legal, finance, customer support — anywhere there's large unstructured text data (multiple languages included) and you need meaning-based, not just keyword-based, retrieval. This is the backbone behind RAG (Retrieval Augmented Generation), which comes up in later chapters.

---

## 6. Revision Points — Read This the Night Before

**MongoDB**
- Document-based NoSQL database. Mapping: Database ↔ Database, Table ↔ Collection, Row ↔ Document (a dictionary), Column ↔ Key (flexible, no fixed schema).
- Connect in 3 steps: `MongoClient(uri)` → pick `db` → pick `collection`. Both DB and collection auto-create on first insert.
- CRUD cheat sheet:
  - **Create:** `insert_one()`, `insert_many()`
  - **Read:** `find_one()` (sample), `find()` (all/filtered) with operators `$gt`, `$lt`, `$gte`, `$lte`, `$eq`, `$ne`
  - **Update:** `update_one()`, `update_many()` — always needs a filter + `$set`
  - **Delete:** `delete_one()`, `delete_many()`
- Flexibility is the core advantage: each document can have a different shape, unlike SQL's fixed schema.
- Watch out for `DuplicateKeyError` when the same `id` is reused.

**Vector Databases (Qdrant)**
- Store the *meaning* of text as a numeric array (vector/embedding), not the raw text alone.
- Pipeline: text → embedding model → vector → store in vector DB with original text as `payload` → convert query to vector too → similarity search → ranked results by score.
- Embedding model output size must exactly match the vector DB collection's configured size (e.g. 3072 for the Gemini embedding model used in class).
- **Cosine similarity** was the distance metric used — score range 0 to 1, higher = closer meaning.
- Enables semantic search: finding relevant results even when the exact words don't match, which is impossible with plain keyword search.
- This is the foundation for RAG (Retrieval Augmented Generation), covered in later, more advanced chapters.

**General Takeaway from Class**
- Both databases exist to solve different problems: MongoDB for flexible structured/document data, Qdrant (vector DB) for meaning-based search over unstructured text.
- In real projects, it's common to use multiple databases together (SQL + MongoDB + Vector DB) depending on the need — "mix and match" based on system design.
