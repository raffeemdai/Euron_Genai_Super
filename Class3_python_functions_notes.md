# Python Functions — Class Notes

*Based on the live session covering functions in Python: definitions, return vs print, arguments, `*args`/`**kwargs`, `map`, `lambda`, decorators, and recursion.*

*Code below is taken directly from the class notebook (`functioninpython.ipynb`), matched with the instructor's spoken explanation from the transcript.*

---

## 1. What Is a Function?

A function is a reusable block of code that takes some **input**, performs a **computation**, and gives back some **output**.

You've already been using **built-in functions** like `print()`, `type()`, `len()`, `sum()` — someone else wrote these, you just consume them. Now we learn to write our **own** functions.

**Why use functions?**
- Reusability — write once, use many times
- Modularity — organize code into logical units
- Readability — named blocks are easier to understand than repeated code

---

## 2. Defining a Function

Use the reserved keyword **`def`**:

```python
def test():
    pass
```

- `def` — declares that a function is being created
- `test` — the function name (can be almost anything)
- `()` — parentheses, used later to accept arguments
- `:` — starts the function body (indented block)
- `pass` — a reserved keyword meaning "do nothing here." Useful as a placeholder anywhere a body is required (functions, loops, `if`, classes) but you don't want to write one yet.

### A simple function

```python
def test1():
    print(2)

test1()
test1()
```
Calling it prints `2` each time — and you can call it as many times as you like, that's reusability in action.

---

## 3. `print()` vs `return` — A Critical Distinction

```python
def test1():
    print(2)

a = test1()      # prints 2, but 'a' captures the RETURN value, not the printed value
type(a)           # -> <class 'NoneType'>
```

- `print()` displays something on screen but its **return value is always `None`**.
- If you try to use that `None` value further (e.g., concatenate or add to it), Python raises an error, because `None` isn't compatible with strings or numbers in arithmetic/concatenation.

```python
a + "sudh"    # TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'

b = test1()
b + 6          # TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

**Rule of thumb:** Don't rely on `print()` as your function's "final value." Use **`return`** instead.

```python
def test2():
    return "sudh"

test2()             # -> 'sudh'
type(test2())        # -> <class 'str'>
test2() + "kumar"    # -> 'sudhkumar'  (concatenation works fine)
```

`return` sends a value back out of the function so it can be captured in a variable and used in further operations. Python automatically figures out the data type of whatever you return.

### Returning multiple values

You can return more than one value — Python packs them into a **tuple**:

```python
def test3():
    return "sudh", [3, 4, 5, 6], (3, 4, 5), {3, 4, 5}, {"key1": "sudh", "key2": "kumar"}

test3()
# -> ('sudh', [3, 4, 5, 6], (3, 4, 5), {3, 4, 5}, {'key1': 'sudh', 'key2': 'kumar'})

a, b, c, d, e = test3()
a   # -> 'sudh'
b   # -> [3, 4, 5, 6]
```

Here `a` unpacks to the string, `b` to the list, `c` to the tuple, `d` to the set, and `e` to the dictionary — all in one return statement.

---

## 4. Parameters and Arguments

A function can accept input via **parameters**:

```python
def test4(a):
    return a + 5

test4(4)   # -> 9
test4()    # TypeError: test4() missing 1 required positional argument: 'a'
```

If you call the function without supplying a required parameter, Python raises a `TypeError` telling you exactly which argument is missing.

### Arithmetic examples

```python
def add(a, b):
    return a + b

add(4, 5)        # -> 9

def subtract(a, b):
    return a - b

subtract(4, 5)   # -> -1

def multiply(a, b):
    return a * b

multiply(4, 5)   # -> 20
```

### A slightly bigger example — filter even/odd from a list

```python
def filter_list(l):
    even = []
    odd = []
    for i in l:
        if i % 2 == 0:
            even.append(i)
        else:
            odd.append(i)
    return even, odd

filter_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# -> ([2, 4, 6, 8, 10], [1, 3, 5, 7, 9])
```

---

## 5. Documenting Functions — Type Hints & Docstrings

You can "decorate" a function definition with **notes for the user** (these are hints, not enforced type checks!):

```python
def filter_list(l: list) -> tuple[list, list]:
    """Filters a list of integers into even and odd numbers.
    So this function always tries to take a list. And it
    And by taking a list, it will be able to process it and filter out
    Even an odd number
    """
    even = []
    odd = []
    for i in l:
        if i % 2 == 0:
            even.append(i)
        else:
            odd.append(i)
    return even, odd
```

- `l: list` — a **type hint** telling the user "I expect a list here." It is **not enforced** — Python will still let you pass a tuple or anything else; it won't fail at this line.

```python
filter_list((1, 2, 3, 4, 5, 6, 7, 8, 9, 10))   # still works even with a tuple passed in!
# -> ([2, 4, 6, 8, 10], [1, 3, 5, 7, 9])
```

- `-> tuple[list, list]` — a hint about the **return type** (a tuple containing two lists).
- `""" ... """` — a **docstring**. Hovering over the function name in an editor shows this text. It's the standard, professional way to document what a function does, what it expects, and what it returns.

**Best practice:** Always write type hints + docstrings for functions you expect others (or future-you) to use.

### Example: find the largest of three numbers

```python
def find_largest(a: int, b: int, c: int) -> int:
    """This is a function which is going to check which one is bigger out of
    these three numbers that we are going to give."""

    if a > b and a > c:
        return a
    elif b > c and b > a:
        return b
    else:
        return c

find_largest(5, 10, 3)   # -> 10
```

---

## 6. Default Argument Values

You can give a parameter a **default value** — if the caller doesn't supply it, the default is used.

First, without a default — every argument is required:

```python
def test5(a, b, c):
    return a + b + c

test5(1, 2, 3)   # -> 6
test5(1, 2)       # TypeError: missing 1 required positional argument: 'c'
```

Now with a default value for `c`:

```python
def test5(a, b, c=10):
    return a + b + c

test5(5, 6, 2)   # c overridden -> 13
```

This is exactly how many built-in functions work — e.g. `print(*objects, sep=' ', end='\n', file=None, flush=False)` has several defaulted parameters.

---

## 7. Variable-Length Arguments: `*args` and `**kwargs`

### The problem

A function with fixed parameters can't handle a variable number of inputs:

```python
def maximum(a, b, c):
    return max(a, b, c)

maximum(5, 6, 7)   # -> 7   (only works for exactly 3 arguments)
```

### `*args` — variable number of positional arguments

```python
def test7(*args):
    return args

test7()                    # -> ()
test7(2, 3, 4, 5, 6)        # -> (2, 3, 4, 5, 6)
test7(3, 4, 5)              # -> (3, 4, 5)
```

- `args` is **not a reserved keyword** — you could call it anything. The instructor demonstrated this directly in class:

```python
def test7(*sudh):     # works exactly the same as *args
    return sudh
```

- `*args` is simply the widely-used convention.
- Whatever you pass gets collected into a **tuple**.

### `**kwargs` — variable number of keyword (key=value) arguments

```python
def test8(**kwargs):
    return kwargs

test8(a=1, b="sudh", phone=234234)
# -> {'a': 1, 'b': 'sudh', 'phone': 234234}
```

- Captures inputs as key/value pairs into a **dictionary**.
- Calling it with plain positional values (no keys) will **fail** — `**kwargs` requires `key=value` form.
- `kwargs` is also just convention, not a reserved word.

### Combining fixed args, defaults, `*args`, and `**kwargs`

```python
def test9(a: int = 6, b: int = 7, *args, **kwargs):
    return a, b, args, kwargs

test9()
# -> (6, 7, (), {})   -- a and b fall back to their default values; args/kwargs are empty
```

### Passing lists via `*args`, then typecasting

```python
def test10(*args):
    return list(args)

test10([1, 3, 4, 54, 5, 6, 7, 8, 9, 0])
# -> [[1, 3, 4, 54, 5, 6, 7, 8, 9, 0]]
```

`*args` always collects into a tuple by default — here `list(args)` typecasts that tuple into a list once inside the function, in case a mutable structure is needed for further operations.

---

## 8. Functions as Arguments — `map()` and `lambda`

### Doing it manually first (for loop)

```python
l = [2, 3, 4, 5, 6, 7, 8, 9]
l_sq = []
for i in l:
    l_sq.append(i ** 2)

l_sq
# -> [4, 9, 16, 25, 36, 49, 64, 81]
```

### Wrapping that logic in a function

```python
def list_sq(l):
    l_sq = []
    for i in l:
        l_sq.append(i ** 2)
    return l_sq

list_sq(l)
# -> [4, 9, 16, 25, 36, 49, 64, 81]
```

### `map(function, iterable)`

`map` takes a **function** and an **iterable**, and applies the function to every element — same result, without writing the loop yourself.

```python
def sq(x):
    return x ** 2

list(map(sq, l))
# -> [4, 9, 16, 25, 36, 49, 64, 81]
```

Internally: `sq(2)`, `sq(3)`, `sq(4)`, ... — each element is "mapped" through the function.

### `lambda` — anonymous (nameless) functions

A `lambda` is a function with no name, written inline — handy as a quick shorthand, especially inside `map`, `filter`, `sorted`, etc.

```python
sqlambda = lambda x: x ** 2
sqlambda(5)   # -> 25
```

Using it directly inside `map`:

```python
list(map(lambda x: x ** 2, l))
# -> [4, 9, 16, 25, 36, 49, 64, 81]   -- same output as the sq() version above
```

- `lambda x: x ** 2` is equivalent to `def sq(x): return x ** 2`, just written inline.
- Using `lambda` vs. a named function is a **style choice**, not inherently "more optimized." Use whichever is clearer for the situation. For long/complex logic, a full `def` function is usually better than a lambda.

### Passing your own function as an argument (custom "map")

```python
def add(a, b):
    return a + b

def calculate(a, b, func):
    return func(a, b)

calculate(4, 5, add)   # -> 9
```

Here, `calculate` receives another function (`add`) as its third argument and calls it internally. This is the same underlying idea `map()` uses — a function accepting another function as input.

---

## 9. Decorators

**Concept:** Just like decorating a house for a festival doesn't change the house itself but adds something extra around it, a **decorator** wraps extra behavior *around* an existing function without modifying its core logic.

### A function to decorate

```python
def welcome(name):
    return "Welcome to function in python " + name

welcome("sudh")
# -> 'Welcome to function in python sudh'
```

### The problem it solves

Suppose many functions need to log their execution time:

```python
import time

def even_odd(l):
    start = time.time()
    even = []
    odd = []
    for i in l:
        if i % 2 == 0:
            even.append(i)
        else:
            odd.append(i)
    end = time.time()
    print("Time taken to execute the function is ", end - start)
    return even, odd

even_odd([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

Repeating the start/end timing logic in **every** function is redundant.

### Writing a decorator

```python
import time

def time_diff(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Time taken to execute the function is ", end - start)
        return result
    return wrapper
```

- `time_diff` takes a function `func` as input.
- Inside it, an inner **`wrapper`** function is defined — this is what actually runs before/after the original function. Using `*args, **kwargs` inside `wrapper` makes it generic, so it works no matter what arguments the decorated function needs.
- The wrapper function is **mandatory** for a custom decorator — it's what lets you inject "before" and "after" behavior around the original function call.

### Applying a decorator with `@`

```python
@time_diff
def even_odd(l):
    even = []
    odd = []
    for i in l:
        if i % 2 == 0:
            even.append(i)
        else:
            odd.append(i)
    return even, odd

even_odd([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# runs even_odd, and automatically prints the time taken too
```

`@time_diff` above a function definition means: "wrap this function with `time_diff`'s behavior." You can reuse the same decorator on **any number of functions**:

```python
@time_diff
def welcome(name):
    return "Welcome to function in python " + name

welcome("sudh")   # prints time taken, then returns the welcome string

@time_diff
def find_largest(a: int, b: int, c: int) -> int:
    """This is a function which is going to check which one is bigger out of
    these three numbers that we are going to give."""

    if a > b and a > c:
        return a
    elif b > c and b > a:
        return b
    else:
        return c

find_largest(5, 10, 3)   # prints time taken, then returns 10
```

You are not required to decorate every function — it's your choice, based on whether that function needs the extra behavior (timing, logging, etc.).

---

## 10. Recursive Functions

**Recursion** = a function calling **itself**.

### Example: Factorial

Mathematically: `5! = 5 × 4 × 3 × 2 × 1`, and by definition `0! = 1! = 1`.

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1              # base case — stops the recursion
    else:
        return n * factorial(n - 1)   # recursive call

factorial(5)   # -> 120
```

**How it unwinds:**
```
factorial(5) = 5 * factorial(4)
factorial(4) = 4 * factorial(3)
factorial(3) = 3 * factorial(2)
factorial(2) = 2 * factorial(1)
factorial(1) = 1                 <- base case reached

Then it resolves backward:
factorial(1) = 1
factorial(2) = 2 * 1 = 2
factorial(3) = 3 * 2 = 6
factorial(4) = 4 * 6 = 24
factorial(5) = 5 * 24 = 120
```

Every recursive function needs:
1. A **base case** — the stopping condition (otherwise infinite recursion → error).
2. A **recursive case** — where the function calls itself with a "smaller" input, moving toward the base case.

### Example: Sum of first N natural numbers

```python
def sum_natural_numbers(n):
    if n == 0:
        return 0
    else:
        return n + sum_natural_numbers(n - 1)

sum_natural_numbers(5)   # -> 15  (5+4+3+2+1)
```

Unwinding:
```
SNN(5) = 5 + SNN(4)
SNN(4) = 4 + SNN(3)
SNN(3) = 3 + SNN(2)
SNN(2) = 2 + SNN(1)
SNN(1) = 1 + SNN(0)
SNN(0) = 0                 <- base case

Resolves back: 1, 3, 6, 10, 15
```

Note: `factorial` and `sum_natural_numbers` are **not** built-in — they're just names chosen by the developer.

---

## 11. Quick Reference Summary

| Concept | Keyword / Syntax | Purpose |
|---|---|---|
| Define a function | `def name(): ...` | Create a reusable block of code |
| Empty body placeholder | `pass` | Avoid syntax errors when body is empty |
| Return a value | `return value` | Send a usable result back (unlike `print`, which returns `None`) |
| Multiple returns | `return a, b, c` | Packed into a tuple automatically |
| Default parameter | `def f(a, b=10):` | Use default if caller omits the argument |
| Variable positional args | `*args` | Collects extra positional args into a tuple |
| Variable keyword args | `**kwargs` | Collects extra `key=value` args into a dict |
| Type hint | `def f(a: int) -> int:` | Notification only, not enforced |
| Docstring | `""" ... """` | Documentation shown on hover |
| Higher-order function | `map(func, iterable)` | Apply a function across an iterable |
| Anonymous function | `lambda x: x**2` | Inline, nameless shorthand function |
| Decorator | `@decorator_name` | Wrap extra behavior around a function |
| Recursion | function calls itself | Break problems into smaller sub-problems with a base case |

---

## 12. Homework / Practice Task

Write the following as separate, well-documented functions (with type hints, return types, and docstrings):

1. **Arithmetic**: `add`, `subtract`, `multiply`, `divide`
2. **Area calculators**: circle, rectangle, triangle, square
3. **Temperature converters**: Celsius↔Fahrenheit, Celsius→Kelvin
4. **Even/odd & divisibility checker**
5. **Largest of three numbers** (without using `max()`)
6. **Grade calculator**: accepts marks in 5 subjects → returns total, percentage, grade, pass/fail
7. **Simple & compound interest calculators**
8. **Leap year checker**
9. **Voting eligibility checker** (nationality + age ≥ 18)
10. **Electricity bill calculator** (unit-based)
11. **Factorial calculator** (using recursion)
12. **Prime number checker**, and list primes in a range (e.g., 10–50)
13. **Palindrome checker**
14. **Armstrong number checker**
15. **Perfect number checker**
16. **Fibonacci series generator**
17. **GCD / LCM calculator**
18. **String analysis**: count uppercase, lowercase, digits, spaces, special characters
19. **Password strength checker**

**Instructions:** For every function — include a type hint for each parameter, a return type hint, a clear docstring, and a descriptive function name.

---

## 13. Q&A / Side Notes

### Why does `*args` collect into a tuple, not a list?

A student asked why `*args` gives you back a **tuple** instead of a **list**. The instructor's answer:

- It comes down to a design decision made by Python's creators — similar to asking "why is your name X and not Y?" Some choices are just fixed by convention/design and can't be reasoned away.
- But there's a practical angle too: it ties back to **mutability**. Tuples are immutable, so packaging the incoming arguments into a tuple protects them from being accidentally changed inside the function. If you specifically need a mutable collection to work with, you already know it's a tuple, so you can simply typecast it — exactly what `test10` above does:

```python
def test10(*args):
    return list(args)   # typecast tuple -> list if you need mutability
```

### Python vs Java — "Where's the `main()` function?"

A student with a Java background asked where Python's equivalent of Java's `public static void main(String[] args)` entry point is, since Java code doesn't run without it.

Key points from the discussion:

- **Java is a pure object-oriented language** in general use — code won't execute unless it's inside a `main` method (or similar invocation), and you must explicitly declare data types (e.g., `int a = 10;` — `a` can *only* ever hold an integer).
- **Python supports both scripting and OOP.** Unlike Java, Python doesn't require a `main` function to run — a simple top-level statement like `a = 0` executes immediately and is understood automatically. This is called **scripting mode**, and it's what the course has been using so far (plain `.ipynb` / top-to-bottom execution), as shown at the very end of the notebook:

```python
a = 0
a = 10
type(a)   # -> <class 'int'>
```

- **Python is a self-typed (dynamically typed) language.** You don't have to declare `int a = 10`; you just write `a = 10` and Python infers the type automatically. This is a major reason Python feels simpler than Java/C/C++/Scala, and why non-programmers can pick it up more easily.
- Python **does** have an equivalent concept for structuring larger, modular, "enterprise-style" code — but it isn't the same as Java's `main`. That will be covered when **Packages & Modules** are introduced, specifically the special `__init__.py` file/convention. The instructor was explicit that this is **not the same thing** as Java's `main` — just a superficially similar-sounding entry-point mechanism for organizing packages.
- **Bottom line:** for now (functions, scripting-style Python), there's no `main()` requirement. The packages/modules chapter (next class) will revisit entry-point-like structure with `__init__.py`.

---

## 14. What's Coming Next

*(from the instructor's end-of-class roadmap, matching the final notebook cell)*

- **Packages & Modules** in Python
- **Exception Handling** in Python
- **Logging** in Python — *(these three together ≈ 1 day)*
- **OOPs** (Object-Oriented Programming) in Python — *(≈ 1 day)*
- **File Handling** in Python
- **Pandas, NumPy, Plotly, Streamlit** — *(≈ 1–2 days)*
- **API development** — FastAPI — *(≈ 3 days)*
- **Database connections** — SQL, NoSQL, Graph, Vector databases (FAISS, ChromaDB, Pinecone, Weaviate) — *(≈ 2 days)*
- **Python project** deployed on **AWS** — *(≈ 1 day)*
- Only after this foundation: agentic systems, RAG, LangGraph/LangChain, "vibe coding" best practices

# Python Decorators

We've already talked about **inner functions**, and we're going to use inner functions inside decorators — that's why the topic was kept open until now. Now it's time to talk about decorators.

File used: `deco.py`

---

## Step 1: A Simple Function (No Decorator Yet)

Let's understand *why* we need decorators before writing one.

We start with a simple `divide` function:

```python
def divide(a, b):
    return a / b

result = divide(4, 2)
print(result)
```

Run it:

```
python deco.py
```

Output:

```
2.0
```

Nothing much — we just wrote a simple function, called it, and printed the result.

---

## Step 2: The Problem — Order of Arguments

Now let's add a twist. If we call `divide(2, 4)`, it will print `0.5`, because the numerator (2) gets divided by the denominator (4).

**Goal:** No matter what order the values are passed in — `divide(4, 2)` or `divide(2, 4)` — the result should always be the bigger number divided by the smaller number (i.e., always `4 / 2`).

**Logic:** Inside `divide`, check if the first value is less than the second value. If so, swap them.

Swapping in Python:

```python
a, b = b, a
```

Then divide the bigger number by the smaller number. So if we make this change directly inside `divide`, it works.

Problem solved, right? We *could* end the video here without decorators. But no — we need to talk about decorators.

---

## Step 3: The Same Problem Appears Again (Subtraction)

To make the case for decorators, let's create another function: `sub`, for subtraction.

```python
def sub(a, b):
    return a - b

result_one = divide(4, 2)
result_two = sub(2, 4)
print(result_one)
print(result_two)
```

If you run this, it prints `-2` (or `-2.0`), because we did the swapping logic only inside `divide`, not inside `sub`. But we're "greedy" — we want the same "bigger minus smaller" behavior for `sub` too.

You might say: "It's simple, just copy the swap logic and paste it into `sub` as well." And that works — now both `sub` and `divide` always operate on the bigger number first, then the smaller number, regardless of the order you pass them in.

**But now notice:** this swapping logic is *common* to both functions. We want to remove this common logic from each function and keep it somewhere else — then just tell each function to "use that feature." This is exactly where **decorators** come in.

---

## Step 4: Creating Your First Decorator

We create a decorator called `greater_first`:

```python
def greater_first():
    pass
```

At this point we just write `pass` so it doesn't throw an error while we build it up.

To *use* a decorator, you place the `@` symbol on top of the method you want to modify. You'll see this pattern a lot once you start working with Python frameworks — you use `@some_decorator` above a function to apply that feature.

```python
@greater_first
def divide(a, b):
    return a / b

@greater_first
def sub(a, b):
    return a - b
```

But `greater_first` isn't doing anything yet, so if you try to run this:

- First error: `greater_first() takes 0 positional arguments but 1 was given`
  - This happens because Python automatically passes the decorated function into the decorator. So the decorator needs to accept that function as a parameter:

```python
def greater_first(func):
    pass
```

- Next error: `NoneType object is not callable`
  - This means the decorator needs to `return` something (a callable), not `None`:

```python
def greater_first(func):
    return
```

### How a decorator actually works

A decorator **takes a function** as a parameter and **returns the same function** (with some added behavior/modification). You can't just `return func` as-is, though — that achieves nothing beyond the original behavior.

To actually change behavior, you create an **inner function** inside the decorator (this is why inner functions were covered earlier). The outer function is the decorator; inside it, we define an inner function commonly named `wrap` (since we're "wrapping" the behavior):

```python
def greater_first(func):
    def wrap(a, b):
        if a < b:
            a, b = b, a
        return func(a, b)
    return wrap
```

Explanation:
- `wrap` takes the **same parameters** as the function being decorated.
- Inside `wrap`, we do the swap logic: if `a` is less than `b`, swap them.
- Then we call the original function (`func`) with the (possibly swapped) values, and return that result.
- The decorator itself returns `wrap` — **not** the same function unmodified.

Why "new values"? Because if you pass `4, 2` (already in order), the same values get passed through. But if you pass `2, 4`, it gets passed through as `4, 2` after swapping.

Run it, and it works — both results print as `2` and `2` (regardless of the order arguments were passed).

---

## Step 5: Understanding How the Decorator Really Works

To understand what's happening under the hood, let's rewrite it **without** the `@` syntax, using explicit reassignment instead:

```python
sub = greater_first(sub)
```

What's happening:
- We take the `sub` function and apply the decorator to it, reassigning `sub` to the *new*, decorated version.
- Inside `greater_first`, `sub` is accepted as `func` (the function parameter).
- Calling `greater_first(sub)` returns `wrap` — but `wrap` itself isn't called yet at this point.
- `wrap` only actually executes when you later call `sub(...)` — that call now goes to `wrap`, which applies your condition/logic and then calls the original function (`func`) with the (possibly swapped) values, executing it and returning the value.

So: whatever function you pass into the decorator, when you call it, you're really calling `wrap`, which does its logic and then calls the original function.

Do the same thing for `divide`:

```python
divide = greater_first(divide)
```

This is **one way** of applying a decorator (manual reassignment). The **second way** — the one done earlier — is using the `@` syntax:

```python
@greater_first
def divide(a, b):
    ...
```

Run it — it still works. So you can use either approach, but the **modern/preferred way** is the `@decorator` syntax placed directly on top of your method to add the wrapper/behavior. (The manual reassignment line can be commented out/removed since it's no longer needed — the `@` decorator already does the job.)

After making these changes, it still works exactly as before.

---

## Step 6: Decorators Aren't Just for Swapping — Example: Logging

Decorators aren't limited to something like swapping two numbers — you can use them for any logic you want. For example: maintaining a **log**.

Let's create another decorator called `log_deco`:

```python
def log_deco(func):
    def wrap(a, b):
        print("Values I'm receiving:", a, ", ", b)
        result = func(a, b)
        print("Result of this operation:", result)
        return result
    return wrap
```

Notes on this decorator:
- It takes a function (`func`) just like any decorator.
- It has its own inner function `wrap(a, b)`.
- Inside `wrap`, we print the incoming values (`a`, `b`) — you could also use string formatting here if preferred, and optionally print the function name too.
- We call the function and store the result, then print the result.
- Since the result was already computed, we **return the same result** rather than calling the function a second time.
- Finally, the decorator returns `wrap`.

To actually apply it, add `@log_deco` on top of the target function:

```python
@log_deco
def sub(a, b):
    return a - b
```

If you only add `@log_deco` to `sub`, logging will only happen for `sub`.

If you also add it to `divide`:

```python
@log_deco
def divide(a, b):
    return a / b
```

...then, using different values (e.g., `8` and `20` for divide) helps you tell which log output belongs to which function — since `divide` is called first, its log appears first with values `8` and `20`, followed by its result. Then `sub`'s log appears with its own values and result.

*(Note: normally, you wouldn't print logs to the console — you'd write them to a file instead.)*

---

## Step 7: A Third Function — `add` (Only Some Decorators Apply)

Let's create one more function, `add`:

```python
def add(a, b):
    return a + b

result_three = add(4, 7)
print(result_three)
```

Running this, the output for `add` doesn't go through `greater_first` — that decorator is specifically for `divide` and `sub`, not for `add`. But we **do** want logging for `add`. So we can selectively apply just the decorator we want:

```python
@log_deco
def add(a, b):
    return a + b
```

Run it — now `add` also logs its values and result. This shows you can choose exactly which decorator(s) to apply to which function.

---

## Step 8: What If We Pass Three Values?

Let's extend `add` to accept three values:

```python
def add(a, b, c):
    return a + b + c

result_three = add(5, 7, 6)
```

Will this work? Since `wrap` inside `log_deco` was defined to only accept two parameters (`a, b`), but we're now calling it with three values, we'd expect an error.

Running it confirms this:

```
TypeError: wrap() takes 2 positional arguments but 3 were given
```

**Question:** Do you need to create a separate decorator for three values? What about five values? Ten values? This brings us back to the earlier topic of **variable-length arguments** (`*args`).

---

## Step 9: Fixing It with `*args`

Instead of hardcoding `a, b` in `wrap`, use `*args` to accept **any number of positional arguments**:

```python
def log_deco(func):
    def wrap(*args):
        print("Values I'm receiving:", args)
        result = func(*args)
        print("Result of this operation:", result)
        return result
    return wrap
```

- `wrap(*args)` accepts however many values you pass.
- Print `args` instead of individual `a, b`.
- When calling the function, pass `*args` through instead of individual `a, b`.

Try it — it works. No matter how many values you pass, they're treated as a **tuple**.

This is how you'd normally define a decorator in practice. (Note: the same `*args` update should ideally be made to `greater_first` too, but that would require changing more of its swap logic — left as an exercise for the viewer to do.)

---

## Step 10: What About Keyword Arguments?

What if you pass a **keyword argument** instead of a plain positional value? With only `*args`, that would break, since keyword arguments aren't captured by `*args` alone.

To be safe and make the decorator fully generic, accept both positional and keyword arguments:

```python
def log_deco(func):
    def wrap(*args, **kwargs):
        print("Values I'm receiving:", args, kwargs)
        result = func(*args, **kwargs)
        print("Result of this operation:", result)
        return result
    return wrap
```

Even if you're not going to use keyword arguments right now, it's good practice to include `**kwargs` so the decorator works generically for **any** function — regardless of whether it uses normal positional parameters or keyword parameters.

---

## Summary

- A **decorator** is a function that takes another function as input and returns a modified version of it (usually via an inner function, commonly named `wrap`).
- The `@decorator_name` syntax placed above a function definition is equivalent to writing `func = decorator_name(func)`.
- Decorators let you extract **common logic** (like argument-order swapping, or logging) out of multiple functions and apply it selectively wherever needed.
- Using `*args` and `**kwargs` in the inner `wrap` function makes decorators generic enough to work with functions that take any number of positional or keyword arguments.
- In this lesson, two decorators were built:
  - `greater_first` — ensures the bigger number always comes first (used with `divide` and `sub`).
  - `log_deco` — logs the input values and the result of any function it's applied to (used with `sub`, `divide`, and `add`).

That's the end of the topic on decorators. Hope it made sense!
