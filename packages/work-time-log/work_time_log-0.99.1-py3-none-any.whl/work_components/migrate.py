"""Temporary migration code between program versions."""


# Remove in v0.100 #


def warn_deprecated_switch_name(mode):
    """Warn if mode name is not "switch".
    To be removed in v0.100.
    """
    if mode != "switch":
        print(
            f'Command name "{mode}" is deprecated and will be removed in the '
            'upcoming version. Please use "switch" instead.'
        )


# Remove in v1 #


def raise_old_protocol_version(row):
    """Raise if row only has two elements (no category and message).
    To be removed in v1.
    """
    if len(row) == 2:
        raise IOError(
            "Detected old protocol version. "
            "Please migrate using v0.93 and then try again."
        )
