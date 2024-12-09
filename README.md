# Roast Your X Profile 🎭

A fun Python project that generates humorous, Santa-style roasts based on X (formerly Twitter) profiles using the Grok AI model.

## 🎯 Project Overview

This project connects to X's API to fetch profile information and uses Grok AI to generate witty, Christmas-themed roasts in the style of the profile owner acting as Santa Claus. It's a fun way to create humorous content while maintaining respect for the source material.

## 🔧 Project Structure

```
roast-your-x-profile/
├── grok/
│   ├── api.py              # Main API interactions with X and Grok
│   ├── grokask.py          # Standalone Grok interaction module
│   └── generated_script_example.txt  # Example output
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 📁 File Descriptions

### api.py
- Handles X API integration
- Fetches user profiles and tweets
- Processes profile data
- Generates roasts using Grok AI
- Includes rate limiting and error handling

### grokask.py
- Standalone module for direct Grok AI interactions
- Provides a simple interface for asking questions to Grok
- Can be used independently for general AI conversations

### generated_script_example.txt
- Contains example outputs
- Shows the format and style of generated roasts
- Serves as a reference for expected results

## 🚀 Setup and Usage

1. Clone the repository:
```bash
git clone https://github.com/Fogggy-Chao/roast-your-x-profile.git
```

2. Create a `.env` file with your API keys:
```env
XAI_API_KEY = your_xai_api_key
TWITTER_BEARER_TOKEN = your_twitter_bearer_token
```

3. Install required dependencies:
```bash
pip install openai requests python-dotenv
```

4. Run the main script:
```bash
python -m grok.api
```

Or use the standalone Grok interface:
```bash
python -m grok.grokask
```

## 🎮 Features

- Fetches X profile information including:
  - User description
  - Pinned tweets
  - Recent tweets
- Generates Santa-style roasts using Grok AI
- Rate limit handling for X API
- Error handling and retry mechanisms
- Standalone Grok interaction module

## ⚠️ Important Notes

- Keep your API keys secure and never commit them to the repository
- Respect X's rate limits
- Use the generated content responsibly
- The roasts are meant to be humorous, not harmful

## 🔑 Requirements

- Python 3.6+
- X (Twitter) API access
- Grok AI API access
- Required Python packages (see Setup)

## 🤝 Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

[MIT License](https://choosealicense.com/licenses/mit/)