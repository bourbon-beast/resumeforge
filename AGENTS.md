# AGENTS.md

## 🧠 Agent Instructions for ResumeForge / JobTailor

This project is a React + Python application. Backend logic is in `robot_brain/`, and the frontend React app is in `src/`.

---

### 🔧 Setup Instructions

Before beginning any task, **run the setup script every time you open a new terminal session or pull new changes**:

```bash
./setup.sh
```

This script takes care of creating or re-activating the Python virtual environment, installing dependencies, and configuring formatters. If the script doesn't exist yet, ensure the following steps are performed manually:

1. **Python Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r robot_brain/requirements.txt
   ```

   Remember to re-run `source venv/bin/activate` at the start of each new shell
   session so the virtual environment is active.

2. **Node Dependencies**

   ```bash
   npm install
   ```

3. **Code Formatters & Linters**

   ```bash
   pip install black flake8 isort
   npm install prettier eslint
   ```

---

### 📆 Dependency Management

* **Python backend:** Use `robot_brain/requirements.txt`
* **Frontend (React):** Use `package.json` in the project root

---

### 🧪 Testing

* **Python tests** (if present): Run via `pytest` or `unittest`

  ```bash
  pytest tests/
  ```
* **React tests**: Run via `npm test` (assuming Create React App or Vite setup)

---

### 🧹 Code Formatting & Linting

* Python (backend):

  ```bash
  black robot_brain/
  isort robot_brain/
  flake8 robot_brain/
  ```

* React (frontend):

  ```bash
  prettier --write src/
  eslint src/ --fix
  ```

---

### ✅ Conventions

* Use conventional commit messages (e.g. `feat:`, `fix:`, `chore:`).
* Keep backend and frontend logic modular and separated.
* Use prompt templates from `robot_brain/prompts/` when writing or modifying prompt logic.

---

### 📁 Key Project Folders

* `robot_brain/`: Backend logic, AI models, prompts, utils, output
* `src/`: Frontend React app
* `output/`: Generated resumes, cover letters, logs
* `prompts/`: Prompt templates for AI instructions

---

End of agent instructions.
