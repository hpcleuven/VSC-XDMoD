import datetime as dt
import json

resources_path = "./resource_files/resources.json"
resource_types_path = "./resource_files/resource_types.json"


def is_valid_resource(creation_dict):
    all_attributes = [
        "resource",
        "name",
        "description",
        "resource_type",
        "pi_column",
        "shared_jobs",
        "timezone",
    ]
    mandatory_attributes = [
        "resource",
        "name",
        "resource_type",
    ]
    
    for key in creation_dict.keys():
        if key not in all_attributes:
            raise Exception(f'unexpected attribute "{key}"')
    
    for attribute in mandatory_attributes:
        if attribute not in creation_dict.keys():
            raise Exception(f'mandatory attribute "{attribute}" missing')
    
    if type(creation_dict["resource"]) != str:
        raise TypeError('"resource" must be of type str.')
    
    if type(creation_dict["name"]) != str:
        raise TypeError('"name" must be of type str.')
    
    if type(creation_dict["resource_type"]) != str:
        raise TypeError('"resource_type" must be of type str.')
    
    with open(resource_types_path, "r") as f:
        resource_types = json.load(f)
        if creation_dict["resource_type"] not in resource_types["resource_types"]:
            raise Exception(
                f'{creation_dict["resource_type"]} not found in {resource_types_path}'
            )

    if "description" in creation_dict.keys():
        if type(creation_dict["description"]) != str:
            raise TypeError('"description" must be of type str.')
    
    if "pi_column" in creation_dict.keys():
        if type(creation_dict["pi_column"]) != str:
            raise TypeError('"pi_column" must be of type str')
    
    if "shared_jobs" in creation_dict.keys():
        if type(creation_dict["shared_jobs"]) != bool:
            raise TypeError('"shared_jobs" must be of type bool')
    
    if "timezone" in creation_dict.keys():
        if type(creation_dict["timezone"]) != str:
            raise TypeError('"timezone" must be of type str')
        if creation_dict["timezone"] not in zoneinfo.available_timezones():
            raise Exception(
                f'Could not recognize {creation_dict["timezone"]} as a valid timezone'
            )
    
    return creation_dict


def is_valid_resource_spec(creation_dict, resources):
    all_attributes = [
        "resource",
        "nodes",
        "processors",
        "ppn",
        "start_date",
        "end_date",
        "percent_allocated",
    ]
    mandatory_attributes = [
        "resource",
        "nodes",
        "processors",
        "ppn",
        "start_date",
    ]
    
    if type(creation_dict) != dict:
        raise TypeError('"creation_dict" must be of type dictionary')
    
    if type(creation_dict["resource"]) != str:
        raise TypeError('"resource" must be of type str.')
    
    if creation_dict["resource"] not in [res.resource() for res in resources]:
        raise Exception(f'{creation_dict["resource"]} not found in {resources_path}')
    
    for key in creation_dict.keys():
        if key not in all_attributes:
            raise Exception(f'unexpected attribute "{key}"')
    
    for attribute in mandatory_attributes:
        if attribute not in creation_dict.keys():
            raise Exception(f'mandatory attribute "{attribute}" missing')
    
    if type(creation_dict["resource"]) != str:
        raise Exception('resource {resource_spec["resource"]} not str')
    else:
        resource = creation_dict["resource"]
    
    if type(creation_dict["nodes"]) != int:
        raise Exception(
            f'type error for {resource}: nodes {resource_spec["nodes"]} not int'
        )
    else:
        nodes = creation_dict["nodes"]
    
    if type(creation_dict["ppn"]) != int:
        raise Exception(
            f'type error for {resource}: ppn {resource_spec["ppn"]} not int'
        )
    else:
        ppn = creation_dict["ppn"]
    
    if type(creation_dict["processors"]) != int:
        raise Exception(
            f'type error for {resource}: processors {resource_spec["processors"]} not int'
        )
    else:
        procs = creation_dict["processors"]
    
    start = creation_dict["start_date"]
    if not check_date(start):
        raise Exception(f"date error for {resource}: start_date not yyyy-mm-dd")
    start = dt.date.fromisoformat(start)
    
    if "end_date" in creation_dict.keys():
        end = creation_dict["end_date"]
        if not check_date(end):
            raise Exception(f"date error for {resource}: end_date not yyyy-mm-dd")
        end = dt.date.fromisoformat(end)
        if start > end:
            raise Exception(f"sanity error for {resource}: end_date < start_date")
        
    
    if "percent_allocated" in creation_dict.keys():
        percent_allocated = creation_dict["percent_allocated"]
        if type(percent_allocated) != int:
            raise TypeError('"percent_allocated" must be of type int')
        if percent_allocated < 0 or percent_allocated > 100:
            raise Exception(
                f"{percent_allocated} is not a valid value for percent_allocated.\nMust be an integer between 0 and 100"
            )
    
    if nodes > procs:
        raise Exception(f"{resource}: nodes > processors")
    
    if nodes * ppn != procs:
        raise Exception(f"{resource}: nodes * ppn != procs")

    return creation_dict


def check_date(date_string):
    try:
        #dt.datetime.strptime(date_string, "%Y-%m-%d") # python 3.6 compatible
        dt.date.fromisoformat(date_string) # only python 3.8+
    except:
        return False
    return True
