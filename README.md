# How to run the application

Step 1: conda create --name myenv python=3.12.4

Step 2: conda activate myenv

Step 3: pip install -r requirements.txt

Step 4: Create a .env variable with your OpenAI API key, with the name: OPENAI_API_KEY

Step 5: Run the create_db notebook, to create the Chroma Vector DB

Step 6: Query ChatGPT with the Chroma Vector DB by typing in the command prompt: python query.py "your question"
