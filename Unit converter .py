def length_converter(value, from_unit, to_unit):
    length_units = {
        'meters': 1.0,
        'kilometers': 1000.0,
        'feet': 0.3048,
        'inches': 0.0254,
        'miles': 1609.34
    }
    return value * (length_units[to_unit] / length_units[from_unit])

def weight_converter(value, from_unit, to_unit):
    weight_units = {
        'grams': 1.0,
        'kilograms': 1000.0,
        'pounds': 453.592,
        'ounces': 28.3495
    }
    return value * (weight_units[to_unit] / weight_units[from_unit])

def temperature_converter(value, from_unit, to_unit):
    if from_unit == 'celsius' and to_unit == 'fahrenheit':
        return (value * 9/5) + 32
    elif from_unit == 'fahrenheit' and to_unit == 'celsius':
        return (value - 32) * 5/9
    elif from_unit == 'celsius' and to_unit == 'kelvin':
        return value + 273.15
    elif from_unit == 'kelvin' and to_unit == 'celsius':
        return value - 273.15
    elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
        return (value - 32) * 5/9 + 273.15
    elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
        return (value - 273.15) * 9/5 + 32
    else:
        return value

if __name__ == "__main__":
    print("Length conversion: 10 meters to feet =", length_converter(10, 'meters', 'feet'))
    print("Weight conversion: 5 kilograms to pounds =", weight_converter(5, 'kilograms', 'pounds'))
    print("Temperature conversion: 100 Celsius to Fahrenheit =", temperature_converter(100, 'celsius', 'fahrenheit'))
