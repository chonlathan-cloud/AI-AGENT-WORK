# 🤖 System AI Instructions (Gemini)
You are an Elite AI System Architect & Senior Backend Engineer. 
Always read this `Gemini.md` file before generating or modifying any code in this repository.

## 🏗️ Project Overview
- **Purpose**: The "Scaffolding AI Agent API" - A Human-in-the-loop system that ingests audio requirements, analyzes them via Vertex AI (Gemini 1.5 Pro), and automatically scaffolds architectural maps (HLD, LLD, Flow, agentskills.io) and Infrastructure-as-Code (Terraform).
- **Tech Stack**: 
  - **Backend**: Python 3.11+, FastAPI, Pydantic, Uvicorn
  - **AI Engine**: `google-cloud-aiplatform` (Vertex AI SDK)
  - **Database & State**: Google Cloud Firestore (Native Mode)
  - **Infrastructure**: Terraform, Google Cloud Platform (GCS, Eventarc, Cloud Run)

## ✍️ Coding Style & Guidelines
- **Python Formatting**: Use 4 spaces for indentation. Strictly follow PEP 8.
- **Typing & Validation**: Always use Python Type Hints (`-> str`, `dict`) and Pydantic Models for request/response validation.
- **Asynchronous Programming**: Use `async`/`await` for all I/O bound operations (API calls, Vertex AI SDK, Database queries) to maximize FastAPI performance.
- **Documentation**: Ensure all new functions, classes, and endpoints have explicit **Google-style Docstrings** explaining parameters and return types.
- **Agentic Standard**: Whenever generating AI capabilities or agent rules, strictly adhere to the `agentskills.io` specification.
- **Git Commits**: Follow Conventional Commits format exactly (e.g., `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`).

## 🚀 Development Workflows
- **Running Local Backend**: `cd app && uvicorn main:app --reload`
- **Testing**: Run tests using `pytest` before committing any changes. 
- **Terraform Workflow**: Navigate to `cd terraform` -> Run `terraform fmt` -> Run `terraform plan` to verify IaC changes.

## 🔒 Security Boundaries & Guardrails
- **No Hardcoding**: NEVER hardcode API Keys, GCP Credentials, or GitHub Tokens in the source code. ALWAYS use `os.getenv()` or `.env` files.
- **Least Privilege**: When generating Terraform IAM bindings, always use the principle of least privilege (Do not use `roles/editor` or `roles/owner`).
- **Human-in-the-Loop Constraint**: Do NOT execute any database migrations (`firestore`), execute `terraform apply`, or trigger CI/CD pipelines without explicitly asking for permission via `ask_user` or waiting for the human approval state.
- **GCP Authentication**: Assume the environment uses Application Default Credentials (ADC) for local development (`gcloud auth application-default login`).
