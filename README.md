# Flask Hello World Demo

This is a minimal Flask "Hello World" demo.

Quick start (uses the provided `env` virtualenv in the workspace):

```bash
# Install dependencies into the included venv
/home/wcx/code/projectTemplate/env/bin/python -m pip install -r requirements.txt

# Run the app
/home/wcx/code/projectTemplate/env/bin/python app.py

# Run tests
/home/wcx/code/projectTemplate/env/bin/python -m pytest -q
```

Route:
- GET / -> returns `Hello, World!`
