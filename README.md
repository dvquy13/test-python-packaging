# Python Package Docker Setup

This repository demonstrates how to package a Python project with a `src` module structure so that `from src import ...` works correctly in Docker containers without "No module named src" errors.

## Project Structure

```
test-python-packaging/
├── src/
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   └── predictor.py
│   └── utils/
│       ├── __init__.py
│       └── preprocessing.py
├── pyproject.toml
├── modelserving/
│   └── pytorch_serving/
│       └── Dockerfile
└── README.md
```

## Problem

When deploying Python projects with `src` module structure to Docker, you often encounter:
```
ModuleNotFoundError: No module named 'src'
```

This happens because Python can't find the `src` module in the container's Python path.

## Solution

We use the **package installation approach** with **selective dependency installation** which installs the project as a proper Python package using `pip install`. This ensures the `src` module is available system-wide while only installing required dependencies for each environment.

### Key Components

1. **pyproject.toml**: Defines the package configuration with selective dependency groups
2. **Dockerfile**: Installs the package with only production dependencies
3. **Debugging**: Shows build context to help with CI/CD setup
4. **Selective Dependencies**: Uses optional-dependencies to control what gets installed

## Dockerfile Explanation

The `modelserving/pytorch_serving/Dockerfile` uses this strategy:

```dockerfile
# Copy only necessary files (not everything)
COPY pyproject.toml /tmp/package/
COPY src/ /tmp/package/src/

# Install package with only production dependencies
RUN pip install '/tmp/package/[production]'

# Work from different directory to prove it works
WORKDIR /workspace
```

### Why This Works

1. **Package Installation**: `pip install` makes `src` available in Python's site-packages
2. **Global Availability**: Can import `from src import ...` from any directory
3. **No PYTHONPATH Required**: Doesn't rely on current working directory or environment variables
4. **Clean Separation**: Source code location is independent of runtime location
5. **Selective Dependencies**: Only installs dependencies needed for specific environments (production vs development)

## Testing Commands

### 1. Build the Docker Image

```bash
# From repository root
docker build -f modelserving/pytorch_serving/Dockerfile -t test-src-package .
```

### 2. Test Basic Import

```bash
# Test that src modules can be imported
docker run --rm test-src-package
```

Expected output:
```
Successfully imported src modules from installed package!
```

### 3. Test from Different Directory

```bash
# Verify imports work from any directory (not just where source code is)
docker run --rm test-src-package python -c "
import sys; 
print('Working from:', sys.path[0]); 
from src.model import predictor; 
from src.utils import preprocessing; 
print('All imports successful!')
"
```

Expected output:
```
Working from: 
All imports successful!
```

### 4. Verify Only Production Dependencies Are Installed

```bash
# Check which packages are installed (should only see production dependencies)
docker run --rm test-src-package pip list
```

Expected to see:
- python-dotenv (production dependency)  
- NOT ruff and loguru (dev dependencies)

```bash
# Verify dev dependencies are NOT installed
docker run --rm test-src-package python -c "
import sys
try:
    import ruff
    print('ERROR: ruff (dev dependency) should not be installed!')
    sys.exit(1)
except ImportError:
    print('✓ ruff (dev dependency) correctly not installed')

try:
    import loguru  
    print('ERROR: loguru (dev dependency) should not be installed!')
    sys.exit(1)
except ImportError:
    print('✓ loguru (dev dependency) correctly not installed')

try:
    import dotenv
    print('✓ python-dotenv (production dependency) correctly installed')
except ImportError:
    print('ERROR: python-dotenv (production dependency) missing!')
    sys.exit(1)
"
```

Expected output:
```
✓ ruff (dev dependency) correctly not installed
✓ loguru (dev dependency) correctly not installed  
✓ python-dotenv (production dependency) correctly installed
```

### 5. Debug Build Context (if needed)

The Dockerfile includes debugging information that shows:
- What files are available in the build context
- Directory structure validation
- Contents of pyproject.toml

This helps when setting up CI/CD pipelines like GitLab CI.

## Alternative Approaches (Not Recommended)

## CI/CD Considerations

### GitLab CI Build Context

The `docker build` command in GitLab CI typically runs from the repository root:

```yaml
# .gitlab-ci.yml
build:
  script:
    - docker build -f modelserving/pytorch_serving/Dockerfile -t my-image .
```

If your CI runs from a different directory, the debugging output will help identify the issue.

## Selective Dependency Management

This project implements **selective dependency installation** to ensure Docker containers only include necessary dependencies while maintaining full functionality for development environments.

### Key Strategy: Empty Main Dependencies

The solution uses an **empty main dependencies** approach:

```toml
dependencies = []  # No main dependencies

[project.optional-dependencies]
dev = [
    "loguru>=0.7.3",    # Development/debugging
    "ruff>=0.11.12"     # Linting
]
production = [
    "python-dotenv>=1.0.0",  # Production runtime
]
```

### Benefits

1. **Docker Optimization**: `pip install .[production]` only installs production dependencies
2. **Development Flexibility**: `uv sync --extra dev --extra production` installs everything locally
3. **Clean Separation**: Clear distinction between dev and production requirements
4. **Cost Effective**: Smaller Docker images with fewer security vulnerabilities

### Development Environment Commands

```bash
# Install all dependencies (recommended for development)  
uv sync --extra dev --extra production

# Install only dev dependencies
uv sync --extra dev

# Install only production dependencies  
uv sync --extra production

# Install all optional dependencies
uv sync --all-extras
```

### Legacy pip Support

For environments using pip instead of uv:

```bash
# Install all dependencies
pip install -e .[dev,production]

# Install only production dependencies
pip install -e .[production]
```

## Package Configuration

For the Docker packaging approach to work, your `pyproject.toml` must be configured to include the `src` module. Here's how to set it up:

### Required Configuration

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your-package-name"
version = "1.0.0"
description = "Your package description"
requires-python = ">=3.7"
dependencies = [
    # Add your dependencies here
]

[tool.setuptools.packages.find]
where = ["."]
include = ["src*"]
```

### Key Configuration Explained

- **`where = ["."]`**: Tells setuptools to look for packages in the current directory (repository root)
- **`include = ["src*"]`**: Tells setuptools to include any package that starts with "src" (i.e., the `src` directory)
- **`[build-system]`**: Specifies that we're using setuptools to build the package
- **`[project]`**: Defines basic package metadata

### How It Works

When you run `pip install /tmp/package/`, setuptools:

1. Reads the `pyproject.toml` configuration
2. Discovers the `src` directory based on `include = ["src*"]`
3. Installs `src` as a Python package in site-packages
4. Makes `from src import ...` available globally

### Alternative Configurations

If your source code is structured differently, adjust accordingly:

```toml
# If your modules are in the root directory
[tool.setuptools.packages.find]
where = ["."]
include = ["mymodule*", "utils*"]

# If your source code is in a different directory
[tool.setuptools.packages.find]
where = ["source"]
include = ["*"]
```