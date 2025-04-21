from flask import Flask

app = Flask(__name__)

@app.route('/flag')
def flag():
    return "HOSHINO{i5_pr0t0tYp3_p0llUt10n_hum4nm4d3_&_h41z41_g0}"

if __name__ == '__main__':
    app.run(host='localhost', port=6000)