from termcolor import colored
from rm2trash.core.trash_manager import TrashManager
from rm2trash.core import global_variables


def need_confirm(func):
    def res(args):
        user_input = input(
            colored(
                "YOU CANNOT UNDO THIS!!! ARE YOU SURE? [y/n] ",
                color="red",
                attrs=["bold"],
            )
        )
        if user_input.upper() not in ["Y", "YES"]:
            return
        return func(args)

    return res


@need_confirm
def delete(args):
    tm = TrashManager()
    if args.indexes is not None:
        tm.delete_in_trash_by_indexes(args.indexes)
    else:
        tm.delete_in_trash_by_name_pattern(args.pattern)


def remove(args):
    tm = TrashManager()
    tm.move_files_or_dirs_to_trash(args.files_or_dirs)


@need_confirm
def empty(_):
    tm = TrashManager()
    tm.empty_trash()


def list_command(_):
    tm = TrashManager()
    tm.list_data()


def restore(args):
    tm = TrashManager()
    if args.indexes is not None:
        tm.restore_from_trash_by_indexes(args.indexes)
    else:
        tm.restore_from_trash_by_name_pattern(args.pattern)


def print_trash_path(_):
    print(global_variables.RM2TRASH_TRASH_PATH.absolute(), end="")


def print_data_path(_):
    print(global_variables.RM2TRASH_DATA_PATH.absolute(), end="")
