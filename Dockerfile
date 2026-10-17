# ---------------------------------------------------------------
# Dockerfile = a recipe that builds an "image": a snapshot of a
# computer with everything the tests need already installed.
# Anyone who runs this image gets the exact same environment, so
# "it works on my machine" stops being a problem.
# ---------------------------------------------------------------

# Start from Microsoft's official image that already contains Python,
# Chromium/Firefox/WebKit and all the system libraries browsers need.
# The version here must match playwright==... in requirements.txt.
FROM mcr.microsoft.com/playwright/python:v1.63.0-jammy

# All following commands run inside this folder in the image.
WORKDIR /app

# Copy requirements first and install them BEFORE copying the rest of the code.
# Docker caches each step ("layer"), so when only test code changes,
# it skips the slow pip install on the next build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual project files.
COPY pytest.ini .
COPY tests ./tests

# What runs when you start a container from this image.
# Extra arguments passed to `docker run` are appended, e.g. `-m api`.
ENTRYPOINT ["pytest"]
