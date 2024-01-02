# Hybrid Query Forwarder (HQF) Server Guide

## Introduction
The Hybrid Query Forwarder (HQF) server is a port forwarding server designed to streamline the process of request forwarding and efficiently route queries to a designated target. This guide provides basic steps for setting up and testing your HQF server, making it accessible for users without an extensive background in networking.

## Step 1: Downloading the Server Source Files
The source code for the HQF server can be downloaded from the provided resources. These files are typically hosted on code-sharing platforms like GitHub. Follow the instructions on the platform to download the files, ensuring you obtain the latest version to avoid potential compatibility issues.

## Step 2: Running the Chatbot and Local Knowledge Base
Before launching the HQF server, it is necessary to start the components that will interact with the server, which usually include a Chatbot and a local knowledge base. Follow the instructions for these components to ensure they are running correctly before initiating the HQF server.

## Step 3: Launching the Server
After starting the necessary auxiliary components, you can proceed to launch the HQF server:

1. Open your terminal or command line interface.
2. Enter the following command to start the service:
   ```
   uvicorn main:app --host 0.0.0.0 --port 5000
   ```
   This command tells Uvicorn, an AsyncIO server, to run `main:app`, where `main` is typically the Python file name and `app` is the FastAPI application instance in the file. The `--host 0.0.0.0` allows the server to be open to all network interfaces, while `--port 5000` specifies that the service runs on port 5000.

## Step 4: Testing with Postman
Postman is a popular API development tool used for testing server responses. Here’s how to test your HQF server with Postman:

1. Open Postman.
2. Enter your HQF server URL in the following format:
   ```
   http://192.168.0.xxx:5000/forward/xxxx
   ```
3. As an example, if you want to ask about "snacks in Yunnan," you would enter:
   ```
   http://192.168.0.94:5000/forward/Introduce snacks in Yunnan
   ```
4. Send the request and wait to view the response.

`192.168.0.xxx` represents your host machine's LAN IP address, and `xxxx` represents the question you wish to ask.

## Important Notes
- Ensure that your server and Postman are on the same network.
- If you encounter connection issues, check if your firewall settings are blocking the HQF server.
- Using `0.0.0.0` as the host makes your service visible to all devices on the network, so be aware of potential security risks.

By following these steps, you should now be able to successfully set up and test your Hybrid Query Forwarder server, enjoying an efficient and seamless query forwarding experience.
