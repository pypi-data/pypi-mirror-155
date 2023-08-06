#!/usr/bin/env python3# (C) Copyright 2021 ECMWF and JSC
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF and JSC do not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
from __future__ import annotations

import os
from typing import Union, List
import numpy as np
import pandas as pd
import xarray as xr
import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import normalize

List_or_string = Union[List, str]

__version__ = "0.2.0"

URL = "https://storage.ecmwf.europeanweather.cloud"

PATTERN = "{url}/MAELSTROM_AP5/unet_ds_t2m_{date}.nc"


@normalize("x","date-list(%Y%m)")
def DateListNormaliser(x):
    return x


class Downscaling(Dataset):
    class_name = "Downsclaing_Dataset"
    name = "IFS t2m dataset"
    home_page = "https://git.ecmwf.int/projects/MLFET/repos/maelstrom-downscaling-ap5"
    licence = "Apache Licence Version 2.0"
    documentation = "-"
    citation = "-"
    terms_of_use = (
        "By downloading data from this dataset, you agree to the terms and conditions defined at "
        "https://git.ecmwf.int/projects/MLFET/repos/maelstrom-downscaling-ap5/browse/climetlab-maelstrom-downscaling-ap5/LICENSE"
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    dates_all = pd.date_range("2016-01-01", "2020-12-01", freq="MS")
    dates_all = dates_all[dates_all.month.isin(list(np.arange(4, 10)))]

    all_datelist = DateListNormaliser(dates_all)    

    dataset_types = {"training": dates_all[dates_all.year.isin(list(np.arange(2016, 2020)))],
                     "validation": dates_all[np.logical_and(dates_all.year.isin([2020]),
                                                            dates_all.month.isin([5, 7, 8]))],
                     "testing": dates_all[np.logical_and(dates_all.year.isin([2020]),
                                                         dates_all.month.isin([4, 6, 9]))],
                     # augmenetd datasets are stored in individual files
                     "training_aug": "maelstrom-downscaling_train_aug.nc",
                     "validation_aug": "maelstrom-downscaling_val_aug.nc",
                     "testing_aug": "maelstrom-downscaling_test_aug.nc"}

    default_datelist = dataset_types["training"]

    def __init__(self, months: List = None, dataset: str = None):
        """
        Initialize data loader instance
        :param months: list of months for which downscaling data is requested
        :param dataset: name of dataset (see dataset_types-dictionary)
        """

        assert not (months is None and dataset is None), "Either list of months or dataset-name must be passed."

        self.dataset = dataset

        if (not self.dataset is None) and (not months is None):
            print("List of months and dataset-name cannot be processed simultaneously. months will be ignored.")

        if self.dataset is None:
            self.date = self.parse_date(months)
        else:
            if not self.dataset in self.dataset_types.keys():
                raise ValueError("Unknown dataset type {0} passed. Valid choices are [{1}]"
                                 .format(dataset, ",".join(self.dataset_types.keys())))
            if isinstance(self.dataset_types[self.dataset], str):
                self.date = None
            else:
                self.date = self.parse_date(self.dataset_types[self.dataset])
        # get the requested data
        self._load()

    def _load(self):
        """
        Builds the URL-request and retrieves the data.
        :return: -
        """
        if self.date is None:       # in case, no date is specified, a sngle URL-request is created
            data_url = os.path.join(*os.path.normpath(PATTERN).split(os.path.sep)[:-1],
                                    self.dataset_types[self.dataset])
            data_url = data_url.replace("{url}", URL)
            self.source = cml.load_source("url", data_url)
        else:
            request_dict = dict(url=URL, date=self.date)
            self.source = cml.load_source("url-pattern", PATTERN, request_dict, merger=Merger())

    def parse_date(self, dates: List_or_string):
        """
        Parse individual date or list of dates for downscaling dataset
        :param dates: list of dates (months) or individual month
        :return: normalized date string suitable for requiring downscaling data
        """
        if dates is None:
            dates = self.default_datelist
        dates = DateListNormaliser(dates)
        check_date = [d for d, date in enumerate(dates) if date not in self.all_datelist]
        if check_date:
            print("The following passed months are not available in the dataset:")
            for index in check_date:
                print("* {0}".format(dates[index]))
            raise ValueError("Unavailable months requested. Check your input.")

        return dates


class Merger:
    def __init__(self, engine: str = "netcdf4", options=None):
        """Initializes merger based on xarray's open_mfdataset.
        :param engine: Engine to read netCDF-files (see open_mfdataset-documentation for more details).
        :param options: Additional options passed to open_mfdataset.
        :return: -
        """
        self.engine = engine
        self.options = options if options is not None else {}

    def to_xarray(self, paths: List):
        """
        Merger to read data from multiple netCDF-files
        :param paths: list containing paths to netCDF-data files to be read
        :return: -
        """
        return xr.open_mfdataset(
            paths,
            engine=self.engine,
            parallel=True,
            **self.options
        )
