# Class 2 — Python Basics (19th July 2026)

## Setup Recap
- Create a `.ipynb` file (IPython/Jupyter Notebook) in VS Code (with the Jupyter extension) or use **Google Colab** if you haven't set up Python locally — Colab is free and gives you RAM + disk to run basic-to-intermediate Python code online.
- Run cells with **Shift+Enter** or **Ctrl+Enter**.
- Quick sanity check:
  ```python
  1+1
  # 2
  ```

## Why We Write Code
Think of code as a translator between *you* and the *computer*. No matter how fancy the logic gets, its entire job is to **process data**. If there's no data to work with, there's no reason to write the code in the first place. So before learning "how to build things," we first learn "what kinds of data Python can hold."

---

## 1. Variables — Labeled Boxes in Memory

**Analogy:** Imagine memory as a big warehouse full of storage boxes. When you write `age = 10`, Python grabs a box, puts `10` inside it, and sticks a label on the box that says `age`. Whenever you call `age`, Python walks to that box and hands you what's inside.

```python
a = 10
a          # 10
type(a)    # int
```

Python is a **self-typed (dynamically-typed) language** — you never have to declare "this variable will hold an integer" like you would in Java or C. Python looks at what you store and figures out the type automatically. This is why Python feels a lot like plain English — natural and forgiving.

---

## 2. The Core Data Types

### 2.1 Integer (`int`)
Whole numbers, no decimal part.
```python
a = 10
type(a)   # int
```

### 2.2 Float (`float`)
Numbers with a decimal point.
```python
b = 4.56
type(b)   # float
```

### 2.3 String (`str`)
A sequence of characters. You can wrap it in single quotes, double quotes, or triple quotes — all three work the same way for a simple string.
```python
s  = "sudh"
s1 = 'euron'
s2 = """raj"""

type(s)   # str
type(s1)  # str
type(s2)  # str
```

### 2.4 Boolean (`bool`)
Only two possible values: `True` and `False`. **Analogy:** think of a boolean as a light switch — only ON or OFF, nothing in between.

Internally, Python treats `True` as `1` and `False` as `0`. So arithmetic on booleans behaves like arithmetic on `1`s and `0`s:
```python
c  = True
c1 = False
type(c)     # bool
type(c1)    # bool

True + True    # 2   (1 + 1)
False * True   # 0   (0 * 1)
```

### 2.5 Complex Numbers (`complex`)
From math class: a complex number has a **real part** and an **imaginary part** (`a + ib`, where `i = √-1`). Python uses `j` (or `J`) instead of `i` to represent the imaginary unit — writing `i` will throw a syntax error.

```python
c = 5 + 6j
type(c)     # complex

c = 5 + 6J  # capital J also works
type(c)     # complex

c.real      # 5.0  -> extract the real part
c.imag      # 6.0  -> extract the imaginary part
```
You'll rarely use complex numbers unless you're building a math-heavy tool.

**Quick recap of the "hard" (single-value) data types:**
```python
int
float
bool     # not "boolean" — the actual Python keyword is bool
complex
str
```

---

## 3. Strings in Depth — Indexing & Slicing

**Analogy:** A string is like a train of connected boxcars, where each boxcar (character) has a numbered seat. Python numbers them automatically — starting at `0` from the left (forward index) and starting at `-1` from the right (backward index).

For the string `"sudhanshu"`:

| Char | s | u | d | h | a | n | s | h | u |
|---|---|---|---|---|---|---|---|---|---|
| Forward index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| Backward index | -9 | -8 | -7 | -6 | -5 | -4 | -3 | -2 | -1 |

### 3.1 Indexing — fetching ONE character
```python
s = "sudhanshu"
s[1]     # 'u'   (forward index)
s[-8]    # 'u'   (backward index, same character)
s[0]     # 's'
s[6]     # 's'   (the second "s" in the word)
s[15]    # IndexError: string index out of range
```
Going beyond the available indexes gives an **IndexError** — Python simply has nowhere to point to.

### 3.2 Slicing — fetching a CHUNK of characters
**Analogy:** Indexing gets you one seat; slicing gets you a whole row of seats using `start : end : step`.

Key rule: slicing always fetches **up to `end - 1`**, never including `end` itself.
```python
s[0:4]     # 'sudh'   -> starts at 0, stops before index 4
s[0:8:2]   # 's d n h' pattern -> every 2nd character
s[0:9:2]   # picks alternate characters across the whole string
s[0:90]    # no error! Slicing never throws "out of range" — it just
           # grabs whatever is available and stops
```

**Direction conflict:** slicing needs the start, stop, and step to all "agree" on direction, otherwise you get an **empty string**.
```python
s[0:9:-1]    # ''  -> start(0) to stop(9) is a forward move,
             #        but step is -1 (backward) = conflict
s[0:-9:-1]   # ''  -> 0 and -9 point to the same character = no room to move
s[-9:0:-1]   # ''  -> same direction conflict
s[-9:0:1]    # ''  -> again conflicting
```

Reversing a string (a very common trick):
```python
s[::-1]     # reverses the whole string
s[8::-1]    # same result -> start at last index, walk backward with no fixed end
```
-----
# Python String Slicing — Theory & Direction-Conflict Examples

## The Setup

```python
s = "sudhanshu"
```

This string has **9 characters**. Python lets you address each character two ways — counting from the left (forward index) or counting from the right (backward/negative index):

```
character:            s   u   d   h   a   n   s   h   u
forward index:        0   1   2   3   4   5   6   7   8
backward index:      -9  -8  -7  -6  -5  -4  -3  -2  -1
```

**Analogy:** Imagine 9 people standing in a line. You can point at someone by saying "3rd from the left" (forward index) *or* "3rd from the right" (backward index). Same person, two different ways to describe where they're standing.

---

## Negative Indexes Are Just Another Name for the Same Spot

`-9` and `0` both point at the **same character** — the very first one (`'s'`).

To convert any negative index into its normal ("forward") equivalent, use:

```
negative_index + len(string) = forward_index
```

```python
s = "sudhanshu"
len(s)          # 9
-9 + len(s)     # 0   -> confirms -9 means "position 0"
```

Keeping this conversion in your back pocket makes every "confusing" slicing result make sense instantly.

---

## The One Rule Behind All Slicing

```python
s[start : stop : step]
```

Reads as: **"Stand at `start`, take steps of size `step`, and stop just before reaching `stop`."**

- If `step` is **positive** → you must walk **rightward** (toward higher index numbers) to make progress.
- If `step` is **negative** → you must walk **leftward** (toward lower index numbers) to make progress.

If the direction you *need* to walk (to get from `start` to `stop`) doesn't match the direction your `step` allows, you can't move at all.

**Key behaviour:** Unlike indexing (`s[15]`), slicing **never raises an error** — even a nonsensical or "conflicting" slice just returns an **empty string** `''`.

---

## Worked Examples

### 1. `s[0:9:-1]` → `''`
*(Genuine direction conflict)*

- Start at position `0` (`'s'`).
- Stop target is `9` — that's to the **right**.
- To get from `0` to `9`, you'd need to walk **rightward**.
- But `step = -1` only allows walking **leftward**.
- Wrong direction → zero steps possible → `''`.

**Analogy:** You're facing left, but told to "walk toward the person on your right." You physically can't — so you stay put and return nothing.

---

### 2. `s[0:-9:-1]` → `''`
*(Zero-width range)*

- Start position: `0`.
- Stop position: `-9` → normalize: `-9 + 9 = 0`.
- Start and stop are the **same spot** (`0`).
- Zero distance to cover, regardless of step direction → `''`.

**Analogy:** "Walk from where you're standing... to where you're standing." Nowhere to go.

---

### 3. `s[-9:0:-1]` → `''`
*(Zero-width range)*

- Start position: `-9` → normalize: `-9 + 9 = 0`.
- Stop position: `0`.
- Start and stop are again the **same spot** (`0`).
- No gap to walk through → `''`.

**Analogy:** Same overlap as example 2, just written with the negative number on the *start* side instead of the *stop* side.

---

### 4. `s[-9:0:1]` → `''`
*(Zero-width range, even with a "valid" direction)*

- Start position: `-9` → normalize: `0`.
- Stop position: `0`.
- Start and stop overlap once more.
- This time `step = 1` (forward) is technically a valid direction — but it doesn't matter, because there's no distance between start and stop to move across.
- Result: `''`.

**Analogy:** Even facing the correct way, if you're already standing exactly where you're told to stop, you still take zero steps.

---

## Summary Table

| Slice | Start → Stop (normalized) | Reason it's empty |
|---|---|---|
| `s[0:9:-1]` | `0 → 9` | **Direction conflict** — need to go right, step forces left |
| `s[0:-9:-1]` | `0 → 0` | **Zero-width range** — start and stop are the same index |
| `s[-9:0:-1]` | `0 → 0` | **Zero-width range** — start and stop are the same index |
| `s[-9:0:1]` | `0 → 0` | **Zero-width range** — start and stop are the same index |

### The Real Takeaway
There are only **two distinct reasons** a slice comes back empty:

1. **True direction conflict** — the step's direction (forward/backward) doesn't match the direction needed to travel from `start` to `stop`. *(Only Example 1 above.)*
2. **Zero-width range** — after converting negative indexes to their positive equivalents, `start` and `stop` turn out to be the exact same position, so there's no ground to cover at all, no matter what the step is. *(Examples 2, 3, and 4.)*

**Practical tip:** Whenever a slice unexpectedly returns `''`, normalize any negative numbers first (`negative_index + len(string)`), then ask two questions:
- Are `start` and `stop` the same value? → zero-width range.
- If not, does the step's direction actually move you from `start` toward `stop`? → check for a direction conflict.
----
---

## 4. List — The "Everything Container" (Mutable)

**Analogy:** A list is like a shopping bag — you can toss in anything (numbers, text, even another bag) and you're free to reach in and swap items around whenever you like.

```python
l = [3, 4, 5, 6, 34, 56, 234.45, True, "Sudh", 4 + 8j]
type(l)     # list

l1 = [[3, 4, 5, 6], [4, 5, 6, 7], 45.56, False]
type(l1)    # list
```

Lists support the **exact same indexing/slicing rules as strings**:
```python
l[7]        # True
l[0:9:2]    # every alternate element from index 0 to 8
```

Since a list can hold a list, you index into the "outer" list first, then the "inner" one:
```python
l1[0]        # [3, 4, 5, 6]   -> the inner list at index 0
type(l1[0])  # list
l1[0][2:]    # [5, 6]  -> slice INSIDE that inner list
```

### Lists are Mutable
You can permanently change an item at a given index:
```python
l[0] = "sudhanshu"
l    # index 0 is now "sudhanshu" instead of 3
```

---

## 5. Tuple — The "Locked" Container (Immutable)

**Analogy:** If a list is a shopping bag, a tuple is a sealed box — you can look at what's inside and even peek into a smaller box placed inside it, but you can't reach in and swap the sealed box's own items.

```python
t = (2, 3, 4, 5, 6, "sudh", True)
type(t)     # tuple

t[0]        # 2         -> indexing works
t[0:5:2]    # slicing works too
```

### Tuples are Immutable
```python
t[0] = "sudhanshu"
# TypeError: 'tuple' object does not support item assignment
```

**The tricky interview question:** if a tuple *contains* a mutable object (like a list), can you change that inner list?
```python
t1 = (3, 4, 5, 6, [3, 4, 5, 6], "sudh", (3, 4, 5))

t1[0] = "sudh"        # ❌ Error — changing the tuple's own slot
t1[4][0] = "sudh"     # ✅ Works! You're not touching the tuple's slot —
                      #    you're mutating the LIST that lives inside it
t1[-1][0] = "sudh"    # ❌ Error — that slot holds a tuple, which is immutable
```
**Why this matters:** the tuple's rule is "you cannot replace what I'm holding at an index." It says nothing about whether the *object itself* (like a list) can change internally. That's the loophole.

### Use case of Tuples
Anywhere you want **protection from accidental changes** — e.g., storing DB credentials, API keys/secrets, or fixed configuration values. Since the values are locked, no other part of your code can accidentally overwrite them.

You can convert a tuple into a list any time you *do* need to modify it, without touching the original tuple:
```python
list(t1)    # creates a brand-new list from t1's contents
```

---

## 6. Set — Unique, Unordered Collection

**Analogy:** A set is like a guest list where no name can appear twice — if you try to add a duplicate name, it's simply ignored.

```python
s = {2, 3, 4, 5, 65, 76, 3, 34, 4, 5, 3, 3, 43, 5, 65, 6, 3, 3, 45, 5, 56}
s    # duplicates are automatically removed
```

⚠️ **Watch out:** `{}` by itself creates a **dictionary**, not an empty set (Python needs at least one value inside to know you mean "set").
```python
s1 = {}
type(s1)   # dict  (empty curly braces default to dict!)
```

Because Python is **case-sensitive**, `"sudh"` and `"Sudh"` are different values — only exact duplicates get removed:
```python
s = {1, 2, 1, 2, 2, 3, 2, 3, "sudh", True, "sudh", "Sudh"}
s   # True is removed because True == 1, which already exists in the set
```

### Sets are "unordered"
With small integers, the output can *look* sorted — but that's a coincidence of how Python stores small numbers internally, not a guarantee. Mix in strings and larger data, and the "order" disappears completely:
```python
s2 = {234, 54, 5, 65, 7564, 43242, 56, 346, "sudh", "xyz", 23.45}
s2   # no predictable ordering at all
```

Because there's no fixed order, **sets don't support indexing or slicing**:
```python
s2[0]
# TypeError: 'set' object is not subscriptable
```
To access elements positionally, typecast it first: `list(s2)`.

---

## 7. Dictionary — Key : Value Pairs

**Analogy:** Just like a real dictionary maps a *word* to its *meaning*, a Python dictionary maps a **key** to a **value**.

```python
d = {}
type(d)          # dict

d = {"name": "sudh"}
d["name"]        # 'sudh'  -> fetch value using the key (not an index number!)
```

A more realistic dictionary:
```python
d = {
    "name": "sudh",
    "Age": 35,
    "subject": ["python", "ml", "ops", "genai"],
    "mail_id": "sudhanshu@euron.one"
}

d["subject"]     # ['python', 'ml', 'ops', 'genai']
```

### Rule: keys must be unique
If you repeat a key, the **last value wins** — earlier ones are silently overwritten:
```python
d = {"name": "sudh", "Age": 35,
     "subject": ["python", "ml", "ops", "genai"],
     "mail_id": "sudhanshu@euron.one",
     "name": "sudhanshu kumar"}   # duplicate "name" key
d["name"]   # 'sudhanshu kumar' -> only the latest value survives
```

### What can be a key?
Keys must be **immutable and "hashable"** — int, float, string, boolean, complex, and tuple are allowed. Lists, sets, and dictionaries are **not** allowed as keys (they're mutable).
```python
d[123]      # ✅ int key works
d[8j]       # ✅ complex key works
d[True]     # ✅ boolean key works
d["#"]      # ✅ works only because "#" is wrapped as a string
d[[1,2,3]]  # ❌ TypeError: unhashable type: 'list'
d[{1,2,3}]  # ❌ unhashable type: 'set'
d[(1,2,3)]  # ✅ tuple works — it's immutable
```

### Dictionaries are mutable
You can update an existing key or add a brand-new one:
```python
d = {"name": "sudh", "Age": 35, "subject": ["python", "ml", "ops", "genai"]}

d["name"] = "sudhanshu kumar"     # updates existing key
d["address"] = "bangalore india"  # adds a new key
```

---

## 8. Summary of Data Types

**Single-value types:**
```python
int, float, bool, complex, str
```

**Collection (multi-value) types:**
```python
list    # mutable, ordered
tuple   # immutable, ordered
set     # mutable, unordered, unique values only
dict    # mutable, key-value pairs
```

---

## 9. Handy Built-in Functions

### `print()` — display output
```python
print("my name is sudh")
```

### `type()` — check the data type
```python
type("sudh")   # str
```

### `len()` — check the length / number of elements
Works on strings, lists, tuples, sets, and dictionaries alike:
```python
len("sudh")   # 4
len(l)        # count of items in list l
len(t1)       # count of items in tuple t1
len(s)        # count of items in set s
len(d)        # count of key-value pairs in dict d
```

### `input()` — take user input
**Important quirk:** `input()` *always* returns a **string**, no matter what the user types.
```python
a = input("enter the value")
type(a)     # str  (even if the user typed "30")
```
To use the entered value as a number, **typecast** it:
```python
a = int(input("enter the value"))
type(a)     # int
```
If the user types something that can't become an integer (like "sudh"), Python raises a `ValueError`.

### `range()` — generates a sequence of numbers
**Analogy:** `range()` is like a treadmill — it doesn't hand you the numbers all at once, it just sets up the machine to produce them one step at a time as needed (a "generator"). To *see* them immediately, wrap it in `list()`.

```python
range(5)              # range(0, 5) -> shows the "machine," not the numbers
list(range(5))         # [0, 1, 2, 3, 4]
list(range(3, 5))      # [3, 4]
list(range(3, 50, 2))  # step of 2: 3, 5, 7 ... 49
list(range(0, 101, 2)) # all even numbers from 0 to 100
```

### `enumerate()` — attach an index to each element
Useful when you need both the **position** and the **value** of items in a list.
```python
l1 = [[3, 4, 5, 6], [4, 5, 6, 7], 45.56, False]
list(enumerate(l1))
# [(0, [3, 4, 5, 6]), (1, [4, 5, 6, 7]), (2, 45.56), (3, False)]
```

---

## 10. String Quoting Rules

Single (`'...'`), double (`"..."`), and triple (`'''...'''` / `"""..."""`) quotes all create a `str`:
```python
s  = "sudh"    # str
s1 = 'sudh'    # str
s2 = """sudh"""  # str
```

### Triple quotes → multi-line strings
When you need a string spanning multiple lines, triple quotes let you write it out naturally. Python stores the line breaks internally using the newline character `\n`.
```python
s3 = """
fsf
fdsfsdfds
fds
"""
s3
# '\nfsf\nfdsfsdfds\nfds\n'
```

### Quote clashes
If your string itself contains an apostrophe, mixing quote types avoids confusing Python:
```python
s = ' i'm traveling'      # ❌ SyntaxError: unterminated string literal
s = " i'm traveling"      # ✅ double quotes outside, single quote inside
s = ' i"m traveling'      # ✅ single quotes outside, double quote inside
```

---

## Key Takeaways
- Python figures out data types automatically — no manual declarations needed.
- **Indexing** = one element; **Slicing** = a range of elements (`end` is always excluded).
- **List = mutable**, **Tuple = immutable** (but a mutable object *inside* a tuple can still change internally).
- **Set** = unique values, no guaranteed order, no indexing.
- **Dictionary** = key–value pairs; keys must be unique and immutable/hashable.
- `input()` always returns a string — typecast when you need a number.
- `range()` is a generator — wrap it in `list()` to see its contents.

## Homework / Next Class Preview
- Task will be posted on the dashboard (check notifications on mail/web/app) based on today's + yesterday's discussion.
- **Pod discussion:** Tuesday, 8:00 PM IST, via the BBB (Big Blue Button) link inside your dashboard — informal peer intro/discussion, not recorded.
- **Next class topics:** built-in functions for string/list/tuple/dict, then conditional statements (`if`/`else`), followed by loops (`for`, `while`).
