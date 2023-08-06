from ._cached import get_cached_license_info as get_cached_license_info
from ._exceptions import LicenseError as LicenseError
from ._helpers import print_error as print_error, print_warning as print_warning
from ._offline import get_offline_license_info as get_offline_license_info
from datetime import timedelta

def validate_all_with_user_prompt(product_name: str, account_id: str, keygen_verify_key: Union[str, None] = ..., product_id: Union[str, None] = ..., refresh_cache_period: timedelta = ..., cache_age_warning: timedelta = ..., cache_age_error: timedelta = ..., expiry_warning: timedelta = ..., message_before_user_prompt: Union[str, None] = ...) -> None: ...
