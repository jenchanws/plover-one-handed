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

  CONSONANTS = {
    "-F": "S-", "-P": "T-", "-L": "P-", "-T": "H-", "-D": "*",
    "-R": "S-", "-B": "K-", "-G": "W-", "-S": "R-", "-Z": "*",
  }

  MIRRORED_CONSONANTS = {
    "-F": "*", "-P": "H-", "-L": "P-", "-T": "T-", "-D": "S-",
    "-R": "*", "-B": "R-", "-G": "W-", "-S": "K-", "-Z": "S-",
  }

  PAIRED_VOWELS = {"-U": "A-", "-E": "O-"}

  UNPAIRED_VOWELS = {}

  def __init__(self, engine):
    super().__init__()
    self.engine = engine
    self.engine.hook_connect("config_changed", self._on_config_changed)
    # If we're in the middle of a two-handed stroke, this stores the first half
    self.half_stroke = None

    # If the layout is mirrored, the left half goes (from left-to-right)
    # * H- P- T- S- rather than S- T- P- H- *.
    self._mirrored = False
    # If the vowels are paired, A-/-U and O-/-E are on the same key.
    self._paired_vowels = False

  def start(self):
    self._on_config_changed(None)
    super().start()

  def stop(self):
    pass

  def _on_config_changed(self, _):
    self.half_stroke = set()

    system = self.engine.config["system_name"].lower()
    if not system.startswith("one-handed"):
      # Only override if we're using one of the one-handed layouts
      return

    # Override the default behavior when a new stroke is sent
    self.engine._machine.stroke_subscribers.pop(0)
    self.engine._machine.add_stroke_callback(self._machine_stroke_callback)

    self._mirrored = "mirrored" in system
    self._paired_vowels = "paired" in system

  def _machine_stroke_callback(self, steno_keys):
    self.engine._same_thread_hook(self._on_stroked, steno_keys)

  @property
  def _right_bank(self):
    keys = self.MIRRORED_CONSONANTS if self._mirrored else self.CONSONANTS
    if self._paired_vowels:
      keys.update(self.PAIRED_VOWELS)
    return keys

  def _right_to_left(self, key):
    """Return the left-hand version of the right-hand key 'key'."""
    return self._right_bank.get(key, key)

  @property
  def _left_bank(self):
    return set(self._right_bank.values())

  def _on_stroked(self, steno_keys):
    # Left half keys should not be mapped to anything, so this should (ideally)
    # be identical to 'steno_keys'
    orig_keys = {key for key in steno_keys if key not in self._left_bank}
    self.engine._trigger_hook('stroked', Stroke(orig_keys))

    if LEFT_ONLY in steno_keys and RIGHT_ONLY not in steno_keys:
      # If there is already a half stroke, send that out as its own stroke
      # then translate the current stroke separately
      if self.half_stroke:
        self.engine._on_stroked(self.half_stroke)
        self.half_stroke = set()
      steno_keys = {self._right_to_left(key) for key in orig_keys if key != LEFT_ONLY}
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
        steno_keys |= {self._right_to_left(key) for key in self.half_stroke}
        self.engine._on_stroked(steno_keys)
        self.half_stroke = set()
      else:
        self.half_stroke = steno_keys
  