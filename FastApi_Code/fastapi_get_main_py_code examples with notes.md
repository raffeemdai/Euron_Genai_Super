# FastAPI `main.py`: Code Explanations, Usage, Purpose, Syntax & Memory Tricks

> **File:** `main.py` (Super30 FastAPI GET API): 14 GET endpoints
> **Version:** updated for your **latest `main.py`**, in which the `get=0` typo is already fixed to `ge=0`.
> **Tested with:** FastAPI 0.141.1 · Pydantic 2.13.5 · Python 3.12. Every "actual response" below was produced by running your updated file, not guessed.
> **Legend:** 🎯 Purpose · 🔍 How it works · 🚀 Usage · 📌 Noting points · ⚠️ Gotcha · 🧠 Memory trick

---

## Table of Contents

1. [Big picture: what this file is](#1-big-picture)
2. [How to run & test](#2-how-to-run--test)
3. [Core concepts you need first](#3-core-concepts)
4. [Imports & app object](#4-imports--app-object)
5. [Endpoint-by-endpoint explanations](#5-endpoint-by-endpoint)
6. [Change log, remaining bugs & improvements (verified)](#6-change-log-remaining-bugs--improvements)
7. [Syntax cheat sheet](#7-syntax-cheat-sheet)
8. [Memory tricks (master list)](#8-memory-tricks-master-list)
9. [Endpoint summary table](#9-endpoint-summary-table)
10. [Interview Q&A](#10-interview-qa)
11. [Practice exercises](#11-practice-exercises)

---

# 1. Big Picture

## 🎯 What this file does
`main.py` is a **learning API** that demonstrates, step by step, the different ways FastAPI receives input using only **GET** requests:

| Stage | Endpoints | What it teaches |
|---|---|---|
| **A. Query parameters (plain)** | `/student`, `/course`, `/skills` | Reading `?key=value` from the URL, including lists |
| **B. Path parameters + response model** | `/add/{num1}/{num2}`, `/add_new/...` | Values inside the URL path, structured output |
| **C. Pydantic model as input with `Depends()`** | `/add_new1`, `/multiply`, `/square`, `/check`, `/age`, `/table`, `/profile`, `/number` | Validation rules (`ge`, `le`, `min_length`) in a reusable model |

Progression: **plain function args → typed/validated args → model-based input & output**.

## 🔍 Request lifecycle (mentally trace every endpoint with this)

```
Client (browser / curl / Swagger)
   │  GET /square/9
   ▼
FastAPI matches route  ──►  reads path/query params
   │                             │
   │                       validates types & rules (Pydantic)
   │                             │   fails → 422 Unprocessable Entity (client's mistake)
   ▼                             ▼
your function runs  ──►  returns dict / model
   │
   ▼
response_model validates & filters the output
   │   fails → 500 Internal Server Error (server's mistake)
   ▼
JSON response 200 OK
```

---

# 2. How to run & test

```bash
pip install fastapi uvicorn          # (or: pip install "fastapi[standard]")
uvicorn main:app --reload            # main = file main.py, app = the FastAPI() object
# newer alternative:  fastapi dev main.py
```

| URL | What you get |
|---|---|
| `http://127.0.0.1:8000/` | Welcome message |
| `http://127.0.0.1:8000/docs` | **Swagger UI**, interactive, auto-generated from your code, with "Try it out" |
| `http://127.0.0.1:8000/redoc` | ReDoc documentation |
| `http://127.0.0.1:8000/openapi.json` | Raw OpenAPI schema |

**Test from terminal:**

```bash
curl "http://127.0.0.1:8000/student?name=Rahul&batch=Super30&role=Student"
curl "http://127.0.0.1:8000/add/10/20"
```

**Test from Python (no server needed):**

```python
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
print(client.get("/add/10/20").json())      # {'num1': 10, 'num2': 20, 'result': 30}
```

📌 `uvicorn main:app` → **`module:variable`** (file name without `.py`, then the app object name).
🧠 **"main colon app"**: *file : object*.

---

# 3. Core Concepts

## 3.1 HTTP GET
Used to **read** data. Inputs travel in the **URL** (path + query string). No request body is expected.

## 3.2 Path parameter vs Query parameter

| | **Path parameter** | **Query parameter** |
|---|---|---|
| Looks like | `/add/10/20` | `/student?name=Rahul&batch=A` |
| Declared with | `{name}` in the route string | Just a function argument **not** in the route string |
| Identifies | *which resource* | *filters / options* |
| Required? | Always | Required unless it has a default |
| Example in file | `/square/{num1}` | `/student` |

**Detection rule (FastAPI's logic):**
> Name appears inside `{ }` in the route → **path param**. Otherwise (simple types) → **query param**.

🧠 **"Curly = Path, Question-mark = Query."** `{ }` in the decorator → Path; `?` in the URL → Query.

## 3.3 Required vs optional

```python
def f(name: str):              # required
def f(name: str = "guest"):    # optional, default "guest"
def f(name: str | None = None) # optional, may be None
def f(topic: list[str] = Query(...))   # required (the ... means "no default")
```

## 3.4 `list[str]` needs `Query(...)`
FastAPI assumes complex types (like `list`) belong in the **request body**. To read a **list from the URL**, you must say so with `Query(...)`. URL format is a **repeated key**:

```
?topic=RAG&topic=Neo4j     →   ["RAG", "Neo4j"]
```

## 3.5 Pydantic `BaseModel` & `Field`
A `BaseModel` describes data as typed fields; Pydantic **validates** it. `Field(...)` adds rules and docs:

| Field argument | Meaning | Applies to |
|---|---|---|
| `ge=` | **g**reater than or **e**qual (≥) | numbers |
| `gt=` | **g**reater **t**han (>) | numbers |
| `le=` | **l**ess than or **e**qual (≤) | numbers |
| `lt=` | **l**ess **t**han (<) | numbers |
| `min_length=` / `max_length=` | length limits | strings, lists |
| `pattern=` | regex | strings |
| `description=` | shows in Swagger docs | all |
| `default=` | default value | all |

⚠️ **`get` is NOT a valid argument.** (Your earlier version had this typo; it is now fixed.) The correct name is `ge` (fixed in your latest file, see [Section 6](#6-change-log-remaining-bugs--improvements)).

## 3.6 `Depends()` with a Pydantic model (class dependency)

```python
def square_number(data: SquareInput = Depends()):
```

- Empty `Depends()` means: *"use the type hint (`SquareInput`) as the thing to build."*
- FastAPI reads each **field of the model** (`num1`) from the **path or query** (by name), validates it against the `Field` rules, builds the model object, and hands it to your function as `data`.
- Result: **validation rules live in a reusable model**, not scattered inside the function.

Verified behaviour in this file:
- Field name **is** in the route (`/square/{num1}`) → read from the **path**.
- Field name **isn't** in the route (`/add_new1`) → read from the **query string** (`?num1=..&num2=..`).

🧠 **"Empty Depends = use my type hint as the recipe."**

## 3.7 `response_model` (output contract)
`response_model=Model` tells FastAPI: *"whatever I return must match this model; filter and document it."* You can also use a **return annotation** (`-> TableResponse`), which does the same job in modern FastAPI.

## 3.8 Status codes seen in this file

| Code | Meaning | Who's at fault | Example |
|---|---|---|---|
| **200** | OK | n/a | `/add/10/20` |
| **404** | Route not found | client | `/nope`, `/profile//5` |
| **422** | Validation failed (missing param, wrong type, rule broken) | **client** | `/square/101` |
| **500** | Unhandled server error | **server** | `/add/150/1` (see Section 6!) |

🧠 **"4xx = *you* messed up, 5xx = *we* messed up."**

---

# 4. Imports & App Object

```python
from fastapi import FastAPI,Query
from pydantic import BaseModel,Field, EmailStr, HttpUrl

app = FastAPI(title="Super30 FastAPI GET API")
```

| Item | Purpose |
|---|---|
| `FastAPI` | The main class; creating an instance gives you the web application |
| `Query` | Lets you configure query parameters, needed for `list[str]` |
| `BaseModel` | Base class for data models (Pydantic) |
| `Field` | Adds constraints/description to a model field |
| `EmailStr` | Email-validating type. ⚠️ **Imported but never used** |
| `HttpUrl` | URL-validating type. ⚠️ **Imported but never used** |
| `app = FastAPI(title=...)` | Creates the app; `title` appears in `/docs` |

📌 `EmailStr` needs an extra package: `pip install email-validator`. Importing it works, but **using** it in a model without that package raises `ImportError` (verified). Since it's unused, remove it or install the package before you use it.

📌 Later in the file there's a mid-file `from fastapi import Depends`. It works, but convention is to put **all imports at the top**:

```python
from fastapi import FastAPI, Query, Depends
```

🧠 **"Import the Four: FastAPI, Query, Depends, (Pydantic) BaseModel + Field."**

---

# 5. Endpoint-by-Endpoint

## Endpoint 1: `GET /` (welcome)

```python
@app.get("/")
def welcome():
    return {"message": "Welcome to the Super30 FastAPI "}
```

🎯 **Purpose:** Health-check / landing route. Confirms the server is running.

🔍 **How it works:**
- `@app.get("/")` → decorator: *"when a GET arrives at `/`, run the function below."*
- Function returns a Python `dict` → FastAPI converts it to **JSON** automatically.

🚀 **Usage:** `GET /` →
```json
{"message":"Welcome to the Super30 FastAPI "}
```

📌 **Noting points**
- Decorator syntax: **`@app.<http_method>("<path>")`**.
- Function name (`welcome`) doesn't affect the URL; the **path string** does. (The name becomes the operation id in docs.)
- The message has a trailing space before the closing quote (`"...FastAPI "`), which is harmless but probably unintended.

🧠 **"@app.get = *when someone GETs this path, run this function*."**

---

## Endpoint 2: `GET /student` (query params, all required)

```python
@app.get("/student")
def student_details(name: str, batch: str, role: str):
    """Return the requested student details as a JSON-serializable mapping."""
    return {"name": name, "batch": batch, "role": role}
```

🎯 **Purpose:** Simplest form of input, **query parameters** echoed back.

🔍 **How it works:**
- `name`, `batch`, `role` aren't in the route string → **query params**.
- No defaults → **all three required**.
- Type hint `str` → FastAPI validates/converts.
- The triple-quoted string is a **docstring**; FastAPI shows it as the endpoint description in `/docs`.

🚀 **Usage**
```
GET /student?name=Rahul&batch=Super30&role=Student
→ {"name":"Rahul","batch":"Super30","role":"Student"}
```
Missing params:
```
GET /student?name=Rahul
→ 422 {"detail":[{"type":"missing","loc":["query","batch"],"msg":"Field required"...},
                  {"type":"missing","loc":["query","role"],...}]}
```

📌 **Noting points**
- Each missing param is reported separately in the 422 `detail` list (`loc` says *where* and *which*).
- Query order doesn't matter.
- Make optional with `role: str = "Student"`.

🧠 **"No default = must supply."**

---

## Endpoint 3: `GET /course` (query params + list)

```python
@app.get("/course")
def course_details(
    course_name: str,
    Mentor: str,
    course_duration: str,
    topic: list[str] = Query(...)
):
    return {"course_name": course_name, "Mentor": Mentor,
            "course_duration": course_duration, "topics": topic}
```

🎯 **Purpose:** Shows how to accept **multiple values for one parameter** (a list) alongside normal params.

🔍 **How it works:**
- `topic: list[str] = Query(...)` → read a **list** from the query string; `...` = **required**.
- The URL repeats the key: `topic=RAG&topic=Neo4j`.
- Note the JSON key changes from `topic` (input) to `topics` (output), because you wrote it that way.

🚀 **Usage**
```
GET /course?course_name=AI&Mentor=Sudh&course_duration=3m&topic=RAG&topic=Neo4j
→ {"course_name":"AI","Mentor":"Sudh","course_duration":"3m","topics":["RAG","Neo4j"]}
```

⚠️ **Gotcha: `Mentor` is capitalized.** Parameter names are **case-sensitive**:
```
GET /course?...&mentor=Sudh...   → 422  (loc: ["query","Mentor"] "Field required")   ← verified
```
Prefer lowercase `mentor` (Python naming convention), and it avoids client mistakes.

📌 **Noting points**
- Python rule: params **without** defaults must come **before** params with defaults. `topic` has a (Query) default, so it correctly comes last.
- If the client sends only one `topic`, you still get a list with one item.
- Without `Query(...)`, FastAPI would treat `list[str]` as a **request body** (wrong for GET).

🧠 **"List in URL = Query + repeat the key."** (`Query(...)` — *three dots = required*.)

---

## Endpoint 4: `GET /skills` (list only)

```python
@app.get("/skills")
def get_skills(skill: list[str] = Query(...)):
    return {"skills": skill}
```

🎯 **Purpose:** Minimal example isolating the **list query parameter**.

🚀 **Usage**
```
GET /skills?skill=Python&skill=SQL   → {"skills":["Python","SQL"]}
GET /skills                          → 422 (skill required)
```

📌 Make it optional: `skill: list[str] = Query(default=[])` or `Query(None)`.
📌 Docstring says "mapping"; it does return a dict, so it's fine.

🧠 **"Same key, many values."**

---

## Endpoint 5: `GET /add/{num1}/{num2}` (path params + response model)

```python
class addition(BaseModel):
    num1: int = Field(ge=0, le=100, description="First number to add")
    num2: int = Field(ge=0, le=100, description="Second number to add")
    result: int = Field(ge=0, le=200, description="Result of addition")


@app.get("/add/{num1}/{num2}", response_model=addition)
def add_numbers(num1: int, num2: int):
    return addition(num1=num1, num2=num2, result=num1 + num2)
```

🎯 **Purpose:** Introduce **path parameters** and a **structured response** (`response_model`).

🔍 **How it works:**
1. `{num1}` and `{num2}` in the route → function args with the **same names** are path params.
2. `int` type → `"10"` in the URL is converted to `10`; `"abc"` → 422.
3. The function builds an `addition` object (num1, num2, result) and returns it.
4. `response_model=addition` validates and documents the output shape.

🚀 **Usage** (verified)
```
GET /add/10/20   → 200 {"num1":10,"num2":20,"result":30}
GET /add/abc/1   → 422 (int_parsing error, loc: ["path","num1"])
```

⚠️ **Verified problem: out-of-range input gives 500, not 422** (this got *wider* after the `ge` fix):
```
GET /add/150/1   → 500 Internal Server Error    ← should be a 422
GET /add/-5/3    → 500 Internal Server Error    ← should be a 422 (was 200 before the typo fix)
```
- **Why:** the function args are plain `int` (no limits), so FastAPI happily accepts `150` and `-5`. Then **your own code** builds `addition(num1=150, ...)`; the model's rules (`le=100`, and now the working `ge=0`) reject it **inside your function** → an unhandled `ValidationError` → **500**.
- **What the `ge` fix changed:** before, the broken `get=0` meant negatives *slipped through* (200 with a wrong-but-accepted result). Now the rule is real, but it fires *after* the request was accepted, so negatives **crash with 500**. The typo fix was correct; the endpoint just needs its limits on the **inputs** too (see Section 6, Issue A).
- Rules on a *response model* only kick in on output, which is a server-side failure.

📌 **Noting points**
- Constraints on a model do **not** protect the endpoint's *inputs* unless the model is the input (via `Depends()`) or you use `Path(...)`. (Fix in [Section 6](#6-change-log-remaining-bugs--improvements).)
- Class named `addition` (lowercase). PEP 8 says classes use **PascalCase** → `Addition`.

🧠 **"Path in `{}` → same name in function."** and **"Limits belong on the way IN, not only on the way OUT."**

---

## Endpoint 6: `GET /add_new/{num1}/{num2}` (slimmer response)

```python
class result_new(BaseModel):
    result: int = Field(ge=0, le=20000, description="Result of arthmetic operation")

class add_numbers_query(BaseModel):
    num1: int = Field(ge=0, le=100, description="First number to add")
    num2: int = Field(ge=0, le=100, description="Second number to add")

@app.get("/add_new/{num1}/{num2}", response_model=result_new)
def add_numbers_new(num1: int, num2: int):
    return result_new(result=num1 + num2)
```

🎯 **Purpose:** Same addition, but the response contains **only `result`**, and `result_new` is a **reusable response model** (used again by `/add_new1` and `/multiply`).

🔍 **How it works:** Path params `num1`, `num2` (plain ints) → returns `result_new(result=sum)`.

🚀 **Usage** (verified)
```
GET /add_new/10/20      → 200 {"result":30}
GET /add_new/-5/3       → 500 Internal Server Error   (result -2 < ge=0; was 200 before the typo fix)
GET /add_new/20000/5    → 500 Internal Server Error   (result 20005 > le=20000)
```

📌 **Noting points**
- `add_numbers_query` is defined **here but not used by this endpoint**; it's used in the *next* one.
- "arthmetic" is a typo of "arithmetic" (only in the description text shown in docs).
- Path params accept any int here (no bound), so huge **or negative** results reach your function and blow up the response model (500). Now that `ge=0` works, `result_new` also rejects any negative sum, so e.g. `/add_new/-5/3` crashes.

🧠 **"Response model = output bouncer."** Bad output → 500 (the server's fault).

---

## Endpoint 7: `GET /add_new1` (**first `Depends()` use**, query params from a model)

```python
from fastapi import  Depends

@app.get("/add_new1", response_model=result_new)
def add_numbers_new1( numbers: add_numbers_query = Depends()):
    return result_new(result=numbers.num1 + numbers.num2)
```

🎯 **Purpose:** Show the **model-as-input** pattern. The `add_numbers_query` model **declares the input fields and rules**; the function just uses them.

🔍 **How it works:**
1. `Depends()` + type hint `add_numbers_query` → FastAPI reads `num1`, `num2` from the request.
2. The route has **no `{}`**, so they come from the **query string**.
3. Values are validated (`le=100` works ✔), then the model object arrives as `numbers`.
4. You access fields as `numbers.num1`, `numbers.num2` (attribute access, not `["num1"]`).

🚀 **Usage** (verified)
```
GET /add_new1?num1=10&num2=20    → 200 {"result":30}
GET /add_new1?num1=150&num2=1    → 422 "Input should be less than or equal to 100" (loc: query,num1)
GET /add_new1?num1=1             → 422 num2 missing
GET /add_new1?num1=-5&num2=1     → 422 "Input should be greater than or equal to 0" (loc: query,num1)   ← fixed by `ge`
```

📌 **Noting points**
- This is **the right way** to get 422 (client error) for out-of-range input, unlike `/add` and `/add_new`. **Both** bounds (`ge=0` and `le=100`) now work here.
- Swagger `/docs` shows `num1`, `num2` as query inputs with descriptions from `Field(description=...)`.
- Import placed mid-file: works, but move to the top.

🧠 **"Model = form; Depends() = hand me the filled-in form."**

---

## Endpoint 8: `GET /multiply/{num1}/{num2}` (`Depends()` reading from the **path**)

```python
class multiply(BaseModel):
    num1: int = Field(ge=0, le=100, description="First number to multiply")
    num2: int = Field(ge=0, le=100, description="Second number to multiply")

@app.get("/multiply/{num1}/{num2}")
def multiply_numbers(numbers : multiply = Depends()):
    return result_new(result=numbers.num1 * numbers.num2)
```

🎯 **Purpose:** Same `Depends()` pattern, but now the route **has** `{num1}` `{num2}`, so the model's fields are read from the **path**.

🔍 **How it works:** Field names (`num1`, `num2`) match the `{}` names in the route → path params → validated by the model → product returned in `result_new`.

🚀 **Usage** (verified)
```
GET /multiply/5/6      → 200 {"result":30}
GET /multiply/500/6    → 422 (le=100, loc: path,num1)
GET /multiply/-1/6     → 422 "Input should be greater than or equal to 0" (loc: path,num1)   ← fixed by `ge`
```

📌 **Noting points**
- **Key learning:** the same model works for path *or* query; **the route string decides**.
- No `response_model=` on the decorator here, but it still returns JSON fine; add `response_model=result_new` for consistent docs.
- Max product 100×100 = 10 000 ≤ 20 000 → `result_new`'s limit is never hit.
- Class `multiply` vs function `multiply_numbers`. Similar names are confusing; use `MultiplyInput`.

🧠 **"Same model, different address: route has `{}` → Path, else → Query."**

---

## Endpoint 9: `GET /square/{num1}`

```python
class SquareInput(BaseModel):
    num1: int = Field(ge=0, le=100, description="Number to square")

class SquareResponse(BaseModel):
    number: int
    square: int

@app.get("/square/{num1}", response_model=SquareResponse)
def square_number( data: SquareInput = Depends() ):
    return SquareResponse(number=data.num1, square=data.num1 ** 2)
```

🎯 **Purpose:** The **clean, correct pattern**: separate **Input model** (validation) and **Response model** (output shape).

🔍 **How it works:** `num1` from the path → validated `0 ≤ num1 ≤ 100` (correct `ge`!) → `** 2` (exponent) → returns `{number, square}`.

🚀 **Usage** (verified)
```
GET /square/9     → 200 {"number":9,"square":81}
GET /square/101   → 422 "less than or equal to 100"
GET /square/-1    → 422 "greater than or equal to 0"     ← `ge` enforced (this model was always spelled correctly)
```

📌 **Noting points**
- `**` is the power operator (`5 ** 2 = 25`). `^` in Python is XOR, **not** power.
- Naming: `XxxInput` / `XxxResponse` = the convention to follow throughout.
- Field name differs between input (`num1`) and output (`number`); this is fine, they are different models.

🧠 **"Two models per endpoint: one for coming IN, one for going OUT."**

---

## Endpoint 10: `GET /check/{num1}` (even / odd)

```python
class EvenoddInput(BaseModel):
    num1: int = Field(ge=0, le=100, description="Number to find even or odd")

class EvenoddResponse(BaseModel):
    number: int
    type: str

@app.get("/check/{num1}", response_model=EvenoddResponse)
def even_odd_number(data: EvenoddInput = Depends()):
    if data.num1 % 2 == 0:
        return EvenoddResponse(number=data.num1, type="Even")
    else:
        return EvenoddResponse(number=data.num1, type="Odd")
```

🎯 **Purpose:** Add **conditional logic (if/else)** inside an endpoint.

🔍 **How it works:** `%` is modulo (remainder). Remainder 0 when divided by 2 → even; otherwise odd.

🚀 **Usage** (verified)
```
GET /check/4   → {"number":4,"type":"Even"}
GET /check/7   → {"number":7,"type":"Odd"}
```

📌 **Noting points**
- A field named `type` shadows Python's built-in `type` *inside the class body only*; legal and common in APIs, but a name like `parity` avoids confusion.
- Shorter equivalent: `type="Even" if data.num1 % 2 == 0 else "Odd"`.

🧠 **"Remainder zero after ÷2 → Even."**

---

## Endpoint 11: `GET /age/{num1}` (child / adult / senior)

```python
class AgeInput(BaseModel):
    num1: int = Field(ge=0, le=100, description="Number to find adult or child or senior citizen")

class AgeResponse(BaseModel):
    age: int
    message: str

@app.get("/age/{num1}", response_model=AgeResponse)
def check_age(data: AgeInput = Depends()):
    if data.num1 < 18:
        return AgeResponse(age=data.num1, message="Child")
    elif data.num1 < 60:
        return AgeResponse(age=data.num1, message="Adult")
    else:
        return AgeResponse(age=data.num1, message="Senior Citizen")
```

🎯 **Purpose:** **if / elif / else** with three categories.

🔍 **How it works (thresholds):**

| Age | Message |
|---|---|
| 0 – 17 | Child |
| 18 – 59 | Adult |
| 60 – 100 | Senior Citizen |

🚀 **Usage** (verified): `/age/10` → Child · `/age/30` → Adult · `/age/70` → Senior Citizen · `/age/101` → 422.

📌 **Noting points**
- `elif data.num1 < 60` only runs if the first check failed, so it means "18 to 59".
- The field is called `num1` although it holds an age; rename to `age` for clarity (route `/age/{age}`).
- The description text says "Number to find adult or child…" but the value is an age.

🧠 **"18 and 60: kid < 18 ≤ adult < 60 ≤ senior."**

---

## Endpoint 12: `GET /table/{num1}` (multiplication table)

```python
class TableInput(BaseModel):
    num1: int = Field(ge=0, le=100, description="Number to find multiplication table")

class TableResponse(BaseModel):
    number: int
    table: list[str]

@app.get("/table/{num1}", response_model=TableResponse)
def multiplication_table(data: TableInput = Depends()) -> TableResponse:
    table = [f"{data.num1} x {i} = {data.num1 * i}" for i in range(1, 11)]
    return TableResponse(number=data.num1, table=table)
```

🎯 **Purpose:** Return a **list in the response**; introduces **list comprehension**, **f-strings**, and a **return type annotation**.

🔍 **How it works:**
- `range(1, 11)` → 1…10 (end is **exclusive**).
- f-string `f"{a} x {i} = {a*i}"` embeds expressions.
- List comprehension builds 10 strings in one line.
- `-> TableResponse` = return annotation (FastAPI also uses it as the response model).

🚀 **Usage** (verified)
```
GET /table/3 → {"number":3,"table":["3 x 1 = 3","3 x 2 = 6", ... ,"3 x 10 = 30"]}
```

📌 **Noting points**
- Response field type `list[str]` → a JSON array of strings.
- Here both `response_model=` and `->` are given; only one is needed.
- Equivalent loop form: `table=[]; for i in range(1,11): table.append(...)`.

🧠 **"range(1, 11) gives 1 to 10: the stop is a *closed door*."**

---

## Endpoint 13: `GET /profile/{name}/{age}` (string + number path params)

```python
class ProfileInput(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Person name")
    age: int = Field(ge=1, le=100, description="Person age")

class ProfileResponse(BaseModel):
    name: str
    age: int

@app.get("/profile/{name}/{age}", response_model=ProfileResponse)
def profile_details(data: ProfileInput = Depends()) -> ProfileResponse:
    return ProfileResponse(name=data.name, age=data.age)
```

🎯 **Purpose:** Mix **different types** (str + int) with **different rules** (`min_length`/`max_length` for strings, `ge`/`le` for numbers).

🚀 **Usage** (verified)
```
GET /profile/Rahul/24    → {"name":"Rahul","age":24}
GET /profile/Rahul/0     → 422 (age ≥ 1)
GET /profile/Rahul/200   → 422 (age ≤ 100)
GET /profile//5          → 404  (empty path segment never matches the route)
GET /profile/%20/5       → 200  {"name":" ","age":5}   ← a single space passes min_length=1
```

📌 **Noting points**
- `%20` = URL-encoded space. Use `%20` for spaces in URLs: `/profile/Rahul%20Kumar/24`.
- `min_length=1` counts a space as a character, so it isn't a "not blank" check. To reject blanks use `pattern=r"\S"` or strip in a validator.
- Path parameters can't contain `/` unless you use the `{name:path}` converter.
- For real profile data you'd use **POST + JSON body**, not GET with names in the URL.

🧠 **"Strings get *length* rules, numbers get *size* rules."** (`min_length/max_length` vs `ge/le`)

---

## Endpoint 14: `GET /number/{number}` (multi-output analysis)

```python
class NumberInput(BaseModel):
    number: int = Field(ge=0, le=1000, description="Number to analyze")

class NumberResponse(BaseModel):
    number: int
    square: int
    cube: int
    even: bool

@app.get("/number/{number}", response_model=NumberResponse)
def number_analysis(data: NumberInput = Depends()) -> NumberResponse:
    return NumberResponse(
        number=data.number,
        square=data.number ** 2,
        cube=data.number ** 3,
        even=data.number % 2 == 0
    )
```

🎯 **Purpose:** Combine everything: one input → **several computed outputs** including a **boolean**.

🔍 **How it works:** `** 2` square, `** 3` cube, `% 2 == 0` gives `True/False` directly (no if/else needed).

🚀 **Usage** (verified)
```
GET /number/12    → {"number":12,"square":144,"cube":1728,"even":true}
GET /number/1001  → 422 (le=1000)
```

📌 **Noting points**
- JSON booleans are lowercase (`true`), Python's are `True`, and FastAPI converts automatically.
- Path param name = model field name = `number`. That's why `{number}` in the route matches.
- Range up to 1000 keeps cube ≤ 1 000 000 000; Python ints can't overflow anyway.

🧠 **"Boolean shortcut: the comparison *is* the answer."** (`even = n % 2 == 0`)

---

# 6. Change Log, Remaining Bugs & Improvements

All behaviour below was confirmed by running your **updated** `main.py`.

## ✅ What you fixed: `get=0` → `ge=0` (8 places)

```python
num1: int = Field(get=0, le=100, ...)     # ❌ old
num1: int = Field(ge=0,  le=100, ...)     # ✅ now
```
Result of the fix (verified):
- The Pydantic `PydanticDeprecatedSince20` warnings at startup are **gone** (importing the file with warnings-as-errors now succeeds).
- The `Depends()`-based endpoints now enforce **both** bounds, so negatives get a proper **422**:

| Request | Before fix | After fix |
|---|---|---|
| `/add_new1?num1=-5&num2=1` | 200 `{"result":-4}` | **422** (`ge=0`) |
| `/multiply/-1/6` | 200 `{"result":-6}` | **422** (`ge=0`) |

🧠 **`ge` = "Greater-or-Equal", not the HTTP verb GET.**

## ⚠️ Side-effect to understand: the fix exposed a **500** on two endpoints

| Request | Before fix | After fix |
|---|---|---|
| `/add/-5/3` | 200 `{"num1":-5,"num2":3,"result":-2}` | **500** |
| `/add_new/-5/3` | 200 `{"result":-2}` | **500** |
| `/add/150/1` | 500 | 500 (unchanged) |
| `/add_new/20000/5` | 500 | 500 (unchanged) |

**Why:** these two routes take plain `int` path params, so the bad value reaches your function, and the (now working) model rules raise a `ValidationError` inside your code. **Lesson: the typo was hiding a design problem.** Model limits only protect the *output* there.

## 🐞 Issue A (still open): `/add/{num1}/{num2}` and `/add_new/{num1}/{num2}` return 500 for invalid numbers

**Fix:** put the limits on the inputs so FastAPI answers **422**:

```python
from typing import Annotated
from fastapi import FastAPI, Path

@app.get("/add/{num1}/{num2}", response_model=addition)
def add_numbers(
    num1: Annotated[int, Path(ge=0, le=100)],
    num2: Annotated[int, Path(ge=0, le=100)],
):
    return addition(num1=num1, num2=num2, result=num1 + num2)
```
Verified: `/add/10/20` → 200 · `/add/150/1` → **422** · `/add/-5/3` → **422**.

For `/add_new/...`, either do the same, or switch it to the `Depends()` style already used by `/add_new1` / `/multiply`.

## ⚠️ Issue B (still open): Unused imports
`EmailStr`, `HttpUrl` are never used, and `EmailStr` needs `email-validator` if you *do* use it. Remove them or use them, e.g.:

```python
class Contact(BaseModel):
    email: EmailStr          # pip install email-validator
    website: HttpUrl
```

## ⚠️ Issue C (still open): Import in the middle of the file
`from fastapi import Depends` → move to the top: `from fastapi import FastAPI, Query, Depends`.

## ⚠️ Issue D (still open): Naming conventions (PEP 8)

| Current | Better |
|---|---|
| `class addition` | `class Addition` |
| `class multiply` | `class MultiplyInput` |
| `class result_new` | `class ResultResponse` |
| `class add_numbers_query` | `class AddInput` |
| `Mentor` (param) | `mentor` |
| `/add_new`, `/add_new1` | clearer distinct names (e.g. `/add-v2`, `/add-query`) |

## ⚠️ Issue E (still open): Duplicate model definitions
`addition`, `add_numbers_query`, `multiply` all repeat the same `num1/num2` fields. One shared model works for all:

```python
class TwoNumbers(BaseModel):
    num1: int = Field(ge=0, le=100, description="First number")
    num2: int = Field(ge=0, le=100, description="Second number")

class Addition(TwoNumbers):          # inheritance: adds `result`
    result: int = Field(ge=0, le=200)

class ResultOut(BaseModel):
    result: int

@app.get("/multiply/{num1}/{num2}", response_model=ResultOut)
def multiply_numbers(numbers: Annotated[TwoNumbers, Depends()]):
    return ResultOut(result=numbers.num1 * numbers.num2)
```
Verified: `/multiply/5/6` → `{"result":30}`, `/multiply/-1/6` → 422, `/multiply/500/6` → 422.

## ⚠️ Issue F (still open): `Mentor` capitalized
`/course` requires `Mentor` exactly; `?mentor=...` → 422 (verified again). Prefer lowercase.

## ⚠️ Issue G (still open): Minor text polish
- Welcome message has a trailing space (`"...FastAPI "`).
- `"arthmetic"` → `"arithmetic"`.
- `AgeInput.num1` holds an *age*; name it `age`.
- `/profile/{name}/{age}` accepts a single space as a name (`min_length=1` counts spaces).

## 💡 Bonus improvements
- Add `tags=["Math"]` to group endpoints in `/docs`.
- Split into routers (`APIRouter`) as the file grows.
- Use `POST` + request body for creating/sending real data (profiles, courses).

---

# 7. Syntax Cheat Sheet

```python
# App
app = FastAPI(title="My API", version="1.0")

# Route decorators (one per HTTP verb)
@app.get("/path")       # read
@app.post("/path")      # create
@app.put("/path")       # replace
@app.patch("/path")     # partial update
@app.delete("/path")    # delete

# Parameters
def f(name: str)                                # required query param
def f(name: str = "guest")                      # optional query param
def f(tags: list[str] = Query(...))             # required list  (?tags=a&tags=b)
@app.get("/u/{uid}") def f(uid: int)            # path param
def f(n: Annotated[int, Path(ge=0, le=100)])    # path param + validation
def f(q: Annotated[str, Query(min_length=2)])   # query param + validation

# Models
class M(BaseModel):
    x: int = Field(ge=0, le=100, description="...")   # ge/gt/le/lt
    s: str = Field(min_length=1, max_length=50)        # string length
    ok: bool
    items: list[str]

# Model as input (fields read from path/query by name)
def f(data: M = Depends()): ...
def f(data: Annotated[M, Depends()]): ...          # modern style

# Output
@app.get("/x", response_model=Out)                 # or:  def f() -> Out:

# Run
uvicorn main:app --reload
```

**Python refreshers used in the file**

| Syntax | Meaning | Example |
|---|---|---|
| `**` | power | `9 ** 2 = 81` |
| `%` | remainder | `7 % 2 = 1` |
| `f"{x}"` | f-string | `f"{n} x {i} = {n*i}"` |
| `[expr for i in range(1, 11)]` | list comprehension | builds the table |
| `x if cond else y` | ternary | shorter even/odd |
| `-> Type` | return annotation | `-> TableResponse` |
| `"""text"""` | docstring | shown in Swagger |

---

# 8. Memory Tricks (Master List)

| # | Concept | 🧠 Trick |
|---|---|---|
| 1 | Decorator | **"@app.METHOD(PATH): when someone METHODs PATH, run me."** |
| 2 | Path vs Query | **"Curly = Path, Question mark = Query."** |
| 3 | Path meaning | Path = *Place* (which item). Query = *Qualifier* (filters/options) |
| 4 | Required | **"No default = must supply."** `Query(...)` → three dots = required |
| 5 | List in URL | **"Same key, many values"**: `?topic=a&topic=b`, and lists need `Query` |
| 6 | `ge / le` | **G**reater-**E**qual, **L**ess-**E**qual. **Never `get`!** (`gt/lt` = strict) |
| 7 | String vs number rules | Strings → **length** rules · Numbers → **size** rules |
| 8 | `Depends()` | **"Empty Depends = use my type hint as the recipe."** |
| 9 | Model source | Route has `{}` → Path · No `{}` → Query |
| 10 | Two models | **"One model IN, one model OUT."** (`XxxInput` / `XxxResponse`) |
| 11 | Status codes | **4xx = you messed up (422), 5xx = we messed up (500)** |
| 12 | 422 vs 500 | Validating **requests** → 422 · Failing to build the **response** → 500 |
| 13 | `response_model` | **Output bouncer**, only valid data leaves |
| 14 | `range(1, 11)` | Stop is a **closed door** → 1…10 |
| 15 | `**` vs `^` | `**` = power, `^` = XOR (trap!) |
| 16 | `%` | Remainder; `% 2 == 0` → even |
| 17 | Run command | **"module : app"** → `uvicorn main:app` |
| 18 | Docs | **`/docs`** = *"Docs, Try it out!"*, free interactive tester |
| 19 | Debug 422 | Read `loc` (where), `msg` (why), `type` (what kind) |
| 20 | Whole flow | **Route → Validate → Run → Validate output → JSON** |

**One-sentence master recap:**
> *"Pick a verb + path, declare inputs as typed function args or a `Depends()` model with `ge/le` rules, return a response model, and FastAPI validates both ends and writes the docs for you."*

---

# 9. Endpoint Summary Table

| # | Route | Input source | Input model? | Output | Notable behaviour (tested) |
|---|---|---|---|---|---|
| 1 | `/` | none | – | dict | 200 |
| 2 | `/student` | query ×3 | – | dict | 422 if any missing |
| 3 | `/course` | query ×3 + list `topic` | – | dict | `Mentor` case-sensitive |
| 4 | `/skills` | query list | – | dict | list needs `Query(...)` |
| 5 | `/add/{num1}/{num2}` | path | ❌ (plain ints) | `addition` | 150 → **500**, −5 → **500** (should be 422) |
| 6 | `/add_new/{num1}/{num2}` | path | ❌ | `result_new` | 20000+5 → **500**, −5+3 → **500** |
| 7 | `/add_new1` | query | `add_numbers_query` | `result_new` | 150 → 422 ✔, −5 → 422 ✔ |
| 8 | `/multiply/{num1}/{num2}` | path | `multiply` | `result_new` | 500 → 422 ✔, −1 → 422 ✔ |
| 9 | `/square/{num1}` | path | `SquareInput` | `SquareResponse` | 0–100 enforced ✔ |
| 10 | `/check/{num1}` | path | `EvenoddInput` | `EvenoddResponse` | Even/Odd |
| 11 | `/age/{num1}` | path | `AgeInput` | `AgeResponse` | Child/Adult/Senior |
| 12 | `/table/{num1}` | path | `TableInput` | `TableResponse` | list of 10 strings |
| 13 | `/profile/{name}/{age}` | path | `ProfileInput` | `ProfileResponse` | age 1–100; `" "` passes name |
| 14 | `/number/{number}` | path | `NumberInput` | `NumberResponse` | square, cube, even; ≤ 1000 |

---

# 10. Interview Q&A

**Q1. What is FastAPI and why use it?**
A modern Python web framework built on Starlette + Pydantic. It gives high performance, automatic validation from type hints, and auto-generated interactive docs (`/docs`).

**Q2. Path vs query parameters?**
Path params are part of the URL path and identify a resource (`/users/5`). Query params come after `?` and filter/option the request (`/users?role=admin`). In FastAPI, a name inside `{}` in the route is a path param; other simple-typed args are query params.

**Q3. What happens when validation fails?**
FastAPI returns **422 Unprocessable Entity** with a `detail` list describing `loc`, `msg`, and `type` for each error.

**Q4. Why `Query(...)` for `list[str]`?**
FastAPI treats complex types as request-body by default. `Query(...)` says "read this from the query string" (and `...` = required).

**Q5. What does `Depends()` with a Pydantic model do?**
FastAPI builds the model from path/query values by field name, validates them, and injects the object into the function. It centralizes validation rules.

**Q6. `response_model` purpose?**
Validates and filters the outgoing data, and documents the response schema in OpenAPI.

**Q7. 422 vs 500?**
422 = the client sent invalid input (caught by FastAPI). 500 = the server hit an unhandled error (e.g., your code raised, or the response failed validation).

**Q8. Difference between `ge` and `gt`?**
`ge` ≥ (inclusive), `gt` > (strict). Same for `le` / `lt`.

**Q9. Why does `/add/150/1` (and `/add/-5/3`) give a 500 in this project?**
The function args are plain ints (no limits), so the values are accepted; the response model's `le=100` / `ge=0` then fail inside your own code, causing an unhandled `ValidationError`. Fix: `Path(ge=0, le=100)` on the inputs so FastAPI returns 422.

**Q10. What happens if you write `Field(get=0)` instead of `Field(ge=0)`?**
`get` isn't a real constraint. Pydantic v2 treats it as a deprecated extra keyword (prints a warning) and **enforces nothing**, so negatives were accepted. After correcting it to `ge`, the bound is enforced. Note that on endpoints without input validation, this can turn "accepted" into a 500.

**Q11. How do you run a FastAPI app?**
`uvicorn main:app --reload` (or `fastapi dev main.py`).

**Q12. Why prefer POST + body over GET for profile data?**
GET puts data in the URL (logged, cached, length-limited, visible in history). POST with a JSON body is better for structured or sensitive data.

**Q13. Sync `def` vs `async def` endpoints?**
Both work. Use `async def` when awaiting async I/O (DB/HTTP clients); plain `def` runs in a thread pool. This file uses `def` throughout, which is fine for pure computation.

---

# 11. Practice Exercises

1. ✅ *(Done in your latest file)* You fixed `get=0` → `ge=0`. Now confirm `/add_new1?num1=-5&num2=1` returns 422 while `/add/-5/3` returns **500**. Explain why they differ.
2. Convert `/add` and `/add_new` to use `Path(ge=0, le=100)` so `150` gives 422, not 500.
3. Make `topic` in `/course` **optional** (default empty list).
4. Add `GET /divide/{a}/{b}` returning `a / b`; return **400** with a clear message when `b == 0` (`raise HTTPException(status_code=400, detail="Division by zero")`).
5. Add `GET /factorial/{n}` with `n` from 0 to 20.
6. Add `GET /prime/{n}` returning `{"number": n, "is_prime": true/false}`.
7. Add `GET /search?q=...&limit=10` with `q` (min length 2) and optional `limit` (1–50, default 10).
8. Add `tags=["Math"]` to all math endpoints and `tags=["Info"]` to `/student`, `/course`, `/skills`; observe `/docs`.
9. Use `EmailStr` in a model for `GET /contact?email=...&website=...` (install `email-validator`).
10. Write a `pytest` file using `TestClient` that checks 200 and 422 cases for `/square`.

<details>
<summary>Answers (selected)</summary>

```python
# 3. optional list
topic: list[str] = Query(default=[])

# 4. divide
from fastapi import HTTPException
@app.get("/divide/{a}/{b}")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": a / b}

# 5. factorial
import math
@app.get("/factorial/{n}")
def factorial(n: Annotated[int, Path(ge=0, le=20)]):
    return {"n": n, "factorial": math.factorial(n)}

# 6. prime
@app.get("/prime/{n}")
def prime(n: Annotated[int, Path(ge=0, le=1_000_000)]):
    is_prime = n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))
    return {"number": n, "is_prime": is_prime}

# 7. search
@app.get("/search")
def search(q: Annotated[str, Query(min_length=2)],
           limit: Annotated[int, Query(ge=1, le=50)] = 10):
    return {"q": q, "limit": limit}

# 10. test
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_square_ok():
    r = client.get("/square/9")
    assert r.status_code == 200 and r.json() == {"number": 9, "square": 81}

def test_square_out_of_range():
    assert client.get("/square/101").status_code == 422
```
</details>

---

### ✅ Final revision checklist

- [ ] I can explain the request → validate → run → response flow
- [ ] I can tell path params from query params by looking at the route string
- [ ] I know why `list[str]` needs `Query(...)`
- [ ] I know `ge/gt/le/lt`, `min_length/max_length`, and that `get` is not a valid argument (`ge` is)
- [ ] I can explain what empty `Depends()` on a Pydantic model does
- [ ] I know why 422 (client) differs from 500 (server) and how `/add/150/1` and `/add/-5/3` give 500
- [ ] I can write Input + Response models for a new endpoint
- [ ] I can run the app and test in `/docs`, curl, and `TestClient`
