# -*- coding: utf-8 -*-
import os
from app import app

if __name__ == '__main__':
    import werkzeug.serving
    werkzeug.serving.run_simple("localhost", int(os.environ.get("PORT", 8080)), app)
    # port = int(os.environ.get("PORT", 8080))
    # app.run('0.0.0.0', port=port)