from typing import Optional
from pathlib import Path
import yaml

import logging

logger = logging.getLogger(__name__)

class Config:
    def __init__(self,
            text: Optional[str] = None,
            file: Optional[Path] = None):
        if text is not None:
            self._parse(text)
        elif file is not None:
            text = Path(file).read_text()
            self._parse(text)
        else:
            raise Exception('Invalid configuration specified')

    def _parse(self, raw_text: str):
        yaml_obj = yaml.safe_load(raw_text)
        self._watchList = yaml_obj['watchlist']
        self._seq_unit_hdr_len = yaml_obj['seq_unit_hdr_len']
        self._num_of_msgs = int(yaml_obj['num_of_msgs'])
        self._msg_rate_p_sec = int(yaml_obj['msg_rate_p_sec'])
        self._verbose = bool(yaml_obj['verbose'])
        self._output_file = str(yaml_obj['output_file'])
        self._audit_log_file = str(yaml_obj['audit_log_file'])
        self._trace_log_file = str(yaml_obj['trace_log_file'])

    def seq_unit_hdr_len(self) -> int:
        return self._seq_unit_hdr_len

    def num_of_msgs(self) -> int:
        return self._num_of_msgs

    def msg_rate_p_sec(self) -> int:
        return self._msg_rate_p_sec

    def verbose(self) -> bool:
        return self._verbose

    def output_file(self) -> str:
        return self._output_file

    def audit_log_file(self) -> str:
        return self._audit_log_file

    def trace_log_file(self) -> str:
        return self._trace_log_file

    def watch_list(self):
        return self._watchList
