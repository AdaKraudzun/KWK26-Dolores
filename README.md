# Dolores

Dolores is an AI assistant designed to empower women and gender minorities by providing personalized advice, legal guidance, and actionable tips to navigate workplace discrimination, safety concerns, and economic mistreatment.

🤗 **Originally built as a Hugging Face Space:** https://huggingface.co/spaces/kode-with-klossy/4.3-groupB1-capstone

> ⚠️ Note: This Space is no longer live. The code in this repo is the full project.

## How it looks

<img width="827" height="548" alt="Screenshot 1" src="https://github.com/user-attachments/assets/bc37f71c-9d88-4887-8561-5ce0eba8e9ae" />
<img width="827" height="553" alt="Screenshot 2" src="https://github.com/user-attachments/assets/26c4d3e2-c7cc-48d6-92bb-75c5a200f667" />


## What it does

* **Workplace & Pay Advice:** Helps users identify economic mistreatment, negotiate pay, and draft HR emails.
* **Safety & Legal Guidance:** Assists users in recognizing abuse and navigating employment and safety laws.
* **Resource Connections:** Links users to legal toolkits, support services, and emergency hotlines.

## How it works

When a user submits a prompt, Dolores utilizes Retrieval-Augmented Generation (RAG). The user's query is converted into embeddings via Sentence Transformers to search a custom research knowledge base for the most relevant context chunks. These relevant chunks are appended to the system prompt, which instructs the model to generate accurate, helpful advice.

## Built with

- **Gradio** — the interface
- **Hugging Face Inference Providers** — the AI model (`Qwen/Qwen2.5-7B-Instruct`)
- **Sentence Transformers** — used `all-MiniLM-L6-v2` to convert text chunks and user queries into vector embeddings for similarity matching in RAG
- **Knowledge Base (`knowledge.txt`)** — the custom dataset containing legal rights, workplace advice, and support resources

## What I learned

One of our biggest technical challenges was fixing code execution order issues and managing long build and run times on Hugging Face. To solve this, we collaborated closely as a team to structure our RAG functions efficiently, timed our test runs around our breaks, and carefully curated a high-quality knowledge base so Dolores could deliver fast, accurate, and reliable responses.

## About

Built at [Kode With Klossy](https://www.kodewithklossy.com) AI/ML Camp,
Summer 2026, by Ada, Adiba, Lasyasri, Susanna.
