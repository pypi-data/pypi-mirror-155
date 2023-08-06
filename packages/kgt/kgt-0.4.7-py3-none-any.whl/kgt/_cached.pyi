from ._exceptions import ValidationError as ValidationError
from ._helpers import print_warning as print_warning, safeget as safeget, string_to_dict as string_to_dict, to_datetime as to_datetime
from datetime import timedelta
from pathlib import Path

def get_cached_license_info(account_id: str, key: str, keygen_verify_key: Union[str, None], cache_path: Union[Path, str], refresh_cache_period: Union[timedelta, int]): ...
