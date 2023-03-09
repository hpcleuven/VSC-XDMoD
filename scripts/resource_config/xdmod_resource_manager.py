import datetime as dt
import json
import pytz

import config_checks


class Resource:
    def __init__(self, creation_dict):
        self._dict = config_checks.is_valid_resource(creation_dict)
        self._resource = self._dict["resource"]
        self._name = self._dict["name"]
        self._resource_type = self._dict["resource_type"]

        if "description" in self._dict.keys():
            self._description = self._dict["description"]
        else:
            self._description = "No Description Given"

        if "pi_column" in self._dict.keys():
            self._pi_column = self._dict["pi_column"]
        else:
            self._pi_column = ""

        if "shared_jobs" in self._dict.keys():
            self._shared_jobs = self._dict["shared_jobs"]
        else:
            self._shared_jobs = False

        if "timezone" in self._dict.keys():
            self._timezone = self._dict["timezone"]
        else:
            self._timezone = "Europe/Brussels"

    def resource(self):
        return self._resource

    def name(self):
        return self._name

    def resource_type(self):
        return self._resource_type

    def description(self):
        return self._description

    def pi_column(self):
        return self._pi_column

    def get(self):
        return self._dict

    def __repr__(self):
        return json.dumps(self._dict, indent=4)

    def __str__(self):
        return json.dumps(self._dict, indent=4)


class Resource_Spec:
    def __init__(self, creation_dict, resources):
        self._dict = config_checks.is_valid_resource_spec(creation_dict, resources)
        self._resource = self._dict["resource"]
        self._nodes = self._dict["nodes"]
        self._processors = self._dict["processors"]
        self._ppn = self._dict["ppn"]
        if "start_date" in self._dict.keys():
            self._start_date = dt.date.fromisoformat(self._dict["start_date"])
        else:
            self._start_date = dt.date.fromisoformat("2000-01-01")
        if "end_date" in self._dict.keys():
            self._end_date = dt.date.fromisoformat(self._dict["end_date"])
        else:
            self._end_date = dt.date.fromisoformat("2100-01-01")
        if "percent_allocated" in self._dict.keys():
            self._percent_allocated = self._dict["percent_allocated"]
        self.id = str(
            self._resource + "_" + str(self._start_date) + "_" + str(self._end_date)
        )

    def resource(self):
        return self._resource

    def nodes(self):
        return self._nodes

    def processors(self):
        return self._processors

    def ppn(self):
        return self._ppn

    def start_date(self):
        return self._start_date

    def end_date(self):
        return self._end_date

    def percent_allocated(self):
        return self._percent_allocated

    def get(self):
        return self._dict

    def __repr__(self):
        return json.dumps(self._dict, indent=4)

    def __str__(self):
        return json.dumps(self._dict, indent=4)

