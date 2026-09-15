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
