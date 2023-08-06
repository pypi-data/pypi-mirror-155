from typing import Optional

from .model import AppData
from .parallel import run_thread
from .component import warning_callback
from ..core import gpg
from ..core.crypt import load_authority_key


def load_authority_key_threaded(app_data: AppData) -> None:
    """Retrieve and refresh the key certification authority's PGP key in
    threaded mode. This avoids freezing the entire application when the
    refresh sometimes takes a couple of seconds.
    """
    # This function is responsible for taking the returned value from
    # load_authority_key() and assign it to the correct attribute of app_data.
    def update_authority_key_in_app_data(key: Optional[gpg.Key]) -> None:
        app_data.validation_authority_key = key

    show_warning = warning_callback("Certification Authority Key Loading Error")
    run_thread(
        load_authority_key,
        f_kwargs=dict(sett_config=app_data.config),
        forward_errors=show_warning,
        signals=dict(warning=show_warning, result=update_authority_key_in_app_data),
        report_config=app_data.config,
    )
