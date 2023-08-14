#!/bin/which python3
import math
from math import acos, cos, sin
from typing import Dict, List

takeoff: Dict[int, Dict] = {
    2300: {
        'weight': 2300,
        'ias_at_50': 68,
        'altitude': {
            0: {  # sea level
                'head_wind': {
                    0: {
                        'ground_run': 865,
                        'clear_50': 1525
                    },
                    10: {
                        'ground_run': 615,
                        'clear_50': 1170
                    },
                    20: {
                        'ground_run': 405,
                        'clear_50': 850
                    }
                }
            },
            2500: {
                'head_wind': {
                    0: {
                        'ground_run': 1040,
                        'clear_50': 1910
                    },
                    10: {
                        'ground_run': 750,
                        'clear_50': 1485
                    },
                    20: {
                        'ground_run': 505,
                        'clear_50': 1100
                    }
                }
            },
            5000: {
                'head_wind': {
                    0: {
                        'ground_run': 1255,
                        'clear_50': 2480
                    },
                    10: {
                        'ground_run': 920,
                        'clear_50': 1955
                    },
                    20: {
                        'ground_run': 630,
                        'clear_50': 1480
                    }
                }
            },
            7500: {
                'head_wind': {
                    0: {
                        'ground_run': 1565,
                        'clear_50': 3855
                    },
                    10: {
                        'ground_run': 1160,
                        'clear_50': 3110
                    },
                    20: {
                        'ground_run': 810,
                        'clear_50': 2425
                    }
                }
            }
        }
    },
    2000: {
        'weight': 2000,
        'ias_at_50': 63,
        'altitude': {
            0: {  # sea level
                'head_wind': {
                    0: {
                        'ground_run': 630,
                        'clear_50': 1095
                    },
                    10: {
                        'ground_run': 435,
                        'clear_50': 820
                    },
                    20: {
                        'ground_run': 275,
                        'clear_50': 580
                    }
                }
            },
            2500: {
                'head_wind': {
                    0: {
                        'ground_run': 755,
                        'clear_50': 1325
                    },
                    10: {
                        'ground_run': 530,
                        'clear_50': 1005
                    },
                    20: {
                        'ground_run': 340,
                        'clear_50': 720
                    }
                }
            },
            5000: {
                'head_wind': {
                    0: {
                        'ground_run': 905,
                        'clear_50': 1625
                    },
                    10: {
                        'ground_run': 645,
                        'clear_50': 1250
                    },
                    20: {
                        'ground_run': 425,
                        'clear_50': 910
                    }
                }
            },
            7500: {
                'head_wind': {
                    0: {
                        'ground_run': 1120,
                        'clear_50': 2155
                    },
                    10: {
                        'ground_run': 810,
                        'clear_50': 1685
                    },
                    20: {
                        'ground_run': 595,
                        'clear_50': 1255
                    }
                }
            }
        }
    },
    1700: {
        'weight': 1700,
        'ias_at_50': 58,
        'altitude': {
            0: {  # sea level
                'head_wind': {
                    0: {
                        'ground_run': 435,
                        'clear_50': 780
                    },
                    10: {
                        'ground_run': 290,
                        'clear_50': 570
                    },
                    20: {
                        'ground_run': 175,
                        'clear_50': 385
                    }
                }
            },
            2500: {
                'head_wind': {
                    0: {
                        'ground_run': 520,
                        'clear_50': 920
                    },
                    10: {
                        'ground_run': 355,
                        'clear_50': 680
                    },
                    20: {
                        'ground_run': 215,
                        'clear_50': 470
                    }
                }
            },
            5000: {
                'head_wind': {
                    0: {
                        'ground_run': 625,
                        'clear_50': 1095
                    },
                    10: {
                        'ground_run': 430,
                        'clear_50': 820
                    },
                    20: {
                        'ground_run': 270,
                        'clear_50': 575
                    }
                }
            },
            7500: {
                'head_wind': {
                    0: {
                        'ground_run': 765,
                        'clear_50': 1370
                    },
                    10: {
                        'ground_run': 535,
                        'clear_50': 1040
                    },
                    20: {
                        'ground_run': 345,
                        'clear_50': 745
                    }
                }
            }
        }
    }
}


def calculate_headwind_component(runway: float, wind_speed: float, wind_dir: float) -> float:
    recip: float = 0.0
    if runway < 180:
        recip = runway + 180
    else:
        recip = runway - 180

    recip_wind: float = 0.0
    if wind_dir < 180:
        recip_wind = wind_dir + 180
    else:
        recip_wind = wind_dir - 180

    runway_radians: float = runway * math.pi / 180.0
    wind_radians: float = wind_dir * math.pi / 180.0
    runway_x: float = sin(runway_radians)
    runway_y: float = cos(runway_radians)
    wind_x: float = sin(wind_radians)
    wind_y: float = cos(wind_radians)
    dot_product: float = (runway_x * wind_x) + (runway_y * wind_y)
    theta_radians: float = acos(dot_product)
    theta_degrees: float = round(theta_radians * 180 / math.pi)
    significant_figures: float = 100.0
    parallel_component: float = round(significant_figures * wind_speed * cos(theta_radians)) / significant_figures
    xwind_component: float = round(significant_figures * wind_speed * sin(theta_radians)) / significant_figures

    return parallel_component


def interpolate(value: float, lower_value: float, upper_value: float, lower_bound: float, upper_bound: float):
    if value <= lower_bound:
        return lower_value
    if value >= upper_bound:
        return upper_value

    interpolated: float = lower_value + (((upper_value - lower_value) / (upper_bound - lower_bound)) * (value - lower_bound))
    return interpolated


def interpolate_altitude_data(altitude: int, head_wind: float, altitude_data: Dict[int, Dict]) -> Dict[str, float]:
    available_altitudes: List[int] = sorted(altitude_data.keys())
    lower_altitude_data: Dict[str, Dict] = None
    upper_altitude_data: Dict[str, Dict] = None
    lower_altitude: int = 0
    upper_altitude: int = 0
    result: Dict[str, float] = {}

    for i in range(1, len(available_altitudes)):
        if available_altitudes[i - 1] < altitude < available_altitudes[i]:
            lower_altitude = available_altitudes[i - 1]
            upper_altitude = available_altitudes[i]
            lower_altitude_data = altitude_data[lower_altitude]
            upper_altitude_data = altitude_data[upper_altitude]
            break

    if lower_altitude_data is None and upper_altitude_data is None:
        print('Check the density altitude. We have no performance data to calculate the take off distance')
        return result

    # get the headwind data
    available_wind = sorted(lower_altitude_data['head_wind'].keys())
    lower_lower_wind_data: Dict[str, float] = None
    upper_lower_wind_data: Dict[str, float] = None
    lower_upper_wind_data: Dict[str, float] = None
    upper_upper_wind_data: Dict[str, float] = None

    lower_head_wind: int = 0
    upper_head_wind: int = 0

    if int(head_wind) in available_wind:
        lower_head_wind = int(head_wind)
        upper_head_wind = int(head_wind)
    else:
        for i in range(1, len(available_wind)):
            if available_wind[i - 1] < head_wind < available_wind[i]:
                lower_head_wind = available_wind[i - 1]
                upper_head_wind = available_wind[i]
                break
        if lower_head_wind == upper_head_wind == 0:
            lower_head_wind = available_wind[-1:][0]
            upper_head_wind = lower_head_wind
    lower_lower_wind_data = lower_altitude_data['head_wind'][lower_head_wind]
    upper_lower_wind_data = lower_altitude_data['head_wind'][upper_head_wind]
    lower_upper_wind_data = upper_altitude_data['head_wind'][lower_head_wind]
    upper_upper_wind_data = upper_altitude_data['head_wind'][upper_head_wind]

    interpolated_lower_wind_data: Dict[str, float] = {}
    interpolated_upper_wind_data: Dict[str, float] = {}
    for key in lower_lower_wind_data.keys():
        #  Do lower
        lower_value: float = lower_lower_wind_data[key]
        upper_value: float = upper_lower_wind_data[key]
        value: float = interpolate(head_wind, lower_value, upper_value, lower_head_wind, upper_head_wind)
        interpolated_lower_wind_data[key] = value

        # Do upper
        lower_value = lower_upper_wind_data[key]
        upper_value = upper_upper_wind_data[key]
        value = interpolate(head_wind, lower_value, upper_value, lower_head_wind, upper_head_wind)
        interpolated_upper_wind_data[key] = value

    # interpolate the altitude from the interpolated wind
    for key in interpolated_lower_wind_data.keys():
        lower_value: float = interpolated_lower_wind_data[key]
        upper_value: float = interpolated_upper_wind_data[key]
        value: float = interpolate(altitude, lower_value, upper_value, lower_altitude, upper_altitude)
        result[key] = value

    return result


if __name__ == '__main__':
    runway: float = float(input('What runway are you taking off from? '))
    wind_speed: float = float(input('What is the wind speed (kts)? '))
    wind_dir: float = float(input('What is the wind direction? '))
    headwind_speed: float = calculate_headwind_component(runway * 10.0, wind_speed, wind_dir)
    density_altitude: float = float(input('What is the density altitude (ft)? '))
    temperature: float = float(input('What is the temperature (F)? '))
    weight: int = int(input('What is your take-off weight (lb)? '))
    dry_grass: str = input('Is the runway surface dry grass (N/y)? ')

    # find the upper and lower bounds for the interpolation
    available_weights = sorted(takeoff.keys())
    lower_weight_data = None
    upper_weight_data = None
    lower_weight = 0
    upper_weight = 0

    for i in range(1, len(available_weights)):
        if available_weights[i - 1] < weight <= available_weights[i]:
            lower_weight = available_weights[i - 1]
            upper_weight = available_weights[i]
            lower_weight_data = takeoff[lower_weight]
            upper_weight_data = takeoff[upper_weight]
            break

    if lower_weight_data is None and upper_weight_data is None:
        print('No weight data found for flight. Please check you\'re not overweight')
        exit(1)

    lower_interpolation: Dict[str, float] = interpolate_altitude_data(int(density_altitude), headwind_speed, lower_weight_data['altitude'])
    upper_interpolation: Dict[str, float] = interpolate_altitude_data(int(density_altitude), headwind_speed, upper_weight_data['altitude'])
    interpolated_result: Dict[str, float] = {}

    for key in lower_interpolation.keys():
        lower_value: float = lower_interpolation[key]
        upper_value: float = upper_interpolation[key]
        value = interpolate(weight, lower_value, upper_value, lower_weight, upper_weight)
        interpolated_result[key] = value

    # apply temperature above standard correction
    if temperature > 59.0:
        multiplicative_factor: float = (temperature - 59) / 25
        for key in interpolated_result.keys():
            value: float = interpolated_result[key]
            ten_percent: float = value * 0.1
            value = value + (ten_percent * multiplicative_factor)
            interpolated_result[key] = value

    # apply the dry grass runway correction
    dry_grass = dry_grass.lower()
    # apply 7% of the 50ft to both ground run and clear 50
    if dry_grass.startswith('y'):
        correction: float = interpolated_result['clear_50'] * 0.07
        for key in interpolated_result.keys():
            value: float = interpolated_result[key]
            value = value + correction
            interpolated_result[key] = value

    print('Headwind Component: %0.1f kts' % headwind_speed)
    print('Ground Roll: %0.0f ft' % interpolated_result['ground_run'])
    print('Distance to clear 50ft: %0.0f ft' % interpolated_result['clear_50'])

