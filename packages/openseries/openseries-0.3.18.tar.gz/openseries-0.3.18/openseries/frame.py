# -*- coding: utf-8 -*-
import copy
import datetime as dt
import logging
import math
import os
import random
import string
from pathlib import Path
from typing import List, Union, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import scipy.stats as ss
import statsmodels.api as sm
from pandas.tseries.offsets import CDay
from plotly.offline import plot

from openseries.datefixer import date_offset_foll
from openseries.load_plotly import load_plotly_dict
from openseries.risk import (
    calc_max_drawdown,
    drawdown_series,
    drawdown_details,
    cvar_down,
    var_down,
)
from openseries.series import OpenTimeSeries
from openseries.sweden_holidays import SwedenHolidayCalendar, holidays_sw


class OpenFrame(object):
    constituents: List[OpenTimeSeries]
    sweden: SwedenHolidayCalendar
    tsdf: pd.DataFrame
    weights: List[float]

    def __init__(
        self,
        constituents: List[OpenTimeSeries],
        weights: List[float] = None,
        sort: bool = True,
    ):
        """
        :param constituents:  List of objects of Class OpenTimeSeries.
        :param weights:       List of weights in float64 format.
        :param sort:          argument in Pandas df.concat added to fix issue when upgrading py and pd
        """
        self.weights = weights
        self.tsdf = pd.DataFrame()
        self.sweden = SwedenHolidayCalendar(holidays_sw)
        self.constituents = constituents
        if constituents is not None and len(constituents) != 0:
            self.tsdf = pd.concat(
                [x.tsdf for x in self.constituents], axis="columns", sort=sort
            )
        else:
            logging.warning("OpenFrame() was passed an empty list.")

        if weights is not None:
            assert len(self.constituents) == len(
                self.weights
            ), "Number of TimeSeries must equal number of weights."

        if len(set(self.columns_lvl_zero)) != len(self.columns_lvl_zero):
            raise Exception("TimeSeries names/labels must be unique.")

    def __repr__(self):

        return "{}(constituents={}, weights={})".format(
            self.__class__.__name__, self.constituents, self.weights
        )

    def from_deepcopy(self):

        return copy.deepcopy(self)

    def all_properties(self, properties: list = None) -> pd.DataFrame:

        if not properties:
            properties = [
                "value_ret",
                "geo_ret",
                "arithmetic_ret",
                "vol",
                "downside_deviation",
                "ret_vol_ratio",
                "sortino_ratio",
                "z_score",
                "skew",
                "kurtosis",
                "positive_share",
                "var_down",
                "cvar_down",
                "vol_from_var",
                "worst",
                "worst_month",
                "max_drawdown",
                "max_drawdown_date",
                "max_drawdown_cal_year",
                "first_indices",
                "last_indices",
                "lengths_of_items",
                "span_of_days_all",
            ]
        prop_list = [getattr(self, x) for x in properties]
        results = pd.concat(prop_list, axis="columns").T
        return results

    def calc_range(
        self,
        months_offset: int = None,
        from_dt: dt.date = None,
        to_dt: dt.date = None,
    ) -> Tuple[dt.date, dt.date]:
        """
        Function to create user defined time frame.

        :param months_offset: number of months offset as positive integer.
                              Overrides use of from_date and to_date
        :param from_dt: Specific from date
        :param to_dt: Specific to date
        """
        if months_offset is not None or from_dt is not None or to_dt is not None:
            if months_offset is not None:
                earlier = date_offset_foll(
                    self.last_idx,
                    calendar=CDay(calendar=self.sweden),
                    months_offset=-months_offset,
                )
                assert (
                    earlier >= self.first_idx
                ), "Function calc_range returned earlier date < series start"
                later = self.last_idx
            else:
                if from_dt is not None and to_dt is None:
                    assert from_dt >= self.first_idx, (
                        "Function calc_range returned " "earlier date < series start"
                    )
                    earlier, later = from_dt, self.last_idx
                elif from_dt is None and to_dt is not None:
                    assert (
                        to_dt <= self.last_idx
                    ), "Function calc_range returned later date > series end"
                    earlier, later = self.first_idx, to_dt
                elif from_dt is not None or to_dt is not None:
                    assert to_dt <= self.last_idx and from_dt >= self.first_idx, (
                        "Function calc_range returned " "dates outside series range"
                    )
                    earlier, later = from_dt, to_dt
                else:
                    earlier, later = self.first_idx, self.last_idx
            while not self.tsdf.index.isin([earlier]).any():
                earlier -= dt.timedelta(days=1)
            while not self.tsdf.index.isin([later]).any():
                later += dt.timedelta(days=1)
        else:
            earlier, later = self.first_idx, self.last_idx

        return earlier, later

    def align_index_to_local_cdays(self):
        """
        Changes the index of the associated pd.DataFrame tsdf to align with
        local calendar business days.
        """
        date_range = [
            d.date()
            for d in pd.date_range(
                start=self.tsdf.first_valid_index(),
                end=self.tsdf.last_valid_index(),
                freq=CDay(calendar=self.sweden),
            )
        ]
        self.tsdf = self.tsdf.reindex(date_range, method=None, copy=False)
        return self

    @property
    def length(self) -> int:

        return len(self.tsdf.index)

    @property
    def lengths_of_items(self) -> pd.Series:

        return pd.Series(
            data=[self.tsdf.loc[:, d].count() for d in self.tsdf],
            index=self.tsdf.columns,
            name="observations",
        )

    @property
    def item_count(self) -> int:

        return self.tsdf.shape[1]

    @property
    def columns_lvl_zero(self) -> list:

        return self.tsdf.columns.get_level_values(0).tolist()

    @property
    def columns_lvl_one(self) -> list:

        return self.tsdf.columns.get_level_values(1).tolist()

    @property
    def first_idx(self) -> dt.date:

        return self.tsdf.index[0]

    @property
    def first_indices(self) -> pd.Series:

        return pd.Series(
            data=[i.first_idx for i in self.constituents],
            index=self.tsdf.columns,
            name="first indices",
        )

    @property
    def last_idx(self) -> dt.date:

        return self.tsdf.index[-1]

    @property
    def last_indices(self) -> pd.Series:

        return pd.Series(
            data=[i.last_idx for i in self.constituents],
            index=self.tsdf.columns,
            name="last indices",
        )

    @property
    def span_of_days(self) -> int:
        """
        Number of days from the first date to the last.
        Be aware that this is not the same for all constituents.
        """
        return (self.last_idx - self.first_idx).days

    @property
    def span_of_days_all(self) -> pd.Series:
        """
        Number of days from the first date to the last for all items in the frame.
        """
        return pd.Series(
            data=[c.span_of_days for c in self.constituents],
            index=self.tsdf.columns,
            name="span of days",
        )

    @property
    def yearfrac(self) -> float:
        """
        Length of timeseries expressed as fraction of a year with 365.25 days.
        Be aware that this is not the same for all constituents.
        """
        return self.span_of_days / 365.25

    @property
    def periods_in_a_year(self) -> float:
        """
        The number of businessdays in an average year for all days in the data.
        Be aware that this is not the same for all constituents.
        """
        return self.length / self.yearfrac

    @property
    def geo_ret(self) -> pd.Series:
        """
        Geometric annualized return.
        """
        if self.tsdf.iloc[0].isin([0.0]).any():
            raise Exception(
                "Error in function geo_ret due to an initial value being zero."
            )
        else:
            return pd.Series(
                data=(self.tsdf.iloc[-1] / self.tsdf.iloc[0]) ** (1 / self.yearfrac)
                - 1,
                name="Geometric return",
            )

    def geo_ret_func(
        self,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Geometric annualized return.

        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        fraction = (later - earlier).days / 365.25
        return pd.Series(
            data=(self.tsdf.loc[later] / self.tsdf.loc[earlier]) ** (1 / fraction) - 1,
            name="Subset Geometric return",
        )

    @property
    def arithmetic_ret(self) -> pd.Series:
        """
        Arithmetic annualized return.
        """
        return pd.Series(
            data=np.log(self.tsdf).diff().mean() * self.periods_in_a_year,
            name="Arithmetic return",
        )

    def arithmetic_ret_func(
        self,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        Arithmetic annualized return.

        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed:
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            how_many = self.tsdf.loc[earlier:later].count(numeric_only=True)
            time_factor = how_many / fraction
        return pd.Series(
            data=np.log(self.tsdf.loc[earlier:later]).diff().mean() * time_factor,
            name="Subset Arithmetic return",
        )

    @property
    def value_ret(self) -> pd.Series:
        """
        Simple return from first to last observation.
        """
        if self.tsdf.iloc[0].isin([0.0]).any():
            raise Exception(
                f"Error in function value_ret due to an initial value "
                f"being zero. ({self.tsdf.head(3)})"
            )
        else:
            return pd.Series(
                data=self.tsdf.iloc[-1] / self.tsdf.iloc[0] - 1,
                name="Total return",
            )

    def value_ret_func(
        self,
        logret: bool = False,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Simple or log return from the first to the last observation.

        :param logret: True for log return and False for simple return.
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if self.tsdf.iloc[0].isin([0.0]).any():
            raise Exception(
                "Error in function value_ret_func() due to an "
                "initial value being zero."
            )
        else:
            if logret:
                ret = np.log(self.tsdf.loc[later] / self.tsdf.loc[earlier])
            else:
                ret = self.tsdf.loc[later] / self.tsdf.loc[earlier] - 1
            return pd.Series(data=ret, name="Subset Total return")

    def value_ret_calendar_period(self, year: int, month: int = None) -> pd.Series:
        """
        Function to calculate simple return for a specific calendar period.

        :param year: Year of the period to calculate.
        :param month: Optional month of the period to calculate.
        """
        if month is None:
            period = str(year)
        else:
            period = "-".join([str(year), str(month).zfill(2)])
        vrdf = self.tsdf.copy()
        vrdf.index = pd.DatetimeIndex(vrdf.index)
        rtn = vrdf.pct_change().copy()
        rtn = rtn.loc[period] + 1
        rtn = rtn.apply(np.cumprod, axis="index").iloc[-1] - 1
        rtn.name = period
        return rtn

    @property
    def vol(self, logret: bool = False) -> pd.Series:
        """
        Annualized volatility. Pandas .std() is the equivalent of
        stdev.s([...]) in MS excel.
        """
        if logret:
            vld = np.log(self.tsdf).diff()
            vld.iloc[0] = 0.0
        else:
            vld = self.tsdf.pct_change()
        return pd.Series(
            data=vld.std() * np.sqrt(self.periods_in_a_year), name="Volatility"
        )

    def vol_func(
        self,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        Annualized volatility. Pandas .std() is the equivalent of
        stdev.s([...]) in MS excel.

        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed:
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            how_many = self.tsdf.loc[earlier:later].count(numeric_only=True)
            time_factor = how_many / fraction
        return pd.Series(
            data=self.tsdf.loc[earlier:later].pct_change().std() * np.sqrt(time_factor),
            name="Subset Volatility",
        )

    @property
    def downside_deviation(self) -> pd.Series:
        """
        Downside Deviation is here the standard deviation of returns that are
        below a Minimum Accepted Return of zero. It is used to calculate the
        Sortino Ratio.
        """
        dddf = self.tsdf.pct_change()

        return pd.Series(
            data=np.sqrt((dddf[dddf < 0.0] ** 2).sum() / self.length)
            * np.sqrt(self.periods_in_a_year),
            name="Downside deviation",
        )

    def downside_deviation_func(
        self,
        min_accepted_return: float = 0.0,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        Downside Deviation is the standard deviation of returns that are below
        a given Minimum Accepted Return (MAR). It is used to calculate the
        Sortino Ratio.

        :param min_accepted_return: The annualized Minimum Accepted Return (MAR)
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed:
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        how_many = self.tsdf.loc[earlier:later].pct_change().count(numeric_only=True)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            time_factor = how_many / fraction

        dddf = (
            self.tsdf.loc[earlier:later]
            .pct_change()
            .sub(min_accepted_return / time_factor)
        )

        return pd.Series(
            data=np.sqrt((dddf[dddf < 0.0] ** 2).sum() / how_many)
            * np.sqrt(time_factor),
            name="Subset Downside deviation",
        )

    @property
    def z_score(self, logret: bool = False) -> pd.Series:
        """
        Z-score as (last return - mean return) / standard deviation of return
        :param logret:
        """
        if logret:
            zd = np.log(self.tsdf).diff()
            zd.iloc[0] = 0.0
        else:
            zd = self.tsdf.pct_change()
        return pd.Series(data=(zd.iloc[-1] - zd.mean()) / zd.std(), name="Z-score")

    def z_score_func(
        self,
        logret: bool = False,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Z-score as (last return - mean return) / standard deviation of return

        :param logret:
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if logret:
            zd = np.log(self.tsdf.loc[earlier:later]).diff()
            zd.iloc[0] = 0.0
        else:
            zd = self.tsdf.loc[earlier:later].pct_change()
        return pd.Series(
            data=(zd.iloc[-1] - zd.mean()) / zd.std(), name="Subset Z-score"
        )

    @property
    def skew(self, logret: bool = False) -> pd.Series:
        """
        Skew of the return distribution.
        """
        if logret:
            vld = np.log(self.tsdf).diff()
            vld.iloc[0] = 0.0
        else:
            vld = self.tsdf.pct_change()
        return pd.Series(
            data=ss.skew(vld, bias=True, nan_policy="omit"),
            index=self.tsdf.columns,
            name="Skew",
        )

    def skew_func(
        self,
        logret: bool = False,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Skew of the return distribution.

        :param logret:
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if logret:
            vld = np.log(self.tsdf.loc[earlier:later]).diff()
            vld.iloc[0] = 0.0
        else:
            vld = self.tsdf.loc[earlier:later].pct_change()
        return pd.Series(
            data=ss.skew(vld, bias=True, nan_policy="omit"),
            index=self.tsdf.columns,
            name="Subset Skew",
        )

    @property
    def kurtosis(self, logret: bool = False) -> pd.Series:
        """
        Kurtosis of the return distribution.
        """
        if logret:
            vld = np.log(self.tsdf).diff()
            vld.iloc[0] = 0.0
        else:
            vld = self.tsdf.pct_change()
        return pd.Series(
            data=ss.kurtosis(vld, fisher=True, bias=True, nan_policy="omit"),
            index=self.tsdf.columns,
            name="Kurtosis",
        )

    def kurtosis_func(
        self,
        logret: bool = False,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Kurtosis of the return distribution.

        :param logret:
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if logret:
            vld = np.log(self.tsdf.loc[earlier:later]).diff()
            vld.iloc[0] = 0.0
        else:
            vld = self.tsdf.loc[earlier:later].pct_change()
        return pd.Series(
            data=ss.kurtosis(vld, fisher=True, bias=True, nan_policy="omit"),
            index=self.tsdf.columns,
            name="Subset Kurtosis",
        )

    @property
    def ret_vol_ratio(self) -> pd.Series:
        """
        Ratio of geometric return and annualized volatility.
        """
        ratio = self.geo_ret / self.vol
        ratio.name = "Return vol ratio"
        return ratio

    def ret_vol_ratio_func(
        self,
        riskfree_rate: float = None,
        riskfree_column: Union[tuple, int] = -1,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        The Sharpe Ratio equals geometric return of an asset minus a risk free return
        divided by the volatility of the asset. It implies that the riskfree asset has
        zero volatility.

        :param riskfree_rate: A risk free rate provided as a float.
        :param riskfree_column: Column of timeseries that is the denominator in the ratio.
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed: Fixing the parameter to simplify testing.
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        how_many = self.tsdf.loc[earlier:later].iloc[:, 0].count()
        fraction = (later - earlier).days / 365.25

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = how_many / fraction

        ratios = []
        if riskfree_rate is None:
            if isinstance(riskfree_column, tuple):
                riskfree = self.tsdf.loc[earlier:later].loc[:, riskfree_column]
                riskfree_item = riskfree_column
                riskfree_label = self.tsdf.loc[:, riskfree_column].name[0]
            elif isinstance(riskfree_column, int):
                riskfree = self.tsdf.loc[earlier:later].iloc[:, riskfree_column]
                riskfree_item = self.tsdf.iloc[:, riskfree_column].name
                riskfree_label = self.tsdf.iloc[:, riskfree_column].name[0]
            else:
                raise Exception("base_column should be a tuple or an integer.")

            for item in self.tsdf:
                if item == riskfree_item:
                    ratios.append(0.0)
                else:
                    longdf = self.tsdf.loc[earlier:later].loc[:, item]
                    georet = float(
                        (longdf.iloc[-1] / longdf.iloc[0]) ** (1 / fraction) - 1
                    )
                    riskfree_ret = float(
                        (riskfree.iloc[-1] / riskfree.iloc[0]) ** (1 / fraction) - 1
                    )
                    vol = float(longdf.pct_change().std() * np.sqrt(time_factor))
                    ratios.append((georet - riskfree_ret) / vol)

            return pd.Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sharpe Ratios vs {riskfree_label}",
            )
        else:
            for item in self.tsdf:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                georet = float((longdf.iloc[-1] / longdf.iloc[0]) ** (1 / fraction) - 1)
                vol = float(longdf.pct_change().std() * np.sqrt(time_factor))
                ratios.append((georet - riskfree_rate) / vol)

            return pd.Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sharpe Ratios (rf={riskfree_rate:.2%})",
            )

    @property
    def sortino_ratio(self) -> pd.Series:
        """
        Ratio of geometric return and downside deviation with a riskfree rate
        of zero.
        """
        sortino = self.geo_ret / self.downside_deviation
        sortino.name = "Sortino ratio"
        return sortino

    def sortino_ratio_func(
        self,
        riskfree_rate: float = None,
        riskfree_column: Union[tuple, int] = -1,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        The Sortino ratio calculated as ( geometric return - risk free return )
        / downside deviation. The ratio implies that the riskfree asset has
        zero volatility, and a minimum acceptable return of zero.

        :param riskfree_rate: A risk free rate provided as a float.
        :param riskfree_column: Column of timeseries that is the denominator in the ratio.
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed: Fixing the parameter to simplify testing.
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        how_many = self.tsdf.loc[earlier:later].iloc[:, 0].count()
        fraction = (later - earlier).days / 365.25

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = how_many / fraction

        ratios = []
        if riskfree_rate is None:
            if isinstance(riskfree_column, tuple):
                riskfree = self.tsdf.loc[earlier:later].loc[:, riskfree_column]
                riskfree_item = riskfree_column
                riskfree_label = self.tsdf.loc[:, riskfree_column].name[0]
            elif isinstance(riskfree_column, int):
                riskfree = self.tsdf.loc[earlier:later].iloc[:, riskfree_column]
                riskfree_item = self.tsdf.iloc[:, riskfree_column].name
                riskfree_label = self.tsdf.iloc[:, riskfree_column].name[0]
            else:
                raise Exception("base_column should be a tuple or an integer.")

            for item in self.tsdf:
                if item == riskfree_item:
                    ratios.append(0.0)
                else:
                    longdf = self.tsdf.loc[earlier:later].loc[:, item]
                    georet = float(
                        (longdf.iloc[-1] / longdf.iloc[0]) ** (1 / fraction) - 1
                    )
                    riskfree_ret = float(
                        (riskfree.iloc[-1] / riskfree.iloc[0]) ** (1 / fraction) - 1
                    )
                    dddf = longdf.pct_change()
                    downdev = float(
                        math.sqrt(
                            (dddf[dddf.values < 0.0].values ** 2).sum() / how_many
                        )
                        * np.sqrt(time_factor)
                    )
                    ratios.append((georet - riskfree_ret) / downdev)

            return pd.Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sortino Ratios vs {riskfree_label}",
            )
        else:
            for item in self.tsdf:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                georet = float((longdf.iloc[-1] / longdf.iloc[0]) ** (1 / fraction) - 1)
                dddf = longdf.pct_change()
                downdev = float(
                    math.sqrt((dddf[dddf.values < 0.0].values ** 2).sum() / how_many)
                    * np.sqrt(time_factor)
                )
                ratios.append((georet - riskfree_rate) / downdev)

            return pd.Series(
                data=ratios,
                index=self.tsdf.columns,
                name=f"Sortino Ratios (rf={riskfree_rate:.2%},mar=0.0%)",
            )

    @property
    def max_drawdown(self) -> pd.Series:
        """
        Max drawdown from peak to recovery.
        """
        return pd.Series(data=calc_max_drawdown(self.tsdf), name="Max drawdown")

    @property
    def max_drawdown_date(self) -> pd.Series:
        """
        Date when Max drawdown occurred.
        """
        md_dates = [c.max_drawdown_date for c in self.constituents]
        return pd.Series(
            data=md_dates, index=self.tsdf.columns, name="Max drawdown dates"
        )

    def max_drawdown_func(
        self,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Max drawdown from peak to recovery.

        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        return pd.Series(
            data=calc_max_drawdown(self.tsdf.loc[earlier:later]),
            name="Subset Max drawdown",
        )

    @property
    def max_drawdown_cal_year(self) -> pd.Series:
        """
        Max drawdown in a single calendar year.
        """
        md = (
            self.tsdf.groupby([pd.DatetimeIndex(self.tsdf.index).year])
            .apply(lambda x: calc_max_drawdown(x))
            .min()
        )
        md.name = "Max drawdown in cal yr"
        return md

    @property
    def worst(self) -> pd.Series:
        """
        Most negative percentage change.
        """
        return pd.Series(data=self.tsdf.pct_change().min(), name="Worst")

    def worst_func(
        self,
        observations: int = 1,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Most negative percentage change.

        :param observations:
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        return pd.Series(
            data=self.tsdf.loc[earlier:later]
            .pct_change()
            .rolling(observations, min_periods=observations)
            .sum()
            .min(),
            name=f"Subset Worst {observations}day period",
        )

    @property
    def worst_month(self) -> pd.Series:
        """
        Most negative month.
        """
        wdf = self.tsdf.copy()
        wdf.index = pd.DatetimeIndex(wdf.index)
        return pd.Series(
            data=wdf.resample("BM").last().pct_change().min(),
            name="Worst month",
        )

    @property
    def cvar_down(self, level: float = 0.95) -> pd.Series:
        """
        Downside Conditional Value At Risk, "CVaR".
        :param level: The sought CVaR level as a float
        """
        cvar_df = self.tsdf.copy(deep=True)
        var_list = [
            cvar_df.loc[:, x]
            .pct_change()
            .sort_values()
            .iloc[
                : int(math.ceil((1 - level) * cvar_df.loc[:, x].pct_change().count()))
            ]
            .mean()
            for x in self.tsdf
        ]
        return pd.Series(
            data=var_list, index=self.tsdf.columns, name=f"CVaR {level:.1%}"
        )

    def cvar_down_func(
        self,
        level: float = 0.95,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        Downside Conditional Value At Risk, "CVaR".
        :param level: The sought CVaR level as a float
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        cvar_df = self.tsdf.loc[earlier:later].copy(deep=True)
        var_list = [
            cvar_df.loc[:, x]
            .pct_change()
            .sort_values()
            .iloc[
                : int(math.ceil((1 - level) * cvar_df.loc[:, x].pct_change().count()))
            ]
            .mean()
            for x in self.tsdf
        ]
        return pd.Series(
            data=var_list, index=self.tsdf.columns, name=f"CVaR {level:.1%}"
        )

    @property
    def var_down(self, level: float = 0.95, interpolation: str = "lower") -> pd.Series:
        """
        Downside Value At Risk, "VaR". The equivalent of
        percentile.inc([...], 1-level) over returns in MS Excel.
        :param level: The sought VaR level as a float
        :param interpolation: type of interpolation in quantile function
                              (default value in quantile is linear)
        """
        return pd.Series(
            data=self.tsdf.pct_change().quantile(
                1 - level, interpolation=interpolation
            ),
            name=f"VaR {level:.1%}",
        )

    def var_down_func(
        self,
        level: float = 0.95,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        interpolation: str = "lower",
    ) -> pd.Series:
        """
        Downside Value At Risk, "VaR". The equivalent of
        percentile.inc([...], 1-level) over returns in MS Excel.
        :param level: The sought VaR level as a float
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param interpolation: type of interpolation in quantile function
                              (default value in quantile is linear)
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        return pd.Series(
            data=self.tsdf.loc[earlier:later]
            .pct_change()
            .quantile(1 - level, interpolation=interpolation),
            name=f"VaR {level:.1%}",
        )

    @property
    def vol_from_var(
        self, level: float = 0.95, interpolation: str = "lower"
    ) -> pd.Series:
        """
        Volatility implied from downside VaR assuming a normal distribution.
        :param level: The sought VaR level as a float
        :param interpolation: type of interpolation in quantile function
                              (default value in quantile is linear)
        """
        imp_vol = (
            -np.sqrt(self.periods_in_a_year)
            * self.var_down_func(interpolation=interpolation)
            / ss.norm.ppf(level)
        )
        return pd.Series(data=imp_vol, name=f"Imp vol from VaR {level:.0%}")

    def vol_from_var_func(
        self,
        level: float = 0.95,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        interpolation: str = "lower",
        drift_adjust: bool = False,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        Volatility implied from downside VaR assuming a normal distribution.
        :param level: The sought VaR level as a float
        :param months_from_last:
        :param from_date:
        :param to_date:
        :param interpolation: type of interpolation in quantile function
                              (default value in quantile is linear)
        :param drift_adjust:
        :param periods_in_a_year_fixed:
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            fraction = (later - earlier).days / 365.25
            how_many = self.tsdf.loc[earlier:later].count(numeric_only=True)
            time_factor = how_many / fraction
        if drift_adjust:
            imp_vol = (-np.sqrt(time_factor) / ss.norm.ppf(level)) * (
                self.tsdf.loc[earlier:later]
                .pct_change()
                .quantile(1 - level, interpolation=interpolation)
                - self.tsdf.loc[earlier:later].pct_change().sum()
                / len(self.tsdf.loc[earlier:later].pct_change())
            )
        else:
            imp_vol = (
                -np.sqrt(time_factor)
                * self.tsdf.loc[earlier:later]
                .pct_change()
                .quantile(1 - level, interpolation=interpolation)
                / ss.norm.ppf(level)
            )
        return pd.Series(data=imp_vol, name=f"Subset Imp vol from VaR {level:.0%}")

    def target_weight_from_var(
        self,
        target_vol: float = 0.175,
        min_leverage_local: float = 0.0,
        max_leverage_local: float = 99999.0,
        level: float = 0.95,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        interpolation: str = "lower",
        drift_adjust: bool = False,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        A position target weight from the ratio between a VaR implied
        volatility and a given target volatility.
        :param target_vol:
        :param min_leverage_local:
        :param max_leverage_local:
        :param level: The VaR level as a float
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param interpolation: type of interpolation in quantile function
                              (default value in quantile is linear)
        :param drift_adjust:
        :param periods_in_a_year_fixed:
        """
        vfv = self.vol_from_var_func(
            level=level,
            months_from_last=months_from_last,
            from_date=from_date,
            to_date=to_date,
            interpolation=interpolation,
            drift_adjust=drift_adjust,
            periods_in_a_year_fixed=periods_in_a_year_fixed,
        )
        vfv = vfv.apply(
            lambda x: max(min_leverage_local, min(target_vol / x, max_leverage_local))
        )
        return pd.Series(data=vfv, name=f"Weight from target vol {target_vol:.1%}")

    @property
    def positive_share(self) -> pd.Series:
        """
        The share of percentage changes that are positive.
        """
        pos = self.tsdf.pct_change()[1:][self.tsdf.pct_change()[1:] > 0.0].count()
        tot = self.tsdf.pct_change()[1:].count()
        answer = pos / tot
        answer.name = "Positive share"
        return answer

    def positive_share_func(
        self,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
    ) -> pd.Series:
        """
        The share of percentage changes that are positive.

        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        """
        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        pos = (
            self.tsdf.loc[earlier:later]
            .pct_change()[1:][self.tsdf.loc[earlier:later].pct_change()[1:] > 0.0]
            .count()
        )
        tot = self.tsdf.loc[earlier:later].pct_change()[1:].count()
        answer = pos / tot
        answer.name = "Positive share"
        return answer

    @property
    def correl_matrix(self) -> pd.DataFrame:
        """
        Correlation matrix
        """
        corr_matrix = self.tsdf.pct_change().corr(method="pearson", min_periods=1)
        corr_matrix.columns = corr_matrix.columns.droplevel(level=1)
        corr_matrix.index = corr_matrix.index.droplevel(level=1)
        corr_matrix.index.name = "Correlation"
        return corr_matrix

    def add_timeseries(self, new_series: OpenTimeSeries):
        """
        :param new_series:
        """
        self.constituents += [new_series]
        self.tsdf = pd.concat([self.tsdf, new_series.tsdf], axis="columns", sort=True)
        return self

    def delete_timeseries(self, lvl_zero_item: str):
        """
        Function drops the selected item.
        :param lvl_zero_item:
        """
        if self.weights:
            new_c, new_w = [], []
            for cc, ww in zip(self.constituents, self.weights):
                if cc.label != lvl_zero_item:
                    new_c.append(cc)
                    new_w.append(ww)
            self.constituents = new_c
            self.weights = new_w
        else:
            self.constituents = [
                ff for ff in self.constituents if ff.label != lvl_zero_item
            ]
        self.tsdf.drop(lvl_zero_item, axis="columns", level=0, inplace=True)
        return self

    def resample(self, freq="BM"):
        """
        Function resamples (changes) timeseries frequency.
        :param freq: Freq str https://pandas.pydata.org/pandas-docs/stable/
                              user_guide/timeseries.html#dateoffset-objects
        """
        self.tsdf.index = pd.DatetimeIndex(self.tsdf.index)
        self.tsdf = self.tsdf.resample(freq).last()
        self.tsdf.index = [d.date() for d in pd.DatetimeIndex(self.tsdf.index)]
        return self

    def trunc_frame(
        self,
        start_cut: dt.date = None,
        end_cut: dt.date = None,
        before: bool = True,
        after: bool = True,
    ):
        """
        Function truncates DataFrame such that all timeseries
        have the same length.
        :param start_cut: Optional manually entered date
        :param end_cut: Optional manually entered date
        :param before: If True method will truncate to the common earliest
                       start date also when start_cut = None.
        :param after: If True method will truncate to the common latest
                      end date also when end_cut = None.
        """
        if not start_cut and before:
            start_cut = self.first_indices.max()
        if not end_cut and after:
            end_cut = self.last_indices.min()
        self.tsdf.sort_index(inplace=True)
        self.tsdf = self.tsdf.truncate(before=start_cut, after=end_cut, copy=False)
        for x in self.constituents:
            x.tsdf = x.tsdf.truncate(before=start_cut, after=end_cut, copy=False)
        if len(set(self.first_indices)) != 1 or len(set(self.last_indices)) != 1:
            logging.warning(
                "One or more constituents still not truncated to same "
                "start and/or end dates."
            )
        return self

    def value_nan_handle(self, method: str = "fill"):
        """
        Function handles NaN in valueseries.
        """
        assert method in [
            "fill",
            "drop",
        ], "Method must be either fill or drop passed as string."
        if method == "fill":
            self.tsdf.fillna(method="pad", inplace=True)
        else:
            self.tsdf.dropna(inplace=True)
        return self

    def return_nan_handle(self, method: str = "fill"):
        """
        Function handles NaN in returnseries.
        """
        assert method in [
            "fill",
            "drop",
        ], "Method must be either fill or drop passed as string."
        if method == "fill":
            self.tsdf.fillna(value=0.0, inplace=True)
        else:
            self.tsdf.dropna(inplace=True)
        return self

    def value_to_ret(self, logret=False):
        """
        Function converts a valueseries into a returnseries.
        Simple return matches method applied by Bloomberg.
        Log return would be: self.tsdf = np.log(self.tsdf).diff() + 1.0

        :param logret: True for log return and False for simple return.
        """
        if logret:
            self.tsdf = np.log(self.tsdf).diff()
        else:
            self.tsdf = self.tsdf.pct_change()
        self.tsdf.iloc[0] = 0
        new_labels = ["Return(Total)"] * self.item_count
        arrays = [self.tsdf.columns.get_level_values(0), new_labels]
        self.tsdf.columns = pd.MultiIndex.from_arrays(arrays)
        return self

    def value_to_diff(self, periods: int = 1):
        """
        Function converts a valueseries to a series of its 1 period differences

        :param periods:
        """
        self.tsdf = self.tsdf.diff(periods=periods)
        self.tsdf.iloc[0] = 0
        new_labels = ["Return(Total)"] * self.item_count
        arrays = [self.tsdf.columns.get_level_values(0), new_labels]
        self.tsdf.columns = pd.MultiIndex.from_arrays(arrays)
        return self

    def value_to_log(self, reverse: bool = False):
        """
        Function converts valueseries into logarithmic returns equivalent to
        LN(value[t] / value[t=0]) in MS excel.
        :param reverse: If True the function applies the equivalent of
                        EXP[...] on the entire series.
        """
        if reverse:
            self.tsdf = np.exp(self.tsdf)
            new_labels = ["Price(Close)"] * self.item_count
            arrays = [self.tsdf.columns.get_level_values(0), new_labels]
            self.tsdf.columns = pd.MultiIndex.from_arrays(arrays)
        else:
            self.tsdf = np.log(self.tsdf / self.tsdf.iloc[0])
            new_labels = ["Return(Total)"] * self.item_count
            arrays = [self.tsdf.columns.get_level_values(0), new_labels]
            self.tsdf.columns = pd.MultiIndex.from_arrays(arrays)
        return self

    def to_cumret(self):
        """
        Function does a rebase of all time series by first calling
        value_to_ret() and then calculating the cumulative.
        """
        if not any(
            [
                True if x == "Return(Total)" else False
                for x in self.tsdf.columns.get_level_values(1).values
            ]
        ):
            self.tsdf = self.tsdf.pct_change()
            self.tsdf.iloc[0] = 0
        self.tsdf = self.tsdf.add(1.0)
        self.tsdf = self.tsdf.apply(np.cumprod, axis="index") / self.tsdf.iloc[0]
        new_labels = ["Price(Close)"] * self.item_count
        arrays = [self.tsdf.columns.get_level_values(0), new_labels]
        self.tsdf.columns = pd.MultiIndex.from_arrays(arrays)
        return self

    def relative(
        self,
        long_column: int = 0,
        short_column: int = 1,
        base_zero: bool = True,
    ):
        """
        Function calculates cumulative relative return between two series.
        A new series is added to the frame.

        :param long_column: Column # of timeseries bought
        :param short_column: Column # of timeseries sold
        :param base_zero: If set to False 1.0 is added to allow for a capital
                          base and to apply e.g. a volatility calculation
        """
        assert self.tsdf.shape[1] > long_column >= 0 and isinstance(long_column, int), (
            "Both arguments must be integers and within a range no larger or "
            "smaller than the number of columns."
        )
        assert self.tsdf.shape[1] > short_column >= 0 and isinstance(
            short_column, int
        ), (
            "Both arguments must be integers and within a range no larger or "
            "smaller than the number of columns."
        )
        rel_label = (
            self.tsdf.iloc[:, long_column].name[0]
            + "_over_"
            + self.tsdf.iloc[:, short_column].name[0]
        )
        if base_zero:
            self.tsdf[rel_label, "Relative return"] = (
                self.tsdf.iloc[:, long_column] - self.tsdf.iloc[:, short_column]
            )
        else:
            self.tsdf[rel_label, "Relative return"] = (
                1.0 + self.tsdf.iloc[:, long_column] - self.tsdf.iloc[:, short_column]
            )

    def tracking_error_func(
        self,
        base_column: Union[tuple, int] = -1,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        The Tracking Error is the standard deviation of the
        difference between the fund and the index returns.

        :param base_column: Column of timeseries that is the denominator in the ratio.
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed: Fixing the parameter to simplify testing.
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        fraction = (later - earlier).days / 365.25

        if isinstance(base_column, tuple):
            shortdf = self.tsdf.loc[earlier:later].loc[:, base_column]
            short_item = base_column
            short_label = self.tsdf.loc[:, base_column].name[0]
        elif isinstance(base_column, int):
            shortdf = self.tsdf.loc[earlier:later].iloc[:, base_column]
            short_item = self.tsdf.iloc[:, base_column].name
            short_label = self.tsdf.iloc[:, base_column].name[0]
        else:
            raise Exception("base_column should be a tuple or an integer.")

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = shortdf.count() / fraction

        terrors = []
        for item in self.tsdf:
            if item == short_item:
                terrors.append(0.0)
            else:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                relative = 1.0 + longdf - shortdf
                vol = float(relative.pct_change().std() * np.sqrt(time_factor))
                terrors.append(vol)

        return pd.Series(
            data=terrors,
            index=self.tsdf.columns,
            name=f"Tracking Errors vs {short_label}",
        )

    def info_ratio_func(
        self,
        base_column: Union[tuple, int] = -1,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        The Information Ratio equals ( fund return less index return ) divided by the
        Tracking Error. And the Tracking Error is the standard deviation of the
        difference between the fund and the index returns.

        :param base_column: Column of timeseries that is the denominator in the ratio.
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed: Fixing the parameter to simplify testing.
        """

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        fraction = (later - earlier).days / 365.25

        if isinstance(base_column, tuple):
            shortdf = self.tsdf.loc[earlier:later].loc[:, base_column]
            short_item = base_column
            short_label = self.tsdf.loc[:, base_column].name[0]
        elif isinstance(base_column, int):
            shortdf = self.tsdf.loc[earlier:later].iloc[:, base_column]
            short_item = self.tsdf.iloc[:, base_column].name
            short_label = self.tsdf.iloc[:, base_column].name[0]
        else:
            raise Exception("base_column should be a tuple or an integer.")

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = shortdf.count() / fraction

        ratios = []
        for item in self.tsdf:
            if item == short_item:
                ratios.append(0.0)
            else:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                relative = 1.0 + longdf - shortdf
                georet = float(
                    (relative.iloc[-1] / relative.iloc[0]) ** (1 / fraction) - 1
                )
                vol = float(relative.pct_change().std() * np.sqrt(time_factor))
                ratios.append(georet / vol)

        return pd.Series(
            data=ratios,
            index=self.tsdf.columns,
            name=f"Info Ratios vs {short_label}",
        )

    def capture_ratio_func(
        self,
        ratio: str,
        base_column: Union[tuple, int] = -1,
        months_from_last: int = None,
        from_date: dt.date = None,
        to_date: dt.date = None,
        periods_in_a_year_fixed: int = None,
    ) -> pd.Series:
        """
        The Up (Down) Capture Ratio is calculated by dividing the annualized returns
        of the asset during periods that the benchmark returns are positive (negative)
        by the annualized returns of the benchmark during the same periods.
        CaptureRatio.BOTH is the Up ratio divided by the Down ratio.
        Source: 'Capture Ratios: A Popular Method of Measuring Portfolio Performance
        in Practice', Don R. Cox and Delbert C. Goff, Journal of Economics and
        Finance Education (Vol 2 Winter 2013).
        https://www.economics-finance.org/jefe/volume12-2/11ArticleCox.pdf

        :param ratio: A string as either 'up', 'down' or 'both'.
        :param base_column: Column of timeseries that is the denominator in the ratio.
        :param months_from_last: number of months offset as positive integer.
                                 Overrides use of from_date and to_date
        :param from_date: Specific from date
        :param to_date: Specific to date
        :param periods_in_a_year_fixed: Fixing the parameter to simplify testing.
        """
        assert ratio in [
            "up",
            "down",
            "both",
        ], "Ratio must be one of 'up', 'down' or 'both'."

        earlier, later = self.calc_range(months_from_last, from_date, to_date)
        fraction = (later - earlier).days / 365.25

        if isinstance(base_column, tuple):
            shortdf = self.tsdf.loc[earlier:later].loc[:, base_column]
            short_item = base_column
            short_label = self.tsdf.loc[:, base_column].name[0]
        elif isinstance(base_column, int):
            shortdf = self.tsdf.loc[earlier:later].iloc[:, base_column]
            short_item = self.tsdf.iloc[:, base_column].name
            short_label = self.tsdf.iloc[:, base_column].name[0]
        else:
            raise Exception("base_column should be a tuple or an integer.")

        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = shortdf.count() / fraction

        ratios = []
        for item in self.tsdf:
            if item == short_item:
                ratios.append(0.0)
            else:
                longdf = self.tsdf.loc[earlier:later].loc[:, item]
                if ratio == "up":
                    uparray = (
                        longdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_return = uparray.prod() ** (1 / (len(uparray) / time_factor)) - 1
                    upidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_idx_return = (
                        upidxarray.prod() ** (1 / (len(upidxarray) / time_factor)) - 1
                    )
                    ratios.append(up_return / up_idx_return)
                elif ratio == "down":
                    downarray = (
                        longdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_return = (
                        downarray.prod() ** (1 / (len(downarray) / time_factor)) - 1
                    )
                    downidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_idx_return = (
                        downidxarray.prod() ** (1 / (len(downidxarray) / time_factor))
                        - 1
                    )
                    ratios.append(down_return / down_idx_return)
                elif ratio == "both":
                    uparray = (
                        longdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_return = uparray.prod() ** (1 / (len(uparray) / time_factor)) - 1
                    upidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values > 0.0]
                        .add(1)
                        .values
                    )
                    up_idx_return = (
                        upidxarray.prod() ** (1 / (len(upidxarray) / time_factor)) - 1
                    )
                    downarray = (
                        longdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_return = (
                        downarray.prod() ** (1 / (len(downarray) / time_factor)) - 1
                    )
                    downidxarray = (
                        shortdf.pct_change()[shortdf.pct_change().values < 0.0]
                        .add(1)
                        .values
                    )
                    down_idx_return = (
                        downidxarray.prod() ** (1 / (len(downidxarray) / time_factor))
                        - 1
                    )
                    ratios.append(
                        (up_return / up_idx_return) / (down_return / down_idx_return)
                    )

        if ratio == "up":
            resultname = f"Up Capture Ratios vs {short_label}"
        elif ratio == "down":
            resultname = f"Down Capture Ratios vs {short_label}"
        elif ratio == "both":
            resultname = f"Up-Down Capture Ratios vs {short_label}"
        else:
            resultname = ""

        return pd.Series(
            data=ratios,
            index=self.tsdf.columns,
            name=resultname,
        )

    def ord_least_squares_fit(
        self, endo_column: tuple, exo_column: tuple, fitted_series: bool = True
    ) -> float:
        """
        Function adds a new column with a fitted line using
        Ordinary Least Squares.
        :param endo_column: The column of the dependent variable
        :param exo_column: The column of the exogenous variable.
        :param fitted_series: If True the fit is added to the Dataframe
        """
        y = self.tsdf.loc[:, endo_column]
        x = self.tsdf.loc[:, exo_column]
        model = sm.OLS(y, x).fit()
        if fitted_series:
            self.tsdf[endo_column[0], exo_column[0]] = model.predict(x)

        return float(model.params)

    def make_portfolio(self, name: str) -> pd.DataFrame:
        """

        :param name:
        """
        if self.weights is None:
            raise Exception(
                "OpenFrame weights property must be provided to run the "
                "make_portfolio method."
            )
        df = self.tsdf.copy()
        if not any(
            [
                True if x == "Return(Total)" else False
                for x in self.tsdf.columns.get_level_values(1).values
            ]
        ):
            df = df.pct_change()
            df.iloc[0] = 0
        portfolio = df.dot(self.weights)
        portfolio = portfolio.add(1.0).cumprod().to_frame()
        portfolio.columns = pd.MultiIndex.from_product([[name], ["Price(Close)"]])
        return portfolio

    def rolling_info_ratio(
        self,
        long_column: int = 0,
        short_column: int = 1,
        observations: int = 21,
        periods_in_a_year_fixed: int = None,
    ) -> pd.DataFrame:
        """
        The Information Ratio equals ( fund return less index return ) divided by the
        Tracking Error. And the Tracking Error is the standard deviation of the
        difference between the fund and the index returns.

        :param long_column: Column of timeseries that is the numerator in the ratio.
        :param short_column: Column of timeseries that is the denominator in the ratio.
        :param observations: The length of the rolling window to use is set as
                             number of observations.
        :param periods_in_a_year_fixed: Fixing the parameter to simplify testing.
        """
        ratio_label = (
            f"{self.tsdf.iloc[:, long_column].name[0]}"
            f" / {self.tsdf.iloc[:, short_column].name[0]}"
        )
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = self.periods_in_a_year

        relative = (
            1.0 + self.tsdf.iloc[:, long_column] - self.tsdf.iloc[:, short_column]
        )

        retdf = (
            relative.pct_change().rolling(observations, min_periods=observations).sum()
        )
        retdf = retdf.dropna().to_frame()

        voldf = relative.pct_change().rolling(
            observations, min_periods=observations
        ).std() * np.sqrt(time_factor)
        voldf = voldf.dropna().to_frame()

        ratiodf = (retdf.iloc[:, 0] / voldf.iloc[:, 0]).to_frame()
        ratiodf.columns = pd.MultiIndex.from_product(
            [[ratio_label], ["Information Ratio"]]
        )
        return ratiodf

    def rolling_corr(
        self,
        first_column: int = 0,
        second_column: int = 1,
        observations: int = 21,
    ) -> pd.DataFrame:
        """
        Function calculates correlation between two series.
        The period with at least the given number of observations is the first
        period calculated.
        :param first_column: The position as integer of the first timeseries
                             to compare
        :param second_column: The position as integer of the second timeseries
                              to compare
        :param observations: The length of the rolling window to use is set as
                             number of observations
        """
        corr_label = (
            self.tsdf.iloc[:, first_column].name[0]
            + "_VS_"
            + self.tsdf.iloc[:, second_column].name[0]
        )
        corrdf = (
            self.tsdf.iloc[:, 0]
            .pct_change()[1:]
            .rolling(observations, min_periods=observations)
            .corr(self.tsdf.iloc[:, 1].pct_change()[1:])
        )
        corrdf = corrdf.dropna().to_frame()
        corrdf.columns = pd.MultiIndex.from_product(
            [[corr_label], ["Rolling correlation"]]
        )
        return corrdf

    def rolling_vol(
        self,
        column: int,
        observations: int = 21,
        periods_in_a_year_fixed: int = None,
    ) -> pd.DataFrame:
        """
        Calculates rolling annualised volatilities.

        :param column: Position as integer of column of returns over which
                       to calculate.
        :param observations: Number of observations in the overlapping window.
        :param periods_in_a_year_fixed:
        """
        if periods_in_a_year_fixed:
            time_factor = periods_in_a_year_fixed
        else:
            time_factor = self.periods_in_a_year
        vol_label = self.tsdf.iloc[:, column].name[0]
        df = self.tsdf.iloc[:, column].pct_change()
        voldf = df.rolling(observations, min_periods=observations).std() * np.sqrt(
            time_factor
        )
        voldf = voldf.dropna().to_frame()
        voldf.columns = pd.MultiIndex.from_product(
            [[vol_label], ["Rolling volatility"]]
        )
        return voldf

    def rolling_return(self, column: int, observations: int = 21) -> pd.DataFrame:
        """
        Calculates sum of the returns in a rolling window.

        :param column: Position as integer of column of returns over which
                       to calculate.
        :param observations: Number of observations in the overlapping window.
        """
        ret_label = self.tsdf.iloc[:, column].name[0]
        retdf = (
            self.tsdf.iloc[:, column]
            .pct_change()
            .rolling(observations, min_periods=observations)
            .sum()
        )
        retdf = retdf.dropna().to_frame()
        retdf.columns = pd.MultiIndex.from_product([[ret_label], ["Rolling returns"]])
        return retdf

    def rolling_cvar_down(
        self, column: int, level: float = 0.95, observations: int = 252
    ) -> pd.DataFrame:
        """
        Calculates rolling annualized downside CVaR.

        :param column: Position as integer of column over which to calculate.
        :param observations: Number of observations in the overlapping window.
        :param level: The sought CVaR level as a float
        """
        cvar_label = self.tsdf.iloc[:, column].name[0]
        cvardf = (
            self.tsdf.iloc[:, column]
            .rolling(observations, min_periods=observations)
            .apply(lambda x: cvar_down(x, level=level))
        )
        cvardf = cvardf.dropna().to_frame()
        cvardf.columns = pd.MultiIndex.from_product([[cvar_label], ["Rolling CVaR"]])
        return cvardf

    def rolling_var_down(
        self,
        column: int,
        level: float = 0.95,
        interpolation: str = "lower",
        observations: int = 252,
    ) -> pd.DataFrame:
        """
        Calculates rolling annualized downside VaR.

        :param column: Position as integer of column over which to calculate.
        :param level: The sought VaR level as a float
        :param interpolation: type of interpolation in quantile function
                              (default value in quantile is linear)
        :param observations: Number of observations in the overlapping window.
        """
        var_label = self.tsdf.iloc[:, column].name[0]
        vardf = (
            self.tsdf.iloc[:, column]
            .rolling(observations, min_periods=observations)
            .apply(lambda x: var_down(x, level=level, interpolation=interpolation))
        )
        vardf = vardf.dropna().to_frame()
        vardf.columns = pd.MultiIndex.from_product([[var_label], ["Rolling VaR"]])
        return vardf

    def to_drawdown_series(self):
        """
        Converts all series to drawdown series.

        """
        for t in self.tsdf:
            self.tsdf.loc[:, t] = drawdown_series(self.tsdf.loc[:, t])
        return self

    def drawdown_details(self) -> pd.DataFrame:
        """
        Returns a DataFrame with: 'Max Drawdown', 'Start of drawdown',
            'Date of bottom', 'Days from start to bottom', &
            'Average fall per day' for each constituent.
        """
        mddf = pd.DataFrame()
        for i in self.constituents:
            tmpdf = i.tsdf.copy()
            tmpdf.index = pd.DatetimeIndex(tmpdf.index)
            dd = drawdown_details(tmpdf)
            dd.name = i.label
            mddf = pd.concat([mddf, dd], axis="columns")
        return mddf

    def plot_series(
        self,
        mode: str = "lines",
        tick_fmt: str = None,
        filename: str = None,
        directory: str = None,
        labels: list = None,
        auto_open: bool = True,
        add_logo: bool = True,
        show_last: bool = False,
        output_type: str = "file",
    ) -> (go.Figure, str):
        """
        Function to draw a Plotly graph with lines in Captor style.

        :param mode: The type of scatter to use, lines, markers or
                     lines+markers.
        :param tick_fmt: None, '%', '.1%' depending on number of decimals
                         to show.
        :param filename: Name of Plotly file. Include .html
        :param directory: Directory where Plotly html file is saved.
        :param labels
        :param auto_open: Determines whether or not to open a browser window
                          with the plot.
        :param add_logo: If True a Captor logo is added to the plot.
        :param show_last: If True the last data point is highlighted as red dot
                          with a label.
        :param output_type: file or div.
        """
        if labels:
            assert (
                len(labels) == self.item_count
            ), "Must provide same number of labels as items in frame."
        else:
            labels = self.columns_lvl_zero
        if not directory:
            directory = os.path.join(str(Path.home()), "Documents")
        if not filename:
            filename = "".join(random.choices(string.ascii_letters, k=6)) + ".html"
        plotfile = os.path.join(os.path.abspath(directory), filename)
        assert mode in [
            "lines",
            "markers",
            "both",
        ], "Style must be specified as lines, markers or both."
        if mode == "both":
            mode = "lines+markers"

        data = []
        for item in range(self.item_count):
            data.append(
                go.Scatter(
                    x=self.tsdf.index,
                    y=self.tsdf.iloc[:, item],
                    hovertemplate="%{y}<br>%{x|%Y-%m-%d}",
                    line=dict(width=2.5, dash="solid"),
                    mode=mode,
                    name=labels[item],
                )
            )

        fig, logo = load_plotly_dict()
        fig["data"] = data
        figure = go.Figure(fig)
        figure.update_layout(yaxis=dict(tickformat=tick_fmt))

        if add_logo:
            figure.add_layout_image(logo)

        if show_last is True:
            if tick_fmt:
                txt = "Last " + "{:" + "{}".format(tick_fmt) + "}"
            else:
                txt = "Last {}"

            for item in range(self.item_count):
                figure.add_scatter(
                    x=[self.tsdf.iloc[:, item].index[-1]],
                    y=[self.tsdf.iloc[-1, item]],
                    mode="markers + text",
                    marker={"color": "red", "size": 12},
                    hovertemplate="%{y}<br>%{x|%Y-%m-%d}",
                    showlegend=False,
                    text=[txt.format(self.tsdf.iloc[-1, item])],
                    textposition="top center",
                )

        plot(
            figure,
            filename=plotfile,
            auto_open=auto_open,
            link_text="",
            include_plotlyjs="cdn",
            config=fig["config"],
            output_type=output_type,
        )

        return figure, plotfile


def key_value_table(
    series: Union[OpenFrame, List[OpenTimeSeries]],
    headers: list = None,
    attributes: list = None,
    cols: list = None,
    swe_not_eng: bool = True,
    pct_fmt: bool = False,
    transpose: bool = False,
) -> pd.DataFrame:
    """
    Method creates a table with some key statistics.

    :param series: The data for which key values will be calculated.
    :param headers: New names for the items.
    :param attributes: A list of strings corresponding to the attribute names
                       of the key values to present.
    :param cols: The labels corresponding to the key values.
    :param swe_not_eng: True for Swedish and False for English.
    :param pct_fmt: Converts values from float to percent formatted str.
    :param transpose: Gives the option to transpose the DataFrame returned.
    """
    if isinstance(series, OpenFrame):
        basket = series.from_deepcopy()
    else:
        basket = OpenFrame(series)

    if attributes and cols:
        assert len(attributes) == len(
            cols
        ), "Must pass the same number of attributes as column labels"

    if not attributes:
        attributes = [
            "geo_ret",
            "vol",
            "worst_month",
            "var_down",
            "ret_vol_ratio",
        ]
        if basket.last_idx.year - 1 < basket.first_idx.year:
            first_ret = basket.value_ret_calendar_period(basket.last_idx.year)
            first_yr = basket.last_idx.year
        else:
            first_ret = basket.value_ret_calendar_period(basket.last_idx.year - 1)
            first_yr = basket.last_idx.year - 1
        if basket.last_idx.year == basket.first_idx.year:
            attributes = [
                basket.value_ret_calendar_period(basket.last_idx.year),
                pd.Series(
                    data=[""] * basket.item_count,
                    index=basket.vol.index,
                    name="",
                ),
            ] + [getattr(basket, x) for x in attributes]
            if swe_not_eng:
                cols = [
                    f"Avkastning ({basket.last_idx.year})",
                    "",
                    "Årsavkastning från start",
                    "Volatilitet",
                    "Värsta månad",
                    "VaR 95% (daglig)",
                    "Ratio (avk/vol)",
                ]
            else:
                cols = [
                    f"Return ({basket.last_idx.year})",
                    "",
                    "Annual return from start",
                    "Volatility",
                    "Worst month",
                    "VaR 95% (daily)",
                    "Ratio (ret/vol)",
                ]
        else:
            attributes = [
                basket.value_ret_calendar_period(basket.last_idx.year),
                first_ret,
            ] + [getattr(basket, x) for x in attributes]
            if swe_not_eng:
                cols = [
                    f"Avkastning ({basket.last_idx.year})",
                    f"Avkastning ({first_yr})",
                    "Årsavkastning från start",
                    "Volatilitet",
                    "Värsta månad",
                    "VaR 95% (daglig)",
                    "Ratio (avk/vol)",
                ]
            else:
                cols = [
                    f"Return ({basket.last_idx.year})",
                    f"Return ({first_yr})",
                    "Annual return from start",
                    "Volatility",
                    "Worst month",
                    "VaR 95% (daily)",
                    "Ratio (ret/vol)",
                ]
    else:
        attributes = [getattr(basket, x) for x in attributes]

    keyvalues = pd.concat(attributes, axis="columns")
    if cols:
        keyvalues.columns = cols
    if swe_not_eng:
        date_range = (
            f"Från {basket.first_idx:%d %b, %Y} " f"till {basket.last_idx:%d %b, %Y}"
        )
    else:
        date_range = (
            f"From {basket.first_idx:%d %b, %Y} " f"to {basket.last_idx:%d %b, %Y}"
        )

    if headers:
        if len(headers) == len(keyvalues.columns):
            keyvalues.columns = headers
        else:
            keyvalues.index = headers
    if isinstance(keyvalues.index, pd.MultiIndex):
        keyvalues.index = keyvalues.index.droplevel(level=1)
    keyvalues.index.name = date_range

    if pct_fmt:
        keyvalues = keyvalues.applymap(lambda x: "{:.2%}".format(x))

    if transpose:
        keyvalues = keyvalues.T

    return keyvalues
