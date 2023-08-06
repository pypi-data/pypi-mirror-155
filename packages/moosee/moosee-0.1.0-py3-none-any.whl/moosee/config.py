# ========================================================================== #
# Config file for moosee program                                             #
# ========================================================================== #

# Available lock modes:
# fixed (locks mouse at mouse_x_lock and mouse_y_lock coords)
# free  (locks mouse at current position)
lock_mode: str = "free"
lock_x: int = 500
lock_y: int = 500

# Moosee does <times> photos every <delay> seconds
times: int = 3
delay: float = 1.0
# Enable to return mouse position to locked if it was moved within delay 
return_to_lock: bool = False

# hotkeys
# if open hotkey is none, script will be active from the beginning
open_hotkey: str or None = None
close_hotkey: str = "alt + q"

# Supported save modes:
# dir | directory | default
# Devs will add telegram mode in future!
save_mode: str = "dir"
# If telegram bot or telegram specified, you can specify
# user or channel to send pics.
# In directory mode specify relative or absolute path to dir
save_dir: str = "."


do_catch_camera: bool = True
do_catch_screen: bool = True
do_execute_script: bool = False
# better to specify absolute path
executable: str = ""
