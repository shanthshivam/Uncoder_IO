from app.converter.core.exceptions.core import BasePlatformException
from app.converter.core.exceptions.iocs import BaseIOCsException
from app.converter.core.exceptions.parser import BaseParserException
from app.converter.core.exceptions.render import BaseRenderException


def handle_translation_exceptions(func):
    def exception_handler(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result:
                print("Translated successfully.")
                return True, result
            else:
                print("Unexpected error.")
                return False, f"Unexpected error. To resolve it, please, contact us via GitHub."
        except (BaseParserException, BasePlatformException, BaseRenderException, BaseIOCsException) as err:
            print(f"Unexpected error. {str(err)}")
            return False, str(err)
        except Exception as err:
            print(f"Unexpected error. {str(err)}")
            return False, f"Unexpected error. To resolve it, please, contact us via GitHub."
    return exception_handler
