from flask import Flask, request, jsonify
import logging
import os
import traceback
from json import load, loads

import agents
import llmsetup
import route
import toolkit

app = Flask(__name__)


app.route('/routePrompt', methods=['POST'])
def routePrompt():
    try:
        _data = request.get_data(as_text=True, parse_form_data=True)
        data = loads(_data)
        phrase = data.get("text")
        if not phrase:
            raise ValueError("Text parameter is missing.")
        result = route.route_query(phrase)
        return {"is_toxic": result}
    except ValueError as ve:
        stack_trace = traceback.format_exc()
        logging.error(f"Validation error:\n{stack_trace}")
        return {"error": f"Validation error:\n{stack_trace}"}, 400
    except Exception as e:
        stack_trace = traceback.format_exc()
        logging.error(f"Error moderating text:\n{stack_trace}")
        return {"error": f"Unexpected error occurred:\n{stack_trace}"}, 500
    
