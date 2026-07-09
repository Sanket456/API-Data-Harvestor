# API-Data-Harvestor

🏗️ Resilient API Data Harvester (Bronze Layer Ingestion)
A robust Data Engineering extraction pipeline built to reliably pull live financial data from public APIs and land it into a raw storage layer.
This project simulates the "Extract" and "Load" phases of a modern ELT (Extract, Load, Transform) pipeline, preparing raw JSON payloads for downstream tabular processing.


🧠 The Engineering Challenge
When pulling high volumes of data from external REST APIs, pipelines often fail due to server rate-limiting (429 Too Many Requests), temporary server crashes (500 Internal Server Error), or sudden network drops. A naive requests.get() script will immediately crash, requiring manual engineering intervention.
The Solution: Adaptive Resilience
This pipeline implements an Exponential Backoff Algorithm to guarantee data delivery.
If the API rejects the request, the engine intercepts the error rather than crashing.
It pauses execution, dynamically doubling the wait time between each retry (e.g., 1s, 2s, 4s, 8s).
It masks the automated request using standard browser User-Agent headers to bypass basic bot-blocking middleware.


🏗️ Architecture: The Bronze Layer
This script strictly adheres to the Medallion Architecture pattern (commonly used in Databricks and PySpark environments).
Extract: Connects to the CoinGecko API to pull the top 50 cryptocurrencies by market cap.
Load (Bronze Layer): The data is intentionally not cleaned during this step. It is dumped as a raw, heavily nested JSON file (raw_market_data.json) directly into local storage. This preserves the immutable historical state of the payload before any transformations occur.

🚀 Quick Start (Running the Pipeline)

1. Install dependencies:

pip install requests


2. Execute the ingestion script:

python api_harvester.py


3. Check the Output:
Upon successful execution, the script will automatically generate a data/ directory and drop the raw JSON payload inside.
