from flask import Flask, request, jsonify
from datetime import datetime
from flasgger import Swagger, APISpec, Schema, fields

app = Flask(__name__)
swagger = Swagger(app)

# # API 문서 생성을 위한 스키마 정의


# class DateSchema(Schema):
#     format = fields.String(description='날짜 형식')


# # API 문서 생성
# spec = APISpec(
#     title='Date API',
#     version='1.0.0',
#     openapi_version='3.0.2',
#     plugins=[
#         'apispec.ext.flask',
#         'apispec.ext.marshmallow',
#     ],
# )

# # API 문서에 API 정보 추가
# with app.test_request_context():
#     spec.path(view=get_date)


@app.route('/date', methods=['GET'])
def get_date():
    """
    날짜 정보를 반환하는 API

    ---
    parameters:
      - name: format
        in: query
        type: string
        required: false
        description: 날짜의 형식
    responses:
      200:
        description: 날짜 정보
        schema:
          type: object
          properties:
            date:
              type: string
              description: 날짜 정보
      400:
        description: 잘못된 요청
        schema:
          type: object
          properties:
            error:
              type: string
              description: 에러 메시지
    """
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
