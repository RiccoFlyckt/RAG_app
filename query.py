import argparse
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import List, Set, Tuple

GPTMODEL = "gpt-4o-mini" #ChatGPT modelname
CHROMA_PATH = "chroma"  #Vector DB path
PROMPT_TEMPLATE = """
Dem der skriver er kun ansatte fra Vejle Sygehus. Vejle Sygehus er en del af Sygehus Lillebælt. Det er meget vigtigt at du er sød og flink overfor brugerne. Klokken er nu: {current_time}. Når der er et spørgsmål, hvor du nævner klokken eller tid, skal du altid skrive svaret baseret på tidspunktet, efterfulgt af dit svar. Det er MEGET vigtigt at du også skriver klokken til personen.Svar på spørgsmålet baseret på den følgende kontekst:
{context}
---
Spørgsmål: {question}
"""

def load_api_key() -> str:
    """
    Load the OpenAI API key from environment variables.
    Raises an error if the key is not set.
    """
    load_dotenv()  # Load environment variables from a .env file
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return openai_api_key

def get_current_time() -> str:
    """
    Get the current time formatted as 'Day HH:MM'.
    """
    return datetime.now().strftime("%A %H:%M")

def get_query_text() -> str:
    """
    Parse the command line arguments to get the query text.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    return args.query_text

def prepare_database() -> Chroma:
    """
    Prepare the Chroma database with OpenAI embeddings.
    """
    embedding_function = OpenAIEmbeddings()
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

def search_database(db: Chroma, query_text: str, threshold: float = 0.7) -> List[List[str]]: # The threshold is 0.7 if nothing else is specified
    """
    Search the database for documents similar to the query text.
    Only return documents with a relevance score above the threshold, defaulted to 0.7.
    """
    results = db.similarity_search_with_relevance_scores(query_text, k=3) 
    return [[result, score] for result, score in results if score >= threshold] # Only a doc is returned, if a doc has a score higher than the specified threshold.

def format_context(filtered_results: List[List[str]]) -> Tuple[str, Set[str]]:
    """
    Format the context texts and sources from the filtered results.
    """
    context_texts = []
    sources = set() #A set was utilized, as we dont want duplicates of sources.
    for doc, _score in filtered_results:
        context_texts.append(doc.page_content)
        sources.add(doc.metadata.get("url", "No URL available")) #if no url is available, we specify that we did not find an url
    return "\n\n---\n\n".join(context_texts), sources

def create_prompt(context_text: str, query_text: str, current_time: str) -> str:
    """
    Create the prompt text by formatting the template with context, query, and current time.
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context_text, question=query_text, current_time=current_time)

def get_response(GPTMODEL: str,prompt: str, api_key: str) -> str:
    """
    Get the response from the ChatOpenAI model using the prompt and API key.
    """
    model = ChatOpenAI(model = GPTMODEL,api_key=api_key, max_tokens=4000, temperature=0.2) # We wanted the model to be more precise and less creative, and hence found a temperature of 0.2 as good. 
    response = model.invoke(prompt)
    return response.content # Only return the content of the response

def main():
    """
    Main function to execute the script.
    Loads API key, processes query, searches the database,
    creates a prompt, and prints the response.
    """
    try:
        openai_api_key = load_api_key()  # Load API key from environment
        query_text = get_query_text()  # Get query text from command line
        current_time = get_current_time()  # Get the current time

        db = prepare_database()  # Prepare the Chroma database
        filtered_results = search_database(db, query_text)  # Search the database for similar docs based on the prompt

        if not filtered_results:
            print("Unable to find matching results.")
            return # If no results are found, then we should exit the program, to ensure that the model only answers questions based on relevant context

        context_text, sources = format_context(filtered_results)  # Format context and sources for the relevant doc(s)
        prompt = create_prompt(context_text, query_text, current_time)  # Create the prompt for ChatGPT
        response_text = get_response(GPTMODEL, prompt, openai_api_key)  # Get the response from ChatGPT

        formatted_response = f"Svar: {response_text}\nKilder: {', '.join(sources)}"
        print(formatted_response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
