from flask import Flask, request, jsonify
from datetime import datetime
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/date', methods=['GET'])
def get_date():
    """
    오늘의 날짜를 지정한 형식으로 반환한다.

    ---
    parameters:
      - name: format
        in: query
        type: string
        required: false
        description: 출력 날짜 형식 (1 YYYY-MM-DD, 2 YYYYMMDD)
    responses:
      200:
        description: Today's date
        schema:
          type: object
          properties:
            date:
              type: string
              example: 20231013
              description: Today's date
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    format_type = request.args.get('format')

    # format 파라미터가 없거나 1인 경우
    if format_type is None or format_type == '1':
        return jsonify(date=datetime.now().strftime('%Y-%m-%d'))
    # format 파라미터가 2인 경우
    elif format_type == '2':
        return jsonify(date=datetime.now().strftime('%Y%m%d'))
    # format 파라미터가 잘못된 값일 때의 처리
    else:
        return jsonify(error='Invalid format parameter'), 400


@app.route('/filename', methods=['POST'])
def get_filename():
    """
    업로드 한 파일의 이름을 반환한다.

    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: upload 할 파일
    responses:
      200:
        description: 파일의 이름
        schema:
          type: object
          properties:
            size:
              type: string
              example: sample.txt
              description: 파일의 이름
      400:
        description: Invalid request
        schema:
          type: object
          properties:
            error:
              type: string
              example: 요청이 잘못 되었습니다.
              description: Error message
    """
    file = request.files.get('file')

    # 파일이 없을 때의 처리
    if file is None:
        return jsonify(error='File not found'), 400

    # 파일 크기 구하기
    # size = os.path.getsize(file.filename)

    return jsonify(name=file.filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)
