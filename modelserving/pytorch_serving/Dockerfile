FROM python:3.11-slim

# Copy only the necessary files for package installation
COPY pyproject.toml /tmp/package/
COPY src/ /tmp/package/src/

# Debug: Show what's in the build context and validate structure
RUN echo "=== BUILD CONTEXT VALIDATION ===" && \
    echo "Build context contents:" && \
    ls -la /tmp/package/ && \
    echo "=== SOURCE CODE CHECK ===" && \
    ls -la /tmp/package/src/ && \
    echo "=== PYPROJECT.TOML CHECK ===" && \
    cat /tmp/package/pyproject.toml && \
    echo "=========================="

# Validate required files exist
RUN if [ ! -f /tmp/package/pyproject.toml ]; then \
        echo "ERROR: pyproject.toml not found in build context!"; \
        exit 1; \
    fi && \
    if [ ! -d /tmp/package/src ]; then \
        echo "ERROR: src directory not found in build context!"; \
        exit 1; \
    fi

# Install the package globally from the temporary location
RUN pip install /tmp/package/

# Clean up the temporary files
RUN rm -rf /tmp/package

# Set working directory to a different location
WORKDIR /workspace

# Default command for testing - this will only work if the package is properly installed
CMD ["python", "-c", "from src.model.predictor import *; from src.utils.preprocessing import *; print('Successfully imported src modules from installed package!')"]