import datetime
import sys
from influxdb import InfluxDBClient
from flask import Flask, request, render_template

try:
    from credential import db_config
    influxdb_ip = db_config['influxdb_ip']
    influxdb_port = db_config['influxdb_port']
    influxdb_username = db_config['influxdb_username']
    influxdb_password = db_config['influxdb_password']
    influxdb_dbname = db_config['influxdb_dbname']
    db_cli = InfluxDBClient(
        influxdb_ip,
        influxdb_port,
        influxdb_username,
        influxdb_password,
        influxdb_dbname)
except (NameError, ImportError, KeyError) as e:
    sys.exit(1)

app = Flask(__name__, static_url_path='./static', static_folder='./static')
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  # 設置瀏覽器不緩存


@app.route('/weight-recorder', methods=['GET', 'POST'])
def start_here():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        weight = float(request.form.get('weight'))
        print(f'got input weight: {weight}')

        record_time = datetime.datetime.utcnow()

        data = [
            {
                'measurement': 'weightrecord',
                'tags': {'name': 'Balao'},
                'time': record_time,
                'fields': {'weight': weight}
            }
        ]
        print(db_cli.write_points(data))

        return render_template('result.html', weight=weight)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
