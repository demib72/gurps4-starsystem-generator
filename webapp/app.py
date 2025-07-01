from flask import Flask, render_template, request, jsonify
from stargen import generate_star_system, StarSystemConfig
from stargen.utils.serializer import serialize_star_system

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    open_cluster = request.form.get('open_cluster')
    num_stars = request.form.get('num_stars')
    age = request.form.get('age')

    config = StarSystemConfig(
        open_cluster=True if open_cluster == 'true' else False if open_cluster == 'false' else None,
        num_stars=int(num_stars) if num_stars else None,
        age=float(age) if age else None,
    )

    ss = generate_star_system(config)
    data = serialize_star_system(ss)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
