# config.py
# Configuration file for agentic_rag project.
# Contains URLs to fetch, and chunking parameters for text splitting.

# List of blog post URLs to use in the RAG system
URLS = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]

# Chunking parameters for text splitting
CHUNK_SIZE = 100
CHUNK_OVERLAP = 50 