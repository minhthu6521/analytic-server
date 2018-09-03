
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/analytic-server/")

from analytic-server import create_app

app = create_app('../config.py')
app.run()