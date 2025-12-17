import logging
from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info

from schema import *
from model import Session, Symptom
from controllers import *

# Logging
logging.basicConfig(filename='entendedor.log', level=logging.INFO)

# App Configs
info = Info(title="EntendeDor API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost"]
)

# Register OpenAPI route
@app.get("/", doc_ui=False)
def home():
    return redirect("/openapi")

# Register Controllers functions
authController.register_auth_routes(app)
usersController.register_users_routes(app)
symptomsController.register_symptoms_routes(app)
recordsController.register_records_routes(app)
eventsController.register_events_routes(app)

# App Run
if __name__ == '__main__':
    print("\033[96m" + "EntendeDor - Sistema de Monitoramento de Dor Crônica" + "\033[96m")
    print("")
    print("\033[0m" + "Aplicação rodando em: " + "\033[4;37m" + "http://127.0.0.1:5000" + "\033[4;37m")
    print("\033[0m")
    app.run(host="0.0.0.0", port=5000, debug=True)