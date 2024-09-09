FROM python:3.12-slim

#RUN apk add --no-cache git gcc musl-dev libffi-dev openssl-dev cargo nodejs npm
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libffi-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /wd/app
WORKDIR /wd/app

ARG GITHUB_ACCESS_TOKEN=''
ARG REPOSITORY_DESTINATION__APP='app'
ARG REPOSITORY_DESTINATION=${REPOSITORY_DESTINATION__APP}
ARG REPOSITORY_SOURCE='github.com/cqr-cryeye-forks/repo-scraper'
ARG REPOSITORY_COMMIT='b1b693d6b673c8fa3f716bd4188fc245a970503f'

RUN git clone --depth 1 \
        https://${GITHUB_ACCESS_TOKEN}@${REPOSITORY_SOURCE} \
        ${REPOSITORY_DESTINATION}

COPY . /wd/app

RUN pip install --no-cache-dir --requirement requirements.txt

RUN echo "Finding repo-scraper..." && find / -name "repo-scraper" && echo "Running repo-scraper --help" && repo-scraper --help || echo "repo-scraper not found"


#ENTRYPOINT ["python3", "run_repo-scraper.py", "--repo-url", "https://github.com/WebGoat/WebGoat", "--output", "data.json"]
#ENTRYPOINT ["python3", "run_repo-scraper.py", "--repo-url", "https://github.com/digininja/DVWA", "--output", "data.json"]
#ENTRYPOINT ["python3", "run_repo-scraper.py", "--repo-url", "https://github.com/OWASP/NodeGoat", "--output", "data.json"]
#ENTRYPOINT ["python3", "run_repo-scraper.py", "--repo-url", "https://github.com/juice-shop/juice-shop", "--output", "data.json"]
#ENTRYPOINT ["python3", "run_repo-scraper.py", "--repo-url", "https://github.com/appsecco/dvna", "--output", "data.json"]
#ENTRYPOINT ["python3", "run_repo-scraper.py", "--repo-url", "https://github.com/prateek147/DVIA-v2", "--output", "data.json"]
ENTRYPOINT ["python3", "run_repo-scraper.py", "--repo-url", "https://github.com/Evil2997/dummy_project", "--output", "data.json"]

#ENTRYPOINT ["python3", "run_repo-scraper.py", "--input-zip", "111.zip",  "--output", "data.json"]
#ENTRYPOINT ["python3", "run_repo-scraper.py", "--input-zip", "", "--output", "data.json", "--git-ignore"]
