from dotenv import load_dotenv
import os
import logging

load_dotenv()

#API keys
GROQ_API_KEY = os.get.env("GROQ_API_KEY", "")
GEMINI_API_KEY= os.get.env("GEMINI_API_KEY", "")

#Provider and Logging
ACTIVE_PROVIDER = os.get.env("ACTIVE_PROVIDER", "groq")
LOG_LEVEL = os.get.env("LOG_LEVEL", "INFO")
LOG_FORMAT     = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FMT   = "%H:%M:%S"

#API endpoints
GROQ_URL = ""
GEMINI_URL = ""
OLLAMA_URL = ""