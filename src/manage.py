"""Django's command-line utility for administrative tasks."""

import os
import sys


def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    return hasattr(sys, "gettrace") and sys.gettrace() is not None


def start_debugger():
    debug_port = os.getenv("DEBUG_PORT")
    if not debug_port or debugger_is_active():
        return

    try:
        import debugpy
        debugpy.listen(("0.0.0.0", int(debug_port)))
    except Exception:
        pass


def main():
    """Run administrative tasks."""
    sys.path.append(
        os.path.join(os.path.dirname(__file__), "..")
    )  # Add the project directory to PYTHONPATH
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line

        start_debugger()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
