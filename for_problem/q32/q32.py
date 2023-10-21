from flask import Flask, request, jsonify, render_template
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


# 템플릿 엔진으로 index.html을 렌더링한다.
@app.route('/')
def get_index():
    return (render_template('index.html'))

# 두 문자열을 파라미터로 받아서 두 문자열의 길이의 합을 반환하는 GET 메소드


@app.route('/total_length', methods=['GET'])
def total_length():
    """
    두 문자열을 파라미터로 받아서 두 문자열의 길이의 합을 반환한다.

    ---
    parameters:
      - name: string1
        in: query
        type: string
        required: true
        description: 문자열1
        example: innovation academy
      - name: string2
        in: query
        type: string
        required: true
        description: 문자열2
        example: exciting
    responses:
      200:
        description: 두 문자열의 길이의 합
        schema:
          type: object
          properties:
            total_length:
              type: integer
              description: 두 문자열의 길이의 합
              example: 26
      400:
        description: 파라미터 오류
        schema:
          type: object
          properties:
            error:
              type: string
              description: 오류 메시지
              example: One or two Parameter(s) missing
    """

    string1 = request.args.get('string1')
    string2 = request.args.get('string2')
    if string1 == None or string2 == None:
        return jsonify(error='One or two Parameter(s) missing'), 400
    return jsonify(total_length=len(string1) + len(string2))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)
