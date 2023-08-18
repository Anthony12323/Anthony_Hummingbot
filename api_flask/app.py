from flask import Flask, render_template, request
import asyncio
import os
import sys
sys.path.append('hbot-remote-client-py')
from hbotrc import BotCommands

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forms', methods=['POST'])
def handle_form():
    data = request.get_json(force=True)
    #bid_spread = data['bid_spread']
    #ask_spread = data['ask_spread']

    #with open("Users/anthonybenitez/Desktop/Hummingbot/control/hbot-remote-client-py/examples/commands_example.py") as f:
        #exec(f.read())

    send_config(data)
    
    return '''processed'''

async def run_commands(client, data):
    if "bid_spread" in data:
        resp = client.config([('bid_spread', data['bid_spread'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "ask_spread" in data:
        resp = client.config([('ask_spread', data['ask_spread'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "minimum_spread" in data:
        resp = client.config([('minimum_spread', data['minimum_spread'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "order_refresh_time" in data:
        resp = client.config([('order_refresh_time', data['order_refresh_time'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "max_order_age" in data:
        resp = client.config([('max_order_age', data['max_order_age'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "order_refresh_tolerance_pct" in data:
        resp = client.config([('order_refresh_tolerance_pct', data['order_refresh_tolerance_pct'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "order_amount" in data:
        resp = client.config([('order_amount', data['order_amount'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "price_ceiling" in data:
        resp = client.config([('price_ceiling', data['price_ceiling'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "price_floor" in data:
        resp = client.config([('price_floor', data['price_floor'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "price_ceiling_pct" in data:
        resp = client.config([('price_ceiling_pct', data['price_ceiling_pct'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "price_floor_pct" in data:
        resp = client.config([('price_floor_pct', data['price_floor_pct'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "ping_pong_enabled" in data:
        resp = client.config([('ping_pong_enabled', data['ping_pong_enabled'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "order_levels" in data:
        resp = client.config([('order_levels', data['order_levels'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "order_level_amount" in data:
        resp = client.config([('order_level_amount', data['order_level_amount'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "order_level_spread" in data:
        resp = client.config([('order_level_spread', data['order_level_spread'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)
    if "price_type" in data:
        resp = client.config([('price_type', data['price_type'])])
        print(f'Config Command Response: {resp}')
        await asyncio.sleep(1)

def send_config(data):
    _id = "hbot1"
    client = BotCommands(
        host='localhost',
        port=1883,
        username='Anthony',
        password='Anthony',
        bot_id=_id,
    )
    asyncio.new_event_loop().run_until_complete(run_commands(client, data))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
