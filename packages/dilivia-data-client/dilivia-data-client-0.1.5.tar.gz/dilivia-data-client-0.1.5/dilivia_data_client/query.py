from datetime import datetime

import io
from typing import List

import pandas as pd
import requests

from dilivia_data_client.mapping_dilivia import \
    DILIVIA_START_DATE_TIME, DILIVIA_DATE_TIME_FORMAT, \
    LIST_MODULES, DICT_METRICS, ALL_METRICS


def query(id_: str or List[str],
          start: datetime = DILIVIA_START_DATE_TIME,
          end: datetime = datetime.now(),
          list_modules: List[str] = LIST_MODULES) -> dict:
    """
    Cette fonction va créer un objet JSON "query" à partir des attributs suivants :\n
        - "vid" : l'identifiant d'un véhicule donné
        - "start" : début de la période considérée
        - "end" : fin de la période considérée
        - "list_module" : liste des différents modules considérés
    """
    gts_ids = []
    if isinstance(id_, List):
        gts_ids = id_
    elif isinstance(id_, str) and not id_ == '':
        gts_ids = [id_]
    return {
        "modulesName": list_modules,
        "start": datetime.strftime(start, DILIVIA_DATE_TIME_FORMAT),
        "end": datetime.strftime(end, DILIVIA_DATE_TIME_FORMAT),
        "gtsIds": gts_ids
    }


def headers_(**kwargs) -> dict:
    headers_dict = {}
    for key, value in kwargs.items():
        if value is not None:
            headers_dict[key] = value
    return headers_dict


def headers(auth_token: str) -> dict:
    """
    Cette fonction va créer l'en tête d'un fichier -
    accessible à partir d'un token "auth_token" donné
    """
    return {'Accept': 'text/plain',
            'Accept-Encoding': 'identity',
            'Content-Type': 'application/json',
            'X-Warp10-Token': auth_token}


def headers_druid(auth_token: str) -> dict:
    return {'Content-Type': 'application/json',
            'Authorization': auth_token}


def query_druid(id_: str or List[str],
                start: datetime = DILIVIA_START_DATE_TIME,
                end: datetime = datetime.now(),
                metrics: List[str] = ALL_METRICS,
                datasource: str = 'dilivia-data-client') -> dict:

    sql = "SELECT " + ', '.join(metrics) + " " + \
          "FROM \"" + datasource + "\" " + \
          "WHERE " + \
          (  # au cas où aucun véhicule n'est entré
              "id in ('" + ("', '".join(id_) if isinstance(id_, List)
                            else id_)
              + "') and " if (id_ != [] and id_ != '')
              else ""
          ) \
          + "'" + start.strftime(DILIVIA_DATE_TIME_FORMAT) + "' <= __time " + \
          "and __time <= '" + end.strftime(DILIVIA_DATE_TIME_FORMAT) + "' "
    return {
        "header": "true",
        "resultFormat": "csv",
        "query": sql
    }


def error_status_code(request_post: requests.models.Response) -> bool:
    """
    Cette fonction renvoie :\n
        - "False" lorsque la connexion du request_post ne présente aucun défaut (status_code = 200)
        - "True" lorsque la connexion du request_post présente un défaut
    """
    return request_post.status_code != 200


def is_fetch_connexion(list_raw_names: List[str]) -> (bool, str):
    bool_ = 'date' in list_raw_names
    data_place_str = 'fetch' if bool_ else 'druid'
    return bool_, data_place_str


def dataframe_read_csv(csv: str) -> pd.DataFrame:
    """
    A partir de la dataframe au format csv,
    cette fonction va générer les données correspondantes sous forme de dataframe
    """
    dict_types, dict_target_types = {}, {}
    metrics_names_dict = DICT_METRICS.get_dict_metrics_names()
    raw_names_dict = DICT_METRICS.get_dict_raw_names()

    list_raw_names = csv.split('\n')[0].split(',')  # first line from the csv (raw_names)
    is_fetch_bool, data_place_str = is_fetch_connexion(list_raw_names)
    ls = []
    for rn in list_raw_names:
        try:
            ls.append(raw_names_dict[rn]['metric_name'])
        except Exception:
            ls.append(rn + " Error")

    list_metrics_names = []
    for raw_name in list_raw_names:
        try:
            list_metrics_names.append(raw_names_dict[raw_name]['metric_name'])
        except Exception:
            list_metrics_names.append(raw_name)

    for metric_name in list_metrics_names:
        if metric_name != 'date_time':
            try:
                dict_types[metrics_names_dict[metric_name][data_place_str]['raw_name']] =\
                    metrics_names_dict[metric_name]['type']
                dict_target_types[metrics_names_dict[metric_name][data_place_str]['raw_name']] =\
                    metrics_names_dict[metric_name]['target_type']
            except Exception:
                dict_types[metric_name] = str
                dict_target_types[metric_name] = str
    try:
        dataframe_ = pd.read_csv(io.StringIO(csv), sep=",", dtype=dict_types,
                                 parse_dates=['date'] if is_fetch_bool else None)
        dataframe_.fillna(0, inplace=True)
        dataframe_.astype(dict_target_types)
        dataframe_.rename(inplace=True, columns=dict(zip(list_raw_names, list_metrics_names)))
        return dataframe_
    except (pd.errors.EmptyDataError, ValueError):
        return pd.DataFrame()
