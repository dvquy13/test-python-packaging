# Project Overview

This project demonstrates how to package a Python project with a `src` module structure for Docker deployment with **selective dependency installation**. It solves the common "No module named src" error by installing the project as a proper Python package using `pip install`, while ensuring Docker containers only include necessary dependencies.

## Key aspects:
- Uses `pyproject.toml` with **empty main dependencies** for selective installation
- **Selective dependency management** using optional-dependencies groups
- Installs the package globally in Docker containers with only production dependencies
- Enables `from src import ...` to work from any directory
- Includes debugging features for CI/CD troubleshooting
- Dynamic versioning using VERSION file
- Optimized Docker images with minimal dependencies

## Project structure:
- `src/` directory with model and utils modules
- `handler.py` TorchServe handler implementation
- `modelserving/pytorch_serving/Dockerfile` for containerization
- `VERSION` file for dynamic versioning (currently 1.0.0)
- Package installation approach instead of PYTHONPATH manipulation

## Selective Dependency Management Strategy

The project uses an **empty main dependencies** approach with optional-dependencies for selective installation:

### Configuration Pattern:
```toml
dependencies = []  # Empty main dependencies

[project.optional-dependencies]
dev = ["loguru>=0.7.3", "ruff>=0.11.12"]        # Development tools
production = ["python-dotenv>=1.0.0"]           # Production runtime
```


## uv Configuration
The project is configured for Python uv but maintains full compatibility with pip:
- `[tool.uv]` section for uv-specific settings
- Uses `[project.optional-dependencies]` instead of `[dependency-groups]` for pip compatibility
- Dynamic versioning with `version = {file = "VERSION"}`
- Docker uses `pip install .[production]` for selective installation

The solution makes the `src` module available system-wide by installing it as a proper Python package, eliminating dependency on working directory or environment variables, while ensuring optimal dependency management across environments.