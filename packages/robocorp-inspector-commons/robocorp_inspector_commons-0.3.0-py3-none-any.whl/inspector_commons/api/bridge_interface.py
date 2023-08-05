from inspector_commons.bridge.browser_bridge import BrowserBridge
from inspector_commons.bridge.windows_bridge import WindowsBridge
from inspector_commons.config import Config
from inspector_commons.context import Context


class BridgeConnector(BrowserBridge):
    def __init__(self, logger, *args, **kwargs):
        config = Config()
        config.set("remote", None)
        config.set("debug", True)
        context = Context(logger, config)
        super().__init__(context, *args, **kwargs)


class WindowsBridgeConnector(WindowsBridge):
    def __init__(self, logger, *args, **kwargs):
        config = Config()
        config.set("remote", None)
        config.set("debug", True)
        context = Context(logger, config)
        super().__init__(context, *args, **kwargs)
