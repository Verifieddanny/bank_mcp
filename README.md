# ArmorIQ MCP Banking Server

A secure Model Context Protocol (MCP) server implementation built with Python and FastAPI for the ArmorIQ Intern Recruitment Assignment.

## 🚀 Hosted URL
**Production URL:** [https://bank-mcp.onrender.com/](https://bank-mcp.onrender.com/)  
**Interactive API Docs:** [https://bank-mcp.onrender.com/docs](https://bank-mcp.onrender.com/docs)

## 🔐 Authentication
This API is secured using API Key authentication. To interact with the endpoints, you must include the following header in your requests:

- **Header Name:** `access_token`
- **Header Value:** `armoriq_secure_key_2025` 
*(Note: Managed via environment variables in production)*.

## 🛠️ Features
- **Account Creation**: Register new users with an initial deposit.
- **Deposit**: Securely add funds to an existing account.
- **Withdrawal**: Remove funds with automated balance verification.
- **Balance Inquiry**: Real-time balance retrieval.
- **Transaction History**: Audit trail of all account activities.

## 🛡️ Security Implementation
1. **SQL Injection Prevention**: Utilized **SQLAlchemy ORM** and parameterized queries to prevent injection attacks.
2. **Authentication Layer**: Implemented a global dependency to validate `access_token` headers, successfully resolving the "Missing Authentication" high-severity finding from the ArmorIQ Sentry scan.
3. **Environment Configuration**: Sensitive keys are managed via `os.getenv` to follow the 12-factor app security best practices.
4. **CORS Policy**: Configured to manage cross-origin requests safely.

## 💻 Local Setup
1. **Clone & Install**:
   ```bash
   git clone <your-repo-url>
   pip install -r requirements.txt

```

2. **Set Environment Variable**:
```bash
export ARMORIQ_SECRET=armoriq_secure_key_2025

```


3. **Run**:
```bash
uvicorn main:app --reload

```



## 🏗️ Tech Stack

* **FastAPI** | **SQLAlchemy** | **SQLite** | **Render**

