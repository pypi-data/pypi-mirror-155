#!/usr/bin/env python3

""" The DAO for the recess files. """

import datetime as dt
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import DefaultDict, Dict, List, Optional

from work_components import util
from work_components.consts import RECESS_DIRECTORY_NAME, RECESS_FILE_EXTENSION

# Each recess file is a JSON dictionary with three elements:
# holidays          = []  --  a list of holidays
# reduced_hour_days = {}  --  a dictionary of days with reduced hours, with each value being the reduced hour value
# vacations         = []  --  a list of vacations
#
# For example:
# {
#   "holidays" : [
#     "2021-01-05"
#   ],
#   "reduced_hour_days" : {
#     "2021-01-05": 4.0
#   },
#   "vacations" : [
#     "2021-01-03"
#   ]
# }
#
# Each list needs to be unique, but days may be in multiple.


# TODO:
# 1.) Prevent duplicates (or handle smartly)
# 2.) Rename directory?
# 3.) Store holidays and vacations separately in wvac file? (Would allow to use the list as a single source of truth of vacations.)

DATE_FORMAT: str = "%Y-%m-%d"


@dataclass
class Recess:
    date: dt.date

    def __init__(self, date: dt.date):
        self.date = date

    def __str__(self) -> str:
        return self.date.strftime(DATE_FORMAT)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Recess):
            return False
        return o.date == self.date

    def __lt__(self, other) -> bool:
        return self.date < other.date

    def print(self) -> str:
        return str(self)


@dataclass
class Holiday(Recess):
    pass


@dataclass
class Vacation(Recess):
    pass


@dataclass
class ReducedHourDay(Recess):
    hours: float = 0

    def __init__(self, date: dt.date, hours: float):
        super().__init__(date=date)
        self.hours = hours

    def print(self) -> str:
        return f"{self.date.strftime(DATE_FORMAT)} ({self.hours} hours)"


@dataclass
class AssociatedRecess:
    holiday: Optional[Holiday] = None
    vacation: Optional[Vacation] = None
    reduced_hour_day: Optional[ReducedHourDay] = None

    @property
    def empty(self):
        return self == AssociatedRecess()


class ExistsError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class RecessFile:
    """ Writes to file on update. Creates directory and file if nonexistent. """

    holidays_k: str = "holidays"
    reduceds_k: str = "reduced_hour_days"
    vacations_k: str = "vacations"

    # work_directory (see work_components/consts.py)
    # |- recess/
    #    |- 2020.wvac
    #    |- 2021.wvac
    def __init__(self, recess_directory: Path, year: int) -> None:
        self.recess_directory = recess_directory
        self.file: Path = Path(recess_directory, f"{year}.{RECESS_FILE_EXTENSION}")
        self.holidays: List[Holiday] = []
        self.reduced_hour_days: List[ReducedHourDay] = []
        self.vacations: List[Vacation] = []
        if not self.file.exists():
            return

        with self.file.open(mode="r") as vf:
            try:
                vf_json = json.load(vf)
            except Exception as e:
                raise IOError(f"Invalid free days file {self.file}: {e}") from e

        # We intentionally do not check for an erroneous file here,
        # as this should not be edited by the user.

        self.holidays = [
            Holiday(date=dt.datetime.strptime(holi_day, DATE_FORMAT).date())
            for holi_day in vf_json[RecessFile.holidays_k]
        ]
        self.reduced_hour_days = [
            ReducedHourDay(
                date=dt.datetime.strptime(redu_day, DATE_FORMAT).date(), hours=hours
            )
            for redu_day, hours in vf_json[RecessFile.reduceds_k].items()
        ]
        self.vacations = [
            Vacation(date=dt.datetime.strptime(vaca_day, DATE_FORMAT).date())
            for vaca_day in vf_json[RecessFile.vacations_k]
        ]

    def add_any(self, container: List, add_us: List):
        if container and add_us:
            assert isinstance(add_us[0], type(container[0]))
        if exist := list(filter(lambda a: a in container, add_us)):
            raise ExistsError(
                f"Free day(s) already stored: {','.join([str(e) for e in exist])}"
            )
        container.extend(add_us)
        self._write_out()

    def remove(self, date: dt.date) -> None:
        """ Remove a recess day. If the date is present in more than one list, raises. """
        in_holidays: bool = Holiday(date=date) in self.holidays
        in_reduceds: bool = any([rhd.date == date for rhd in self.reduced_hour_days])
        in_vacations: bool = Vacation(date=date) in self.vacations
        if not in_holidays and not in_reduceds and not in_vacations:
            raise ValueError(
                f"Free day {date.strftime('%d.%m.%Y')} could not be "
                "removed, as it does not exist."
            )
        # XOR (^) is only True if exactly one of the arguments is True.
        if not (in_holidays ^ in_reduceds ^ in_vacations):
            raise NotImplementedError(
                "Ambiguous! Date is present in multiple free days lists. "
                "Please remove manually."
            )

        if in_holidays:
            self._remove_any(self.holidays, Holiday(date=date))
        elif in_reduceds:
            for rhd in self.reduced_hour_days:
                if rhd.date == date:
                    self._remove_any(self.reduced_hour_days, rhd)
        elif in_vacations:
            self._remove_any(self.vacations, Vacation(date=date))

    def _remove_any(self, container: List, remove_me):
        if container:
            assert isinstance(remove_me, type(container[0]))
        try:
            container.remove(remove_me)
        except ValueError as val_err:
            raise RuntimeError("Could not delete nonexistent free day.") from val_err
        self._write_out()

    def _write_out(self):
        """ Write cached days to file. Creates directory and file if nonexistent. """

        # Create recess directory if it does not exist.
        self.recess_directory.mkdir(exist_ok=True)

        out_dict = {
            RecessFile.holidays_k: [str(h) for h in sorted(self.holidays)],
            RecessFile.reduceds_k: {
                str(rhd): rhd.hours for rhd in sorted(self.reduced_hour_days)
            },
            RecessFile.vacations_k: [str(v) for v in sorted(self.vacations)],
        }

        with self.file.open(mode="w") as vf:
            json.dump(out_dict, vf, indent="\t")


class RecessDao:
    """ Interface to manage recess. Handles `RecessFile`s internally. """

    def __init__(self, work_directory: Path) -> None:
        self.directory: Path = work_directory.joinpath(RECESS_DIRECTORY_NAME)
        self.recess_files: Dict[int, RecessFile] = {}

    def _get(self, year: int) -> RecessFile:
        """ Load RecessFile from cache. If not cached, load from disk. """
        if year not in self.recess_files:
            self.recess_files[year] = RecessFile(self.directory, year)
        return self.recess_files[year]

    def get_holidays(self, year: int) -> List[Holiday]:
        return self._get(year=year).holidays

    def get_reduced_hour_days(self, year: int) -> List[ReducedHourDay]:
        return self._get(year=year).reduced_hour_days

    def get_vacations(self, year: int) -> List[Vacation]:
        # TODO: We could return these as ranges of continuous days
        return self._get(year=year).vacations

    def has_days(self, year: int) -> bool:
        rf: RecessFile = self._get(year=year)
        return (
            len(rf.holidays) > 0
            or len(rf.reduced_hour_days) > 0
            or len(rf.vacations) > 0
        )

    def add_holiday(self, date: dt.date) -> None:
        rf: RecessFile = self._get(year=date.year)
        rf.add_any(rf.holidays, [Holiday(date=date)])

    def add_reduced_hour_day(self, date: dt.date, hours: float) -> None:
        rf: RecessFile = self._get(year=date.year)
        rf.add_any(rf.reduced_hour_days, [ReducedHourDay(date=date, hours=hours)])

    def add_vacation(self, first_day: dt.date, last_day: dt.date) -> None:
        dates: List[dt.date] = util.get_period(first_day, last_day)
        vacations_by_year: DefaultDict[int, List[Vacation]] = defaultdict(list)
        for date in dates:
            vacations_by_year[date.year].append(Vacation(date=date))
        for year in vacations_by_year:
            rf: RecessFile = self._get(year=year)
            rf.add_any(rf.vacations, vacations_by_year[year])

    def remove(self, dates: List[dt.date]) -> None:
        """ Remove recess day(s). If any date is present in more than one list, raises. """
        for date in dates:
            self._get(year=date.year).remove(date=date)

    def get_recess_for(self, date: dt.date) -> AssociatedRecess:
        """Return all associated recess objects for the given date."""
        associated_recess = AssociatedRecess()
        r_file: RecessFile = self._get(year=date.year)

        its_rhds = list(filter(lambda d: d.date == date, r_file.reduced_hour_days))
        if len(its_rhds) > 1:
            raise ExistsError(f"Multiple reduced days found for {date}")

        if len(its_rhds) == 1:
            associated_recess.reduced_hour_day = its_rhds[0]

        if (holiday := Holiday(date=date)) in r_file.holidays:
            associated_recess.holiday = holiday
        if (vacation := Vacation(date=date)) in r_file.vacations:
            associated_recess.vacation = vacation
        return associated_recess

    def reduced_hours(self, date: dt.date) -> Optional[float]:
        """
        Get the reduced hours for a given date. The lowest value is returned, that
        means if a date is added as reduced_hour_day with 2 hours and as a vacation,
        0 is returned.

        Returns None if hours are not reduced on the given day.
        """
        associated_recess: AssociatedRecess = self.get_recess_for(date)
        if associated_recess.empty:
            return None

        if associated_recess.reduced_hour_day is not None:
            return associated_recess.reduced_hour_day.hours

        # Has holiday or vacation
        return 0
