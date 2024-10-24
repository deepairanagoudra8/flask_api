# from flask import Flask, request, jsonify
# import xmltodict
# import json
# import requests
#
# app = Flask(__name__)
#
# ENCRYPT_API_URL = 'http://localhost:5003/encrypt'  # Adjust the URL based on the encrypting API
#
# @app.route('/transform', methods=['POST'])
# def transform():
#     try:
#         # Extract the input data
#         data = request.get_json()
#         if not data or 'input_type' not in data or 'output_type' not in data:
#             return jsonify({"error": "Missing input_type or output_type"}), 400
#
#         input_type = data['input_type']
#         output_type = data['output_type']
#         content = data.get('data')
#
#         # Log the incoming request for debugging
#         print("Transformer received:", data)
#
#         if not content:
#             return jsonify({"error": "No data provided"}), 400
#
#         # Convert based on input_type and output_type
#         if input_type == 'xml' and output_type == 'json':
#             data_dict = xmltodict.parse(content)
#             json_data = json.dumps(data_dict)
#             print("Converted JSON Data:", json_data)
#             return jsonify({"data": json_data}), 200
#
#         elif input_type == 'json' and output_type == 'xml':
#             data_dict = json.loads(content)
#             xml_data = xmltodict.unparse(data_dict, pretty=True)
#             print("Converted XML Data:", xml_data)
#             return jsonify({"data": xml_data}), 200
#
#         else:
#             return jsonify({"error": "Unsupported input/output type combination"}), 400
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5002)

#
# from flask import Flask, request, jsonify
# import xmltodict
# import json
#
# app = Flask(__name__)
#
# transformers = {
#     'xml_to_json': 'xml_to_json',
#     'json_to_xml': 'json_to_xml',
#     'text_to_json': 'text_to_json',
#     'xml_to_text': 'xml_to_text',
#     'json_to_text': 'json_to_text'
# }
#
#
# def xml_to_json(content):
#     data_dict = xmltodict.parse(content)
#     json_data = json.dumps(data_dict)
#     return json_data
#
# def json_to_xml(content):
#     data_dict = json.loads(content)
#     xml_data = xmltodict.unparse(data_dict, pretty=True)
#     return xml_data
#
# def text_to_json(content):
#     json_data = json.dumps({"text": content})
#     return json_data
#
# def xml_to_text(content):
#     data_dict = xmltodict.parse(content)
#     text_data = json.dumps(data_dict)  # Basic conversion to text
#     return text_data
#
# def json_to_text(content):
#     data_dict = json.loads(content)
#     text_data = json.dumps(data_dict, indent=4)
#     return text_data
#
# @app.route('/transform', methods=['POST'])
# def transform():
#     try:
#         transformer_key = request.json.get('transformer')
#         content = request.json.get('data')
#
#         if not transformer_key or not content:
#             return jsonify({"error": "Missing transformer or data"}), 400
#
#         if transformer_key not in transformers:
#             return jsonify({"error": f"Invalid transformer key. Must be one of {list(transformers.keys())}"}), 400
#
#         # Dynamically call the corresponding transformer function
#         transformer_function = globals()[transformers[transformer_key]]
#         transformed_data = transformer_function(content)
#
#         return jsonify({"data": transformed_data}), 200
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5002)


from flask import Flask, request, jsonify
import xmltodict
import json

app = Flask(__name__)

transformers = {
    'xml_to_json': 'xml_to_json',
    'json_to_xml': 'json_to_xml',
    'text_to_json': 'text_to_json',
    'xml_to_text': 'xml_to_text',
    'json_to_text': 'json_to_text'
}

def xml_to_json(content):
    try:
        data_dict = xmltodict.parse(content)
        json_data = json.dumps(data_dict)
        print("XML to JSON:", json_data)
        return json_data
    except Exception as e:
        print("Error in xml_to_json:", str(e))
        raise

def json_to_xml(content):
    try:
        data_dict = json.loads(content)  # Ensure input is valid JSON
        xml_data = xmltodict.unparse(data_dict, pretty=True)
        print("JSON to XML:", xml_data)
        return xml_data
    except Exception as e:
        print("Error in json_to_xml:", str(e))
        raise

def text_to_json(content):
    try:
        json_data = json.dumps({"text": content})
        print("Text to JSON:", json_data)
        return json_data
    except Exception as e:
        print("Error in text_to_json:", str(e))
        raise

def xml_to_text(content):
    try:
        data_dict = xmltodict.parse(content)
        # Convert the data dictionary to a simple text representation
        text_data = '\n'.join(f"{key}: {value}" for key, value in data_dict['users']['user'][0].items())
        print("XML to Text:", text_data)
        return text_data
    except Exception as e:
        print("Error in xml_to_text:", str(e))
        raise

def json_to_text(content):
    try:
        data_dict = json.loads(content)  # Ensure input is valid JSON
        # Create a readable string format
        text_data = '\n'.join(f"{key}: {value}" for key, value in data_dict['user'].items())
        print("JSON to Text:", text_data)
        return text_data
    except Exception as e:
        print("Error in json_to_text:", str(e))
        raise



@app.route('/transform', methods=['POST'])
def transform():
    try:
        transformer_key = request.json.get('transformer')
        content = request.json.get('data')

        if not transformer_key or not content:
            return jsonify({"error": "Missing transformer or data"}), 400

        if transformer_key not in transformers:
            return jsonify({"error": f"Invalid transformer key. Must be one of {list(transformers.keys())}"}), 400

        # Dynamically call the corresponding transformer function
        transformer_function = globals()[transformers[transformer_key]]
        transformed_data = transformer_function(content)

        return jsonify({"data": transformed_data}), 200

    except Exception as e:
        print(f"Error in transform route: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
