from flask import Flask, render_template
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


# 템플릿 엔진으로 index.html을 렌더링한다.
@app.route('/')
def get_index():
    return (render_template('index.html'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889, debug=True)
