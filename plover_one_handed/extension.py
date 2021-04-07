from threading import Thread
from plover import log
from plover.steno import Stroke

LEFT_ONLY = "l"
RIGHT_ONLY = "r"

RIGHT_TO_LEFT = {
  "-F": "S-", "-P": "T-", "-L": "P-", "-T": "H-", "-D": "*",
  "-R": "S-", "-B": "K-", "-G": "W-", "-S": "R-", "-Z": "*",
}

LEFT = set(RIGHT_TO_LEFT.values())

OTHER_KEYS = {
  "A-": "A-", "O-": "O-", "#": "#",
  **{"-" + key: "-" + key for key in "EUFRPBLGTSDZ"}
}

class OneHandedLayout(Thread):

  def __init__(self, engine):
    super().__init__()
    self.engine = engine
    self.engine.hook_connect("config_changed", self._on_config_changed)
    # If we're in the middle of a two-handed stroke, this stores the first half
    self.half_stroke = None

  def start(self):
    self._on_config_changed(None)
    super().start()

  def stop(self):
    pass

  def _on_config_changed(self, _):
    self.half_stroke = set()
    # Override the default behavior when a new stroke is sent
    self.engine._machine.stroke_subscribers.pop(0)
    self.engine._machine.add_stroke_callback(self._machine_stroke_callback)

  def _machine_stroke_callback(self, steno_keys):
    self.engine._same_thread_hook(self._on_stroked, steno_keys)

  def _on_stroked(self, steno_keys):
    # Left half keys should not be mapped to anything, so this should (ideally)
    # be identical to 'steno_keys'
    orig_keys = {key for key in steno_keys if key not in LEFT}
    self.engine._trigger_hook('stroked', Stroke(orig_keys))

    if LEFT_ONLY in steno_keys and RIGHT_ONLY not in steno_keys:
      # If there is already a half stroke, send that out as its own stroke
      # then translate the current stroke separately
      if self.half_stroke:
        self.engine._on_stroked(self.half_stroke)
        self.half_stroke = set()
      steno_keys = {RIGHT_TO_LEFT.get(key, key) for key in orig_keys if key != LEFT_ONLY}
      self.engine._on_stroked(steno_keys)
    elif RIGHT_ONLY in steno_keys:
      if self.half_stroke:
        self.engine._on_stroked(self.half_stroke)
        self.half_stroke = set()
      steno_keys = {key for key in orig_keys if key != RIGHT_ONLY}
      self.engine._on_stroked(steno_keys)
    else:
      if self.half_stroke:
        # If there is already a half stroke, that would be the LEFT half of
        # the final stroke, and the current one would be the RIGHT half
        steno_keys |= {RIGHT_TO_LEFT.get(key, key) for key in self.half_stroke}
        self.engine._on_stroked(steno_keys)
        self.half_stroke = set()
      else:
        self.half_stroke = steno_keys
  