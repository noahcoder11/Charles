from openai import OpenAI
import config

oai_client = OpenAI(api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])