import os
import obsws_python as obs
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("OBS_PASSWORD")
if not password:
    raise ValueError(".envにOBS_PASSWORDが設定されてへん")

client = obs.ReqClient(
    host="localhost",
    port=4455,
    password=password,
)

version = client.get_version()
print("接続成功！")
print(f"OBSバージョン: {version.obs_version}")
print(f"WebSocketバージョン: {version.obs_web_socket_version}")

client.disconnect()
