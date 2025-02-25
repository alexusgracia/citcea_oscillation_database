nohup python3 app.py > flask.log 2>&1 &

ps aux | grep app.py

kill -9 <PID>
