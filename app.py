import os
import random
import csv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


@app.route("/")
def index():
    return "You call index()"


@app.route("/callback", methods=["POST"])
def callback():
    """Messaging APIからの呼び出し関数"""
    # LINEがリクエストの改ざんを防ぐために付与する署名を取得
    signature = request.headers["X-Line-Signature"]
    # リクエストの内容をテキストで取得
    body = request.get_data(as_text=True)
    # ログに出力
    app.logger.info("Request body: " + body)

    try:
        # signature と body を比較することで、リクエストがLINEから送信されたものであることを検証
        handler.handle(body, signature)
    except InvalidSignatureError:
        # クライアントからのリクエストに誤りがあったことを示すエラーを返す
        abort(400)

    return "OK"


def load_responses_from_csv():
    """CSVファイルから返答データを読み込み"""
    responses = []
    csv_file = "responses.csv"

    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                responses.append(row["message"])
        return responses
    except FileNotFoundError:
        print(f"CSVファイル '{csv_file}' が見つかりません。")
        return []
    except Exception as e:
        print(f"CSVファイル読み込みエラー: {e}")
        return []


def get_random_response():
    """CSVファイルからランダムな返答を取得"""
    responses = load_responses_from_csv()

    if responses:
        return random.choice(responses)
    else:
        return "返答データが見つかりませんでした。"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # CSVファイルからランダムな返答を取得
    reply_txt = get_random_response()

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_txt))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
