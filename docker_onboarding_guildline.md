# Docker Onboarding Guideline

A beginner-friendly guide to Docker: installing it on Windows/macOS, pulling the
right images from Docker Hub, using everyday Docker commands, and using Docker to
develop Python web apps and Node.js applications. Everything here maps to how
this repo (`AI-Trader`) is actually containerized — see `docker-compose.yml`,
`service/server/Dockerfile`, and `service/frontend/Dockerfile`.

> New here? Work through this file top to bottom, then try the repo's own
> `docker compose up -d --build` at the end.

---

## Table of contents

1. [What Docker is, in one paragraph](#1-what-docker-is-in-one-paragraph)
2. [Install Docker Desktop](#2-install-docker-desktop)
   - [Windows: prerequisites](#21-prerequisites)
   - [Windows: install WSL 2](#22-install-wsl-2-the-engine-underneath-docker)
   - [Windows: install Docker Desktop](#23-install-docker-desktop)
   - [Windows: configure Docker Desktop](#24-docker-desktop-configuration)
   - [Windows: first-time setup](#25-first-time-setup-and-running-your-first-container)
   - [Windows: run an application](#26-running-an-application-from-docker-desktop)
   - [Windows: pull the latest images](#27-pulling-the-latest-images)
   - [macOS](#on-macos-intel-or-apple-silicon)
3. [Docker Hub — getting the right images](#3-docker-hub--getting-the-right-images)
   - [Find and check images on Docker Hub](#finding-and-checking-images-on-docker-hub)
   - [How image names work](#how-image-names-work)
   - [Production pulls: worked example](#production-pulls-worked-example)
4. [Essential Docker commands](#4-essential-docker-commands)
5. [Develop a Python web app with Docker](#5-develop-a-python-web-app-with-docker)
6. [Develop a Node.js app with Docker](#6-develop-a-nodejs-app-with-docker)
7. [Orchestrate everything with Docker Compose](#7-orchestrate-everything-with-docker-compose)
8. [Troubleshooting](#8-troubleshooting)
9. [Cheat sheet](#9-cheat-sheet)

---

## 1. What Docker is, in one paragraph

Docker packages an application **and everything it needs** (runtime, libraries,
system tools) into an **image**. A running image is a **container**. The huge
win: "it works on my machine" stops being a thing, because your machine, your
teammate's machine, and the production server all run the *same* image.

Key vocabulary you'll see everywhere:

| Term       | Meaning                                                                 |
|------------|-------------------------------------------------------------------------|
| Image      | A read-only template (like a zip of your app + runtime).                |
| Container  | A running instance of an image (like a process that started from a zip).|
| Dockerfile | A recipe file that builds an image.                                     |
| Compose    | A YAML file that defines and runs several containers together.          |
| Volume     | Persistent storage that survives container restarts.                    |
| Port       | The door a container exposes (`host:container`, e.g. `8000:8000`).      |
| Hub        | Docker's public registry of ready-made images.                          |

---

## 2. Install Docker Desktop

Docker Desktop includes Docker Engine, the Docker CLI, and Docker Compose in one
install. It's the fastest way to start on Windows and macOS.

### On Windows (Windows 10/11 Home, Pro, or Enterprise)

Docker Desktop on Windows runs Linux containers inside a lightweight VM managed
by WSL 2. This section walks through installation, configuration, first-time
setup, running an application, and pulling images — in that order.

#### 2.1 Prerequisites

- **Windows 10 64-bit (v2004+) or Windows 11.** Home and Pro editions both work.
- **Hardware virtualization enabled** in the BIOS ("Intel VT-x" / "AMD-V");
  most machines have this on by default.
- **~4 GB free RAM** (8 GB+ recommended when running several containers) and a
  few GB of free disk for images.
- **A (free) Docker account** — needed for the Docker Hub sign-in step.

#### 2.2 Install WSL 2 (the engine underneath Docker)

WSL 2 is Microsoft's built-in Linux environment. Docker Desktop uses it as its
backend, so no separate VM software is needed.

1. Open **PowerShell as Administrator** and run:

   ```powershell
   wsl --install
   ```

   This installs WSL 2 plus a default Linux distro (Ubuntu) and may ask you to
   restart. If WSL is already present, make sure it's version 2:

   ```powershell
   wsl --set-default-version 2
   ```

2. **Restart Windows** when prompted.

> **Legacy alternatives** (only if WSL 2 isn't available): Docker Desktop can
> fall back to Hyper-V. You can also install the Docker Engine directly inside
> a WSL 2 distro (no Docker Desktop at all), but that's advanced — skip it
> until you're comfortable.

#### 2.3 Install Docker Desktop

1. Download the **"Docker Desktop for Windows"** installer from
   <https://www.docker.com/products/docker-desktop/> (the `-amd64.exe` build).

2. Double-click the installer and walk through the wizard:

   - Leave **"Use WSL 2 instead of Hyper-V"** checked — this is the backend you
     just set up in step 2.2.
   - Leave **"Add shortcut to desktop"** checked for convenience.
   - Click **Install**, let it finish, then **Close and restart**.

3. On first launch, accept the **license / service agreement**.

4. **Sign in** with your Docker account (or create one) in the sign-in window.
   Signing in is required for Docker Hub pulls and for the UI's search/pull
   features; if you skip it, CLI pulls still work but UI search won't.

5. **Verify** — open PowerShell (or your terminal) and run:

   ```powershell
   docker version
   docker compose version
   ```

   You should see **Client** and **Server** sections with version info. If the
   Server section is missing, Docker Desktop hasn't finished starting — open it
   and wait for the whale icon to stop animating.

#### 2.4 Docker Desktop configuration

Click the whale icon in the system tray → **Settings** (gear). The panels that
matter for everyday work:

- **General**
  - *Start Docker Desktop when you log in* — keep on if you use Docker daily.
  - *Use the WSL 2 based engine* — leave on; it's the backend from step 2.2.
- **Resources** — how much of your machine the Docker VM may use:
  - *CPUs* and *Memory* — the defaults (2 CPUs / 2 GB) are fine for one small
    container, but this repo runs **six**; bump memory to **4 GB+** if builds
    are slow or containers get OOM-killed.
  - *Disk image size* — cap on the virtual disk holding images and volumes;
    raise it if `docker system df` reports the disk full.
  - Leave enough RAM/CPUs free for Windows itself — don't max everything out.
- **WSL Integration** — if you installed extra Linux distros, this is where you
  enable Docker inside each one. The default distro is enabled automatically.
- **Docker Engine** — advanced JSON daemon config; beginners rarely touch this.
- **Features in development** — Buildx (multi-platform builds) and Compose v2
  are on by default; leave them.
- **Kubernetes** — only needed if you're learning Kubernetes; leave it off.

Any change to Resources/Engine needs **Apply & restart**. Afterwards confirm the
whale icon shows *Engine running*.

#### 2.5 First-time setup and running your first container

With Docker Desktop running, do a quick smoke test:

1. Right-click the whale icon → **Dashboard** (or just run `docker` in a
   terminal). The *Get started* panel offers a sample `docker/welcome-to-docker`
   image you can run with one click.

2. From PowerShell, run your first real container:

   ```powershell
   docker run -d --name hello -p 8000:8000 python:3.11-slim python -m http.server 8000
   ```

   This pulls `python:3.11-slim`, starts a tiny HTTP server, and maps port 8000
   to your machine. Open <http://localhost:8000> — you'll see a directory
   listing generated *inside the container*.

3. Stop and remove it (full command set comes in Section 4):

   ```powershell
   docker stop hello; docker rm hello
   ```

#### 2.6 Running an application from Docker Desktop

Docker Desktop is more than a tray icon — it has a full GUI that mirrors the CLI:

- **Containers tab** — every container, with one-click start/stop/restart, plus
  *Logs* (streams output, like `docker logs -f`) and a *Terminal* (like
  `docker exec -it ...`).
- **Images tab** — every image on your machine; *Pull* downloads a new one and
  *Run* launches it with port/env options.

To run this entire repo from the UI:

1. Open PowerShell **in the repo root** (`D:\OpenSource\AI-Trader`) and run:

   ```powershell
   docker compose up -d --build
   ```

2. Switch to the Docker Desktop **Containers** tab — all six services
   (backend, worker, seed, frontend, db, redis) appear there. Click any
   container to stream its **Logs** or open a **Terminal**.
3. Open the frontend at <http://localhost:3000> and the API docs at
   <http://localhost:8000/docs>.

#### 2.7 Pulling the latest images

Two equivalent ways — the CLI or the Docker Desktop UI:

**From the CLI:**

```powershell
docker pull python:3.11-slim   # pull a specific tag
docker pull postgres           # pull the latest tag
docker pull node:20-alpine
docker pull redis:7-alpine
```

Re-running `docker pull` on an image you already have updates it to the newest
version of that tag.

**From the UI / Docker Hub:**

1. Docker Desktop → **Images** tab → search box → type e.g. `redis` → **Pull**.
2. Or open the image's page on Docker Hub (e.g.
   <https://hub.docker.com/_/redis>) and use the **Copy docker pull command**
   button on the right-hand side for the exact command.

**About the `latest` tag:** `docker pull python` pulls `python:latest`. That's
fine for quick experiments, but **not** for your own apps — a bare `latest`
breaks reproducibility (your teammate's pull may fetch a different version than
yours). Pin a version tag in Dockerfiles and compose files instead
(`python:3.11-slim`, `node:20-alpine`), which is exactly what this repo does.

### On macOS (Intel or Apple Silicon)

1. Download **"Docker Desktop for Mac"** from
   <https://www.docker.com/products/docker-desktop/>. Choose the **Apple Chip**
   build if you have an M1/M2/M3/M4 Mac; the Intel build otherwise.

2. Double-click the `.dmg`, drag the Docker icon into `Applications`, and open
   it. You'll be asked for your password to install helper tools — this is
   normal.

3. **Verify** in Terminal:

   ```bash
   docker version
   docker compose version
   ```

Both macOS and Windows installs give you a friendly GUI (Docker Desktop) plus a
CLI you can use from any terminal. The rest of this guide is CLI-only, because
that's what you'll script and use on servers.

---

## 3. Docker Hub — getting the right images

Docker Hub (<https://hub.docker.com/>) is the public registry where most
ready-made images live. You never build the world from scratch — you *start from*
a base image and add your app.

### Finding and checking images on Docker Hub

Before you `pull` anything, figure out *which* image you actually need. Here is
the full check-and-find workflow.

**Step 1 — search on hub.docker.com**

1. Go to <https://hub.docker.com/search>.
2. Type the technology you need, e.g. `postgres`, `python`, `redis`, `nginx`,
   `node`.
3. Read the result list:
   - **DOCKER OFFICIAL IMAGE** badge — vetted and maintained by the upstream
     project/Docker. Prefer these over everything else.
   - **Verified Publisher** badge — maintained by the company behind the
     software (e.g. `bitnami/`, `mongo/`, `microsoft/`).
   - **Stars** and **Downloads** — popularity and adoption signals.
   - The name — `postgres` (official) vs `sameersbn/postgresql` (community);
     pick the official one whenever it exists.
4. Click through to the image page (Step 2) before committing to anything.

**Step 2 — read the image page**

Each image page (`https://hub.docker.com/_/<name>`) answers "is this the right
image, and which tag?":

- **Overview tab → Supported tags** — the exact tag list, e.g. Postgres shows
  `15.7-bookworm, 15-bookworm, 15, latest`. Read this *before* pinning a tag so
  you never reference one that doesn't exist.
- **Tags tab** — every version/flavor with newest first; the place to confirm a
  specific tag like `python:3.11-slim` exists and is maintained.
- **Digest and size** — each tag carries a `sha256:` digest (an immutable
  fingerprint) and a size. Same digest = byte-identical image, guaranteed.
- **How to use this image** — official pages include ready-to-paste
  `docker run` examples and links to the full docs.
- **Pull count / last updated** — a tag that stopped getting updates months ago
  is a red flag for security and fixes.

**Step 3 — search from the CLI**

For quick lookups without leaving the terminal:

```bash
docker search postgres
docker search --filter "is-official=true" postgres   # official images only
docker search --limit 20 redis                       # cap the result count
```

The web search is richer (badges, filters, documentation), so use the site for
serious hunting and `docker search` for fast checks.

**Step 4 — pull it and verify locally**

```bash
docker pull postgres:15
docker image inspect postgres:15 --format '{{.Size}}'   # size in bytes
docker run --rm postgres:15 postgres --version          # confirm the version
```

`docker image inspect` prints the full image metadata (size, digest, exposed
ports, env vars, entrypoint); `docker run --rm <image> <cmd>` runs one command
and cleans up — the fastest way to prove an image is what you expect.

### How image names work

```
<registry>/<namespace>/<name>:<tag>
   docker.io   / postgres   / postgres : 15
                ^official   ^repo     ^tag
```

- **Official images** (Python, Node, Postgres, Redis, Nginx, Ubuntu, …) have no
  namespace prefix: `python`, `node`, `postgres`.
- **Community images** are namespaced, e.g. `bitnami/postgresql`.
- **Tag** = version/flavor selector. Always pin a tag; never use a bare
  `latest` for anything real.

### Picking the right tag (real examples from this repo)

| Image          | Tag used here   | Why                                                 |
|----------------|-----------------|-----------------------------------------------------|
| Python         | `python:3.11-slim` | Matches the backend's Python version; `slim` = smaller than full, still has apt. |
| Node           | `node:20-alpine`  | Alpine = minimal Linux (~5 MB base) — great for `npm ci` + build. |
| Nginx          | `nginx:alpine`    | Serves static frontend files; alpine keeps it tiny. |
| Postgres       | `postgres:15`     | Database version the app targets.                   |
| Redis          | `redis:7-alpine`  | Cache/queue; alpine flavor.                         |

**How to check tags:** follow the [check-and-find workflow](#finding-and-checking-images-on-docker-hub)
above (Tags tab on Docker Hub, or `docker search` / `docker pull` locally). Favor:
- `-slim` for Python: smaller image, same language features, faster pulls.
- `-alpine` for Node/Nginx/Redis: smallest official option.
- Major version tags (`postgres:15`) over `latest`, so nothing breaks silently.

### Pulling an image

```bash
docker pull python:3.11-slim
docker pull node:20-alpine
docker pull postgres:15
docker pull redis:7-alpine
```

You don't need `docker pull` for builds — `docker build` pulls base images
automatically. Pull is handy when you want to run/explore an image by itself:

```bash
docker run --rm -it python:3.11-slim python -c "print('hello from a container')"
```

### Production pulls: worked example

Goal: pick stable, small, pin-able images and pull them exactly as a
deployment Dockerfile would reference them. This example uses the same app
types as this repo — a Python/FastAPI backend and a Node/React frontend.

**Step 1 — decide the runtime version first.** Check what your app actually
needs (`python --version` / `node --version` locally, or the framework's
requirement — e.g. Django 5 needs Python 3.10+). Match the major/minor; don't
blindly grab `latest`. Confirm the tag exists on Docker Hub's Tags tab.

**Step 2 — pull the right Python image.**

For a Python web app (FastAPI/Django/Flask) in production, `python:3.11-slim`
(or `3.12-slim`) is the sweet spot: official, Debian-based so `apt` and native
wheels work, and much smaller than the full `python:3.11` image.

```bash
docker pull python:3.11-slim
docker pull python:3.12-slim
docker run --rm python:3.11-slim python --version   # verify -> Python 3.11.x
```

| Consider | Avoid | Why                                              |
|----------|-------|--------------------------------------------------|
| `python:3.11-slim` | `python:3.11` (full) | Slim ≈ 40 MB smaller, same language features.    |
| `python:3.12-slim` | `python:latest` | `latest` drifts; no reproducibility.             |
| `python:3.11-slim` | `python:3.11-alpine` | Alpine is musl-based; some native wheels break.  |

**Step 3 — build and run a production Python web app.** Using this repo's
backend as the example (Dockerfile is the same pattern as Section 5):

```bash
docker build -t ai-trader-backend ./service/server
docker run -d --name backend-prod -p 8000:8000 ai-trader-backend
```

**Step 4 — pull the right Node.js images.** For a Node/React web app you need
two images: `node:20-alpine` (or the current LTS major, e.g. `node:22-alpine`)
to compile, and `nginx:alpine` to serve the built static files in production.

```bash
docker pull node:20-alpine
docker pull nginx:alpine
docker run --rm node:20-alpine node --version   # verify
docker run -d --rm -p 8080:80 nginx:alpine      # sanity-check nginx serves :80
```

**Step 5 — build and run a production frontend.** Using this repo's frontend
(multi-stage Dockerfile — Node builds, Nginx serves):

```bash
docker build -t ai-trader-frontend ./service/frontend
docker run -d --name frontend-prod -p 3000:80 ai-trader-frontend
```

**Step 6 — production discipline checklist.**

- [ ] Pin exact tags in Dockerfiles and compose files (`python:3.11-slim`,
      `node:20-alpine`); never `latest`.
- [ ] Prefer Node **LTS majors** (`20`, `22`) over newest experimental majors.
- [ ] Re-pull before each deploy — `docker pull <image>` upgrades to the newest
      patch of the same tag.
- [ ] Prove the exact image you'll ship: `docker run --rm <image> <binary> --version`.
- [ ] Pull the runtime (`db`, `redis`, `postgres`) with pinned tags too, as this
      repo's `docker-compose.yml` does.

---

## 4. Essential Docker commands

The lifecycle in one line: **pull/build → run → ps → logs/exec → stop → rm**.

| Command                                   | What it does                                    |
|-------------------------------------------|-------------------------------------------------|
| `docker images`                           | List local images.                              |
| `docker pull <image>`                     | Download an image from Hub.                     |
| `docker build -t <name> <context>`        | Build an image from a Dockerfile.               |
| `docker run <image>`                      | Create + start a container from an image.       |
| `docker run -d -p 8000:8000 <image>`      | Run **detached** (`-d`, background) and map port.|
| `docker ps`                               | List **running** containers.                    |
| `docker ps -a`                            | List all containers (incl. stopped).            |
| `docker logs -f <container>`              | Stream a container's logs (`-f` = follow).      |
| `docker exec -it <container> <cmd>`       | Open a shell *inside* a running container.      |
| `docker stop <container>`                 | Gracefully stop a container.                    |
| `docker start <container>`                | Restart a stopped container.                    |
| `docker rm <container>`                   | Delete a (stopped) container.                   |
| `docker rmi <image>`                      | Delete an image.                                |
| `docker system df`                        | Show disk usage of images/containers.           |
| `docker system prune`                     | Remove unused data (add `-a` to also drop unused images). |

Containers can be referred to by **name** (assigned by you via `--name`) or by
the random **container id** Docker generates. Examples:

```bash
# interactive shell inside a running container
docker exec -it ai-trader-backend bash

# follow logs like `tail -f`
docker logs -f ai-trader-worker
```

### Running a container — anatomy of `docker run`

```bash
docker run -d --name my-app -p 8000:8000 -v ./data:/app/data -e DATABASE_URL=... my-image:latest
```

| Flag      | Meaning                                      |
|-----------|----------------------------------------------|
| `-d`      | Detached — run in background.                |
| `--name`  | Give the container a human-friendly name.    |
| `-p H:C`  | Map host port `H` to container port `C`.     |
| `-v H:C`  | Mount a host folder/volume at container path.|
| `-e KEY=V`| Set an environment variable inside.          |
| `--rm`    | Auto-delete the container when it exits (great for one-offs). |

---

## 5. Develop a Python web app with Docker

This repo's backend is a FastAPI app (`service/server/`). Its `Dockerfile` is
short — the standard pattern for a Python web service:

```dockerfile
# service/server/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Reading a Python Dockerfile, line by line

- `FROM python:3.11-slim` — start from the official Python 3.11 image.
- `ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1` — avoid `.pyc` files and
  log to stdout immediately (so `docker logs` shows real-time output).
- `WORKDIR /app` — all following commands run from `/app` inside the image.
- `COPY requirements.txt ./requirements.txt` — copy deps list **first**.
- `RUN pip install ... -r requirements.txt` — install deps. Copying
  requirements before the code lets Docker cache this expensive step; it only
  re-runs when `requirements.txt` changes.
- `COPY . /app` — copy the rest of the app code.
- `EXPOSE 8000` — documentation; the container listens on 8000.
- `CMD ["uvicorn", "main:app", ...]` — the command run when the container starts.

> Note: this Dockerfile runs uvicorn as root and has no `.dockerignore`. For a
> real project, add `.dockerignore` (exclude `.venv`, `__pycache__`, `.git`,
> `data/`) and a non-root user. See [Section 9](#9-cheat-sheet).

### Build and run it

From the repo root:

```bash
docker build -t ai-trader-backend ./service/server
docker run -d --name backend -p 8000:8000 ai-trader-backend
```

Then open <http://localhost:8000/docs> — FastAPI's auto docs. To stop:

```bash
docker stop backend && docker rm backend
```

### A "develop with hot reload" variant

For local dev you usually want code changes to appear without rebuilding the
image. Mount your source directory over the container copy and start uvicorn
with `--reload`:

```bash
docker run -d --name backend-dev \
  -p 8000:8000 \
  -v "$PWD/service/server":/app \
  -e AI_TRADER_API_BACKGROUND_TASKS=false \
  ai-trader-backend sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
```

Now edit a `.py` file locally and the server restarts automatically.

---

## 6. Develop a Node.js app with Docker

This repo's frontend is a React + Vite SPA (`service/frontend/`). Its Dockerfile
is a **multi-stage** build — the standard modern pattern for frontends:

```dockerfile
# service/frontend/Dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Why two stages?

- **Stage 1 (`build`, `node:20-alpine`):** installs dependencies and compiles
  the app (`npm run build` → `dist/`). Needs Node, npm, and lots of disk.
- **Stage 2 (`nginx:alpine`):** takes only the built `dist/` files and serves
  them with Nginx. The final image has **no Node at all** — it's tiny.

`COPY --from=build /app/dist /usr/share/nginx/html` copies the build output from
stage 1 into Nginx's document root. `nginx.conf` (in `service/frontend/`)
usually rewrites unknown routes to `index.html` so SPA client-side routing works.

### Build and run it

```bash
docker build -t ai-trader-frontend ./service/frontend
docker run -d --name frontend -p 3000:80 ai-trader-frontend
```

Open <http://localhost:3000>. The container listens on 80; you map it to host
port 3000 (`-p 3000:80`).

### Local-dev alternative without Docker

Because a Vite dev server is lighter than a full rebuild, many teams just run
`npm run dev` on the host during development and use Docker for CI/production.
That's fine — Docker isn't mandatory locally, it's what makes builds
reproducible everywhere else. A good middle ground:

```bash
# run the dev server on the host for hot reload
cd service/frontend && npm run dev
```

---

## 7. Orchestrate everything with Docker Compose

A single service is easy; this repo has **six** containers (backend, worker,
seed, frontend, postgres, redis). Compose defines them all in
`docker-compose.yml` and manages them as one unit.

### The one command to run this whole repo

```bash
docker compose up -d --build
```

- `up` — create and start containers.
- `-d` — detach (run in background).
- `--build` — rebuild images first (do this when code changed).

This builds backend/worker/seed/frontend, pulls `postgres:15` and
`redis:7-alpine` from Docker Hub, wires the network and volumes, and starts
everything. Open <http://localhost:3000> (frontend) and
<http://localhost:8000/docs> (API).

### Everyday compose commands

| Command                              | What it does                                |
|--------------------------------------|---------------------------------------------|
| `docker compose up -d --build`       | Build + start everything.                   |
| `docker compose ps`                  | Show container status.                      |
| `docker compose logs -f backend`     | Stream one service's logs.                  |
| `docker compose exec backend bash`   | Shell into a running service container.     |
| `docker compose restart backend`     | Restart one service.                        |
| `docker compose down`                | Stop and remove all containers/network.     |
| `docker compose down -v`             | Same, **and delete volumes** (wipes DB data!). |
| `docker compose pull`                | Pull all images used by the compose file.   |

> **Never** run `docker compose down -v` if you want to keep the Postgres data —
> it deletes the `postgres_data` volume (this repo's data lives there).

### Reading this repo's compose file

- `services` — each named service is one container.
- `build.context` — where the Dockerfile lives (`./service/server`, `./service/frontend`).
- `image: postgres:15` / `redis:7-alpine` — services without a `build` use a
  ready-made Hub image (see [Section 3](#3-docker-hub--getting-the-right-images)).
- `environment` — env vars, e.g. `DATABASE_URL` pointing at the `db` service
  name (compose resolves service names to hostnames).
- `ports` — `"8000:8000"` exposes a service to your machine.
- `depends_on` — startup order; `seed` waits for `backend` to be *healthy*.
- `volumes: postgres_data` — named volume so DB data survives restarts.
- `healthcheck` — how compose/Docker decides the backend is "up".

---

## 8. Troubleshooting

**"Cannot connect to the Docker daemon" / "Docker Engine stopped"**
Docker Desktop isn't running. Launch it and wait for the status to become
"Engine running", then retry.

**"Ports are not available: listen tcp 0.0.0.0:8000: bind: address already in use"**
Something already owns that port. Stop the conflicting process, or pick another
host port: `-p 8001:8000`.

**Container exits immediately (see `docker ps -a` shows Exited)**
Check the logs — the app probably crashed on startup:

```bash
docker logs <container>
```

**"pull access denied ... repository does not exist"**
The image name is wrong. Double-check namespace/tag on Docker Hub.

**Slow builds after tiny changes**
Reorder Dockerfiles so `COPY requirements.txt` (or `package*.json`) comes
*before* `COPY .`, letting Docker cache the dependency install. Keep changing
code out of the early layers.

**Changes not appearing when developing**
You edited files on the host but the container has its own copy — you must
either rebuild (`docker compose up -d --build`) or mount the source with `-v`
(see [Section 5](#5-develop-a-python-web-app-with-docker)).

**Windows-specific: line endings / WSL errors**
Ensure WSL 2 is installed (`wsl --version`). If `docker run` complains about
mounts, re-open your terminal from the same drive so paths match the mount root.

**Wiped my DB by accident**
`docker compose down -v` deleted `postgres_data`. Recover from a backup or
re-seed. This is exactly why volumes matter — and why you don't `-v` casually.

---

## 9. Cheat sheet

```bash
# images
docker build -t my-app ./dir          # build an image
docker images                          # list images
docker rmi my-app                      # delete an image

# run
docker run -d --name my-app -p 8000:8000 my-app   # background run, map port
docker run --rm -it python:3.11-slim bash         # throwaway shell

# containers
docker ps / docker ps -a               # running / all containers
docker logs -f my-app                  # follow logs
docker exec -it my-app bash            # shell inside a running container
docker stop my-app && docker rm my-app # clean stop + remove
docker system prune -a                 # free disk (removes unused images/containers)

# compose
docker compose up -d --build           # build + start everything
docker compose ps                      # status
docker compose logs -f backend         # logs for one service
docker compose exec backend bash       # shell into one service
docker compose down                    # stop everything (keeps volumes!)
docker compose down -v                 # stop + delete volumes (DANGER: wipes data)
```

### Minimum-good-practice checklist for your own Dockerfiles

- [ ] `FROM` a pinned tag (`python:3.11-slim`, `node:20-alpine`), never bare `latest`.
- [ ] Copy dependency manifests before the code to keep layer cache fast.
- [ ] Add a `.dockerignore` (`.venv`, `node_modules`, `.git`, `data/`, `__pycache__`).
- [ ] Use a multi-stage build for Node frontends (build → nginx).
- [ ] Run as a non-root user where possible.
- [ ] Use named volumes (or host mounts) for anything that must persist.

---

## Where this repo's Docker files live

| File                              | Purpose                                      |
|-----------------------------------|----------------------------------------------|
| `docker-compose.yml`              | Defines all six services (backend, worker, seed, frontend, db, redis). |
| `service/server/Dockerfile`       | Python/FastAPI backend image.                |
| `service/frontend/Dockerfile`     | Multi-stage Node build → Nginx image.        |
| `service/frontend/nginx.conf`     | Nginx config for the SPA (route fallback to `index.html`). |

Start here, then read `README.md` for the full architecture and deploy guide.
