import os
import sys

# Add cionuke and all its dependencies. If pip wasn't used to install, those dependencies will need
# to be added to PYTHONPATH env variable
lib_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.append(lib_path)

import ciocore.loggeria
import ciocore.config

# Setup logging
# Nuke monkeypatches sys.stdout, resulting logging from threads being unsafe
# Until a workaround is found, we only log to file
logging_dir = ciocore.loggeria.get_default_log_dir()
ciocore.loggeria.setup_conductor_logging(
    logger_level =  ciocore.loggeria.LEVEL_MAP.get(ciocore.config.config().config['log_level']),
    disable_console_logging = True,
    log_filepath=logging_dir,
    propagate=False
 )

print ("Conductor log: {}".format(logging_dir))

from cionuke.components import  environment, metadata, preview, assets

from cionuke import conductor_menu, entry 
from cionuke import const as k



nuke.menu("Nuke").addCommand("Render/Render selected on Conductor", lambda: entry.add_to_nodes())

if k.FEATURE_DEV:
    nuke.menu("Nuke").addCommand("Render/CIO Dev Refresh and Create", lambda: conductor_menu.dev_reload_recreate())
