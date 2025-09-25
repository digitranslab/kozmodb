from .__about__ import __version__ as version
from .__about__ import __description__ as description
from kozmodb.integrations.libs.const import HANDLER_TYPE
from kozmodb.utilities import log

logger = log.getLogger(__name__)


try:
    from .kozmo_endpoint_handler import KozmoEndpointHandler as Handler

    import_error = None
except Exception as e:
    Handler = None
    import_error = e

title = "Kozmo Endpoint"
name = "kozmo_endpoint"
type = HANDLER_TYPE.ML
icon_path = 'icon.svg'
permanent = False

__all__ = ["Handler", "version", "name", "type", "title", "description", "import_error", "icon_path"]
