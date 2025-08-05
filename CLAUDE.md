# Project Overview

This project demonstrates how to package a Python project with a `src` module structure for Docker deployment. It solves the common "No module named src" error by installing the project as a proper Python package using `pip install`.

## Key aspects:
- Uses `pyproject.toml` to define package configuration with uv support
- Installs the package globally in Docker containers
- Enables `from src import ...` to work from any directory
- Includes debugging features for CI/CD troubleshooting
- Dynamic versioning using VERSION file

## Project structure:
- `src/` directory with model and utils modules
- `modelserving/pytorch_serving/Dockerfile` for containerization
- `VERSION` file for dynamic versioning
- Package installation approach instead of PYTHONPATH manipulation

## uv Configuration
The project is configured for Python uv but maintains full compatibility with pip:
- `[tool.uv]` section for uv-specific settings
- `[dependency-groups]` for modern dependency management
- Dynamic versioning with `version = {file = "VERSION"}`
- Docker still uses regular `pip install` - no uv needed in containers

The solution makes the `src` module available system-wide by installing it as a proper Python package, eliminating dependency on working directory or environment variables.