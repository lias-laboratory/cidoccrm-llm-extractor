# CIDOC CRM LLm Extractor

This project automates the extraction of RDF triples from structured archaeological data using large language models (LLMs) and the CIDOC CRM ontology. It aims to simplify the creation of archaeological knowledge graphs by integrating domain-specific knowledge with LLM prompting strategies.

## Features

- Automatically generates CIDOC CRM-compliant RDF triples from CSV files.
- Implements three prompting strategies: Unguided, Full Ontology, and Ontology Subset.
- Uses GPT-4 via OpenAI’s API for semantic mapping and RDF generation.
- Optimized for archaeological datasets with interdisciplinary data.

## Project Structure

```
/
├── config.py                                 Configuration file for paths, chunk size, and API key.
├── data_loader.py                            Functions for reading files, CSV data, and chunking.
├── llm_interface.py                          Interface for processing data chunks with OpenAI's API.
├── main.py                                   Main script to process CSV files and generate RDF triples.
├── data/
│   ├── input/
│   ├── ontologies/                           Ontology JSON files used for extraction logic.
│   │   ├── full_cidoc_crm.json
│   │   └── subset_cidoc_crm.json
│   │   output/                               Folder to store output files.
│   └── prompts/                              Prompt templates for guiding LLM-based extraction.
│   ├── ontology_guided_llm_extraction.txt
│   └── unguided_llm_extraction.txt
├── README.md                                 Project overview and instructions.
└── requirements.txt                          Python dependencies for the project.

```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lias-laboratory/cidoccrm-llm-extractor
   cd cidoccrm-llm-extractor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key in `config.py`:
   ```python
   OPENAI_API_KEY = "your-api-key-here"
   ```

## Usage

### 1. Prepare Your Files

Place your input files in the appropriate directories:

- **CSV files**: `data/input/`
- **Example prompt files** (for guided extraction): `data/input/`

Update the paths in `config.py` as needed:

```python
CSV_FILES = ["data/input/sample_data.csv"]
EXAMPLE_FILES = ["data/input/sample_example.txt"]
SAVE_DIRS = ["data/output/sample_data_with_ontology_1.jsonld"]
```

### 2. Run the Extraction

Launch the script with:

```bash
python main.py
```

The program will prompt you to choose an RDF extraction strategy:

- **1**: Unguided LLM Extraction
- **2**: Full Ontology Prompting
- **3**: Ontology Subset Prompting

Based on your selection, the corresponding extraction function will be executed.

### 3. Output

The generated RDF triples will be saved in the paths specified under `SAVE_DIRS`.


## Prompting Strategies

1. **Unguided LLM Extraction**: Relies solely on the LLM's prior knowledge without any explicit ontology input.
2. **Full Ontology Prompting**: Injects the full CIDOC CRM ontology into the prompt, which can overwhelm the model.
3. **Ontology Subset Prompting** (Best): Uses a carefully curated subset of the ontology tailored for archaeology. This strategy improves precision, recall, and competency question performance.

## Ontologies

This project uses two versions of the CIDOC CRM ontology to guide or constrain the information extraction process:

1. **`full_cidoc_crm.json`**  
   This file contains the complete CIDOC CRM ontology in JSON format. It was sourced from the GitHub repository [LLM_Semantics by dingningpei](https://github.com/dingningpei/LLM_Semantics). It provides the full set of classes and properties defined by CIDOC CRM, allowing for rich and detailed semantic representation.

2. **`subset_cidoc_crm.json`**  
   This version was manually curated to include only the most relevant classes and properties for the specific use case of this project. It simplifies the ontology for more focused extraction and reduces processing overhead during prompt generation and reasoning.

These ontology files are used primarily in the **ontology-guided extraction** mode to structure the prompts and to help the LLM generate semantically accurate RDF triples.

## Data Availability
The input data used in this project is not included in the repository due to privacy, confidentiality, and legal restrictions. 

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Developed as part of the French ANR project Digitalis (ANR-22-CE38-0011-01).

### Contributors

- [Ali Hariri](https://www.lias-lab.fr/members/alihariri/), LIAS, ISAE-ENSMA
- [Stéphane Jean](https://www.lias-lab.fr/members/stephanejean/), LIAS, University of Poitiers 
- [Mickaël Baron](https://www.lias-lab.fr/members/mickaelbaron/), LIAS, ISAE-ENSMA

For more information, visit the [project page](https://digitalis.humanities.science/).

