"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json

import math

def is_nan(value):
    return math.isnan(float(value))


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ['datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous']
    f = open(filename, 'w')
    writer = csv.writer(f)
    # writer.writerow(",".join(fieldnames))
    writer.writerow(fieldnames)
    for result in results:
        row = [result.str_time, result.distance, result.velocity, result._designation, result.neo.name, result.neo.diameter, result.neo.hazardous]
        # row = ["" for x in row if x == "None"]
        # row = ["" for x in row if x == None]
        row = [str(x) for x in row]
        # print(row)
        # row = [1,2,3,4,5,6,7]
        writer.writerow(row)
        # row
        # row.append(result.str_time)
        # row.append(str(result.distance))
        # row.append(str(result.velocity))
        # row.append(result._designation)
        # if result.neo.name == None:
        #     row.append("")
        # else:
        #     row.append(result.neo.name)
        # row.append(str(result.neo.diameter))
        # row.append(str(result.neo.hazardous))
        # writer.writerow(",".join(row))
        # writer.writerow(result.serialize().items())
    f.close()
    # TODO: Write the results to a CSV file, following the specification in the instructions.


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # TODO: Write the results to a JSON file, following the specification in the instructions.
    data = []
    with open(filename, "w") as f:
        for result in results:
            dictionary = {
                "datetime_utc": result.str_time,
                "distance_au": result.distance,
                "velocity_km_s": result.velocity,
                "neo": ({
                    "designation": result.neo.designation,
                    "name": result.neo.name if result.neo.name is not None else "",
                    "diameter_km": result.distance,
                    "potentially_hazardous": (result.neo.hazardous),
                }),
            }
            data.append(dictionary)
        json.dump(data, f, indent="\t")
        f.close()
