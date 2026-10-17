# Study Guide: Understand Every Term in This Project

Read top to bottom once. Then open each file and match the comments to this guide.

## 1. The big picture in one paragraph

Developers change code all the time. Every change might break something. Instead of someone manually checking, we write **automated tests**. We put those tests in a **Docker container** so they run identically everywhere. Then **GitHub Actions** runs the container automatically on every change and every day, and saves a **report**. If anything breaks, the **badge** turns red and the team knows within minutes.

## 2. Glossary

| Term | Plain-English meaning |
|------|----------------------|
| **CI (Continuous Integration)** | Automatically building and testing code every time someone pushes a change. |
| **CD (Continuous Delivery/Deployment)** | Automatically releasing code that passed CI. This project covers the CI part (testing) and is the foundation for CD. |
| **Pipeline** | The automated sequence of steps: checkout, build, test, report. |
| **Workflow** | GitHub's name for one pipeline, defined in a YAML file. |
| **Trigger** | The event that starts a workflow (push, pull request, schedule). |
| **Cron** | A schedule format. `30 2 * * *` = minute 30, hour 2, every day. Times are in UTC. |
| **Runner** | The machine GitHub gives you to run the job (`ubuntu-latest`). |
| **Artifact** | A file produced by a run and saved for download (our test reports). |
| **Badge** | A small status image in the README showing whether the latest run passed. |
| **Docker** | Tool that packages an app plus everything it needs into one portable unit. |
| **Image** | The packaged snapshot (the recipe's result). Built with `docker build`. |
| **Container** | A running instance of an image. Started with `docker run`. Disposable. |
| **Dockerfile** | The text file with the steps to build an image. |
| **Volume mount (`-v`)** | Connects a folder on your machine to a folder in the container, so files (reports) survive. |
| **pytest** | Python's most popular test framework. Finds functions named `test_*` and runs them. |
| **Assertion (`assert`)** | A check. If it is false, the test fails. |
| **Fixture** | Reusable setup code (like a ready HTTP session) that tests receive as arguments. |
| **conftest.py** | The special file where shared fixtures live. |
| **Marker** | A label on tests (`@pytest.mark.api`) so you can run groups: `pytest -m api`. |
| **Parametrize** | Run one test function with many inputs. |
| **Smoke test** | A tiny set of the most critical checks, to quickly see if things are basically alive. |
| **REST API** | A web service you talk to with HTTP requests and get JSON back. |
| **HTTP status codes** | 200 OK, 201 Created, 404 Not Found, 500 Server Error. |
| **JSON** | Text format for data: `{"id": 1, "title": "hello"}`. |
| **Playwright** | Library that controls a real browser from code. |
| **Headless browser** | A browser with no visible window. Required on CI machines. |
| **Locator / selector** | How you point at an element: `#login-button` (CSS id). |
| **Flaky test** | A test that sometimes passes and sometimes fails without code changes. Usually caused by timing. |
| **Timeout** | Maximum time to wait before giving up. |
| **JUnit XML** | A standard test-report format that many CI tools understand. |

## 3. File-by-file walkthrough

**`tests/api/test_posts_api.py`**: sends HTTP requests to a fake API and asserts on status codes and data. It shows GET, POST, DELETE, filtering with query params, a 404 case, and `parametrize`.

**`tests/ui/test_login_ui.py`**: opens a browser, types into the login form, clicks, and asserts on what appears. `expect(...)` waits automatically, which avoids flaky `sleep()` calls.

**`tests/conftest.py`**: defines fixtures (`api_client`, `api_url`, `ui_url`). Notice the tests never create these themselves; pytest hands them in by matching argument names.

**`pytest.ini`**: configuration. `addopts` makes every run produce the HTML and XML reports. `markers` registers `api`, `ui`, `smoke`.

**`requirements.txt`**: exact versions of every library. Pinning versions makes builds reproducible.

**`Dockerfile`**: starts from Microsoft's Playwright image, installs Python packages, copies tests, sets `pytest` as the entry command. Dependencies are copied before code to use Docker's layer cache.

**`.github/workflows/ci.yml`**: the pipeline. `on:` is the triggers, `jobs:` holds the work, each `step` either `uses:` a prebuilt action or `run:`s a shell command. `if: always()` on the upload step guarantees reports are saved even when tests fail.

## 4. What happens when you push code (trace it)

1. You run `git push`.
2. GitHub sees the `push` trigger and reads `ci.yml`.
3. It starts an Ubuntu runner and checks out your code.
4. `docker build` follows the Dockerfile and creates the image.
5. `docker run` starts a container; `pytest` runs all tests inside it.
6. Reports are written to `/app/reports`, which is mounted to the runner's `reports/`.
7. The upload step stores them as the `test-reports` artifact.
8. The run is marked pass or fail, and the README badge updates.

## 5. Interview questions and answers

**What is CI/CD?**
CI automatically builds and tests every change so problems are caught early. CD automatically delivers changes that pass. My pipeline implements the CI/testing side.

**Why use Docker for tests?**
It gives an identical environment locally and in CI, so failures are about the code, not about differences in machines or installed versions.

**What triggers your pipeline?**
Pushes and pull requests to main, a daily cron schedule, and a manual button. The daily run catches problems that appear without any code change, like an external API changing.

**How do you keep UI tests from being flaky?**
I use Playwright's `expect`, which auto-waits for conditions, instead of fixed sleeps. I also set timeouts and keep each test independent.

**What is a fixture?**
Reusable setup/teardown code injected into tests by argument name. Mine provides the HTTP session and base URLs.

**Why upload artifacts even on failure?**
Failed runs are exactly when you need the report to see what broke. `if: always()` ensures the step runs regardless.

**How would you run only API tests?**
`pytest -m api`, using markers.

**What would you add next?**
Run API and UI as separate parallel jobs, test on multiple browsers with a matrix, add screenshots/traces on UI failure, send a Slack/email notification on failure, and add a CD step to deploy after tests pass.

## 6. Try these to learn faster

1. Break a test on purpose (change `== 100` to `== 99`), push, and watch the badge turn red. Open the report artifact and find the failure.
2. Add a new API test for `/comments/1`.
3. Change the cron time and read what the new schedule means.
4. Run `docker run --rm test-suite -m smoke` and see only the smoke tests run.
5. Add a second job in `ci.yml` that runs only `-m api`.
