"""ETI/Domo light device."""

import colorsys
import logging
from typing import List

from .base import TYPE_OPENING, CameDevice, DeviceState

_LOGGER = logging.getLogger(__name__)

# Opening states
OPENING_STATE_STOPPED = 0
OPENING_STATE_OPEN = 1
OPENING_STATE_CLOSE = 2

class CameOpening(CameDevice):
    """ETI/Domo opening device class."""

    def __init__(self, manager, device_info: DeviceState):
        """Init instance."""
        super().__init__(manager, TYPE_OPENING, device_info)

    def switch(self, state):
        """Switch opening to new state."""
        if state is None:
            raise ValueError("State is required")

        self._check_act_id()

        cmd = {
            "cmd_name": "opening_move_req",
            "act_id": self.act_id,
            "wanted_status": state if state is not None else self.state,
        }
        log = {}
        if state is not None:
            log["status"] = cmd["wanted_status"]

        _LOGGER.debug('Set new state for opening "%s": %s', self.name, log)

        self._manager.application_request(cmd)

    @property
    def act_id(self) -> [int]:
        """Return the action ID for device."""
        return self._device_info.get("open_act_id")

    def is_opening(self):
        return self.state == OPENING_STATE_OPEN

    def is_closing(self):
        return self.state == OPENING_STATE_CLOSE

    def is_stopped(self):
        return self.state == OPENING_STATE_STOPPED

    def open(self):
        """Turn off light."""
        self.switch(OPENING_STATE_OPEN)

    def close(self):
        """Turn on light."""
        self.switch(OPENING_STATE_CLOSE)

    def stop(self):
        """Switch light to automatic mode."""
        self.switch(OPENING_STATE_STOPPED)

    def update(self):
        """Update device state."""
        self._force_update("openings")
