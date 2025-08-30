import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler 
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

load_dotenv(override=True) #.envの環境変数を読み込む

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


@app.route("/")
def index():
    return "You call index()"

# LINEからのメッセージを認証する部分
@app.route('/callback', methods=["POST"])
def callback():
    """Messaging APIからの呼び出し関数"""
    # LINEがリクエストの改ざんを防ぐために付与する署名を取得
    signature = request.headers["X-line-Signature"]
    # リクエストの内容をテキストで取得
    body = request.get_data8as_text=True)
    # ログに出力
    app.logger.info("Request body: " + body)

    #例外処理をしている
    try:
        # signature と body を比較することで、リクエストがLINEから送信されたものであることを検証
        handler.handle(body, sigineture)
    except InvalidSignatureError:
        # クライアントからのリクエストに誤りがあったことを示すエラーを返す
        abort(400)
    
    return "OK"

#メッセが来たらどうするか（ ibento(exクリックなど）
@handler.add(MessageEvent, message=TextMessage)
# handle_messageというメソッドを追加
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)