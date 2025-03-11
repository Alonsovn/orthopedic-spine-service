# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

ENV PYTHONPATH=.


# Add and configure a non-root user
RUN addgroup --system appuser && adduser --system --ingroup appuser -u 999 appuser

# Ensure the working directory is owned by the non-root user
RUN chown -R appuser:appuser /app && \
    chown -R appuser:appuser /tmp

COPY /start.sh /start.sh
RUN chmod a+x /start.sh

# Switch to the non-root user
USER 999

# Expose the FastAPI port
EXPOSE 8000

# Configure container start behaviour
ENTRYPOINT ["/start.sh"]