#!/usr/bin/env python3
"""
Tiketa Flask Application Entry Point
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use environment variables for configuration in production
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(debug=debug, host='0.0.0.0', port=port)