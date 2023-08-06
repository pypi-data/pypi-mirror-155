from datetime import datetime, timedelta

import logging
from typing import List

import requests
import pandas as pd

from dateutil.relativedelta import relativedelta
from dilivia_data_client import query
from dilivia_data_client.mapping_dilivia import ALL_METRICS, DICT_METRICS,\
    LIST_METRICS_VEHICLE, LIST_METRICS_VEHICLE_OUTPUT, \
    LIST_METRICS_TRIP, LIST_METRICS_TRIP_OUTPUT,\
    DILIVIA_DATE_TIME_FORMAT, DILIVIA_START_DATE_TIME, MASTER_MODULE

pd.options.mode.chained_assignment = None


URL_FETCH = "https://enovea.dilivia.net/"
ENDPOINT_FETCH = "db/fetch"  # endpoint nécessaire pour la connexion

URL_DRUID = "http://172.20.28.2:8888/druid"
ENDPOINT_DRUID = "/v2/sql"
DATASOURCE_DRUID = "dilivia-data-client"


class Connexion:
    """
    Cette classe va permettre d'établir la connexion vers les données Fetch\n
        - "url" + "endpoint" : permettent d'établir la connexion
        - "token" : permet d'authentifier l'utilisateur et de pouvoir effectuer une requete
    """

    url = ""
    endpoint = ""
    datasource = ""
    token = ""
    connexion_type = ""

    df = pd.DataFrame()
    param_request = {}
    mapping = {}

    def __init__(self, url: str = "", endpoint: str = "", datasource: str = ""):
        """
        Cette méthode initialise les paramètres de connexion
        """
        self.url = url
        self.endpoint = endpoint

        if 'fetch' in url + endpoint:
            self.connexion_type = "fetch"
        elif 'druid' in url + endpoint:
            self.connexion_type = "druid"
            if datasource != "":
                self.datasource = datasource
            else:
                raise Exception("'datasource' must not be null for druid")
        else:
            self.connexion_type = ""

    def copy(self):
        return Connexion(self.url, self.endpoint, self.datasource).auth(self.token)

    def is_fetch_connexion(self):
        return self.connexion_type == "fetch"

    def is_druid_connexion(self):
        return self.connexion_type == "druid"

    def auth(self, token: str = ""):
        """
        Cette méthode authentifie l'utilisateur à l'aide du "token"
        """
        self.token = token
        return self

    def get_list_devices(self) -> List[str]:
        c_new = self.copy()
        df = c_new.select() \
                  .date(DILIVIA_START_DATE_TIME, DILIVIA_START_DATE_TIME + timedelta(days=1)) \
                  .device() \
                  .metrics(["id", "vehicle_id"]) \
                  .dataframe()
        return sorted(set(df["id"]))

    def get_list_vehicles(self) -> List[str]:
        c_new = self.copy()
        df = c_new.select() \
                  .date(DILIVIA_START_DATE_TIME, DILIVIA_START_DATE_TIME + timedelta(days=1)) \
                  .device() \
                  .metrics(["id", "vehicle_id"]) \
                  .dataframe()
        return sorted(set(df["vehicle_id"]))

    def select(self) -> 'Connexion':
        """
        Cette méthode va réinitialiser la requête afin d'en effectuer une nouvelle
        """
        self.param_request = {}
        self.mapping = {}
        self.df = pd.DataFrame()
        return self

    def get_dict_vehicle_devices(self) -> dict:
        c_new = self.copy()
        list_vehicles = c_new.get_list_vehicles()
        df_vehicles = c_new.select()\
            .date(DILIVIA_START_DATE_TIME, DILIVIA_START_DATE_TIME + timedelta(days=1))\
            .device().metrics(["id", "vehicle_id"])\
            .dataframe()
        dict_v2ds = {}
        for vehicle in list_vehicles:
            dict_v2ds[vehicle] = []
            for i in range(len(df_vehicles)):
                if df_vehicles['vehicle_id'].iloc[i] == vehicle:
                    dict_v2ds[vehicle].append(df_vehicles['id'].iloc[i])
        return dict_v2ds

    def get_dict_device_vehicles(self) -> dict:
        c_new = self.copy()
        list_devices = c_new.get_list_devices()
        df_devices = c_new.select()\
            .date(DILIVIA_START_DATE_TIME, DILIVIA_START_DATE_TIME + timedelta(days=1))\
            .device().metrics(["id", "vehicle_id"])\
            .dataframe()
        dict_d2vs = {}
        for device in list_devices:
            dict_d2vs[device] = []
            for i in range(len(df_devices)):
                if df_devices['id'].iloc[i] == device:
                    dict_d2vs[device].append(df_devices['vehicle_id'].iloc[i])
        return dict_d2vs

    def from_device_to_vehicle(self, device, i: int = 0):
        return self.get_dict_device_vehicles()[device][i]

    def from_vehicle_to_device(self, vehicle: str, i: int = 0):
        return self.get_dict_vehicle_devices()[vehicle][i]

    def vehicle(self, vid_: str or List[str] = '') -> 'Connexion':
        """
        Cette méthode va alimenter le param_request en remplissant le champ "vid"
        """
        self.param_request['id'] = self.from_vehicle_to_device(vid_)
        return self

    def vehicles(self, vid_s: List[str] = None):
        self.param_request['id'] = [] if vid_s is None \
            else [self.from_vehicle_to_device(vid_) for vid_ in vid_s]
        return self

    def device(self, id_: str or List[str] = '') -> 'Connexion':
        """
        Cette méthode va alimenter le param_request en remplissant le champ "vid"
        """
        self.param_request['id'] = id_
        return self

    def devices(self, id_s: List[str] = None):
        self.param_request['id'] = [] if id_s is None else id_s
        return self

    def date(self,
             start: datetime = DILIVIA_START_DATE_TIME,
             end: datetime = datetime.now()) -> 'Connexion':
        """
        Cette méthode va alimenter le param_request en remplissant les champs "start" et "end"
        """
        self.param_request['date'] = {
            'start': datetime.strftime(start, DILIVIA_DATE_TIME_FORMAT),
            'end': datetime.strftime(end, DILIVIA_DATE_TIME_FORMAT)
        }
        return self

    def metrics(self, list_metrics: List[str] = ALL_METRICS) -> 'Connexion':
        """
        Cette méthode va alimenter le champ "metrics" de "param_request" à partir de la
        "list_metrics" entrée
        """
        self.param_request['metrics'] = list_metrics
        return self

    def select_device(self, id_: str,
                      start: datetime = DILIVIA_START_DATE_TIME,
                      end: datetime = datetime.now())\
            -> pd.Series:
        """
        Selection des données intéressantes relatives à un véhicule
        """
        dataframe_ = self.select()\
                         .device(id_)\
                         .date(start, end)\
                         .metrics(LIST_METRICS_VEHICLE)\
                         .dataframe()
        somme = dataframe_['trip_distance'].sum()
        dataframe_['trip_distance'].iloc[0] = somme
        dataframe_.columns = LIST_METRICS_VEHICLE_OUTPUT
        return dataframe_.iloc[0]

    def select_vehicle(self, vid_: str,
                       start: datetime = DILIVIA_START_DATE_TIME,
                       end: datetime = datetime.now())\
            -> pd.Series:
        return self.select_device(self.from_vehicle_to_device(vid_), start, end)

    def select_trips(self,
                     id_: str,
                     start=datetime.now() - relativedelta(years=1),
                     end=datetime.now()) \
            -> pd.DataFrame:
        """
        Selection de certaines données pour des trajets
        """
        dataframe_ = self.select() \
                         .device(id_) \
                         .date(start, end) \
                         .metrics(LIST_METRICS_TRIP) \
                         .dataframe()

        dataframe_[['lat', 'lng']] = dataframe_[['lat', 'lng']].astype(str)

        df_stop = (dataframe_.iloc[1::2]).copy()
        df_start = (dataframe_.iloc[::2]).copy()

        df_stop['lng'] = df_stop['lat'].str.cat(df_stop['lng'], sep=', ')
        df_start['lat'] = df_start['lat'].str.cat(df_start['lng'], sep=', ')

        for i in range(df_stop.shape[0]):
            df_stop['lat'].iloc[i] = df_start['lat'].iloc[i]

        df_stop.columns = LIST_METRICS_TRIP_OUTPUT
        df_stop = df_stop.reset_index(drop=True)
        return df_stop

    def select_metrics(self, id_: str,
                       list_metrics: List[str] = ALL_METRICS,
                       start: datetime = datetime.now() - relativedelta(years=1),
                       end: datetime = datetime.now()) \
            -> pd.DataFrame:
        """
        Selection de certaines "metrics"
        """
        return self.select().device(id_).date(start, end).metrics(list_metrics).dataframe()

    def __filter(self, dataframe_: pd.DataFrame) -> 'Connexion':
        """
        Cette méthode va filtrer, parmi toutes les variables des différents modules générés,
        les colonnes intéressantes (metrics) pour l'utilisateur #
        """
        for metric_name in self.param_request['metrics']:
            self.df[metric_name] = dataframe_[metric_name]
        return self

    def __to_query(self) -> dict:
        """
        Cette méthode convertit les query params en query (JSON)
        """
        list_metrics = self.param_request['metrics']
        if self.is_fetch_connexion():
            metrics_names_dict = DICT_METRICS.get_dict_metrics_names()

            param_request_ = self.param_request
            list_modules = []
            for metric_name in list_metrics:
                if metric_name in ALL_METRICS and \
                        not metrics_names_dict[metric_name]['fetch']['module'] in list_modules\
                        and metrics_names_dict[metric_name]['fetch']['module'] != MASTER_MODULE:
                    list_modules.append(
                        metrics_names_dict[metric_name]['fetch']['module']
                    )
            return query.query(param_request_['id'],
                               datetime.strptime(param_request_['date']['start'],
                                                 DILIVIA_DATE_TIME_FORMAT),
                               datetime.strptime(param_request_['date']['end'],
                                                 DILIVIA_DATE_TIME_FORMAT),
                               list_modules)
        elif self.is_druid_connexion():
            list_raw_names = [DICT_METRICS.get_raw_name(metric_name, self.connexion_type)
                              for metric_name in list_metrics]
            return query.query_druid(
                        self.param_request['id'],
                        datetime.strptime(self.param_request['date']['start'],
                                          DILIVIA_DATE_TIME_FORMAT),
                        datetime.strptime(self.param_request['date']['end'],
                                          DILIVIA_DATE_TIME_FORMAT),
                        list_raw_names,
                        self.datasource)
        else:
            return {}

    def __to_headers(self) -> dict:
        if self.is_fetch_connexion():
            return query.headers(self.token)
        elif self.is_druid_connexion():
            return query.headers_druid(self.token)
        else:
            return {}

    def dataframe(self) -> pd.DataFrame:
        try:
            response = requests.post(self.url + self.endpoint, json=self.__to_query(),
                                     headers=self.__to_headers())
            if not query.error_status_code(response):
                try:
                    self.__filter(query.dataframe_read_csv(response.text))
                    return self.df
                except TypeError:
                    logging.error(response.text)
                    id_s = self.param_request['id']
                    id_s_str = ', '.join(id_s) if isinstance(id_s, List) else id_s
                    logging.error('No data for id:' + id_s_str)
            else:
                logging.error("%s %s" % (response, response.reason))
                logging.error(response.text)
        except (requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema, KeyError):
            pass
        return pd.DataFrame()
