# ktaga-lab

## Overview
ktaga-lab contains programs for experiments in Onolab. This repository is designed to facilitate various experimental setups and data analysis tasks.

## Features
- Experiment setup scripts
- Data analysis tools
- Reproducible research environment

## Prerequisites
To run this project, you need to install either of the following dependencies:
- pip
- uv (recommended)
- Docker (for analysis only)

Docker can be used for only data analysis tasks. For experiment setup, you need to install the dependencies using pip or Poetry.

## Setup

### Installation using Poetry

1. **Install uv:**
    - **Windows (PowerShell):**
    ```bash
    winget install astral-sh.uv
    ```

    - **Linux:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    - **macOS:**
    ```bash
    brew install uv
    ```



2. **Setup environment**

    ```bash
    uv init
    ```
    This command will create a `pyproject.toml` file in the current directory.

    ```bash
    uv venv
    ```
    This command will create a virtual environment in the current directory.


3. **Install ktaga-lab:**
    ```bash
    uv add ktaga-lab
    uv sync -U
    ```

4. **Run the application:**
    ```bash
    uv run jupyter lab
    ```

### Installation using pip

You can also install the package using pip. Run the following command to install the package:
```bash
pip install ktaga-lab
```

### Installation using Docker

1. **Clone the repository:**
    ```bash
    git clone https://github.com/hoopdev/ktaga-lab.git
    cd ktaga-lab
    ```

2. **Build the Docker image:**
    Use the `Dockerfile` provided in the repository:
    ```bash
    docker build -t ktaga-lab .
    ```

3. **Run the Docker container:**
    ```bash
    docker run --rm -p 8888:8888 ktaga-lab
    ```

## Access the application

Open your web browser and navigate to `http://localhost:8888` to access the JupyterLab interface.