"""
Hooks for pytest-codecarbon, a pytest plugin measuring carbon output
from your code
"""
import os

import pytest
import pandas as pd
from codecarbon import EmissionsTracker


class Carbon(object):
    """Adds carbon profiling to your tests."""

    def __init__(self, dir):
        self.dir = dir
        self.tracker = None
        self.testnames = []

    def pytest_sessionstart(self, session):
        """Runs at the start of the test session."""
        try:
            os.mkdir(self.dir)
        except OSError:
            pass

        # instead of instantiating a tracker for each test, we instantiate it once
        # then use find and replace to fill in the names for each test
        self.tracker = EmissionsTracker(
            project_name="###", output_dir=self.dir, log_level="critical"
        )

    def pytest_sessionfinish(self, session):
        """Runs at the end of the test session."""
        # we want to change cumulative values to individual values
        df = pd.read_csv(f"{self.dir}/emissions.csv")

        # add row of 0's at top to buffer the diff
        df = pd.concat(
            [pd.DataFrame([0] * df.shape[1], index=df.columns).T, df], axis=0
        )
        for col in ["duration", "emissions", "ram_energy", "energy_consumed"]:
            df[col] = df[col].diff()
        # drop buffer row
        df = df.iloc[1:, :]

        with open(f"{self.dir}/emissions.csv", "w", encoding="utf-8") as file:
            file.write(df.to_csv())

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        """Hook wrapper around each Pytest test."""
        # access internal attribute so we can change project name
        # for each test without re-instantiating the tracker
        self.tracker._project_name = item.name
        self.tracker.start()
        yield
        self.tracker.stop()


def pytest_addoption(parser):
    """Pytest option hook for pytest-codecarbon"""
    group = parser.getgroup("Carbon")
    group.addoption("--carbon", action="store_true", help="generate carbon information")
    group.addoption(
        "--carbon-dir",
        default=f"{os.getcwd()}",
        help="directory for pytest-codecarbon result files",
    )


def pytest_configure(config):
    """Pytest config hook for pytest-codecarbon"""
    if config.getvalue("carbon"):
        config.pluginmanager.register(Carbon(config.getvalue("carbon_dir")))
