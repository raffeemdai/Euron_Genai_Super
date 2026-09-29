# Docker — Complete Beginner-Friendly Study Notes

> **Source:** These notes were prepared from the complete class transcript supplied by you.
>
> **Goal:** Keep **all substantive content from the transcript**, but explain it in a simpler, cleaner way with examples.
>
> **Important:** The transcript contains speech-to-text spellings such as “UVCon/Uvicor”, “BAS”, etc. In the study notes, obvious command/tool names are normalized for readability (for example, **Uvicorn**, **bash**, `docker run -it`). This version contains the polished study notes only — the raw verbatim transcript has been left out to keep this a clean reference document.

---

# Table of Contents

1. [Where Docker Fits in the Course](#1-where-docker-fits-in-the-course)
2. [Why Docker Is Needed](#2-why-docker-is-needed)
3. [Simple Docker Mental Model](#3-simple-docker-mental-model)
4. [Docker, Kubernetes and Terraform](#4-docker-kubernetes-and-terraform)
5. [Docker Installation and Docker Desktop](#5-docker-installation-and-docker-desktop)
6. [Core Docker Terms](#6-core-docker-terms)
7. [Docker Image](#7-docker-image)
8. [Docker Hub](#8-docker-hub)
9. [First Docker Example — Hello World](#9-first-docker-example--hello-world)
10. [Pulling and Running Python Images](#10-pulling-and-running-python-images)
11. [Useful Image and Container Commands](#11-useful-image-and-container-commands)
12. [Foreground vs Background Containers](#12-foreground-vs-background-containers)
13. [Start, Stop, Restart and Remove Containers](#13-start-stop-restart-and-remove-containers)
14. [Container Naming](#14-container-naming)
15. [Interactive Mode and Entering Linux Containers](#15-interactive-mode-and-entering-linux-containers)
16. [Container Resource Isolation](#16-container-resource-isolation)
17. [FastAPI Example Used in the Class](#17-fastapi-example-used-in-the-class)
18. [Creating Your Own Docker Image with a Dockerfile](#18-creating-your-own-docker-image-with-a-dockerfile)
19. [Understanding Each Dockerfile Instruction](#19-understanding-each-dockerfile-instruction)
20. [Building and Running the Custom FastAPI Image](#20-building-and-running-the-custom-fastapi-image)
21. [Inspecting Files Inside a Running Container](#21-inspecting-files-inside-a-running-container)
22. [Git/GitHub + Docker Workflow](#22-gitgithub--docker-workflow)
23. [Port Mapping — Host vs Container](#23-port-mapping--host-vs-container)
24. [`.dockerignore`](#24-dockerignore)
25. [Docker Volume Mentioned in the Class](#25-docker-volume-mentioned-in-the-class)
26. [Multiple Docker Images in a Real Project](#26-multiple-docker-images-in-a-real-project)
27. [Frontend Docker Example](#27-frontend-docker-example)
28. [Docker Compose](#28-docker-compose)
29. [PostgreSQL Service in Compose](#29-postgresql-service-in-compose)
30. [`depends_on` and Environment Variables](#30-depends_on-and-environment-variables)
31. [Running Docker Compose](#31-running-docker-compose)
32. [Image vs Container — Movie Analogy](#32-image-vs-container--movie-analogy)
33. [Docker Desktop vs Docker Hub](#33-docker-desktop-vs-docker-hub)
34. [Docker Desktop vs Rancher Desktop](#34-docker-desktop-vs-rancher-desktop)
35. [How Docker Leads to Kubernetes](#35-how-docker-leads-to-kubernetes)
36. [Course / Project Context Mentioned at the End](#36-course--project-context-mentioned-at-the-end)
37. [Command Cheat Sheet](#37-command-cheat-sheet)
38. [Practice Exercises](#38-practice-exercises)
39. [Interview Questions and Answers](#39-interview-questions-and-answers)

---

# 1. Where Docker Fits in the Course

The class places Docker after topics such as:

- Project setup
- Databases
- APIs
- Git
- GitHub
- Version management

Docker is introduced mainly from the **operations / deployment** side.

The instructor's point is that a real project is not just a simple HTML page. A real project can contain:

- Backend
- Frontend
- Databases
- APIs
- Messaging systems
- Caching systems
- Other services

Docker helps package and run these parts consistently.

---

# 2. Why Docker Is Needed

## The problem

Different developers can have different systems:

- Windows
- macOS
- Linux

Even within the same operating system, versions can differ.

Examples mentioned in the transcript:

- Different Windows versions
- Different macOS versions
- Linux distributions such as Ubuntu, SUSE, Kali, etc.
- Different Python versions
- Different Spark versions
- Different Kafka versions

This can lead to the classic problem:

> **“It works on my machine, but it does not work on your machine.”**

A team of 10–15 people may all have different:

- Operating systems
- Software versions
- Libraries
- Dependencies
- Environment settings

Without Docker, every developer may need to repeat setup and troubleshooting.

## Docker's purpose

Docker tries to create a **portable box/environment** that can run on different host machines.

Very simple idea:

```text
Your Program
    ↓
Docker Container
    ↓
Windows / Mac / Linux
```

Instead of making your application depend heavily on the developer's computer, you package what it needs into Docker.

---

# 3. Simple Docker Mental Model

Think of Docker as a **box**.

Inside the box you can place:

- Operating-system-level environment
- Python
- Java
- Node.js
- Spark
- Kafka
- Your application code
- Required libraries
- Configuration

Then the same box can run on another machine that supports Docker.

```text
+-----------------------------+
| Host Computer               |
| Windows / Mac / Linux       |
|                             |
|   +---------------------+   |
|   | Docker Container    |   |
|   | Python              |   |
|   | FastAPI             |   |
|   | Your Code           |   |
|   +---------------------+   |
+-----------------------------+
```

The transcript repeatedly explains Docker as a **machine/box inside your machine**.

For beginner understanding, that analogy is useful.

---

# 4. Docker, Kubernetes and Terraform

The transcript connects three deployment/operations technologies:

1. **Docker**
2. **Kubernetes**
3. **Terraform**

The instructor describes Terraform as infrastructure-as-code.

The idea presented is:

```text
Docker
   ↓
Package/run applications in containers

Kubernetes
   ↓
Manage containers at larger scale / across machines

Terraform
   ↓
Create/manage infrastructure using code
```

The instructor also says Git/GitHub remains important for collaboration and version management.

---

# 5. Docker Installation and Docker Desktop

The transcript demonstrates installing **Docker Desktop**.

General process described:

1. Search for Docker download.
2. Download the installer appropriate for:
   - Windows
   - Mac
   - Linux
3. Install it.
4. Open **Docker Desktop**.

The instructor notes that Docker Desktop provides many features through a UI.

Items mentioned in Docker Desktop include:

- Containers
- Images
- Logs
- Volumes
- Kubernetes
- Docker Hub / related services
- Gordon / Docker AI chat feature

## Logs

Logs show activity/output from things you run.

## Volumes

The class initially describes volumes as storage / real disk space used for persistence or mounting.

A deeper volume demo was introduced later but not completed in this transcript before the class moved into multi-image/Compose discussion.

---

# 6. Core Docker Terms

The transcript introduces these concepts:

- Image
- Container
- Volume
- Networking
- Storage
- Docker Hub
- Dockerfile
- Docker Compose

The two most important beginner concepts are:

```text
IMAGE → blueprint/package
CONTAINER → running instance of that image
```

---

# 7. Docker Image

The instructor describes an image as a **pre-built environment**.

Example:

You may need:

- Linux
- Python 3.12
- FastAPI
- Uvicorn

Instead of installing everything manually, you can use an image containing the needed environment.

Examples discussed:

- Python images
- Kafka images
- Spark images
- TensorFlow images
- PyTorch images
- Ubuntu images
- NGINX images

## Simple analogy

An image is similar to a prepared software package or system template.

```text
Image:
Python + Linux + required base files
```

It is not the actively running process yet.

---

# 8. Docker Hub

Docker Hub is described as being similar in spirit to GitHub, but for Docker images.

## GitHub

Usually stores and shares:

```text
source code
```

## Docker Hub

Stores and shares:

```text
Docker images
```

Images can be:

- Public
- Private
- Official
- Community-created
- Organization-provided

The transcript searches Docker Hub for examples such as:

- Python
- Kafka
- Spark
- TensorFlow
- PyTorch

The class also points out that image pages contain:

- Tags
- Versions
- Documentation
- Pull commands
- Operating-system information
- Download information

A common command is:

```bash
docker pull <image-name>
```

Example:

```bash
docker pull python
```

With a version/tag:

```bash
docker pull nginx:1.27
```

---

# 9. First Docker Example — Hello World

The transcript runs:

```bash
docker run hello-world
```

What Docker does:

1. Checks whether the `hello-world` image exists locally.
2. If not found locally, Docker pulls it from a registry such as Docker Hub.
3. Docker creates a container from the image.
4. The program inside the container runs.
5. It prints a Docker hello message.

Mental flow:

```text
docker run hello-world
        ↓
Check local image
        ↓
Not found?
        ↓
Pull from Docker Hub
        ↓
Create container
        ↓
Run program
```

After pulling, the image appears under **Images** in Docker Desktop.

---

# 10. Pulling and Running Python Images

To explicitly pull Python:

```bash
docker pull python
```

Without a tag, Docker generally resolves the requested default/latest tag for that repository.

The transcript observes that the Python image is based on Linux/Debian and contains Python.

To run an image:

```bash
docker run python
```

Important point from the class:

Some images may start and immediately stop if their main process finishes or they have nothing persistent to keep them running.

---

# 11. Useful Image and Container Commands

## List local images

The transcript uses:

```bash
docker image ls
```

This shows Docker images available locally.

A commonly used equivalent is:

```bash
docker images
```

## List running containers

```bash
docker ps
```

The instructor explains:

> A running instance of an image is a **container**.

## See all containers

Useful extension:

```bash
docker ps -a
```

This includes stopped containers too.

---

# 12. Foreground vs Background Containers

Running normally may attach the terminal to the container.

Example:

```bash
docker run nginx
```

The transcript describes this as occupying the terminal / foreground.

To run in the background:

```bash
docker run -d nginx
```

`-d` means **detached mode**.

Then:

```bash
docker ps
```

shows the running container.

---

# 13. Start, Stop, Restart and Remove Containers

## Stop

```bash
docker stop <container-name-or-id>
```

Example style from the class:

```bash
docker stop distracted_jackson
```

The key lesson is that you stop a **container**, so you use a container name or ID, not merely an image name.

## Start a stopped container

```bash
docker start <container-name-or-id>
```

## Restart

```bash
docker restart <container-name-or-id>
```

## Remove

A running container normally needs to be stopped before regular removal:

```bash
docker stop <container-name>
docker rm <container-name>
```

Concept:

```text
docker pull  → get image
docker run   → create/run container
docker stop  → stop container
docker start → start existing stopped container
docker rm    → remove container
```

---

# 14. Container Naming

If you do not give a name, Docker can generate one automatically.

The transcript shows examples of automatically generated names such as:

- distracted_jackson
- trusting_chao
- laughing_galileo

To choose your own container name:

```bash
docker run -d --name my-nginx nginx
```

General syntax:

```bash
docker run --name <container-name> <image-name>
```

Example:

```bash
docker run -d --name webserver nginx
```

---

# 15. Interactive Mode and Entering Linux Containers

The transcript demonstrates starting Ubuntu interactively.

Normalized command:

```bash
docker run -it ubuntu bash
```

Meaning:

- `docker run` → create and run a container
- `-i` → interactive input
- `-t` → terminal
- `ubuntu` → image
- `bash` → shell to start

Inside, Linux commands can be executed.

Examples:

```bash
ls
pwd
cat /etc/os-release
```

If `bash` is unavailable in a minimal image, `sh` may work:

```bash
docker run -it <image> sh
```

## Enter an already-running container

The transcript later uses `docker exec` conceptually.

Typical command:

```bash
docker exec -it <container-name> bash
```

or:

```bash
docker exec -it <container-name> sh
```

This is useful when the container is already running and you want a shell inside it.

---

# 16. Container Resource Isolation

The transcript explains that Docker can control the resources available to a container.

Resources discussed include:

- CPU
- Memory/RAM
- Network bandwidth

The mental model is that your physical machine may have large resources, but you can give only a controlled portion to a container.

Example concept:

```text
Host machine:
16 GB RAM
8 CPUs

Container:
2 GB RAM
1 CPU
```

This supports isolation and allows multiple containers to run on one machine without every container using everything.

Example Docker syntax:

```bash
docker run --memory="2g" --cpus="1" nginx
```

The exact command form above is a normalized practical example of the resource-control concept discussed in the transcript.

---

# 17. FastAPI Example Used in the Class

The attached `main.py` contains:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }


@app.get("/students")
def students():

    return [
        {"id": 1, "name": "Sudhanshu"},
        {"id": 2, "name": "Hitesh"},
        {"id": 3, "name": "Krish"}
    ]
```

It creates two endpoints.

## Home endpoint

```http
GET /
```

Response:

```json
{
  "message": "Backend is running"
}
```

## Students endpoint

```http
GET /students
```

Returns three students:

```json
[
  {"id": 1, "name": "Sudhanshu"},
  {"id": 2, "name": "Hitesh"},
  {"id": 3, "name": "Krish"}
]
```

The Docker practical packages this FastAPI application so that another developer can run the same environment without manually reproducing every dependency.

---

# 18. Creating Your Own Docker Image with a Dockerfile

The transcript creates three main files for the FastAPI example:

```text
project/
├── main.py
├── requirements.txt
└── Dockerfile
```

## `requirements.txt`

The class adds:

```text
fastapi
uvicorn
```

## Example Dockerfile matching the class explanation

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The exact base tag may differ from the one shown verbally in the transcript, but the transcript clearly describes a Python 3.12 Linux-based image and these Dockerfile stages.

---

# 19. Understanding Each Dockerfile Instruction

## `FROM`

```dockerfile
FROM python:3.12-slim
```

Purpose:

- Choose the base image.
- The class describes it as a small Linux/Ubuntu-like base where Python is already installed.
- Docker pulls it if it is not already local.

Mental model:

```text
Start with a ready-made machine/environment.
```

---

## `WORKDIR`

```dockerfile
WORKDIR /app
```

Purpose:

- Sets `/app` as the working directory inside the image/container.

After this, relative commands execute from:

```text
/app
```

---

## `COPY requirements.txt .`

```dockerfile
COPY requirements.txt .
```

Meaning:

```text
Copy requirements.txt
FROM local project
TO current working directory in the image
```

Since the working directory is `/app`, it becomes:

```text
/app/requirements.txt
```

---

## `RUN`

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Purpose:

Install required Python packages **inside the image**.

The transcript specifically explains installing FastAPI and Uvicorn from `requirements.txt`.

---

## `COPY . .`

```dockerfile
COPY . .
```

Meaning:

```text
Copy everything from the local build context
into the current working directory in the image
```

The class later enters the container and verifies that files such as:

- `main.py`
- `requirements.txt`
- `Dockerfile`
- other local files

were copied.

---

## `EXPOSE`

```dockerfile
EXPOSE 8000
```

The transcript explains this as declaring the application/container port used by the API.

Important beginner distinction:

`EXPOSE 8000` **does not by itself publish port 8000 to Windows/macOS**.

Actual host access requires port mapping when you run the container, for example:

```bash
docker run -p 5000:8000 my-fastapi
```

---

## `CMD`

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Purpose:

Run the FastAPI server when the container starts.

Explanation:

```text
uvicorn
   ↓
main:app
   ↓
Run FastAPI app object named "app" from main.py
   ↓
0.0.0.0
   ↓
Listen on all interfaces inside the container
   ↓
8000
   ↓
Container's application port
```

---

# 20. Building and Running the Custom FastAPI Image

## Build

The transcript uses the pattern:

```bash
docker build -t <image-name> .
```

Example:

```bash
docker build -t fastapi-test .
```

Meaning:

- `docker build` → build an image
- `-t fastapi-test` → tag/name it
- `.` → use the current folder as the build context

## Run

Without port mapping:

```bash
docker run fastapi-test
```

The FastAPI app may report that it is listening on:

```text
0.0.0.0:8000
```

But the transcript demonstrates that you still may not be able to reach it from the host browser until you publish/map a host port.

---

# 21. Inspecting Files Inside a Running Container

The class enters the running container and verifies the copied files.

Typical command:

```bash
docker exec -it <container-name> sh
```

or:

```bash
docker exec -it <container-name> bash
```

Then:

```bash
pwd
ls
cat main.py
cat requirements.txt
cat Dockerfile
```

This proves that the Docker build copied the local application files into the image/container.

---

# 22. Git/GitHub + Docker Workflow

The class connects the previous Git/GitHub lesson with Docker.

Typical flow:

```text
Developer creates:
main.py
requirements.txt
Dockerfile

        ↓

Push to GitHub

        ↓

Another developer clones repository

        ↓

docker build

        ↓

docker run

        ↓

Same packaged environment runs
```

Commands mentioned conceptually:

```bash
git init
git add .
git commit -m "first"
git branch -M main
git remote add origin <repository-url>
git push
```

Other developer:

```bash
git clone <repository-url>
```

Then they do not need to manually launch `main.py` first.

They can build/run the Docker image:

```bash
docker build -t first-image .
docker run first-image
```

This is the core portability point emphasized by the transcript.

---

# 23. Port Mapping — Host vs Container

This is one of the most important parts of the transcript.

The API is running **inside the container** on port `8000`.

Example:

```text
Container:
0.0.0.0:8000
```

But the browser on your Windows host cannot automatically access that port.

You publish it using:

```bash
docker run -p 5000:8000 fastapi-test
```

Docker port syntax:

```text
-p HOST_PORT:CONTAINER_PORT
```

So:

```text
5000 = Windows/host port
8000 = Docker/container port
```

Diagram:

```text
Browser on Windows
http://localhost:5000
        |
        | host port 5000
        v
+------------------------+
| Docker Container       |
| FastAPI :8000          |
+------------------------+
```

Then access:

```text
http://localhost:5000/
```

Swagger:

```text
http://localhost:5000/docs
```

## Memory trick

```text
LEFT  = host
RIGHT = container

-p HOST:CONTAINER
```

Example:

```bash
docker run -p 5000:8000 fastapi-test
```

---

# 24. `.dockerignore`

The transcript compares `.dockerignore` with `.gitignore`.

## `.gitignore`

Tells Git:

```text
Do not track/push these files.
```

## `.dockerignore`

Tells Docker:

```text
Do not include/copy these files into the Docker build context/image.
```

Example:

```text
__pycache__/
*.pyc
.env
.git/
venv/
```

Why useful:

- Smaller image/build context
- Avoid unnecessary files
- Avoid copying local caches
- Avoid accidentally including secrets such as `.env`

---

# 25. Docker Volume Mentioned in the Class

The instructor introduces Docker volumes as the next storage concept:

> mounting storage/data so that data can exist outside the short-lived container filesystem.

The transcript mentions volumes earlier in Docker Desktop as real storage/disk space and later says the next step is to mount Docker volumes.

The detailed volume command demo is **not fully developed in this transcript** because the discussion moves to multi-image projects and Docker Compose.

Simple practical example for understanding:

```bash
docker run -v mydata:/data ubuntu
```

Mental model:

```text
Container
   |
   +---- mounted persistent volume ----> Docker-managed storage
```

This example is added only to make the transcript's volume concept easier to understand.

---

# 26. Multiple Docker Images in a Real Project

The transcript explains that real systems can have:

- Frontend
- Backend
- Database
- Cache
- Kafka / messaging
- Other services

Instead of putting everything into one box, we can create separate containers.

Example:

```text
Project
│
├── Frontend container
├── Backend container
├── PostgreSQL container
├── Cache container
└── Messaging/Kafka container
```

This creates a management problem if you manually build/run every service one by one.

That is why the transcript introduces **Docker Compose**.

---

# 27. Frontend Docker Example

The transcript creates a frontend folder and describes using a Node image.

Typical structure:

```text
project/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── frontend/
    ├── package.json
    ├── source files
    └── Dockerfile
```

Python dependencies use:

```text
requirements.txt
```

Node/JavaScript dependencies commonly use:

```text
package.json
```

Python:

```bash
pip install ...
```

Node:

```bash
npm install
```

A simplified frontend Dockerfile matching the class explanation:

```dockerfile
FROM node:latest

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

The transcript explains that the Dockerfile inside `frontend/` uses the frontend folder as its local build context, while the backend Dockerfile uses the backend folder.

---

# 28. Docker Compose

When a project has multiple Docker services, the transcript creates:

```text
compose.yaml
```

at the parent/root project level.

Example structure:

```text
project/
├── compose.yaml
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── ...
```

The idea:

```text
One Compose file
      ↓
Manage multiple services together
```

Example based on the transcript:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "5000:8000"

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  postgres:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase
    ports:
      - "5432:5432"
```

---

# 29. PostgreSQL Service in Compose

The transcript points out an important difference.

For backend and frontend, you wrote your own Dockerfiles:

```yaml
backend:
  build: ./backend
```

```yaml
frontend:
  build: ./frontend
```

But for PostgreSQL you may directly use an existing image:

```yaml
postgres:
  image: postgres
```

Docker can pull the PostgreSQL image from Docker Hub.

Then environment settings can initialize:

- Username
- Password
- Database name

Example:

```yaml
environment:
  POSTGRES_USER: user
  POSTGRES_PASSWORD: password
  POSTGRES_DB: mydatabase
```

---

# 30. `depends_on` and Environment Variables

The transcript says the backend may depend on the database.

Example:

```yaml
backend:
  build: ./backend
  depends_on:
    - postgres
```

Meaning at the Compose orchestration level:

```text
Start PostgreSQL service before backend service.
```

The transcript's reasoning is:

> If the API requires the database, the database service should be started before the API service.

It also introduces environment variables such as a database URL.

Example:

```yaml
backend:
  environment:
    DATABASE_URL: postgresql://user:password@postgres:5432/mydatabase
```

Important Compose networking idea:

```text
postgres
```

can be used as the service hostname from another container in the same Compose network.

So backend can communicate with the database by the Compose service name instead of `localhost`.

---

# 31. Running Docker Compose

The transcript uses:

```bash
docker compose up
```

and discusses build behavior.

A common explicit build command is:

```bash
docker compose up --build
```

This builds services whose images need to be built and then starts the complete application stack.

To run in background:

```bash
docker compose up -d
```

To stop/remove the Compose stack:

```bash
docker compose down
```

The transcript's key idea:

```text
Instead of manually:
build backend
run backend
build frontend
run frontend
run database

Use:
docker compose up
```

---

# 32. Image vs Container — Movie Analogy

The instructor gives a simple analogy.

## Image

Downloading a movie file:

```text
movie.mp4
```

It exists, but it is not currently playing.

## Container

When you play the movie:

```text
movie is running
```

Likewise:

```text
Docker image
    ↓ run
Docker container
```

Another analogy in the transcript:

- Downloaded operating-system image = image
- Running/using it = container

---

# 33. Docker Desktop vs Docker Hub

The transcript answers this distinction.

## Docker Hub

A remote library/registry for images.

Think:

```text
Docker Hub = warehouse/library of Docker images
```

## Docker Desktop

A local application/environment used to:

- Run Docker
- View images
- View containers
- View logs
- Work with volumes
- Work with Kubernetes integration
- Access Docker-related local tooling

Think:

```text
Docker Desktop = local Docker working environment
```

---

# 34. Docker Desktop vs Rancher Desktop

At the end of the class a student asks about Rancher Desktop.

The instructor's answer, summarized faithfully:

- They are broadly similar in purpose from a desktop container-development perspective.
- Both can provide container engines.
- Both can expose Kubernetes-related functionality.
- Both support port forwarding concepts.
- Both provide command-line/container tooling.
- Vendor/product implementation differs.

The instructor notes that they had not used Rancher Desktop recently, so this part is presented as their general understanding rather than a detailed product comparison.

---

# 35. How Docker Leads to Kubernetes

The transcript ends by setting up the next topic: **Kubernetes**.

Docker handles containers, often on one machine.

But real production systems may need:

- Multiple machines
- Multiple containers
- Clusters
- Scaling
- Placement of workloads
- Master/worker-type architecture
- Coordination across machines

That leads to Kubernetes.

Simple progression:

```text
Docker
    ↓
Run containers

Kubernetes
    ↓
Manage many containers across many machines
```

The instructor mentions:

- Kubernetes
- K8s
- Pods
- Multiple machines
- Clusters
- Production scale
- Cloud usage

The class describes Kubernetes as the next extension of Docker knowledge.

---

# 36. Course / Project Context Mentioned at the End

The transcript closes with broader course planning.

Topics already discussed or being completed include:

- Python
- Databases
- APIs
- Git
- GitHub
- Docker

Upcoming topics mentioned:

- Kubernetes
- Terraform / infrastructure as code
- System design
- Big-data components
- Agent/RAG-related core topics
- Project building
- Interview preparation

The instructor says future project work will include deeper real-world artifacts such as:

- Case study
- Domain understanding
- Business understanding
- HLD
- LLD
- PRDs
- Capacity planning
- Cost estimation
- Stakeholders
- Full project implementation

The transcript also contains class scheduling/logistics about longer weekend sessions. Those logistics are preserved in the complete transcript appendix below.

---

# 37. Command Cheat Sheet

## Images

```bash
docker pull python
docker pull nginx:1.27
docker image ls
docker images
```

## Run

```bash
docker run hello-world
docker run nginx
docker run -d nginx
```

## Containers

```bash
docker ps
docker ps -a
docker stop <container>
docker start <container>
docker restart <container>
docker rm <container>
```

## Custom name

```bash
docker run -d --name my-nginx nginx
```

## Interactive

```bash
docker run -it ubuntu bash
docker run -it ubuntu sh
```

## Enter running container

```bash
docker exec -it <container> bash
docker exec -it <container> sh
```

## Build image

```bash
docker build -t fastapi-test .
```

## Port mapping

```bash
docker run -p 5000:8000 fastapi-test
```

Memory:

```text
-p HOST_PORT:CONTAINER_PORT
```

## Docker Compose

```bash
docker compose up
docker compose up --build
docker compose up -d
docker compose down
```

---

# 38. Practice Exercises

## Exercise 1 — Hello World

```bash
docker run hello-world
```

Check:

```bash
docker image ls
docker ps -a
```

---

## Exercise 2 — NGINX

```bash
docker pull nginx
docker run -d --name my-nginx nginx
docker ps
```

Stop:

```bash
docker stop my-nginx
```

Start:

```bash
docker start my-nginx
```

Remove:

```bash
docker stop my-nginx
docker rm my-nginx
```

---

## Exercise 3 — Ubuntu Interactive Mode

```bash
docker run -it ubuntu bash
```

Inside:

```bash
pwd
ls
cat /etc/os-release
```

Exit:

```bash
exit
```

---

## Exercise 4 — FastAPI Docker

Create:

```text
main.py
requirements.txt
Dockerfile
```

Build:

```bash
docker build -t fastapi-test .
```

Run:

```bash
docker run -p 5000:8000 fastapi-test
```

Open:

```text
http://localhost:5000/docs
```

---

## Exercise 5 — Docker Compose

Create:

```text
frontend/
backend/
compose.yaml
```

Then:

```bash
docker compose up --build
```

---

# 39. Interview Questions and Answers

## Q1. Why do we use Docker?

Docker packages an application with its required environment and dependencies so it can run more consistently across different systems.

---

## Q2. What is a Docker image?

A Docker image is a packaged template used to create containers.

---

## Q3. What is a Docker container?

A container is a running instance of an image.

---

## Q4. What is Docker Hub?

Docker Hub is a registry where Docker images can be published, stored and pulled.

---

## Q5. Difference between Docker Hub and Docker Desktop?

```text
Docker Hub     → remote image registry/library
Docker Desktop → local Docker development/runtime application
```

---

## Q6. What does `docker pull` do?

Downloads an image from a registry.

```bash
docker pull python
```

---

## Q7. What does `docker run` do?

Creates and starts a container from an image.

```bash
docker run nginx
```

---

## Q8. What does `docker ps` do?

Shows currently running containers.

---

## Q9. What is detached mode?

Runs the container in the background.

```bash
docker run -d nginx
```

---

## Q10. How do you enter a running container?

```bash
docker exec -it <container> bash
```

or:

```bash
docker exec -it <container> sh
```

---

## Q11. What is a Dockerfile?

A Dockerfile is a text file containing instructions for building a custom Docker image.

---

## Q12. What does `FROM` do?

Specifies the base image.

---

## Q13. What does `WORKDIR` do?

Sets the working directory inside the image/container.

---

## Q14. What does `COPY` do?

Copies files from the local build context into the image.

---

## Q15. What does `RUN` do?

Executes a command during image build.

Example:

```dockerfile
RUN pip install -r requirements.txt
```

---

## Q16. What does `CMD` do?

Defines the default command to run when the container starts.

---

## Q17. What is port mapping?

It connects a host port to a container port.

```bash
docker run -p 5000:8000 fastapi-test
```

---

## Q18. Which side is host and which side is container?

```text
-p HOST:CONTAINER
```

---

## Q19. What is `.dockerignore`?

A file that tells Docker what files/directories not to send/include in the Docker build context.

---

## Q20. Why use Docker Compose?

To define and run multiple related containers/services together using one YAML file.

---

## Q21. What is `depends_on`?

It expresses service startup dependency/order in Docker Compose.

---

## Q22. How can backend reach PostgreSQL in Compose?

It can use the PostgreSQL **service name** as a hostname, such as:

```text
postgres
```

---

## Q23. Why does Kubernetes come after Docker?

Docker runs containers; Kubernetes is used to orchestrate/manage many containers across multiple machines at scale.

---
