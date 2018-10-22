from app import app
from config import settings

if __name__ == "__main__":
    # from app.svc.match.playground.chessboard import Chessboard
    # chessboard = Chessboard()
    # chessboard.move(1,2,4,2)
    # chessboard.move(4, 2, 4, 6)
    # chessboard.move(4, 6, 0, 6)
    app.run(host="0.0.0.0", port=settings.PORT_NUMBER)
