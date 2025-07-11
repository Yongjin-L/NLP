# Selfstudy Discussion & Review Support

Streamlit applications that provide AI-powered discussion and review support for academic papers.

## Features

### Discussion App (`appDiscuss.py`)
- AI-powered paper discussion assistance
- Interactive chat interface for academic discussions
- Source citations and references

### Review App (`appReview.py`)
- RAG-powered chat with 51 academic papers
- Enhanced paper review and analysis capabilities
- Author and year-based query optimization

### Common Features
- RAG (Retrieval-Augmented Generation) integration
- Real-time API responses
- Source citations with expandable details
- Session-based chat history

## Local Development

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure secrets:
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

4. Edit `.streamlit/secrets.toml` with your actual API credentials:
```toml
[default]
API_URL = "http://localhost:3000/api/chat/completions"
API_TOKEN = "your-actual-api-token"
MODEL_NAME = "selfstudydiscussion"
REVIEW_MODEL_NAME = "selfstudyreviewedpaper"
```

5. Run the applications:
```bash
# For discussion app
streamlit run appDiscuss.py

# For review app  
streamlit run appReview.py
```

## Deployment on Streamlit Cloud

### Step 1: Push to GitHub

Make sure your `.gitignore` file excludes sensitive files:
- `.streamlit/secrets.toml` is already in `.gitignore`
- Only commit the template file (`.streamlit/secrets.toml.template`)

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository and branch
4. Deploy each app separately:
   - **Discussion App**: Set main file path to `appDiscuss.py`
   - **Review App**: Set main file path to `appReview.py`

### Step 3: Configure Secrets in Streamlit Cloud

1. In your Streamlit Cloud app dashboard, click on "Settings"
2. Go to the "Secrets" tab
3. Add your secrets in TOML format (same configuration for both apps):

```toml
API_URL = "http://localhost:3000/api/chat/completions"
API_TOKEN = "your-actual-api-token"
MODEL_NAME = "selfstudydiscussion"
REVIEW_MODEL_NAME = "selfstudyreviewedpaper"
```

4. Save the secrets
5. Your apps will automatically redeploy with the new configuration

## Security Notes

- **NEVER** commit actual API tokens or sensitive data to Git
- Always use Streamlit's secrets management for sensitive configuration
- The `.gitignore` file is configured to exclude secrets files
- Use the template file as a reference for required secrets structure

## File Structure

```
├── appDiscuss.py                    # Discussion support application
├── appReview.py                     # Paper review application  
├── requirements.txt                 # Python dependencies
├── .streamlit/
│   └── secrets.toml.template       # Secrets template (safe to commit)
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## API Integration

These applications integrate with a custom RAG API that provides:
- Paper content retrieval
- AI-powered responses  
- Source citations and snippets

The API expects requests in the following format:
```json
{
  "model": "selfstudydiscussion",  // or "selfstudyreviewedpaper" for review app
  "messages": [{"role": "user", "content": "your question"}]
}
```

### Model Types:
- **Discussion App**: Uses `selfstudydiscussion` model
- **Review App**: Uses `selfstudyreviewedpaper` model (51 papers dataset) 