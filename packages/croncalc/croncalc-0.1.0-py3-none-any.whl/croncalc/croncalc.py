from itertools import product
from datetime import datetime
from typing import Generator, Optional, Union


class croncalc:
    min_max_values = {
        "day_w": (0, 6),
        "month": (1, 12),
        "day": (1, 31),
        "hour": (0, 23),
        "minute": (0, 59),
    }
    cron_fields = ["minute", "hour", "day", "month", "day_w"]

    def __init__(self, cron_string: str, dt: datetime, or_day: bool = False) -> None:
        self.cron_string = cron_string
        self.cron_values = dict(zip(self.cron_fields, cron_string.split(" ")))
        self.current_dt = dt
        self.or_day = or_day

    @property
    def current_dt_dict(self) -> dict[str, int]:
        return {
            "minute": self.current_dt.minute,
            "hour": self.current_dt.hour,
            "day": self.current_dt.day,
            "month": self.current_dt.month,
            "day_w": self.current_dt.isoweekday(),
        }

    @staticmethod
    def _get_values_from_desc(
        min_val: int,
        max_val: int,
        desc: str,
        actual_val: Optional[int] = None,
        is_prev: Optional[bool] = None,
    ) -> Union[list[int], Generator[int, None, None]]:
        """actual_val and is_prev are needed only if desc=='*'."""
        if desc == "*":
            max_val = min(actual_val + 1, max_val)
            if is_prev:
                return {min_val, actual_val - 1, actual_val, max_val}
            return {min_val, actual_val - 1, actual_val, actual_val + 1, max_val}
        if "-" in desc and "/" in desc:
            min_val = int(desc.split("-")[0])
            max_val = int(desc.split("-")[-1].split("/")[0])
            every = int(desc.split("/")[-1])
            return range(min_val, max_val + 1, every)
        elif "," in desc:
            return (int(i) for i in desc.split(","))
        elif "-" in desc:
            l, u = (int(i) for i in desc.split("-"))
            return range(l, u + 1)
        elif "/" in desc:
            every = int(desc.split("/")[-1])
            return range(min_val, max_val + 1 + every, every)
        else:
            return [int(desc)]

    def find_by_day_week(
        self, is_prev: bool, possible_values: dict[str, list[int]]
    ) -> datetime:
        if self.cron_values["day"] == "*":
            # every 'day' value is okay if 'day_w' != "*" and 'day' == "*"
            possible_values["day"] = []
        cron_string = self.cron_string.split(" ")
        cron_string[2] = "*"  # day = "*"
        cron_string[-1] = "*"  # day_w = "*"
        cron_string = " ".join(cron_string)
        iter = croncalc(cron_string, self.current_dt)
        self.current_dt = iter._add(is_prev)
        if self.or_day:
            while (
                self.current_dt.day not in possible_values["day"]
                or self.current_dt.isoweekday() not in possible_values["day_w"]
            ):
                self.current_dt = iter._add(is_prev)
        else:
            while (
                self.current_dt.day not in possible_values["day"]
                and self.current_dt.isoweekday() not in possible_values["day_w"]
            ):
                self.current_dt = iter._add(is_prev)
        return self.current_dt

    def get_possible_values(
        self, is_prev: bool = False, all_values: bool = False
    ) -> dict[str, Union[list[int], Generator[int, None, None]]]:
        """Get dictionary of allowed values, from month to minute."""
        if all_values:
            return {
                key: range(min_val, max_val + 1)
                if self.cron_values[key] == "*"
                else self._get_values_from_desc(
                    min_val=min_val,
                    max_val=max_val,
                    desc=self.cron_values[key],
                    actual_val=self.current_dt_dict[key],
                    is_prev=is_prev,
                )
                for key, (min_val, max_val) in self.min_max_values.items()
            }
        return {
            key: self._get_values_from_desc(
                min_val=min_val,
                max_val=max_val,
                desc=self.cron_values[key],
                actual_val=self.current_dt_dict[key],
                is_prev=is_prev,
            )
            for key, (min_val, max_val) in self.min_max_values.items()
        }

    def _add(self, is_prev: bool) -> datetime:
        def _get_vals(possible_values: dict[str, set[int]]):
            possible_values.pop("day_w")
            current_tuple = (
                self.current_dt.month,
                self.current_dt.day,
                self.current_dt.hour,
                self.current_dt.minute,
            )
            vals_copy = product(*possible_values.values())
            if is_prev:
                vals_copy = reversed(list(vals_copy))
                vals = []
                others = []
                for val in vals_copy:
                    if val[0] > current_tuple[0]:
                        others.append(val)
                        continue
                    elif val[0] == current_tuple[0]:
                        if val[1] > current_tuple[1]:
                            others.append(val)
                            continue
                        elif val[1] == current_tuple[1]:
                            if val[2] > current_tuple[2]:
                                others.append(val)
                                continue
                            elif val[2] == current_tuple[2]:
                                if val[3] >= current_tuple[3]:
                                    others.append(val)
                                    continue
                    vals.append(val)
                vals.extend(others)
            else:
                vals = []
                others = []
                for val in vals_copy:
                    if val[0] < current_tuple[0]:
                        others.append(val)
                        continue
                    elif val[0] == current_tuple[0]:
                        if val[1] < current_tuple[1]:
                            others.append(val)
                            continue
                        elif val[1] == current_tuple[1]:
                            if val[2] < current_tuple[2]:
                                others.append(val)
                                continue
                            elif val[2] == current_tuple[2]:
                                if val[3] <= current_tuple[3]:
                                    others.append(val)
                                    continue
                    vals.append(val)
                vals.extend(others)
            return vals
            # for val in vals_copy:
            #     for x, y in zip(val, current_tuple):
            #         if x < y:
            #             others.append(val)
            #             break
            #         elif x == y:
            #             continue
            #         else:
            #             vals.append(val)
            #             break
            #     else:
            #         if x == y:
            #             others.append(val)

        whole_time = self.current_dt.replace(second=0, microsecond=0)
        possible_values = self.get_possible_values(is_prev, all_values=True)

        if self.cron_values["day_w"] != "*":
            return self.find_by_day_week(is_prev, possible_values)

        vals = _get_vals(possible_values)
        if is_prev:
            for month, day, hour, minute in vals:
                try:
                    new_dt = whole_time.replace(
                        minute=minute, hour=hour, day=day, month=month
                    )
                    if new_dt > self.current_dt:
                        new_dt = new_dt.replace(year=new_dt.year - 1)
                    break
                except ValueError:  # invalid date: day is out of range for month
                    continue
        else:
            for month, day, hour, minute in vals:
                try:
                    new_dt = whole_time.replace(
                        minute=minute, hour=hour, day=day, month=month
                    )
                    if new_dt < self.current_dt:
                        new_dt = new_dt.replace(year=new_dt.year + 1)
                    break
                except ValueError:  # invalid date: day is out of range for month
                    continue
        self.current_dt = new_dt
        return self.current_dt

    def get_next(self) -> datetime:
        return self._add(is_prev=False)

    def get_prev(self) -> datetime:
        return self._add(is_prev=True)

    @staticmethod
    def match(cron_str: str, dt: datetime) -> bool:
        """Checks whether dt matches with the cront string 'cron_str'."""

        def check_day():
            if (
                iter.current_dt_dict["day"] not in possible_values["day"]
                and iter.current_dt_dict["day_w"] not in possible_values["day_w"]
            ):
                return False
            return True

        iter = croncalc(cron_str, dt)
        possible_values = iter.get_possible_values(all_values=True)
        for key, value in iter.current_dt_dict.items():
            if value not in possible_values[key]:
                if key == "day":
                    if not check_day():
                        return False
                elif key == "day_w":
                    continue  # it was already checked in 'if key == "day"'
                return False
        return True
