"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

import math

def is_nan(value):
    return math.isnan(float(value))

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # TODO: What additional auxiliary data structures will be useful?
        desg_mapping = {neo.designation: neo for neo in neos}
        for approach in approaches:
            approach.neo = desg_mapping[approach._designation]
            approach.neo.approaches.append(approach)
        # TODO: Link together the NEOs and their close approaches.

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        # TODO: Fetch an NEO by its primary designation.
        
        return next((item for item in self._neos if item.designation == designation), None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # TODO: Fetch an NEO by its name.
        return next((item for item in self._neos if item.name == name), None)

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # TODO: Generate `CloseApproach` objects that match all of the filters.

        
        for approach in self._approaches:
            if filters["date"] != None  and approach.str_day != filters["date"].strftime('%Y-%m-%d'):
                # print(filters["date"])
                # print (approach.str_day)
                # print (filters["date"])
                # print (filters["date"] == "1969-07-29")
                continue
            if filters["start_date"] != None and approach.str_day < filters["start_date"].strftime('%Y-%m-%d'):
                continue
            if filters["end_date"] != None and approach.str_day > filters["end_date"].strftime('%Y-%m-%d'):
                continue
            if filters["distance_min"] != None and (approach.distance < filters["distance_min"] or is_nan (approach.distance)):
                continue
            if filters["distance_max"] != None and (approach.distance > filters["distance_max"]  or is_nan (approach.distance)):
                continue
            if filters["velocity_min"] != None and (approach.velocity < filters["velocity_min"]  or is_nan(approach.velocity)):
                continue
            if filters["velocity_max"] != None and (approach.velocity > filters["velocity_max"]  or is_nan(approach.velocity)):
                continue
            if filters["diameter_min"] != None  and (approach.neo.diameter < filters["diameter_min"]  or is_nan(approach.neo.diameter)):
                continue
            if filters["diameter_max"] != None  and (approach.neo.diameter > filters["diameter_max"] or is_nan(approach.neo.diameter)):
                continue
            if filters["hazardous"] != None  and approach.neo.hazardous != filters["hazardous"]:
                continue
            yield approach
