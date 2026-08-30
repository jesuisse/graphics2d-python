"""
This contains constants used by the graphics2d framework
"""

# Layouting

HORIZONTAL = 0
VERTICAL = 1

ALIGN_START = 0
ALIGN_CENTERED = 1
ALIGN_END = 2
FILL = 4
SHRINK = 8
EXPAND = 16

# These are shift constants for horizontal and vertical Layout flags
# e.g. ALIGN_END << V_LAYOUT = V_ALIGN_END
H_LAYOUT = 7
V_LAYOUT = 13

H_ALIGN_START = 64
H_ALIGN_CENTERED = 128
H_ALIGN_END = 256
H_FILL = 512
H_SHRINK = 1024
H_EXPAND = 2048

V_ALIGN_START = 4096
V_ALIGN_CENTERED = 8192
V_ALIGN_END = 16384
V_FILL = 32768
V_SHRINK = 65536
V_EXPAND = 131072
