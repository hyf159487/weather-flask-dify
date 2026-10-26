from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VALID_TOKEN = "itcast"

CITY_CODES = {
    "北京": "101010100",
    "上海": "101020100",
    "广州": "101280101",
    "深圳": "101280601",
    "杭州": "101210101",
    "成都": "101270101",
    "武汉": "101200101",
    "西安": "101110101",
    "南京": "101190101",
    "桂林": "101300501",
    "重庆": "101040100",
    "天津": "101030100",
    "苏州": "101190401",
    "郑州": "101180101",
    "长沙": "101250101",
    "青岛": "101120201",
    "大连": "101070201",
    "宁波": "101210401",
    "厦门": "101230201",
    "福州": "101230101",
    "济南": "101120101",
    "合肥": "101220101",
    "南昌": "101240101",
    "昆明": "101290101",
    "南宁": "101300101",
    "贵阳": "101260101",
    "哈尔滨": "101050101",
    "长春": "101060101",
    "沈阳": "101070101",
    "石家庄": "101090101",
    "太原": "101100101",
    "呼和浩特": "101080101",
    "乌鲁木齐": "101130101",
    "拉萨": "101140101",
    "兰州": "101160101",
    "西宁": "101150101",
    "银川": "101170101",
    "海口": "101310101",
    "三亚": "101310201"
}


@app.post("/weather")
def get_current_weather():
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {VALID_TOKEN}":
        return jsonify({"status": "error", "message": "Invalid Authorization header"}), 403

    body = request.get_json()
    location = body.get("location")
    if not location:
        return jsonify({"status": "error", "message": "location不能为空"})

    city_code = CITY_CODES.get(location)
    if not city_code:
        return jsonify({
            "status": "error",
            "message": f"暂不支持{location}, 支持城市：{','.join(CITY_CODES.keys())}"
        })

    url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return jsonify({"status": "error", "message": f"天气接口请求失败: {str(e)}"})

    try:
        forecast = data["data"]["forecast"][0]
        weather_type = forecast["type"]
        high = forecast["high"]
        low = forecast["low"]
        return f"{location}今天天气：{weather_type}，{low} ~ {high}"
    except (KeyError, IndexError) as e:
        return jsonify({"status": "error", "message": f"天气数据解析失败: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
