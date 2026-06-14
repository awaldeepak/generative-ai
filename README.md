# Generative AI Examples and Tutorials

This repository contains example code, exercises, and small projects demonstrating core Generative AI concepts, including token encoding, vector embeddings, prompting techniques, agent patterns, and retrieval-augmented generation (RAG).

## Overview

- Purpose: Educational examples to learn how to build and experiment with modern GenAI building blocks in Python.
- Audience: Developers, students, and researchers who want runnable, well-organized reference code.

## Repository structure

- `ch_1_Intro_to_GenAI/` — basic building blocks
	- `token_encoding.py` — tokenization & encoding examples
	- `vector_embedding.py` — simple vector embedding examples
- `ch_2_Prompting_Techniques/` — prompt engineering patterns and chatbots
	- `L1_prompting-techniques/` — small examples (zero-shot, few-shot, CoT, self-consistency, persona prompts)
	- `L2_ai-chatbot/main.py` — minimal chatbot example
- `ch_3_AI_Agents/` — agent patterns and demos
	- `main.py` — simple agent orchestration example
	- `weather.html` — demo UI for weather agent (static demo)
- `ch_4_RAG/` — retrieval-augmented generation examples
	- `system_prompt.py` — central system prompt patterns
	- `L1_simple-RAG/main.py` — simple RAG demo
	- `L2_RAG-pipeline/` — a small pipeline with ingestion and main entrypoint

## Prerequisites

- Python 3.8 or newer
- Create a virtual environment (recommended)

## Installation

1. Create and activate a virtual environment:

	 python -m venv .venv
	 source .venv/bin/activate

2. Install dependencies:

	 pip install -r requirements.txt

Note: `requirements.txt` contains libraries used across the examples. Pin versions as needed for reproducibility.

## Usage — quick examples

- Run a prompting example (few-shot):

	python ch_2_Prompting_Techniques/L1_prompting-techniques/L2_few_shot.py

- Start the AI chatbot demo:

	python ch_2_Prompting_Techniques/L2_ai-chatbot/main.py

- Run the simple RAG demo:

	python ch_4_RAG/L1_simple-RAG/main.py

Adjust file paths and parameters inside each script as needed — the examples are intentionally small and annotated.

## Files of interest

- `requirements.txt` — Python dependencies
- `ch_4_RAG/L2_RAG-pipeline/ingestion.py` — shows simple text ingestion patterns
- `ch_3_AI_Agents/main.py` — example agent loop and orchestration

## Contributing

Contributions are welcome. Please open an issue or a pull request with a clear description. Keep examples small, documented, and reproducible.

## License

This project is licensed under the MIT License — see the `LICENSE` file at the repository root for details.

---
Generated: concise project README updated to help new contributors and users run examples.
