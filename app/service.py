from flask import Flask, request, jsonify, render_template
import sys
from flasgger import Swagger
sys.path.append('..')
# from graph import Graph
# from common_util import *
# from db_util import *
import lib.seoul_road_graph
import lib.constant
# from seoul_road import get_seoul_road, calculate_a_path, calculate_paths
import psycopg
from psycopg_pool import ConnectionPool
import logging
import base64
import smtplib
import psutil
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from logging_util import *
import json

app = Flask(__name__)
swagger = Swagger(app)
logging_level = logging.DEBUG

logging.basicConfig(level=logging_level,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# db_pool = ConnectionPool(
#    "dbname=nav host=localhost user=postgres password=1234", min_size=1, max_size=10)

# db_pool = psycopg.pool.SimpleConnectionPool(
#     1,  # 최소 연결 수
#     10,  # 최대 연결 수
#     user='postgres',
#     password='1234',
#     host='localhost',
#     port='5432',
#     database='nav'
# )

# graph 객체 생성
# with db_pool.connection() as conn:
# seoul_road_graph = get_seoul_road(conn, logging_level)
# seoul_road_graph = Graph(db_pool.getconn(), logging_level)
# print(seoul_road_graph.get_graph_info())
seoul_road = lib.seoul_road_graph.SeoulRoad()

# DB 연결을 g 객체에 저장하는 함수
# @app.before_request
# def before_request():
#    g.db_conn = db_pool.connection()


@app.route('/')
def index():
    return render_template('index.html')

# Default Health Check


@app.route('/healthcheck')
def healthcheck():
    """
    서비스의 상태를 체크한다.

    ---
    responses:
        200:
            description: 서비스의 상태
            schema:
                type: object
                properties:
                    status:
                        type: string
                        description: API 서비스 동작 여부 
                        example: OK
                    cpu_usage:
                        type: number
                        description: CPU 사용률
                        example: 38.5
                    memory_usage:
                        type: number
                        description: 메모리 사용률
                        example: 52.3
    """

    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_usage = psutil.virtual_memory().percent
    return jsonify({'status': 'OK', 'cpu_usage': cpu_usage, 'memory_usage': memory_usage}), 200


@app.route('/min-path', methods=['GET'])
def get_path():
    """
    최적 경로를 계산한다.

    ---
    parameters:
        - name: start_spot
          in: query
          type: string
          required: true
          description: 출발지
        - name: end_spot
          in: query
          type: string
          required: true
          description: 도착지
        - name: weight_name
          in: query
          type: string
          required: false
          description: 가중치 이름
          default: distance
        - name: path_type
          in: query
          type: string
          required: false
          description: 경로 탐색 방법
          default: static
    responses:
        200:
            description: 최적 경로
            schema:
                type: object
                properties:
                    result:
                        type: boolean
                        description: 성공 여부
                        example: True
                    path_by_sections:
                        type: array
                        description: 구간 목록으로 표현한 경로
                        items:
                            type: integer
                            description: 구간 ID
                            example: 1220015100
                    path_by_spots:
                        type: array
                        description: 지점 목록으로 표현한 경로
                        items:
                            type: integer
                            description: 지점 ID
                            example: 1220015100
                    cost:
                        type: number
                        description: 경로의 전체 비용
                        example: 1234.5
        400:
            description: 잘못된 요청
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 에러 메시지
                        example: start_spot and end_spot are required
    """
    #    with db_pool.connection() as conn:
    start_spot_name = request.args.get('start_spot', default='', type=str)
    end_spot_name = request.args.get('end_spot', default='', type=str)
    weight_name = request.args.get(
        'weight_name', default='distance', type=str)
    path_type = request.args.get(
        'path_type', default='static', type=str).lower()
    if not start_spot_name or not end_spot_name:
        return jsonify({'error': 'start_spot and end_spot are required'}), 400
    if weight_name not in lib.constant.PERMITTED_WEIGHT[path_type]:
        return jsonify({'error': f'weight_name {weight_name} of path_type {path_type} is not supported'}), 400

    result = seoul_road.get_optimal_path(
        start_spot_name, end_spot_name, weight_name, path_type)
#    result = calculate_a_path(
#        conn, seoul_road_graph, start_spot_name, end_spot_name, weight_name, path_type)

#    print(result)
    if result['result'] == False:
        return jsonify({'error': 'Some Error Invoked', 'cause': result['cause']}), 400
    else:
        return jsonify(result), 200

# 개포동역
# 여의교


@app.route('/spot-ids', methods=['GET'])
def get_spot_ids():
    """
    지점의 이름으로 지점 ID의 목록을 반환한다.

    ---
    parameters:
        - name: spot_name
          in: query
          type: string
          required: true
          description: 지점의 이름
    responses:
        200:
            description: 지점 ID의 목록
            schema:
                type: object
                properties:
                    spot_ids:
                        type: array
                        description: 지점 이름에 대응되는 지점 ID의 목록
                        items:
                            type: integer
                            description: 구간 ID
                            example: 1220015100
        400:
            description: 잘못된 요청
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 에러 메시지
                        example: No spot found
    """
    spot_name = request.args.get('spot_name', type=str)
    if not spot_name:
        return jsonify({'error': 'spot_name is required'}), 400
    result = seoul_road.get_db_spots(spot_name)
    if result == None:
        return jsonify({'error': 'Some Error Invoked'}), 400
    if len(result) == 0:
        return jsonify({'error': 'No spot found'}), 400
    return jsonify({'spot_ids': result}), 200


@app.route('/spot-name', methods=['GET'])
def get_spot_name():
    """
    지점의 ID로 지점 이름을 반환한다.

    ---
    parameters:
        - name: spot_id
          in: query
          type: integer
          required: true
          description: 지점의 ID
    responses:
        200:
            description: 지점의 이름
            schema:
                type: object
                properties:
                    spot_name:
                        type: string
                        description: 지점의 이름
                        example: 개포동역
        400:
            description: 잘못된 요청
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 에러 메시지
                        example: spot_id is required
    """
    spot_id = request.args.get('spot_id', type=str)
    if not spot_id:
        return jsonify({'error': 'spot_id is required'}), 400
    result = seoul_road.get_db_spot_name(spot_id)
    if result == None:
        return jsonify({'error': 'Some Error Invoked'}), 400
    return jsonify({'spot_name': result}), 200


@app.route('/test-path', methods=['GET'])
def get_test_path():
    start_spot_name = request.args.get('start_spot', default='', type=str)
    end_spot_name = request.args.get('end_spot', default='', type=str)
    weight_name = request.args.get(
        'weight_name', default='distance', type=str)
    path_type = request.args.get(
        'path_type', default='static', type=str).lower()
    if not start_spot_name or not end_spot_name:
        return jsonify({'error': 'start_spot and end_spot are required'}), 400
    if weight_name not in lib.constant.PERMITTED_WEIGHT[path_type]:
        return jsonify({'error': f'weight_name {weight_name} of path_type {path_type} is not supported'}), 400

    result = seoul_road.get_optimal_path(
        start_spot_name, end_spot_name, weight_name, path_type)
#    result = calculate_a_path(
#        conn, seoul_road_graph, start_spot_name, end_spot_name, weight_name, path_type)

#    print(result)
    if result['result'] == False:
        return jsonify({'error': 'Some Error Invoked'}), 400
    # spot_list = ''
    # for spot in result['path_by_spots']:
    #     spot_list += spot + ','
    # spot_list = spot_list[:-1]

    result = seoul_road.get_db_spot_names(result['path_by_spots'])

    return jsonify(result), 200


@app.route('/spot-in-path', methods=['GET'])
def get_spot_infos():
    """
    지점의 ID의 목록으로 지점 정보 목록을 반환한다.

    ---
    parameters:
        - name: spot_ids
          in: query
          type: string
          required: true
          description: csv 형태로 정의된 지점의 ID의 목록
          example: 1220022800,1220024800,1220028000
    responses:
        200:
            description: 지점의 이름 목록
            schema:
                type: object
                properties:
                    spot_infos:
                        type: array
                        description: 지점 ID에 대응되는 지점의 정보 목록
                        items:
                            type: object
                            description: 각 지점의 이름과 Y 좌표, X 좌표 값
                            properties:
                                spot_name:
                                    type: string
                                    description: 지점의 이름
                                    example: 개포동역
                                y:
                                    type: number
                                    description: Y 좌표
                                    example: 37.489853
                                x:
                                    type: number
                                    description: X 좌표
                                    example: 127.066409 
        400:
            description: 잘못된 요청
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: 에러 메시지
                        example: Some Error Invoked
    """
    spot_ids = request.args.get('spot_ids', type=str)
    if not spot_ids:
        return jsonify({'error': 'spot_ids is required'}), 400
    spot_id_list = spot_ids.split(',')
    result = seoul_road.get_db_spot_infos(spot_id_list)
    if result == None:
        return jsonify({'error': 'Some Error Invoked'}), 400
    return jsonify({'spot_infos': result}), 200

# 1220022800,1220024800,1220028000,1220031300,1220034700,1220037400,1220035900,1220041800,1220039900,1220038300,1210040400,1210039200,1210038500,1210041200,1210037300,1210035800,1210006100,1210035700,1190001300,1190011000,1190017400,1190002500,1190026100,1190024600,1180030300,1190000300,1190002700,1180028000

# @app.route('/path/all', methods=['GET'])
# def get_all_path():
#     with db_pool.connection() as conn:
#         start_spot_name = request.args.get('start_spot', default='', type=str)
#         end_spot_name = request.args.get('end_spot', default='', type=str)
#         if not start_spot_name or not end_spot_name:
#             return jsonify({'error': 'start_spot and end_spot are required'}), 400

#         result = calculate_paths(
#             conn, seoul_road_graph, start_spot_name, end_spot_name, logging_level)

#     if result['result'] == False:
#         return jsonify({'error': 'Some Error Invoked'}), 400
#     else:
#         return jsonify(result), 200


# @app.route('/section/interpolate', methods=['GET'])
# def get_section_interpolate():
#     with db_pool.connection() as conn:
#         section_id = request.args.get('section_id', default='', type=str)
#         if not section_id:
#             return jsonify({'error': 'section_id is required'}), 400
#         result = get_interpolate_coordinate(conn, section_id, logging_level)
#     if result['result'] == False:
#         return jsonify({'error': 'Some Error Invoked'}), 400
#     else:
#         return jsonify(result), 200


# @app.route('/spot-names', methods=['GET'])
# def get_spot_names():
#     result = {}
#     with db_pool.connection() as conn:
#         result['data'] = get_vertex_name_list(conn)
#     if result['data'] == None:
#         return jsonify({'error': 'Some Error Invoked'}), 400
#     else:
#         return jsonify(result), 200


# @app.route('/save-image', methods=['POST'])
# def save_image():
#     # 이미지 데이터 추출
#     image_data = request.json['image']
#     image_data = image_data.split(',')[1]
#     image_data = base64.b64decode(image_data)

#     # 이미지 파일 생성
#     with open('image.png', 'wb') as f:
#         f.write(image_data)

#     # 메일 전송
#     msg = MIMEMultipart()
#     msg['Subject'] = "Captured Image"
#     msg['From'] = "sender@example.com"
#     msg['To'] = "edberg.s@gmail.com"

#     # 이미지 파일 첨부
#     image_data = open("image.png", 'rb').read()
#     image = MIMEImage(image_data, name="image.png")
#     msg.attach(image)

#     # 메일 전송
#     smtp_server = "smtp.example.com"
#     smtp_port = 587
#     smtp_user = "sender@example.com"
#     smtp_password = "password"
#     smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
#     smtp_conn.starttls()
#     smtp_conn.login(smtp_user, smtp_password)
#     smtp_conn.sendmail(msg['From'], msg['To'], msg.as_string())
#     smtp_conn.quit()

#     return "Image saved and sent to edberg.s@gmail.com"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8889, debug=True)
