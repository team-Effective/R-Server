from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List


# FastAPIインスタンスを作成
app = FastAPI()

origins = [
    "https://client-hoge",
    "http://localhost",
    "http://localhost:8080",
]

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocketの接続管理を行うクラス
class ConnectionManager:
    # クライアントIDとWebSocketを紐づけるための関数
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    # WebSocketの接続を行う関数
    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        await websocket.accept()
        # すでに接続されている場合は、古い接続を切断する
        if client_id in self.active_connections:
            await self.active_connections[client_id].close()
            self.disconnect(client_id)
        # 新しい接続を登録する
        self.active_connections[client_id] = websocket
        print(f"接続中のクライアントID: {ws_manager.active_connections.keys()}")

    # WebSocketの切断を行う関数
    def disconnect(self, client_id: str) -> None:
        print(f"{client_id} の接続を切断します。")
        self.active_connections.pop(client_id, None)

    # プレイヤーごとにミッションの結果通知する関数
    async def send_individual_player_result(self, flag: bool, send_player_id: str) -> None:
        try:
            #flagがTrueの場合はミッション成功、Falseの場合はミッション失敗
            result = '成功' if flag else '失敗'
            print(f"クライアントID '{send_player_id}' に通知します。")
            await self.active_connections[send_player_id].send_text(result)
        except Exception as e:
            print(f"error : {e}")

    # プレイヤーごと(複数)に通知する関数
    async def send_individual_player_message(self, message: str, send_player_id: List[str]) -> None:
        try:
            for player_id in send_player_id:
                print(f"クライアントID '{player_id}' に通知します。")
                await self.active_connections[player_id].send_text(message)
        except Exception as e:
            print(f"error : {e}")

    # 全てのプレイヤーに対して通知する関数
    async def send_all_player_result(self, result: str) -> None:
        for connection in self.active_connections.values():
            await connection.send_text(result)

# ConnectionManagerクラスのインスタンスを作成
ws_manager = ConnectionManager()

# WebSocketの接続を行うエンドポイント
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    try:
        # WebSocketの接続を行う
        await ws_manager.connect(websocket, client_id)
        while True:
            # GMからのリクエストを受信し続ける
            await websocket.receive_json()
            # await websocket.receive_text()

    # WebSocketの切断を検知した場合の処理
    except WebSocketDisconnect as e:
        print(f"Client ID '{client_id}' disconnected. Reason: {e}")
        ws_manager.disconnect(client_id)

# GMからPlayerがミッション失敗or成功の判定を受け取るエンドポイント(指定したPlayerに通知する)
@app.post("/mission_flag/{client_id}")
async def mission_flag(send_player_id: str, flag: bool) -> None:
    try:
        await ws_manager.send_individual_player_result(flag, send_player_id)
    except Exception as e:
        print(f"error : {e}")

# GMからPlayerにミッションが作成されたことを通知するエンドポイント(指定したPlayerに通知する)
@app.post("/create_mission/{client_id}")
async def create_mission(send_player_id: List[str]) -> None:
    try:
        await ws_manager.send_individual_player_message('ミッション作成', send_player_id)

    except Exception as e:
        print(f"error : {e}")


# GMからPlayerにミッションが終了したことを通知するエンドポイント(全Playerに通知する)
@app.post("/mission_end/{client_id}")
async def mission_end() -> None:
    try:
        await ws_manager.send_all_player_result('ミッション終了')
    except Exception as e:
        print(f"error : {e}")

# ゲームのクリアを受け取るエンドポイント(全Playerに通知する)
@app.post("/game_clear/{client_id}")
async def game_clear() -> None:
    try:
        await ws_manager.send_all_player_result('ゲームクリア')
    except Exception as e:
        print(f"error : {e}")

# バリデーションエラーが発生した場合のエラーハンドリング
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content={"detail": exc.errors(), "body": exc.body},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )