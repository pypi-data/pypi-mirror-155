#!/usr/bin/env python3
""" Argument names and the `Arguments` class. """

import argparse
import datetime as dt
import textwrap
from typing import Dict, List, Optional, Union

from work_components import consts
from work_components.util import Color

NAME = "work"

# Commands
# fmt: off
START_NAME =    "start"
STOP_NAME =     "stop"
CANCEL_NAME =   "cancel"
RESUME_NAME =   "resume"
SWITCH_NAMES = ["switch", "pause"]
ADD_NAME =      "add"
STATUS_NAMES = ["status", "s"]
HOURS_NAMES =  ["hours", "h"]
LIST_NAMES =   ["list", "ls"]
DAY_NAME =      "day"
VIEW_NAME =     "view"
EXPORT_NAME =   "export"
EDIT_NAMES =   ["edit", "e"]
REMOVE_NAMES = ["remove", "rm"]
RECESS_NAMES =   ["free-days", "recess"]

CONFIG_NAME =   "config"
REHASH_NAME =   "rehash"
MAINTENANCE_NAMES = [CONFIG_NAME, REHASH_NAME]
# fmt: on


class Mode:
    """ Definition of a 'mode', such as `work start`. """

    def __init__(
        self,
        names: Union[str, List[str]],
        help_text: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.names = [names] if isinstance(names, str) else names
        self.help = help_text
        self.description = description or help_text
        self.parents: List[argparse.ArgumentParser] = []

    def add_as_parser(self, subparsers) -> argparse.ArgumentParser:
        """
        Add this mode to the subparsers action as a new mode parser and
        return the created parser object.
        """
        aliases = self.names[1:] if len(self.names) > 1 else []
        return subparsers.add_parser(
            self.names[0],
            aliases=aliases,
            help=self.help,
            description=self.description,
            parents=self.parents,
        )

    def create_fish_completion(self, all_modes: List[str]) -> str:
        """ Convert given arguments to fish completion. """
        for field in ["help", "description"]:
            if self.__dict__[field]:
                self.__dict__[field] = self.__dict__[field].replace('"', '\\"')

        # Right now, we intentionally ignore aliases.
        return (
            f"complete --command {NAME}"
            f" --arguments \"{' '.join(self.names)}\""
            f" --description \"{self.help or self.description or ''}\""
            f" --condition \"not __fish_seen_subcommand_from {' '.join(all_modes)}\""
        )


MODES: Dict[str, Mode] = {
    START_NAME: Mode(START_NAME, help_text="Start work"),
    STOP_NAME: Mode(STOP_NAME, help_text="Stop work"),
    ADD_NAME: Mode(ADD_NAME, help_text="Add a log entry"),
    SWITCH_NAMES[0]: Mode(
        SWITCH_NAMES,
        help_text="Short-hand for stop & start",
        description=(
            "A short-hand for stop and start. Flags are passed to stop, meaning they "
            "refer to the stopped run."
        ),
    ),
    CANCEL_NAME: Mode(CANCEL_NAME, help_text="Cancel the current run"),
    RESUME_NAME: Mode(
        RESUME_NAME, help_text='Resume the last run today (undo "work stop")'
    ),
    STATUS_NAMES[0]: Mode(STATUS_NAMES, help_text="Print the current status"),
    HOURS_NAMES[0]: Mode(HOURS_NAMES, help_text="Calculate hours worked"),
    LIST_NAMES[0]: Mode(
        LIST_NAMES,
        help_text="List work records",
        description=(
            "List work records (by default the current day)."
            " For other ranges use the optional arguments."
        ),
    ),
    DAY_NAME: Mode(
        DAY_NAME,
        help_text="List the current day with all details",
        description=(
            "List the current day with all details. Shorthand for "
            '"list --include-active --with-breaks --list-empty"'
        ),
    ),
    VIEW_NAME: Mode(
        VIEW_NAME,
        help_text="Views on work records",
        description=(
            "Views on work records (by default of the current day). "
            "Similar to list, but groups by aspects other than date."
        ),
    ),
    EXPORT_NAME: Mode(EXPORT_NAME, help_text="Export records as CSV"),
    EDIT_NAMES[0]: Mode(
        EDIT_NAMES,
        help_text="Edit work records",
        description="Edit work records (by default from the current day)",
    ),
    REMOVE_NAMES[0]: Mode(
        REMOVE_NAMES,
        help_text="Remove records from the log",
        description="Remove records from the log (by default from the current day)",
    ),
    RECESS_NAMES[0]: Mode(
        RECESS_NAMES,
        help_text="Manage free days (vacation, holidays, part-time days)",
        description="Manage free days (vacation, holidays, part-time days). Default mode: --list",
    ),
    CONFIG_NAME: Mode(
        CONFIG_NAME, help_text="Check and interact with the configuration"
    ),
    REHASH_NAME: Mode(
        REHASH_NAME, help_text="Recompute verification checksum after manual edits"
    ),
}


class Arguments:
    """ Allows creating parsers or completions. """

    @staticmethod
    def create_argparser(version, program) -> argparse.ArgumentParser:
        """ Create an `ArgumentParser` instance and return it. """

        parser = argparse.ArgumentParser(
            prog=NAME,
            description="Time tracking with an interaction model inspired by git.",
            epilog="To find out more, check the help page of individual modes.",
        )
        # fmt: off
        parser.add_argument("-H", "--help-verbose", action="store_true",
            help="show a longer help output, similar to a man page")
        parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {version}")
        parser.add_argument("-d", "--debug", action="store_true", help="use a debug directory")
        parser.add_argument("-y", "--dry-run", action="store_true", help="only print output")
        # fmt: on

        modes = parser.add_subparsers(title="modes", dest="mode")

        # Shared help texts
        date_help_text = (
            'Either a date (such as "12.", "1.1." or "5.09.19"), or any prefix of '
            '"today" or "yesterday".'
        )
        # TODO Consider if / how the keyword "again" should be documented
        time_help_text = (
            'Either a time (such as "1:20" or "12:1") or "now" for the current time '
            "(rounded)."
        )

        ## Parent parser for optional entry fields ##

        category_message_parent = argparse.ArgumentParser(add_help=False)
        category_message_parent.add_argument(
            "-c",
            "--category",
            metavar="C",
            help=(
                "Categorize the entry. Anything is allowed, but this will be used for "
                "summarization."
            ),
        )
        category_message_parent.add_argument(
            "-m", "--message", metavar="M", help="Free-text description of the entry."
        )

        MODES[STOP_NAME].parents.append(category_message_parent)
        MODES[ADD_NAME].parents.append(category_message_parent)
        MODES[SWITCH_NAMES[0]].parents.append(category_message_parent)

        ## Parent parsers for dates ##

        single_date_sel_parent = argparse.ArgumentParser(add_help=False)
        single_date_sel_modes = single_date_sel_parent.add_mutually_exclusive_group()
        multi_date_sel_parent = argparse.ArgumentParser(add_help=False)
        multi_date_sel_modes = multi_date_sel_parent.add_mutually_exclusive_group()

        # The alternative (two disjunct parents) would not allow the exclusivity guarantee
        for date_sel_modes in [single_date_sel_modes, multi_date_sel_modes]:
            date_sel_modes.add_argument(
                "-d", "--date", metavar="DATE", help=f"Any DATE – {date_help_text}"
            )
            date_sel_modes.add_argument(
                "-1",
                "--yesterday",
                action="store_const",
                dest="date",
                const="yesterday",
                help="Short-hand for --date yesterday.",
            )
            date_sel_modes.add_argument(
                "-D",
                "--day",
                metavar="DAY",
                help=(
                    'A weekday or any matching prefix, e.g. "Mon", "su" or "wednesday". '
                    "Always selects from the past seven days."
                ),
            )
        multi_date_sel_modes.add_argument(
            "-p",
            "--period",
            metavar="DATE",
            nargs=2,
            help="A specified period, defined by two DATEs.",
        )
        multi_date_sel_modes.add_argument(
            "-s",
            "--since",
            metavar="DATE",
            help="The period between DATE and today.",
        )
        multi_date_sel_modes.add_argument(
            "-w",
            "--week",
            metavar="W",
            type=int,
            nargs="?",
            const=-1,
            help="The current week (no argument) or week no. W of this year.",
        )
        multi_date_sel_modes.add_argument(
            "-m",
            "--month",
            metavar="DATE",
            nargs="?",
            const="today",
            help="The current month (no argument) or the month containing DATE.",
        )

        # Single date selection
        MODES[ADD_NAME].parents.append(single_date_sel_parent)
        MODES[EDIT_NAMES[0]].parents.append(single_date_sel_parent)
        MODES[REMOVE_NAMES[0]].parents.append(single_date_sel_parent)

        # Multi date selection
        MODES[LIST_NAMES[0]].parents.append(multi_date_sel_parent)
        MODES[VIEW_NAME].parents.append(multi_date_sel_parent)
        MODES[EXPORT_NAME].parents.append(multi_date_sel_parent)

        # SINGLE TIME modes

        start_mode = MODES[START_NAME].add_as_parser(modes)
        start_mode.set_defaults(func=program.start)
        start_mode.add_argument(
            "--force",
            action="store_true",
            help="Start anew even if a run is already active.",
        )

        stop_mode = MODES[STOP_NAME].add_as_parser(modes)
        stop_mode.set_defaults(func=program.stop)

        # start / stop have a single time argument
        for single_time_mode in [start_mode, stop_mode]:
            single_time_mode.add_argument("time", metavar="TIME", help=time_help_text)

        # DOUBLE TIME modes

        add_mode = MODES[ADD_NAME].add_as_parser(modes)
        add_mode.set_defaults(func=program.add)
        add_mode.add_argument(
            "time_from", metavar="TIME", help="Start time. " + time_help_text
        )
        add_mode.add_argument(
            "time_to", metavar="TIME", help="End time. " + time_help_text
        )
        add_mode.add_argument(
            "--force",
            action="store_true",
            help=(
                "Add even if an existing entry overlaps. "
                "This can result in three outcomes: The old entry will be... "
                "(1) subsumed (removed). "
                "(2) cut (shortened) to make space. "
                "(3) split in two parts, which are then cut (see 2)."
            ),
        )

        switch_mode = MODES[SWITCH_NAMES[0]].add_as_parser(modes)
        switch_mode.set_defaults(func=program.switch)
        switch_mode.add_argument(
            "time_s",
            metavar="TIME",
            help=("The time to switch runs at. TIME: " + time_help_text),
        )
        switch_mode.add_argument(
            "-s",
            "--start",
            metavar="TIME",
            help="Instead of restarting immediately, start the next run at TIME.",
        )

        # STATE dependent modes

        cancel_mode = MODES[CANCEL_NAME].add_as_parser(modes)
        cancel_mode.set_defaults(func=program.cancel)

        resume_mode = MODES[RESUME_NAME].add_as_parser(modes)
        resume_mode.set_defaults(func=program.resume)
        resume_mode.add_argument(
            "--force",
            action="store_true",
            help="Resume even if a run is active.",
        )

        status_mode = MODES[STATUS_NAMES[0]].add_as_parser(modes)
        status_mode.set_defaults(func=program.status)
        status_mode.add_argument(
            "-o", "--oneline", action="store_true", help="Print status in one line."
        )

        hours_mode = MODES[HOURS_NAMES[0]].add_as_parser(modes)
        hours_mode.set_defaults(func=program.hours)
        hours_mode.add_argument(
            "-d",
            "--workday",
            action="store_true",
            dest="h_workday",
            help="Also show the end time of a complete workday with respect to the week balance.",
        )
        hours_mode.add_argument(
            "-u",
            "--until",
            metavar="H:M",
            dest="h_until",
            help="Also show the hours that will have been worked at the given time.",
        )
        hours_target = hours_mode.add_mutually_exclusive_group()
        target_arg_help_text_stub = "Also show the end time for "
        hours_target.add_argument(
            "-t",
            "--target",
            metavar="H:M",
            dest="h_target",
            help=target_arg_help_text_stub
            + "a workday of the specified length in hours:minutes.",
        )
        hours_target.add_argument(
            "-8",
            "--eight",
            action="store_const",
            dest="h_target",
            const="8",
            help=target_arg_help_text_stub
            + "an 8 hour day (equivalent to --target 8).",
        )
        # Modifiers
        hours_mode.add_argument(
            "-p",
            "--pause",
            metavar="H:M",
            dest="h_pause",
            help="Assume for all calculations that work will be paused hours:minutes.",
        )
        hours_mode.add_argument(
            "-s",
            "--start",
            metavar="H:M",
            dest="h_start",
            help=(
                "Override the start time assumed by hours. May only be used when no "
                "run is active."
            ),
        )

        # PROTOCOL interaction modes

        list_mode = MODES[LIST_NAMES[0]].add_as_parser(modes)
        list_mode.set_defaults(func=program.list_entries)
        list_mode.add_argument(
            "-e", "--list-empty", action="store_true", help="Include empty days."
        )
        list_mode.add_argument(
            "-i",
            "--include-active",
            action="store_true",
            help="Include the active run.",
        )
        list_mode.add_argument(
            "-b", "--with-breaks", action="store_true", help="Also show break lengths."
        )
        list_mode.add_argument(
            "-t",
            "--only-time",
            action="store_true",
            help="Only show record times and omit all optional record attributes.",
        )

        day_mode = MODES[DAY_NAME].add_as_parser(modes)
        day_mode.set_defaults(func=program.day)

        view_mode = MODES[VIEW_NAME].add_as_parser(modes)
        view_mode.set_defaults(func=program.view)
        view_mode.add_argument(
            "mode",
            help=(
                "View mode. by-category summarizes based on category instead of date. "
                "balance shows balance development over time."
            ),
            choices=["by-category", "balance"],
        )

        for listing_mode in [list_mode, view_mode]:
            listing_mode.add_argument(
                "--filter-category",
                "--Fc",
                metavar="PATTERN",
                help=(
                    "Filter: Only include records with matching category. Supports "
                    "glob patterns."
                ),
            )
            listing_mode.add_argument(
                "--filter-message",
                "--Fm",
                metavar="PATTERN",
                help="Filter: Like --filter-category, but for the message.",
            )

        export_mode = MODES[EXPORT_NAME].add_as_parser(modes)
        export_mode.set_defaults(func=program.export)

        edit_mode = MODES[EDIT_NAMES[0]].add_as_parser(modes)
        edit_mode.set_defaults(func=program.edit)

        remove_mode = MODES[REMOVE_NAMES[0]].add_as_parser(modes)
        remove_mode.set_defaults(func=program.remove)

        # RECESS management

        recess_mode = MODES[RECESS_NAMES[0]].add_as_parser(modes)
        recess_mode.set_defaults(func=program.recess)
        recess_mode_modes = recess_mode.add_mutually_exclusive_group()
        recess_mode_modes.add_argument(
            "--add-vacation",
            nargs="+",
            metavar="DATE",
            help="Add a vacation. Either a single day or a begin and end. DATE: "
            + date_help_text,
        )
        recess_mode_modes.add_argument(
            "--add-holiday",
            metavar="DATE",
            help="Add a holiday. DATE: " + date_help_text,
        )
        recess_mode_modes.add_argument(
            "--add-reduced-day",
            nargs=2,
            metavar=("DATE", "HOURS"),
            help=(
                "Add a reduced hour day on DATE (see DATE) with HOURS being a value in "
                "({}, {}).".format(*consts.ALLOWED_WORK_HOURS)
            ),
        )
        recess_mode_modes.add_argument(
            "--remove", nargs="+", metavar="DATE", help="Remove free day(s)."
        )
        recess_mode_modes.add_argument(
            "--list",
            metavar="YEAR",
            type=int,
            nargs="?",
            const=dt.date.today().year,
            help="List free days of YEAR (default: current year)",
        )

        # MAINTENANCE modes

        config_mode = MODES[CONFIG_NAME].add_as_parser(modes)
        config_mode.set_defaults(func=program.config)
        config_mode_modes = config_mode.add_mutually_exclusive_group()
        config_mode_modes.add_argument(
            "-p",
            "--path",
            action="store_true",
            help="Default mode: Print the path of the runtime configuration file.",
        )
        config_mode_modes.add_argument(
            "-c",
            "--create",
            action="store_true",
            help="Create a default runtime configuration with all currently active options.",
        )
        config_mode_modes.add_argument(
            "-e",
            "--expected",
            action="store_true",
            help="Print the contents of an expected runtime configuration file.",
        )
        config_mode_modes.add_argument(
            "-s",
            "--see",
            choices=["dir", "expected hours"],
            help="Check how work is configured (see --help for options).",
        )

        rehash_mode = MODES[REHASH_NAME].add_as_parser(modes)
        rehash_mode.set_defaults(func=program.rehash)

        return parser

    @staticmethod
    def print_verbose_help(parser: argparse.ArgumentParser) -> None:
        """ Print the parser's help with more detailed help below it. """

        parser.print_help()

        two_spaces: str = " " * 2
        fill = lambda s: textwrap.fill(
            s,
            width=80,
            initial_indent=two_spaces,
            subsequent_indent=two_spaces,
            replace_whitespace=False,
            drop_whitespace=False,
        )
        new_epilog = lambda t, c: "\n\n" + t + ":\n" + "\n".join(map(fill, c))

        print("\n\n" + Color.bold("EXTENDED HELP"), end="")

        # fmt: off
        print(
            new_epilog(
                t="rounding",
                c=[
                    "Times are rounded in your favor, to the next full 15 minutes, when"
                        ' you enter "now" instead of an exact time. For example:',
                    '- "work start now" at 10:14 starts at 10:00',
                    '- "work stop now" at 19:01 stops at 19:15',
                ],
            )
            + new_epilog(
                t="expected hours",
                c=[
                    "For some sub-functions (mainly status and hours), you will be nudged to work "
                        "no more, but also no less, than the expected hours. By default, work will "
                        "expect 8 hours for every workday (Mon–Fri). Change the default by editing "
                        "the run-time configuration. To define individual days where less hours "
                        "should be expected, use the free-days command:",
                    "- free-days --add-vacation for vacations (expect 0 hours)",
                    '- free-days --add-holiday for public holidays (expect 0 hours)"',
                    '- free-days --add-reduced-day for part-time days (expect < 8 hours)"',
                ],
            )
            + new_epilog(
                t="balance",
                c=[
                    "Based on the expected hours and the time worked, two balances are "
                        "calculated:",
                    "1) Week balance (shown in status): Total over-/undertime accumulated over "
                        "the current week (starting Monday), up to the day before today.",
                    "2) Current balance (shown in hours): This shows the hours you need to work "
                        "on the current day and how many are remaining.",
                    'To check your balance development over other periods, use "view balance."'
                ],
            )
        )
        # fmt: on
