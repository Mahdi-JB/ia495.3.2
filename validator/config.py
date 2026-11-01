"""Run configuration. Change ONE thing per run, then set a new RUN_NAME."""

RUN_NAME = "run1_length_cap"

# Which schema set to validate against.
#   "default" - permissive free-text fields (the realistic starting point)
#   "tight"   - allow-list style: character sets, enums, hard caps
#               (client guidance: specify exactly what MAY appear, rather than
#                blocklisting what may not)
SCHEMA_SET = "default"

DEFENSES = {
    "schema":             True,   # always on - the baseline
    "length_cap":         True,  # run 1
    "allow_list":         False,  # run 2
    "instruction_screen": False,  # run 3 - DENY-LIST, kept as a measured baseline
}

# Firewall operating mode, mirroring real firewall practice:
#   False -> enforcing: a detection blocks the packet
#   True  -> log only: a detection is recorded but the packet is forwarded anyway
LOG_ONLY = False

# Tunables - these end up in the results header, so they are part of the record
MAX_FREE_TEXT = 300
INSTRUCTION_PATTERNS = [
    "ignore previous", "ignore all previous", "disregard the above",
    "new instructions", "system:", "### ", "you must now", "output exactly",
]
APPROVED_RECIPIENTS = [
    "bob@example.com", "sara@example.com", "ops.team+alerts@example.co.uk",
]

# Optional downstream model (realism only - it is NOT the measurement)
SEND_TO_MODEL = True
MODEL = "llama3.2:3b"
TEMPERATURE = 0
SEED = 42
TRIALS = 3
CANARY_THRESHOLD = 60
