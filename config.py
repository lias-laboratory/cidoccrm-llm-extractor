# List of paths to the input CSV files to be processed.
CSV_FILES = [
    "data/input/sample_data.csv"
]

# List of paths to example files that provide sample output formats for processing.
EXAMPLE_FILES = [
    "data/input/sample_example.txt"
]

# List of paths where the processed RDF triples (in JSON-LD format) will be saved.
SAVE_DIRS = [
    "data/output/sample_data_with_ontology_1.jsonld"
]

# Number of rows per chunk for processing the CSV data.
CHUNK_SIZE = 20

# API key for accessing OpenAI's services.
OPENAI_API_KEY = "your-api-key-here"