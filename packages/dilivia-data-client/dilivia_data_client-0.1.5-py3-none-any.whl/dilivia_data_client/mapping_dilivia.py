from datetime import datetime
import numpy as np


# Liste des 11 modules disponibles

ACCELERATION_MODULE = "AccelerationModule"
CARTO_MODULE = "CartoModule"
ELEVATION_MODULE = "ElevationModule"
GEO_SPATIAL_MODULE = "GeoSpatialModule"
GPS_RAW_MODULE = "GpsRawModule"
GPS_BASE_MODULE = "GpsBaseModule"
LANDUSE_MODULE = "LanduseModule"
TRIP_MODULE = "TripModule"
VEHICLE_MODULE = "VehicleModule"
WEATHER_MODULE = "WeatherModule"

MASTER_MODULE = "MasterModule"

LIST_MODULES = [
    ACCELERATION_MODULE,
    CARTO_MODULE,
    ELEVATION_MODULE,
    GEO_SPATIAL_MODULE,
    GPS_RAW_MODULE,
    GPS_BASE_MODULE,
    LANDUSE_MODULE,
    TRIP_MODULE,
    VEHICLE_MODULE,
    WEATHER_MODULE,

    MASTER_MODULE
]


class MetricsRegistry:
    dict_metrics_names = {}
    dict_raw_names = {}
    dict_fetch_modules_raw_names = {module: [] for module in LIST_MODULES}

    def __init__(self):
        pass

    def add(self, **kwargs):

        metric_name = kwargs.get('metric_name', None)
        type_ = kwargs.get('type_', None)
        target_type_ = kwargs.get('target_type_', None)
        data_place_str = kwargs.get('data_place_str', None)
        raw_name = kwargs.get('raw_name', None)
        module = kwargs.get('module', None)

        if metric_name:
            if metric_name not in self.dict_metrics_names.keys():
                self.dict_metrics_names[metric_name] = {
                        "type": type_,
                        "target_type": target_type_ if target_type_ else type_
                }

            if data_place_str and raw_name:
                self.dict_raw_names[raw_name] = {"metric_name": metric_name}
                self.dict_metrics_names[metric_name][data_place_str] = {"raw_name": raw_name}
                if data_place_str == "fetch":
                    self.dict_metrics_names[metric_name][data_place_str]["module"] = module
                    self.dict_fetch_modules_raw_names[module].append(raw_name)

    def get_dict_metrics_names(self):
        return self.dict_metrics_names

    def get_dict_raw_names(self):
        return self.dict_raw_names

    def get_raw_name(self, metric_name, connexion_type_str):
        return self.dict_metrics_names[metric_name][connexion_type_str]['raw_name']

    def get_list_metrics(self):
        return list(self.dict_metrics_names.keys())


"""""" """""" """"""  """""" """MAPPING_METRICS""" """""" """""" """""" """"""

##################################################################################################
DICT_METRICS = MetricsRegistry()
##################################################################################################

# MasterModule
DICT_METRICS.add(metric_name="date_time", type_=datetime)
DICT_METRICS.add(metric_name="date_time", data_place_str="druid", raw_name="__time")
DICT_METRICS.add(metric_name="date_time", data_place_str="fetch", raw_name="date", module=MASTER_MODULE)

DICT_METRICS.add(metric_name="device_name", type_=str)
DICT_METRICS.add(metric_name="device_name", data_place_str="druid", raw_name="device_name")
DICT_METRICS.add(metric_name="device_name", data_place_str="fetch", raw_name="deviceName", module=MASTER_MODULE)

DICT_METRICS.add(metric_name="id", type_=str)
DICT_METRICS.add(metric_name="id", data_place_str="druid", raw_name="id")
DICT_METRICS.add(metric_name="id", data_place_str="fetch", raw_name="id", module=MASTER_MODULE)

DICT_METRICS.add(metric_name="lat", type_=np.float64)
DICT_METRICS.add(metric_name="lat", data_place_str="fetch", raw_name="lat", module=MASTER_MODULE)

DICT_METRICS.add(metric_name="lng", type_=np.float64)
DICT_METRICS.add(metric_name="lng", data_place_str="fetch", raw_name="lon", module=MASTER_MODULE)


# TripModule
DICT_METRICS.add(metric_name="trip_count", type_=np.float64, target_type_=np.int64)
DICT_METRICS.add(metric_name="trip_count", data_place_str="druid", raw_name="trip_count")
DICT_METRICS.add(metric_name="trip_count", data_place_str="fetch", raw_name="tripCount", module=TRIP_MODULE)

DICT_METRICS.add(metric_name="trip_distance", type_=np.float64)
DICT_METRICS.add(metric_name="trip_distance", data_place_str="druid", raw_name="trip_distance")
DICT_METRICS.add(metric_name="trip_distance", data_place_str="fetch", raw_name="tripDistance", module=TRIP_MODULE)

DICT_METRICS.add(metric_name="trip_duration", type_=np.float64)
DICT_METRICS.add(metric_name="trip_duration", data_place_str="druid", raw_name="trip_duration")
DICT_METRICS.add(metric_name="trip_duration", data_place_str="fetch", raw_name="tripDuration", module=TRIP_MODULE)

DICT_METRICS.add(metric_name="trip_event", type_=str)
DICT_METRICS.add(metric_name="trip_event", data_place_str="druid", raw_name="trip_event")
DICT_METRICS.add(metric_name="trip_event", data_place_str="fetch", raw_name="tripEvent", module=TRIP_MODULE)

DICT_METRICS.add(metric_name="trip_id", type_=str)
DICT_METRICS.add(metric_name="trip_id", data_place_str="druid", raw_name="trip_id")
DICT_METRICS.add(metric_name="trip_id", data_place_str="fetch", raw_name="tripId", module=TRIP_MODULE)

DICT_METRICS.add(metric_name="score_continuity", type_=np.float64)
DICT_METRICS.add(metric_name="score_continuity", data_place_str="druid", raw_name="score_continuity")
DICT_METRICS.add(metric_name="score_continuity", data_place_str="fetch", raw_name="continuityScore", module=TRIP_MODULE)

DICT_METRICS.add(metric_name="distance_from_last_trip", type_=np.float64)
DICT_METRICS.add(metric_name="distance_from_last_trip", data_place_str="druid", raw_name="distance_from_last_trip")
DICT_METRICS.add(metric_name="distance_from_last_trip", data_place_str="fetch", raw_name="distanceFromLastTrip", module=TRIP_MODULE)


# WeatherModule
DICT_METRICS.add(metric_name="weather_temperature", type_=np.int64)
DICT_METRICS.add(metric_name="weather_temperature", data_place_str="druid", raw_name="weather_temperature")
DICT_METRICS.add(metric_name="weather_temperature", data_place_str="fetch", raw_name="temperature", module=WEATHER_MODULE)

DICT_METRICS.add(metric_name="weather_condition", type_=str)
DICT_METRICS.add(metric_name="weather_condition", data_place_str="druid", raw_name="weather_condition")
DICT_METRICS.add(metric_name="weather_condition", data_place_str="fetch", raw_name="condition", module=WEATHER_MODULE)


# VehicleModule
DICT_METRICS.add(metric_name="vehicle_id", type_=str)
DICT_METRICS.add(metric_name="vehicle_id", data_place_str="druid", raw_name="vehicle_id")
DICT_METRICS.add(metric_name="vehicle_id", data_place_str="fetch", raw_name="vehicleId", module=VEHICLE_MODULE)


# GpsBaseModule
DICT_METRICS.add(metric_name="base_gps_duration_delta", type_=np.float64)
DICT_METRICS.add(metric_name="base_gps_duration_delta", data_place_str="druid", raw_name="base_gps_duration_delta")
DICT_METRICS.add(metric_name="base_gps_duration_delta", data_place_str="fetch", raw_name="deltaDuration", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="base_gps_distance_delta", type_=np.float64)
DICT_METRICS.add(metric_name="base_gps_distance_delta", data_place_str="druid", raw_name="base_gps_distance_delta")
DICT_METRICS.add(metric_name="base_gps_distance_delta", data_place_str="fetch", raw_name="deltaGpsDistance", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="base_curve_radius", type_=np.float64)
DICT_METRICS.add(metric_name="base_curve_radius", data_place_str="druid", raw_name="base_curve_radius")
DICT_METRICS.add(metric_name="base_curve_radius", data_place_str="fetch", raw_name="curveRadius", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="base_curve_status", type_=str)
DICT_METRICS.add(metric_name="base_curve_status", data_place_str="druid", raw_name="base_curve_status")
DICT_METRICS.add(metric_name="base_curve_status", data_place_str="fetch", raw_name="curveRadiusCategory", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="raw_gps_lat", type_=np.float64)
DICT_METRICS.add(metric_name="raw_gps_lat", data_place_str="druid", raw_name="raw_gps_lat")
DICT_METRICS.add(metric_name="raw_gps_lat", data_place_str="fetch", raw_name="raw.gps.lat", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="raw_gps_lng", type_=np.float64)
DICT_METRICS.add(metric_name="raw_gps_lng", data_place_str="druid", raw_name="raw_gps_lng")
DICT_METRICS.add(metric_name="raw_gps_lng", data_place_str="fetch", raw_name="raw.gps.lng", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="base_gps_accelerometer_lat", type_=np.float64, target_type_=np.int64)
DICT_METRICS.add(metric_name="base_gps_accelerometer_lat", data_place_str="druid", raw_name="base_gps_accelerometer_lat")
DICT_METRICS.add(metric_name="base_gps_accelerometer_lat", data_place_str="fetch", raw_name="gpsAccX", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="base_gps_accelerometer_lng", type_=np.float64, target_type_=np.int64)
DICT_METRICS.add(metric_name="base_gps_accelerometer_lng", data_place_str="druid", raw_name="base_gps_accelerometer_lng")
DICT_METRICS.add(metric_name="base_gps_accelerometer_lng", data_place_str="fetch", raw_name="gpsAccY", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="daycycle_alt", type_=np.float64)
DICT_METRICS.add(metric_name="daycycle_alt", data_place_str="druid", raw_name="daycycle_alt")
DICT_METRICS.add(metric_name="daycycle_alt", data_place_str="fetch", raw_name="sunAltitude", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="daycycle_status", type_=str)
DICT_METRICS.add(metric_name="daycycle_status", data_place_str="druid", raw_name="daycycle_status")
DICT_METRICS.add(metric_name="daycycle_status", data_place_str="fetch", raw_name="sunStatus", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="base_gps_moving", target_type_=bool)
DICT_METRICS.add(metric_name="base_gps_moving", data_place_str="druid", raw_name="base_gps_moving")
DICT_METRICS.add(metric_name="base_gps_moving", data_place_str="fetch", raw_name="moving", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="base_gps_speed", type_=np.float64)
DICT_METRICS.add(metric_name="base_gps_speed", data_place_str="druid", raw_name="base_gps_speed")
DICT_METRICS.add(metric_name="base_gps_speed", data_place_str="fetch", raw_name="gpsSpeed", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="raw_gps_satellites", type_=np.int64)
DICT_METRICS.add(metric_name="raw_gps_satellites", data_place_str="druid", raw_name="raw_gps_satellites")
DICT_METRICS.add(metric_name="raw_gps_satellites", data_place_str="fetch", raw_name="nbSats", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="raw_gps_hdop", type_=np.int64)
DICT_METRICS.add(metric_name="raw_gps_hdop", data_place_str="druid", raw_name="raw_gps_hdop")
DICT_METRICS.add(metric_name="raw_gps_hdop", data_place_str="fetch", raw_name="hdop", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="high_frequency_acc_x", type_=str)
DICT_METRICS.add(metric_name="high_frequency_acc_x", data_place_str="fetch", raw_name="highFrequencyAccX", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="high_frequency_acc_y", type_=str)
DICT_METRICS.add(metric_name="high_frequency_acc_y", data_place_str="fetch", raw_name="highFrequencyAccY", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="high_frequency_acc_z", type_=str)
DICT_METRICS.add(metric_name="high_frequency_acc_z", data_place_str="fetch", raw_name="highFrequencyAccZ", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="raw_gps_heading", type_=np.float64)
DICT_METRICS.add(metric_name="raw_gps_heading", data_place_str="druid", raw_name="raw_gps_heading")
DICT_METRICS.add(metric_name="raw_gps_heading", data_place_str="fetch", raw_name="azimuth", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="raw_gps_sun_heading", type_=np.float64)
DICT_METRICS.add(metric_name="raw_gps_sun_heading", data_place_str="druid", raw_name="raw_gps_sun_heading")
DICT_METRICS.add(metric_name="raw_gps_sun_heading", data_place_str="fetch", raw_name="sunAzimuth", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="accumulated_duration", type_=np.float64)
DICT_METRICS.add(metric_name="accumulated_duration", data_place_str="druid", raw_name="accumulated_duration")
DICT_METRICS.add(metric_name="accumulated_duration", data_place_str="fetch", raw_name="accumulatedDuration", module=GPS_BASE_MODULE)

DICT_METRICS.add(metric_name="accumulated_distance", type_=np.float64)
DICT_METRICS.add(metric_name="accumulated_distance", data_place_str="druid", raw_name="accumulated_distance")
DICT_METRICS.add(metric_name="accumulated_distance", data_place_str="fetch", raw_name="accumulatedGpsDistance", module=GPS_BASE_MODULE)


# CartoModule
DICT_METRICS.add(metric_name="map_route_distance_sum", type_=np.float64)
DICT_METRICS.add(metric_name="map_route_distance_sum", data_place_str="druid", raw_name="map_route_distance_sum")
DICT_METRICS.add(metric_name="map_route_distance_sum", data_place_str="fetch", raw_name="accumulatedMapMatchDistance", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_route_duration_sum", type_=np.float64)
DICT_METRICS.add(metric_name="map_route_duration_sum", data_place_str="druid", raw_name="map_route_duration_sum")
DICT_METRICS.add(metric_name="map_route_duration_sum", data_place_str="fetch", raw_name="accumulatedMapMatchDuration", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_route_status", type_=str)
DICT_METRICS.add(metric_name="map_route_status", data_place_str="druid", raw_name="map_route_status")
DICT_METRICS.add(metric_name="map_route_status", data_place_str="fetch", raw_name="matchType", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_route_distance_delta", type_=np.float64)
DICT_METRICS.add(metric_name="map_route_distance_delta", data_place_str="druid", raw_name="map_route_distance_delta")
DICT_METRICS.add(metric_name="map_route_distance_delta", data_place_str="fetch", raw_name="deltaMapMatchDistance", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_route_duration_delta", type_=np.float64)
DICT_METRICS.add(metric_name="map_route_duration_delta", data_place_str="druid", raw_name="map_route_duration_delta")
DICT_METRICS.add(metric_name="map_route_duration_delta", data_place_str="fetch", raw_name="deltaMapMatchDuration", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_gps_lat", type_=np.float64)
DICT_METRICS.add(metric_name="map_gps_lat", data_place_str="druid", raw_name="map_gps_lat")
DICT_METRICS.add(metric_name="map_gps_lat", data_place_str="fetch", raw_name="map.gps.lat", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_gps_lng", type_=np.float64)
DICT_METRICS.add(metric_name="map_gps_lng", data_place_str="druid", raw_name="map_gps_lng")
DICT_METRICS.add(metric_name="map_gps_lng", data_place_str="fetch", raw_name="map.gps.lng", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_road_curve_status", type_=str)
DICT_METRICS.add(metric_name="map_road_curve_status", data_place_str="druid", raw_name="map_road_curve_status")
DICT_METRICS.add(metric_name="map_road_curve_status", data_place_str="fetch", raw_name="map.route.curve.status", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_match_azimuth", type_=np.float64)
DICT_METRICS.add(metric_name="map_match_azimuth", data_place_str="fetch", raw_name="mapMatchAzimuth", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_road_curve_radius", type_=np.float64)
DICT_METRICS.add(metric_name="map_road_curve_radius", data_place_str="druid", raw_name="map_road_curve_radius")
DICT_METRICS.add(metric_name="map_road_curve_radius", data_place_str="fetch", raw_name="mapMatchCurveRadius", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_route_altitude", type_=np.float64)
DICT_METRICS.add(metric_name="map_route_altitude", data_place_str="fetch", raw_name="map.route.altitude", module=CARTO_MODULE)

DICT_METRICS.add(metric_name="map_match_gps_speed", type_=np.float64)
DICT_METRICS.add(metric_name="map_match_gps_speed", data_place_str="fetch", raw_name="mapMatchGpsSpeed", module=CARTO_MODULE)


# LanduseModule
DICT_METRICS.add(metric_name="landuse_osm_id", type_=np.float64, target_type_=np.int64)
DICT_METRICS.add(metric_name="landuse_osm_id", data_place_str="fetch", raw_name="landuseOsmId", module=LANDUSE_MODULE)

DICT_METRICS.add(metric_name="landuse_osm_type", type_=str)
DICT_METRICS.add(metric_name="landuse_osm_type", data_place_str="fetch", raw_name="landuseOsmType", module=LANDUSE_MODULE)

DICT_METRICS.add(metric_name="map_landuse", type_=str)
DICT_METRICS.add(metric_name="map_landuse", data_place_str="druid", raw_name="map_landuse")
DICT_METRICS.add(metric_name="map_landuse", data_place_str="fetch", raw_name="landuseType", module=LANDUSE_MODULE)


# ElevationModule
DICT_METRICS.add(metric_name="slope", type_=np.float64)
DICT_METRICS.add(metric_name="slope", data_place_str="fetch", raw_name="slope", module=ELEVATION_MODULE)

DICT_METRICS.add(metric_name="slope_category", type_=str)
DICT_METRICS.add(metric_name="slope_category", data_place_str="fetch", raw_name="slope.category", module=ELEVATION_MODULE)

DICT_METRICS.add(metric_name="altitude", type_=np.float64)
DICT_METRICS.add(metric_name="altitude", data_place_str="fetch", raw_name="altitude", module=ELEVATION_MODULE)

DICT_METRICS.add(metric_name="map_route_slope", type_=np.float64)
DICT_METRICS.add(metric_name="map_route_slope", data_place_str="fetch", raw_name="map.route.slope", module=ELEVATION_MODULE)


# GeoSpatialModule
DICT_METRICS.add(metric_name="delta_time", type_=np.float64)
DICT_METRICS.add(metric_name="delta_time", data_place_str="fetch", raw_name="deltaTime", module=GEO_SPATIAL_MODULE)

DICT_METRICS.add(metric_name="delta_distance", type_=np.float64)
DICT_METRICS.add(metric_name="delta_distance", data_place_str="fetch", raw_name="deltaDistance", module=GEO_SPATIAL_MODULE)


# GpsRawModule
DICT_METRICS.add(metric_name="base_gps_duration_sum", type_=np.float64)
DICT_METRICS.add(metric_name="base_gps_duration_sum", data_place_str="druid", raw_name="base_gps_duration_sum")
DICT_METRICS.add(metric_name="base_gps_duration_sum", data_place_str="fetch", raw_name="sumTime", module=GPS_RAW_MODULE)

DICT_METRICS.add(metric_name="base_gps_distance_sum", type_=np.float64)
DICT_METRICS.add(metric_name="base_gps_distance_sum", data_place_str="druid", raw_name="base_gps_distance_sum")
DICT_METRICS.add(metric_name="base_gps_distance_sum", data_place_str="fetch", raw_name="sumMetre", module=GPS_RAW_MODULE)


# Druid
DICT_METRICS.add(metric_name="raw_sensor_odometer", type_=str)
DICT_METRICS.add(metric_name="raw_sensor_odometer", data_place_str="druid", raw_name="raw_sensor_odometerv")

DICT_METRICS.add(metric_name="recurrent_trip_id", type_=str)
DICT_METRICS.add(metric_name="recurrent_trip_id", data_place_str="druid", raw_name="recurrent_trip_id")

DICT_METRICS.add(metric_name="score_map_route_distance_exactness", type_=np.float64)
DICT_METRICS.add(metric_name="score_map_route_distance_exactness", data_place_str="druid", raw_name="score_map_route_distance_exactness")

DICT_METRICS.add(metric_name="score_map_route_distance_precision", type_=np.float64)
DICT_METRICS.add(metric_name="score_map_route_distance_precision", data_place_str="druid", raw_name="score_map_route_distance_precision")

DICT_METRICS.add(metric_name="score_map_route_path_exactness", type_=np.float64)
DICT_METRICS.add(metric_name="score_map_route_path_exactness", data_place_str="druid", raw_name="score_map_route_path_exactness")

DICT_METRICS.add(metric_name="score_map_route_path_precision", type_=np.float64)
DICT_METRICS.add(metric_name="score_map_route_path_precision", data_place_str="druid", raw_name="score_map_route_path_precision")

DICT_METRICS.add(metric_name="score_raw_distance_exactness", type_=np.float64)
DICT_METRICS.add(metric_name="score_raw_distance_exactness", data_place_str="druid", raw_name="score_raw_distance_exactness")

DICT_METRICS.add(metric_name="score_raw_distance_precision", type_=np.float64)
DICT_METRICS.add(metric_name="score_raw_distance_precision", data_place_str="druid", raw_name="score_raw_distance_precision")

DICT_METRICS.add(metric_name="score_raw_path_exactness", type_=np.float64)
DICT_METRICS.add(metric_name="score_raw_path_exactness", data_place_str="druid", raw_name="score_raw_path_exactness")

DICT_METRICS.add(metric_name="score_raw_path_precision", type_=np.float64)
DICT_METRICS.add(metric_name="score_raw_path_precision", data_place_str="druid", raw_name="score_raw_path_precision")

DICT_METRICS.add(metric_name="raw_gps_accuracy", type_=np.float64)
DICT_METRICS.add(metric_name="raw_gps_accuracy", data_place_str="druid", raw_name="raw_gps_accuracy")

DICT_METRICS.add(metric_name="raw_gps_coordinates", type_=str)
DICT_METRICS.add(metric_name="raw_gps_coordinates", data_place_str="druid", raw_name="raw_gps_coordinates")

DICT_METRICS.add(metric_name="map_road_bridge", type_=bool)
DICT_METRICS.add(metric_name="map_road_bridge", data_place_str="druid", raw_name="map_road_bridge")

DICT_METRICS.add(metric_name="map_road_roundabout", type_=bool)
DICT_METRICS.add(metric_name="map_road_roundabout", data_place_str="druid", raw_name="map_road_roundabout")

DICT_METRICS.add(metric_name="map_road_tunnel", type_=bool)
DICT_METRICS.add(metric_name="map_road_tunnel", data_place_str="druid", raw_name="map_road_tunnel")

DICT_METRICS.add(metric_name="map_road_type", type_=str)
DICT_METRICS.add(metric_name="map_road_type", data_place_str="druid", raw_name="map_road_type")

DICT_METRICS.add(metric_name="map_gps_coordinates", type_=str)
DICT_METRICS.add(metric_name="map_gps_coordinates", data_place_str="druid", raw_name="map_gps_coordinates")


DICT_METRICS.add(metric_name="map_road_speed_limit", type_=np.float64)
DICT_METRICS.add(metric_name="map_road_speed_limit", data_place_str="druid", raw_name="map_road_speed_limit")

DICT_METRICS.add(metric_name="map_road_density", type_=np.int64)
DICT_METRICS.add(metric_name="map_road_density", data_place_str="druid", raw_name="map_road_density")


DICT_METRICS.add(metric_name="map_elevation", type_=str)
DICT_METRICS.add(metric_name="map_elevation", data_place_str="druid", raw_name="map_elevation")

DICT_METRICS.add(metric_name="daycycle_heading", type_=np.int64)
DICT_METRICS.add(metric_name="daycycle_heading", data_place_str="druid", raw_name="daycycle_heading")


# Liste de l'ensemble des métriques
ALL_METRICS = list(DICT_METRICS.dict_metrics_names.keys())

# Listes métriques concernant véhicules et trajets
LIST_METRICS_VEHICLE = ["id", "device_name", "vehicle_id", "trip_distance"]
LIST_METRICS_VEHICLE_OUTPUT = ["id", "device_name", "vehicle_id", "distance"]
LIST_METRICS_TRIP = ["trip_id", "date_time", "id", "device_name",
                     "lat", "lng", "trip_distance", "trip_duration"]
LIST_METRICS_TRIP_OUTPUT = ["trip_id", "date_time", "id", "device_name",
                            "depart", "arrivee", "trip_distance", "trip_duration"]

# Paramètres datetime
DILIVIA_DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DILIVIA_START_DATE_TIME = datetime.strptime("1970-01-01T00:00:00Z", DILIVIA_DATE_TIME_FORMAT)
