import sys
from data_loader import read_file, read_csv, chunk_data
from llm_interface import process_unguided_chunks, process_guided_chunks
from config import CSV_FILES, EXAMPLE_FILES, CHUNK_SIZE, SAVE_DIRS, OPENAI_API_KEY

# Strategy definitions
EXTRACTION_STRATEGIES = {
    "1": {
        "name": "Unguided LLM Extraction",
        "prompt_template": "data/prompts/unguided_llm_extraction.txt"
    },
    "2": {
        "name": "Full Ontology Prompting",
        "prompt_template": "data/prompts/ontology_guided_llm_extraction.txt",
        "ontology_file": "data/ontologies/full_cidoc_crm.json"
    },
    "3": {
        "name": "Ontology Subset Prompting",
        "prompt_template": "data/prompts/ontology_guided_llm_extraction.txt",
        "ontology_file": "data/ontologies/subset_cidoc_crm.json"
    }
}

def choose_extraction_strategy():
    print("\nChoose an RDF extraction strategy:\n")
    for key, strategy in EXTRACTION_STRATEGIES.items():
        print(f"{key}. {strategy['name']}")
    choice = input("\nEnter the number of your choice: ").strip()

    if choice not in EXTRACTION_STRATEGIES:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    print(f"\nSelected strategy: {EXTRACTION_STRATEGIES[choice]['name']}")
    return EXTRACTION_STRATEGIES[choice], choice

def process_unguided(csv_files, chunk_size, save_dirs, api_key, prompt_template):
    print("\nStarting Unguided LLM Extraction...\n")
    if len(save_dirs) != len(csv_files):
        raise ValueError("Mismatch between number of CSV files and save directories.")

    for index, csv_file in enumerate(csv_files):
        print(f"Processing file {index + 1} of {len(csv_files)}: {csv_file}")
        header, rows = read_csv(csv_file)
        chunks = chunk_data(header, rows, chunk_size)

        print("Generating RDF using unguided strategy...")
        final_output = process_unguided_chunks(
            chunks=chunks,
            api_key=api_key,
            prompt_path=prompt_template
        )
        print("-" * 60)
        print("\nGenerated RDF Result:\n")
        print(final_output)
        print("-" * 60)
        save_path = save_dirs[index]
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(final_output)

        print(f"Result saved to: {save_path}")

def process_guided(csv_files, example_files, chunk_size, save_dirs, api_key, prompt_template, ontology_file, strategy_name):
    print("\nSelected strategy: '" + strategy_name + "'\n")
    if len(example_files) != len(csv_files):
        raise ValueError("Each CSV file must have a corresponding example file.")
    if len(save_dirs) != len(csv_files):
        raise ValueError("Mismatch between number of CSV files and save directories.")

    print("Loading ontology...")
    ontology_description = read_file(ontology_file)

    for index, csv_file in enumerate(csv_files):
        print(f"Processing file {index + 1} of {len(csv_files)}: {csv_file}")
        example = read_file(example_files[index])
        header, rows = read_csv(csv_file)
        chunks = chunk_data(header, rows, chunk_size)

        print("Generating RDF using guided strategy 'Unguided LLM Extraction'")
        final_output = process_guided_chunks(
            chunks=chunks,
            ontology_description=ontology_description,
            example=example,
            api_key=api_key,
            prompt_path=prompt_template
        )

        print("\nGenerated RDF Result:\n")
        print(final_output)

        save_path = save_dirs[index]
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(final_output)

        print(f"Result saved to: {save_path}")
        print("-" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("CIDOC CRM LLm Extractor")
    print("=" * 60)

    strategy, strategy_id = choose_extraction_strategy()

    if strategy_id == "1":
        process_unguided(
            csv_files=CSV_FILES,
            chunk_size=CHUNK_SIZE,
            save_dirs=SAVE_DIRS,
            api_key=OPENAI_API_KEY,
            prompt_template=strategy["prompt_template"]
        )
    else:
        process_guided(
            csv_files=CSV_FILES,
            example_files=EXAMPLE_FILES,
            chunk_size=CHUNK_SIZE,
            save_dirs=SAVE_DIRS,
            api_key=OPENAI_API_KEY,
            prompt_template=strategy["prompt_template"],
            ontology_file=strategy["ontology_file"],
            strategy_name=strategy["name"]
        )

    print("\nAll files processed successfully.")
