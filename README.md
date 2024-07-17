# 🚀 Application Setup Guide

This guide will walk you through the process of setting up and running the application. Follow these steps to get started!

## 📋 Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed on your system
- [OpenAI API key](https://platform.openai.com/account/api-keys)

## 🛠️ Setup Instructions

### 1. Create and Activate Conda Environment

```bash
# Create a new conda environment
conda create --name myenv python=3.12.4

# Activate the environment
conda activate myenv
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root and add your OpenAI API key:

```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual OpenAI API key.

### 4. Create Chroma Vector DB

Run the `create_db` notebook to create the Chroma Vector DB:

```bash
jupyter notebook create_db.ipynb
```

Execute all cells in the notebook to create the database.

### 5. Query ChatGPT with Chroma Vector DB

To query ChatGPT using the Chroma Vector DB, use the following command:

For example write a prompt related to the downloaded HTML files:
```bash
python query.py "Fortæl mig om onkologisk afdeling"
```

