import os
import random
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ランダムに返したい言葉のリスト
    responses = [
        "そうだね、プロテインだね",
        "筋肉は裏切らない",
        "ダンベルはずっと待っててくれる。ダンベルはズッ友",
        "寝ろ。",
        "覚えておいて。君は自由だ",
        "筋トレしよう",
        "なんとかなる",
        "鍛えて裏切らないもの。直感と筋肉",
        "筋肉留学。やー",
        "お金は使ったらなくなるけど、筋肉は一生の財産になる。",
        "筋肉の痛みは成長の印",
        "筋肉に聞いてみな",
        "きつくても辛くない!きつくても楽しい!",
        "大きな筋肉に、小さな悩みは宿らない",
        "筋肉はキッチンで作られる",
        "アルコールで消える程度の筋肉はいらない",
        "ジムに来るまでが筋トレだ",
        "休むこともまたトレーニング",

    ]

    # ランダムに1つ選ぶ
    reply_txt = random.choice(responses)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_txt))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
