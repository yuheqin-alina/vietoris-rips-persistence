# Vietoris–Rips Filtration

Interactive web demo of the [Vietoris–Rips filtration](https://en.wikipedia.org/wiki/Vietoris%E2%80%93Rips_filtration) for a 2D point cloud. Grow disks of radius ε and watch edges, triangles, and 3-simplices appear in the Rips complex.

The right panel shows a **persistence barcode** computed with **[GUDHI](https://gudhi.inria.fr/)** (Z₂, full Rips filtration up to dimension 3).

## Features

| Panel | What it shows |
|--------|----------------|
| **Rips complex** | 5–30 sample points (default 15), disks B(pᵢ, ε), edges, triangles, and 3-simplices (4-cliques) |
| **Persistence barcode** | H₀, H₁, H₂ intervals from GUDHI |

**Interactions**

- **Filtration ε** — slider and number field
- **Animate ε** — smooth auto-increase of ε
- **Point cloud models** — ring, three separated rings, two rows, figure eight, grid, tight cluster, or random
- **Load model** — resample at the current point count

## Quick start

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the server (serves the UI and GUDHI API):

```bash
python server.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

> Opening `index.html` directly shows the VR panel only; the barcode needs `python server.py` for `/api/persistence`.

## Mathematics (short)

**Filtration.** For each point pᵢ, use the closed disk B(pᵢ, ε). The Vietoris–Rips complex adds:

- a **vertex** for each point;
- an **edge** between pᵢ, pⱼ when ‖pᵢ − pⱼ‖ ≤ 2ε;
- a **triangle** when all three pairwise edges exist;
- a **3-simplex** on four vertices when all six pairwise edges exist.

**Filtration value.** Edges appear at ε = ‖pᵢ − pⱼ‖ / 2. GUDHI uses edge length internally; the barcode converts to ε = distance / 2 to match the left panel.

## Project structure

```
├── index.html       # Web UI (VR + persistence barcode)
├── server.py        # Flask app + GUDHI API
├── requirements.txt
└── README.md
```

## Publish on GitHub

This repo is **source code** on GitHub. To let people **use the live demo**, also deploy the Python server (see below). GitHub Pages alone cannot run GUDHI.

### 1. Create the repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Name it e.g. `vietoris-rips-persistence`
3. Public, **do not** add a README (you already have one)
4. Create repository

### 2. Push your code from your Mac

```bash
cd /Users/f98liocarrown/Downloads/vietoris-rips-persistence-main

git init
git add index.html server.py requirements.txt README.md .gitignore
git commit -m "Vietoris–Rips demo with GUDHI persistence barcode"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/vietoris-rips-persistence.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Use a [Personal Access Token](https://github.com/settings/tokens) if Git asks for a password.

`.gitignore` keeps `.venv/` and large local files out of the repo.

### 3. Deploy so everyone can open the app (recommended: Render)

Free tier works for demos.

1. Sign in at [render.com](https://render.com) and connect your GitHub account
2. **New → Web Service** → select your repo
3. Settings:
   - **Runtime:** Python 3
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn server:app --bind 0.0.0.0:$PORT`
4. Create Web Service

Render gives a URL like `https://vietoris-rips-persistence.onrender.com`. Share that link—visitors get the full UI and barcode.

Other options: Railway, Fly.io, or a VPS with the same start command.

### What visitors see

| Link type | Works? |
|-----------|--------|
| GitHub repo page | Code + README only |
| Deployed URL (Render, etc.) | Full interactive demo |
| Raw `index.html` on GitHub | VR only; barcode API missing |

## License

Add your preferred license (e.g. MIT) if you publish the repository.
