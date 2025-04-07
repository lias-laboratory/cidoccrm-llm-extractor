import re
from data_loader import read_file
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap, RunnableSequence
from langchain_openai import ChatOpenAI

def create_prompt_template(prompt_path):
    """
    Reads a prompt template from a file and creates a PromptTemplate object.

    Args:
        prompt_path (str): Path to the file containing the prompt template.

    Returns:
        PromptTemplate: A LangChain PromptTemplate object with the defined structure.
    """
    prompt_text = read_file(prompt_path)
    return PromptTemplate(input_variables=["input_data", "ontology_description", "example"], template=prompt_text)

def process_unguided_chunks(chunks, api_key, prompt_path):
    """
    Processes chunks of data without ontology or example (unguided mode) using the LLM.

    Args:
        chunks (list of str): List of data chunks to process.
        api_key (str): API key for accessing OpenAI's services.
        prompt_path (str): Path to the prompt template file.

    Returns:
        str: Combined results of processing all chunks, formatted as RDF JSON-LD.

    Steps:
        1. Initializes the LLM with the provided API key.
        2. Creates a prompt template using `create_prompt_template`.
        3. Sets up a processing chain using LangChain's `RunnableSequence` and `RunnableMap`.
        4. Iterates over each chunk, invoking the chain with the chunk.
        5. Collects and combines the responses into a single string.

    Notes:
        - Prints progress for each chunk being processed.
        - Handles responses with or without a `content` attribute.
    """
    llm = ChatOpenAI(model="gpt-4o", openai_api_key=api_key)
    prompt_template = create_prompt_template(prompt_path)
    chain = RunnableSequence(
        RunnableMap({
            "input_data": lambda x: x,
        }) | prompt_template | llm
    )
    responses = []
    for i, chunk in enumerate(chunks):
        print(f"Processing segment {i+1}/{len(chunks)} ({(i+1)/len(chunks)*100:.2f}%)")
        response = chain.invoke({
            "input_data": chunk
        })
        responses.append(response.content if hasattr(response, "content") else str(response))
    return "\n".join(responses)

def process_guided_chunks(chunks, ontology_description, example, api_key, prompt_path):
    """
    Processes chunks of data with ontology and example (guided mode) using the LLM.

    Args:
        chunks (list of str): List of data chunks to process.
        ontology_description (str): JSON representation of the ontology to use for mapping.
        example (str): Example output format to guide the LLM.
        api_key (str): API key for accessing OpenAI's services.
        prompt_path (str): Path to the prompt template file.

    Returns:
        str: Combined results of processing all chunks, formatted as RDF JSON-LD.

    Steps:
        1. Initializes the LLM with the provided API key.
        2. Creates a prompt template using `create_prompt_template`.
        3. Sets up a processing chain using LangChain's `RunnableSequence` and `RunnableMap`.
        4. Iterates over each chunk, invoking the chain with the chunk, ontology, and example.
        5. Collects and combines the responses into a single string.

    Notes:
        - Prints progress for each chunk being processed.
        - Handles responses with or without a `content` attribute.
    """
    llm = ChatOpenAI(model="gpt-4o", openai_api_key=api_key)
    prompt_template = create_prompt_template(prompt_path)
    chain = RunnableSequence(
        RunnableMap({
            "input_data": lambda x: x,
            "ontology_description": lambda x: x,
            "example": lambda x: x
        }) | prompt_template | llm
    )
    responses = []
    for i, chunk in enumerate(chunks):
        print(f"Processing segment {i+1}/{len(chunks)} ({(i+1)/len(chunks)*100:.2f}%)")
        response = chain.invoke({
            "input_data": chunk,
            "ontology_description": ontology_description,
            "example": example
        })
        responses.append(response.content if hasattr(response, "content") else str(response))
    return "\n".join(responses)