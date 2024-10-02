# ktaga-lab

## Overview
ktaga-lab contains programs and dependencies for experiments in Onolab.
This repository is designed to facilitate various experimental setups and data analysis tasks.

## Prerequisites
To run this project, you need to install either of the following dependencies:
- pip
- uv (recommended)
- Docker (for analysis only)

Docker can be used for only data analysis tasks. For experiment setup, you need to install the dependencies using pip or uv.

## Setup

### Installation using uv

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

### Deploy using Docker

1. Copy .env.example to .env and set the environment variables.
You can set the following environment variables:

- NotebookDir: The directory where the jupyter notebooks are stored. By default, it is set to OneDrive directory, which is shared between the host and the container.

2. **Clone the repository:**
    ```bash
    git clone https://github.com/hoopdev/ktaga-lab.git
    cd ktaga-lab
    ```

2. **Run the Docker compose:**
    ```bash
    docker compose up
    ```

## Access the application

Open your web browser and navigate to `http://localhost:8888` to access the JupyterLab interface.