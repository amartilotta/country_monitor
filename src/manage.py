"""Django's command-line utility for administrative tasks."""
import os
import sys


def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None

def start_debugger():
    if not os.getenv("DEBUG_PORT") or debugger_is_active():
        return
    
    import debugpy
    try:
        debugpy.listen(("0.0.0.0", int(os.getenv("DEBUG_PORT"))))
    except Exception as e:
        pass

def main():
    """Run administrative tasks."""
    sys.path.append(
        os.path.join(os.path.dirname(__file__), "..")
    )  # Agrega el directorio del proyecto al PYTHONPATH
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
