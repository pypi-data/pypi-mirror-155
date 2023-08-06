#!/usr/bin/env python3

# SPDX-License-Identifier: CC0-1.0

# Sample WSGI script for Hydrilla server.
#
# Copyright (C) 2022 Wojtek Kosior

# Uncomment the lines below if you want to use a virtualenv installation of
# Hydrilla.

#from pathlib import Path
#path = Path('/path/to/virtualenv/bin/activate_this.py')
#exec(path.read_text(), {'__file__': str(path)})

from hydrilla.server import start_wsgi

# The following line will initialize Hydrilla with the default, internal
# configuration while also attempting to load /etc/hydrilla/config.json if it's
# present.
application = start_wsgi(standalone_mode=False)

# Comment the above and uncomment this to use a different config file.

#from hydrilla.server import config
#from pathlib import Path
#application = start_wsgi(standalone_mode=False,
#                         obj=config.load([Path('/path/to/config.json')]))
