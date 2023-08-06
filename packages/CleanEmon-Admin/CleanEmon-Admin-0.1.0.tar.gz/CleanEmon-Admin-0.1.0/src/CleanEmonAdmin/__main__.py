import argparse

from .scripts import add_meta
from .scripts import disaggregate
from .scripts import reset_file

parser = argparse.ArgumentParser(description="A set of useful admin-tools for the CleanEmon ecosystem")
parser.add_argument("script", choices=["add-meta", "disaggregate", "reset"],
                    help="script to run")
parser.add_argument("dates", nargs="*", help="list of dates (YYYY-MM-DD) to be used in `disaggregate` or `reset`")
parser.add_argument("--no-safe", action="store_false", help="prompt before proceeding with critical actions")


args = parser.parse_args()

if args.script == "add-meta":
    add_meta()

elif args.script == "disaggregate":
    if args.dates:
        disaggregate(*args.dates, no_prompt=args.no_safe)
    else:
        print("You should provide at least one date")

elif args.script == "reset":
    if args.dates:
        reset_file(*args.dates, no_prompt=args.no_safe)
    else:
        print("You should provide at least one date")

else:
    print("Error on input")
