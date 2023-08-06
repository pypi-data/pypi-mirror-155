#!/usr/bin/env python3

import argparse
from rm2trash.core import logging
from rm2trash.commands import subcommands


def main():
    parser = argparse.ArgumentParser(description="Simple trash commands: rm2trash.")
    parser.add_argument(
        "-l", "--log_level", type=str, default="INFO", help="Log level."
    )
    sub_parsers = parser.add_subparsers(
        title="subcommands", description="All subcommands", required=True
    )

    # Remove
    remove = sub_parsers.add_parser("remove", aliases=["rm"])
    remove.add_argument(
        "files_or_dirs", type=str, nargs="+", help="files or directories to remove."
    )
    remove.set_defaults(func=subcommands.remove)

    # Delete
    delete = sub_parsers.add_parser("delete", aliases=["del"])
    del_group = delete.add_mutually_exclusive_group(required=True)
    del_group.add_argument(
        "-i", "--indexes", type=int, nargs="+", help="trash item index to delete."
    )
    del_group.add_argument(
        "-p", "--pattern", type=str, help="pattern for trash item name to match."
    )
    delete.set_defaults(func=subcommands.delete)

    # Empty
    empty = sub_parsers.add_parser("empty")
    empty.set_defaults(func=subcommands.empty)

    # Restore
    restore = sub_parsers.add_parser("restore")
    restore_group = restore.add_mutually_exclusive_group(required=True)
    restore_group.add_argument(
        "-i", "--indexes", type=int, nargs="+", help="trash item index to restore."
    )
    restore_group.add_argument(
        "-p", "--pattern", type=str, help="pattern for trash item name to match."
    )
    restore.set_defaults(func=subcommands.restore)

    # List
    list_command = sub_parsers.add_parser("list", aliases=["ls"])
    list_command.set_defaults(func=subcommands.list_command)

    # Path
    trash_path = sub_parsers.add_parser("trash-path")
    trash_path.set_defaults(func=subcommands.print_trash_path)
    data_path = sub_parsers.add_parser("data-path")
    data_path.set_defaults(func=subcommands.print_data_path)

    args = parser.parse_args()
    logging.set_level(args.log_level)
    args.func(args)


if __name__ == "__main__":
    main()
