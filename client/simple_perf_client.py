import time
import requests
import json

# Server Base URL
BASE_URL = "http://localhost:8000"

# Function to measure API performance
def measure_api_performance(endpoint, method="GET", payload=None):
    # Measure start time
    start_time = time.time()

    # Make the API call
    if method == "GET":
        response = requests.get(f"{BASE_URL}{endpoint}")
    elif method == "POST":
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
    elif method == "DELETE":
        response = requests.delete(f"{BASE_URL}{endpoint}")
    else:
        raise ValueError("Unsupported HTTP method")

    # Measure end time
    end_time = time.time()
    
    # Calculate total request time in milliseconds
    request_time_ms = round((end_time - start_time) * 1000, 2)

    # Calculate response size in bytes
    response_size_bytes = len(response.content)

    # Parse server response
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = {"error": "Invalid JSON response"}

    # Extract server-side metrics from response
    server_metrics = response_data.get("metrics", [])
    server_processing_time_ms = sum(metric["duration_ms"] for metric in server_metrics)

    # Calculate network time
    network_time_ms = round(request_time_ms - server_processing_time_ms, 2)

    # Return detailed results
    return {
        "endpoint": endpoint,
        "request_time_ms": request_time_ms,
        "server_processing_time_ms": server_processing_time_ms,
        "network_time_ms": network_time_ms,
        "response_size_bytes": response_size_bytes,
        "metrics": server_metrics
    }

# Test Scenario
def run_performance_test():
    scenarios = [
        {"endpoint": "/populate_random_100/", "method": "POST"},
        {"endpoint": "/populate_random_1000/", "method": "POST"},
        {"endpoint": "/fetch/", "method": "GET"},
        {"endpoint": "/clear/", "method": "DELETE"}
    ]

    for scenario in scenarios:
        result = measure_api_performance(
            endpoint=scenario["endpoint"],
            method=scenario["method"]
        )
        print(f"\nTesting {scenario['endpoint']} [{scenario['method']}]")
        print(f"Request Time (ms): {result['request_time_ms']}")
        print(f"Server Processing Time (ms): {result['server_processing_time_ms']}")
        print(f"Network Time (ms): {result['network_time_ms']}")
        print(f"Response Size (bytes): {result['response_size_bytes']}")
        print(f"Metrics: {json.dumps(result['metrics'], indent=2)}")

# Run the test
if __name__ == "__main__":
    run_performance_test()
