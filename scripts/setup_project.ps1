$ErrorActionPreference = 'Stop'

$PROJECT_NAME = 'stock-predictor'
$DJANGO_PROJECT = 'stock_api'
$DJANGO_APP = 'stocks'

Write-Host 'Setting up project structure...'

# -----------------------------
# Create directories
# -----------------------------
New-Item -ItemType Directory -Force -Path backend, ml, scripts | Out-Null
New-Item -ItemType Directory -Force -Path `
    ml\data, `
    ml\features, `
    ml\training, `
    ml\evaluation, `
    ml\artifacts\short, `
    ml\artifacts\medium, `
    ml\artifacts\long | Out-Null

# -----------------------------
# Initialize uv environment
# -----------------------------
Write-Host 'Initializing uv environment...'
uv sync

# -----------------------------
# Create Django project
# -----------------------------
# Write-Host '🧱 Creating Django project...'
# Set-Location backend
# uv run django-admin startproject $DJANGO_PROJECT .
# uv run python manage.py startapp $DJANGO_APP

# -----------------------------
# Create service structure
# -----------------------------
New-Item -ItemType Directory -Force -Path stocks\services | Out-Null
New-Item -ItemType File -Force -Path `
    stocks\services\__init__.py, `
    stocks\services\data_fetch.py, `
    stocks\services\features.py, `
    stocks\services\services.py, `
    stocks\services\inference.py | Out-Null

# -----------------------------
# Create ML training scripts
# -----------------------------
Set-Location ml\training
New-Item -ItemType File -Force -Path `
    train_short.py, `
    train_medium.py, `
    train_long.py | Out-Null

# -----------------------------
# Create placeholders
# -----------------------------
Set-Location ..\..
New-Item -ItemType File -Force -Path README.md, .gitignore | Out-Null

Write-Host '✅ Project setup complete.'
Write-Host 'Next steps:'
Write-Host '1. uv run python backend\manage.py migrate'
Write-Host '2. uv run python backend\manage.py runserver'
