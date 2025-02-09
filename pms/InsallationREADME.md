# Frappe Bench Installation and Setup

This README provides a step-by-step guide on how to install and set up Bench, the command-line tool for managing Frappe applications and sites.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed:

*   Python
*   Node.js >= 18
*   Redis

## Installation

1.  **Install Bench:**

    If you haven't installed Bench yet, follow the official [Frappe installation guide](https://frappeframework.com/docs/v14/user/en/installation). After successful installation, you should be able to run commands starting with `bench`.

2.  **Verify Installation:**

    Open your terminal and run the following command to check the Bench version:

    ```
    bench --version
    ```

    This should output the installed Bench version (e.g., `5.1.0`).

## Setup

1.  **Create the `frappe-bench` Directory:**

    This directory will house your apps and sites. Run the following command to create it:

    ```
    bench init frappe-bench
    ```

    This command performs the following actions:

    *   Creates a Python virtual environment under the `env` directory.
    *   Fetches and installs the `frappe` app as a Python package.
    *   Installs Node.js modules for `frappe`.
    *   Builds static assets.

2.  **Navigate to the `frappe-bench` Directory:**

    ```
    cd frappe-bench
    ```

## Directory Structure

The `frappe-bench` directory contains the following structure:

frappe-bench/
├── Procfile
├── apps
│ └── frappe
├── config
│ ├── pids
│ ├── redis_cache.conf
│ ├── redis_queue.conf
│ └── redis_socketio.conf
├── env
│ ├── bin
│ ├── include
│ ├── lib
│ └── share
├── logs
│ ├── backup.log
│ └── bench.log
└── sites
├── apps.txt
├── assets
└── common_site_config.json


*   **`env`**: Python virtual environment.
*   **`config`**: Configuration files for Redis
*   **`logs`**: Log files for each process (web, worker).
*   **`sites`**: Directory for sites.
*   **`assets`**: Static assets served via Nginx in production.
*   **`apps.txt`**: List of installed Frappe apps.
*   **`common_site_config.json`**: Site configuration available to all sites.
*   **`apps`**: Directory for apps.
*   **`frappe`**: The Frappe app directory.
*   **`Procfile`**: List of processes that run in development.

## Starting the Bench Server

1.  **Start the Server:**

    Inside the `frappe-bench` directory, run the following command to start the Frappe web server:

    ```
    bench start
    ```

    This command starts several processes, including:

    *   A Python web server (Gunicorn)
    *   Redis servers for caching, job queuing, and Socket.IO pub/sub
    *   Background workers
    *   A Node.js server for Socket.IO
    *   A Node.js server for compiling JS/CSS files

    Example output:

    ```
    18:16:36 system | redis_cache.1 started (pid=11231)
    18:16:36 system | redis_socketio.1 started (pid=11233)
    18:16:36 system | redis_queue.1 started (pid=11234)
    18:16:36 system | socketio.1 started (pid=11236)
    18:16:36 system | web.1 started (pid=11237)
    18:16:36 system | watch.1 started (pid=11240)
    18:16:36 system | schedule.1 started (pid=11241)
    18:16:36 system | worker_short.1 started (pid=11242)
    ...
    ```

    The web server will listen on port `8000`.

2.  **Keep the Terminal Running:**

    Do not close the terminal where `bench start` is running. Open another terminal and navigate to the `frappe-bench` directory to execute further Bench commands.

## Next Steps

Now that you have successfully installed and set up Bench, the next step is to create an app and a site where this app will be installed. You can refer to the Frappe documentation for guidance on creating apps and sites.
