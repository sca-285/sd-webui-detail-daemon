"""Detail Daemon presets: starting points for common jobs.

Each preset lists the daemons it uses, in tab order (I, II, ...). A daemon
lists only what differs from DEFAULT. Picking a preset writes these values
into the tabs it uses and switches the other tabs off (their values stay).

Amounts are written for CFG 6. In `both` mode the effect grows with CFG
(sigma is scaled by 1 - amount x 0.1 x CFG), so when a preset is picked its
amounts and offsets are rescaled to the CFG currently set: the same preset then
has about the same strength at CFG 3 as at CFG 9. These are starting values,
not rules; tune Amount first, then Start / End.
"""

REFERENCE_CFG = 6.0

DEFAULT = dict(
    active=True, hires=False, mode="both", amount=0.10, start=0.20, end=0.80, bias=0.50,
    exponent=1.0, start_offset=0.0, end_offset=0.0, fade=0.0, smooth=True,
)

# Controls whose value scales with CFG when a preset is applied.
CFG_SCALED = ("amount", "start_offset", "end_offset")

CUSTOM = "Custom"

PRESETS = {
    "Subtle detail": dict(
        about="A light lift in detail that suits almost any image. One daemon.",
        daemons=[dict(amount=0.10)],
    ),
    "Balanced detail": dict(
        about="Clearly more detail without changing the picture. A good everyday setting. One daemon.",
        daemons=[dict(amount=0.18, end=0.85, bias=0.45)],
    ),
    "Fine texture (skin, fabric, hair)": dict(
        about="Targets the late steps, where small texture forms. Leaves shapes and composition alone. One daemon.",
        daemons=[dict(amount=0.20, start=0.45, end=0.90, bias=0.35)],
    ),
    "Mid-scale detail (scenery, architecture)": dict(
        about="Targets the middle steps: more objects, folds and structure, not just texture. One daemon.",
        daemons=[dict(amount=0.15, start=0.15, end=0.65, bias=0.50)],
    ),
    "Rich detail + cleanup": dict(
        about="Daemon I adds a lot of detail, daemon II removes the excess noise at the very end. Two daemons.",
        daemons=[dict(amount=0.30, start=0.20, end=0.75, bias=0.40, exponent=1.2),
                 dict(amount=-0.10, start=0.80, end=1.00, bias=0.50)],
    ),
    "Smoother, cleaner": dict(
        about="Less detail: cleaner flat areas for illustration and anime styles. One daemon.",
        daemons=[dict(amount=-0.12)],
    ),
    "Hires fix detail": dict(
        about="Daemon I for the first pass, daemon II for the Hires fix pass. Enable Hires fix. Two daemons.",
        daemons=[dict(amount=0.10),
                 dict(hires=True, amount=0.15, start=0.10, end=0.70, bias=0.40)],
    ),
}

CHOICES = [CUSTOM, *PRESETS]


def daemons_for(name, cfg):
    """The preset's daemons as complete dicts, amounts rescaled for `cfg`."""
    preset = PRESETS.get(name)
    if preset is None:
        return None
    try:
        factor = REFERENCE_CFG / max(float(cfg), 1.0)
    except (TypeError, ValueError):
        factor = 1.0
    out = []
    for d in preset["daemons"]:
        full = {**DEFAULT, **d}
        for k in CFG_SCALED:
            full[k] = round(full[k] * factor, 3)
        out.append(full)
    return out
