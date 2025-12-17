from typing import Any

import re
from datetime import datetime

class ValidationHelper():

    def is_valid_date(date):

        # verifica se a data esta no formato adequado, senão retorna false
        dateRegex = r"^\d{4}[-]\d{2}[-]\d{2}$"
        if not re.fullmatch(dateRegex, date):
            return False
        
        # testa se é uma data válida e retorna true ou false
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_time(time):

        # verifica se a hora esta no formato adequado, senão retorna false
        timeRegex = r"^\d{2}[:]\d{2}$"
        if not re.fullmatch(timeRegex, time):
            return False
        
        # testa se é uma hora válida e retorna true ou false
        try:
            datetime.strptime(time, "%H:%M")
            return True
        except ValueError:
            return False

    def is_valid_email(email):
        # testa se é um email válido
        emailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.fullmatch(emailRegex, email):
            return True
        return False