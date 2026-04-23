import sys
import traceback

try:
    from app.main import app
    print("SUCCESS")
except Exception as e:
    with open("error_log.txt", "w") as f:
        f.write(traceback.format_exc())
