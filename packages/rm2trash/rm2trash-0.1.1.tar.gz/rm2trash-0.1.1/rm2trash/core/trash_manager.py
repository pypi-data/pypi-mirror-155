import re
import json
import glob
import shutil
import datetime
from pathlib import Path
from typing import List, Dict
from rm2trash.core import logging
from rm2trash.core.global_variables import RM2TRASH_TRASH_PATH, RM2TRASH_DATA_PATH


class TrashManager:
    def __init__(self) -> None:
        self.database_file = RM2TRASH_DATA_PATH / "rm2trash_db.json"
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.data = self._read_data()

    def search_item(self, pattern: str) -> List[int]:
        res = []
        for i, data in enumerate(self.data):
            if re.search(pattern, data["name"]):
                res.append(i)
        return res

    def move_files_or_dirs_to_trash(self, files_or_dirs: List[str]) -> None:
        path_lists = []
        for f_or_d in files_or_dirs:
            path_lists += glob.glob(f_or_d)

        count = 0
        for f_or_d in path_lists:
            source = Path(f_or_d)
            if not source.exists:
                logging.warning("{} not exists.".format(source))
                continue

            if source.is_symlink():
                logging.info("Unlink {} -> {}.".format(source, source.readlink()))
                source.unlink()
                continue

            target = RM2TRASH_TRASH_PATH / source.name
            suffix_int = 1
            while target.exists():
                target = RM2TRASH_TRASH_PATH / "{}.{}".format(source.name, suffix_int)
                suffix_int += 1

            shutil.move(source, target)
            logging.info("Move {} to trash.".format(str(source)))

            new_item = dict(
                name=source.name,
                source_path=str(source.absolute()),
                trash_path=str(target.absolute()),
                datetime=datetime.datetime.now().strftime(self.time_format),
            )
            self.data.append(new_item)
            count += 1
        logging.info("{} item(s) moved to trash.".format(count))
        self._dump_data(self.data)

    def delete_in_trash_by_indexes(self, indexes: List[int]) -> None:
        index_to_delete = []
        for index in indexes:
            if index < 0 or index >= len(self.data):
                logging.warning(
                    "Invalid index {}, trash currently has {} items.".format(
                        index, len(self.data)
                    )
                )
                continue

            data = self.data[index]
            target = Path(data["trash_path"])
            if not target.exists():
                logging.warning(
                    "Trash to delete {} not exists. Do nothing.".format(target)
                )
            else:
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
                logging.info("Permanently delete {}.".format(data["trash_path"]))
            index_to_delete.append(index)
        logging.info("{} item(s) deleted.".format(len(index_to_delete)))
        self.data = [
            data for i, data in enumerate(self.data) if i not in index_to_delete
        ]
        self._dump_data(self.data)

    def delete_in_trash_by_name_pattern(self, pattern: str) -> None:
        indexes = self.search_item(pattern)
        self.delete_in_trash_by_indexes(indexes)

    def empty_trash(self) -> None:
        self.delete_in_trash_by_indexes(list(range(len(self.data))))

    def restore_from_trash_by_indexes(self, indexes: List[int]) -> None:
        index_to_delete = []
        for index in indexes:
            if index < 0 or index >= len(self.data):
                logging.warning(
                    "Invalid index {}, trash currently has {} items.".format(
                        index, len(self.data)
                    )
                )
                continue

            data = self.data[index]
            source = Path(data["source_path"])
            target = Path(data["trash_path"])
            if not target.exists():
                logging.warning(
                    "Trash item to restore {} not exists. Remove item.".format(target)
                )
                index_to_delete.append(index)
                continue
            if source.exists():
                logging.warning(
                    "Source to restore {} exists. Do nothing.".format(source)
                )
                continue

            shutil.move(target, source)
            index_to_delete.append(index)
            logging.info("Restore {}.".format(source))
        logging.info("{} item(s) restored.".format(len(index_to_delete)))
        self.data = [
            data for i, data in enumerate(self.data) if i not in index_to_delete
        ]
        self._dump_data(self.data)

    def restore_from_trash_by_name_pattern(self, pattern: str) -> None:
        indexes = self.search_item(pattern)
        self.restore_from_trash_by_indexes(indexes)

    def list_data(self) -> None:
        for i, data in enumerate(self.data):
            print(
                '{}: name="{}", source="{}", rm_time="{}"'.format(
                    i, data["name"], data["source_path"], data["datetime"]
                )
            )

    def _read_data(self) -> List[Dict]:
        if not self.database_file.exists():
            return []

        with open(self.database_file, "r") as f:
            return json.load(f)

    def _dump_data(self, data: list) -> None:
        with open(self.database_file, "w") as f:
            json.dump(data, f, indent=2)
