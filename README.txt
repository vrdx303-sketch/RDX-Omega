RDX JHATKA BUILDER PACKAGE

Run builder.py once.
Then:
  cd engine
  pip install -r requirements.txt
  python main.py

The website is separate:
  website/index.html

It communicates with Engine :8000.
Ollama remains on :11434 with qwen2.5-coder:latest.

The builder does not merge the website into the engine.
