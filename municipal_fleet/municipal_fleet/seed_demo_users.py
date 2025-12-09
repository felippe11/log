#!/usr/bin/env python
"""
Helper script to seed demo municipalities and users from the project root,
wrapping the existing Django management command.
"""
import os

import django
from django.core.management import call_command

# Default to dev settings for local usage; can be overridden via env var.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "municipal_fleet.settings.dev")


def main():
    django.setup()
    call_command("seed_demo_users")


if __name__ == "__main__":
    main()
