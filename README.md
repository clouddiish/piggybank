# piggybank

Piggybank is a full-stack web application built with FastAPI, React.js, and PostgreSQL. The project is containerized with Docker for local development and deployed to Microsoft Azure using managed cloud services and GitHub Actions CI/CD.

## features

- REST API built with FastAPI
- PostgreSQL database integration with Alembic migrations
- React.js and Bootstrap frontend
- Docker Compose local development environment
- cloud deployment on Azure
- automatic CI/CD deployment with GitHub Actions

## local development

### dependencies

- Docker
- Docker Compose

### installation

- clone the repository or download the code files
- copy the `.env-example` files from `backend/` and `frontend/` to `.env` and fill in the required environmental variables

### run

- start all services:

```bash
docker compose up --build
```

### output

the application will start with:

- PostgreSQL database
- FastAPI backend: view FastAPI interactive documentation at http://localhost:8000/docs
- React frontend: view at http://localhost:3000

### run backend tests locally

- go to `backend/` dir
- ensure Python 3.13.2 and all project dependencies are installed

```
pip install -r requirements.txt
```

- go to `backend/tests/` dir
- run all tests

```
pytest
```

## Azure deployment

### services used

| component | azure Service |
|---|---|
| Database | Azure Database for PostgreSQL Flexible Server |
| Container Registry | Azure Container Registry |
| Backend | Azure Container Apps |
| Frontend | Azure Static Web Apps |

## CI/CD

Automatic deployment on changes in the `main` branch is configured with GitHub Actions.

### required GitHub Secrets

```text
AZURE_CLIENT_ID
AZURE_STATIC_WEB_APPS_API_TOKEN
AZURE_SUBSCRIPTION_ID
AZURE_TENANT_ID
REACT_APP_API_BASE_URL
```