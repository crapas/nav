from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/date', methods=['GET'])
def get_date():
    format_type = request.args.get('format')

    # format 파라미터가 없거나 '1'이 아닐 때의 처리
    if format_type is None:
        # return datetime.now().strftime('%Y-%m-%d')
        return jsonify(date=datetime.now().strftime('%Y-%m-%d'))
    elif format_type == '1':
        # return datetime.now().strftime('%Y%m%d')
        return jsonify(date=datetime.now().strftime('%Y%m%d'))
    else:
        # return "Invalid format", 400
        return jsonify(error='Invalid format'), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)
