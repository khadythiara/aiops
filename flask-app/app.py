from flask import Flask
import logging
import os

app = Flask(__name__)

# Crée le dossier ./logs s'il n'existe pas (important pour éviter PermissionError)
os.makedirs('./logs', exist_ok=True)

logging.basicConfig(filename='./logs/app.log', level=logging.INFO)

@app.route("/users")
def users():
    app.logger.info("User requested /users")
    return {"users": ["alice", "bob"]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
