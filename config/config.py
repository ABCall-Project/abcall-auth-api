import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        environment = os.getenv('FLASK_ENV')

        if environment == 'local':
            load_dotenv(dotenv_path='.env.local')
        elif environment == 'test':
            load_dotenv(dotenv_path='.env.test')
        else:
            load_dotenv(dotenv_path='.env')

        self.ENVIRONMENT = environment
        self.APP_NAME=os.getenv('APP_NAME')
        self.DATABASE_URI=os.getenv('DATABASE_URI')
        self.PHRASE_KEY=os.getenv('PHRASE_KEY')
        