from flask import Flask, request, jsonify
import logging
import os
import traceback
from json import loads

import route
import toolkit

app = Flask(__name__)

@app.route('/routePrompt', methods=['GET','POST'])
def routePrompt():
    try:
        _data = request.get_data(as_text=True, parse_form_data=True)
        data = loads(_data)
        phrase = data.get("text")
        if not phrase:
            raise ValueError("Text parameter is missing.")
        
        # Assuming route_query returns some kind of result
        result = route.route_query(phrase)
        
        # Use jsonify to return a proper JSON response
        return jsonify(result)
    
    except ValueError as ve:
        stack_trace = traceback.format_exc()
        logging.error(f"Validation error:\n{stack_trace}")
        return jsonify({"error": f"Validation error:\n{stack_trace}"}), 400
    
    except Exception as e:
        stack_trace = traceback.format_exc()
        logging.error(f"Error moderating text:\n{stack_trace}")
        return jsonify({"error": f"Unexpected error occurred:\n{stack_trace}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4999)
