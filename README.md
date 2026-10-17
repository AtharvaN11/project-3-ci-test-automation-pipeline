# CI/CD Test Automation Pipeline

![CI Tests](https://github.com/YOUR_USERNAME/ci-test-automation-pipeline/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10-blue)
![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC)
![Docker](https://img.shields.io/badge/runs%20in-docker-2496ED)

An automated test pipeline: **API tests** and **browser UI tests** written in Python, packaged in **Docker**, and run by **GitHub Actions** on every push, every pull request, and every day on a schedule. Test reports are saved as downloadable build artifacts.

> The badge above turns green when the latest run passes and red when it fails.
> (Replace `YOUR_USERNAME` in the badge URL with your GitHub username.)

## How it works

```
 git push / pull request / daily 08:00 IST
                 |
                 v
        GitHub Actions starts a fresh Linux VM
                 |
                 v
        docker build  ->  image with Python + browsers + tests
                 |
                 v
        docker run    ->  pytest runs inside the container
                 |            |-- API tests  (requests)
                 |            `-- UI tests   (Playwright + Chromium)
                 v
        reports/report.html + reports/junit.xml
                 |
                 v
        uploaded as "test-reports" artifact  +  badge updates
```

## Tech stack

| Tool | Why it's here |
|------|---------------|
| **Python + pytest** | Writes and runs the tests |
| **requests** | Sends HTTP calls for API tests |
| **Playwright** | Drives a real browser for UI tests |
| **pytest-html** | Generates the HTML report |
| **Docker** | Same environment locally and in CI |
| **GitHub Actions** | Runs everything automatically |

## What is tested

- **API** ([JSONPlaceholder](https://jsonplaceholder.typicode.com)): status codes, response fields, filtering, create/delete, 404 handling, parametrized checks.
- **UI** ([Sauce Demo](https://www.saucedemo.com)): valid/invalid/locked-out login, form validation, add to cart, logout.

## Project structure

```
.
├── .github/workflows/ci.yml   # the pipeline definition
├── tests/
│   ├── conftest.py            # shared fixtures (URLs, HTTP session)
│   ├── api/test_posts_api.py  # API tests
│   └── ui/test_login_ui.py    # UI tests
├── Dockerfile                 # how the test image is built
├── pytest.ini                 # pytest settings + reports + markers
├── requirements.txt           # pinned Python dependencies
└── docs/CONCEPTS.md           # beginner study guide (read this!)
```

## Run it locally

### Option A: with Docker (same as CI)

```bash
docker build -t test-suite .
mkdir -p reports
docker run --rm -v "$PWD/reports:/app/reports" test-suite
# run only one group:
docker run --rm -v "$PWD/reports:/app/reports" test-suite -m api
```

Open `reports/report.html` in your browser afterwards.

### Option B: without Docker

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
pytest                # everything
pytest -m api         # only API tests
pytest -m ui          # only UI tests
pytest -m smoke       # only the quick must-pass checks
```

## The CI pipeline

Defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml):

- **Triggers:** push to `main`, pull requests to `main`, daily cron (02:30 UTC), and a manual **Run workflow** button.
- **Steps:** check out code, build the Docker image, run the tests in a container, upload `reports/` as an artifact (even when tests fail).
- **Where to see results:** repo → **Actions** tab → click a run → **Artifacts** → `test-reports`.

## Set it up on your GitHub

1. Create a new empty repo named `ci-test-automation-pipeline` on GitHub.
2. In this folder run:
   ```bash
   git init
   git add .
   git commit -m "Add CI test automation pipeline"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ci-test-automation-pipeline.git
   git push -u origin main
   ```
3. Open the **Actions** tab. The first run starts automatically.
4. Once it is green, the badge in this README shows **passing**.

## Study guide

New to these terms? Read [docs/CONCEPTS.md](docs/CONCEPTS.md): a plain-English glossary, a walkthrough of each file, and interview questions with answers.
