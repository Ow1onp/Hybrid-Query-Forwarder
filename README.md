# Hybrid Query Forwarder (HQF) Server

## Introduction
The Hybrid Query Forwarder server, built with FastAPI, is an efficient and asynchronous forwarding server. It's designed to handle and forward queries from various sources such as Chatbots and local knowledge bases.

## Development Log

### Features
- Asynchronous network request handling for improved response efficiency.
- Flexible server configuration through environment variables.
- Clear error handling and logging.

### Functionality
- Forwards query requests to configured B and C servers.
- Decides whether to forward to C server based on the response from B server.
- Records exceptions during the request process in detail.

### Technology Stack
- Python
- FastAPI
- httpx (Asynchronous HTTP Client)

### Code Analysis
For a detailed code analysis, see [here](#code-analysis).

## Usage Guide

### Step 1: Download Server Source Files
Download the latest version of the HQF server source code from GitHub or similar platforms.

### Step 2: Run Chatbot and Local Knowledge Base
Ensure all components interacting with the HQF server (like Chatbot and local knowledge base) are running correctly.

### Step 3: Start the Server
1. Open a terminal or command-line interface.
2. Run `uvicorn main:app --host 0.0.0.0 --port 5000`.

### Step 4: Test with Postman
Send requests to your HQF server using Postman and observe the responses.

### Important Notes
- Ensure the server and Postman are on the same network.
- Check firewall settings to ensure they don't block the HQF server.
- Be aware of the security risks associated with using 0.0.0.0 as the host.

## Environment Configuration Checklist
- Ensure Python and FastAPI are installed.
- Set B_SERVER_URL and C_SERVER_URL as environment variables.
- Ensure httpx library is installed for asynchronous HTTP requests.

## Test Example
Here's a simple test instance to measure the response time of the server:
```python
import requests
import time


server_url = 'http://192.168.0.94:5000/forward/介绍一下云南的小吃'


num_requests = 100


response_times = []

for i in range(num_requests):
    start_time = time.time()
    response = requests.get(server_url)
    end_time = time.time()

    duration = end_time - start_time
    response_times.append(duration)

    
    if response.status_code == 200:
        print(f'Request {i + 1}/{num_requests}: {response.status_code} in {duration:.4f} seconds, Response: {response.text}')
    else:
        print(f'Request {i + 1}/{num_requests}: Error {response.status_code} in {duration:.4f} seconds')

average_time = sum(response_times) / len(response_times)
max_time = max(response_times)
min_time = min(response_times)
print(f'\nAverage response time: {average_time:.4f} seconds')
print(f'Max response time: {max_time:.4f} seconds')
print(f'Min response time: {min_time:.4f} seconds')

average_time = sum(response_times) / len(response_times)
print(f'\nAverage response time: {average_time:.4f} seconds')
```
Use this script to measure the average, max, and min response times for a set number of requests.

## Contribution
Contributions to the HQF server are welcome, whether they are feature suggestions, code improvements, or bug reports.

## License
This project is licensed under the MIT License. For more details, see the LICENSE file.

---

This README.md aims to provide a comprehensive understanding of the Hybrid Query Forwarder server, including its functionality, development log, and usage guide. It should assist developers in using and contributing to the project.
