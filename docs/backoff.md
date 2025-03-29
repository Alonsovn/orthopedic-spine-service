### How the Retry Mechanism Works

1. Uses backoff.expo (Exponential Backoff)
* First retry after ~1s, second ~2s, third ~4s, etc.
* Prevents overloading the database by spacing out retry attempts.

2. Retries on OperationalError
* Handles transient database issues (e.g., connection timeouts, deadlocks).

3. Limits Retries to 3 Attempts
* Avoids infinite loops by stopping after 3 failed attempts.

4. Custom Logging with backoff_handler
* Logs each retry attempt and the exception that caused it.