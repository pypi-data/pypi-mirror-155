from .bridge_interface import BridgeConnector
from .database_interface import DatabaseConnector

from inspector_commons.utils import IS_WINDOWS

if IS_WINDOWS:
    from .bridge_interface import WindowsBridgeConnector
