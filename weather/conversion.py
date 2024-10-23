def kelvin_to_celsius(kelvin):

    """
    Convert a temperature from Kelvin to Celsius.

    Parameters
    ----------
    kelvin : float
        Temperature in Kelvin

    Returns
    -------
    float
        Temperature in Celsius, rounded to two decimal places
    """
    celsius = kelvin - 273.15
    return round(celsius, 2)

