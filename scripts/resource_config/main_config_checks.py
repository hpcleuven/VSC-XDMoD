import copy
import json
import os
from xdmod_resource_manager import Resource, Resource_Spec


def check_resource_configs(vsc_site):
    root="VSC-XDMoD/resource_files/"
    local_resources_path = root + "resources.json"
    local_resource_specs_path = root + "resource_specs.json"
    remote_resources_path = root + vsc_site + "/resources.json"
    remote_resource_specs_path = root + vsc_site + "/resource_specs.json"

    with open(local_resources_path, "r") as f1, open(
        local_resource_specs_path, "r"
    ) as f2, open(remote_resources_path, "r") as f3, open(
        remote_resource_specs_path, "r"
    ) as f4:
        local_resources = json.load(f1)
        local_resource_specs = json.load(f2)
        remote_resources = json.load(f3)
        remote_resource_specs = json.load(f4)

    # sync resources.json
    
    print(">>> Sanity Checking Resources <<<")
    local_resources = generate_resources(local_resources)
    remote_resources = generate_resources(remote_resources)
    
    updated_local_resources = copy.deepcopy(local_resources)
    resources = [res.resource() for res in local_resources]
    for ref in remote_resources:
        if ref.resource() in resources:
            for i in range(len(local_resources)):
                if local_resources[i].resource() == ref.resource():
                    updated_local_resources[i] = ref
        else:
            updated_local_resources.append(ref)

    print(">>> Sanity Checking Resource_specs <<<")
    local_resource_specs = generate_resource_specs(
        local_resource_specs, local_resources
    )
    remote_resource_specs = generate_resource_specs(
        remote_resource_specs, updated_local_resources
    )
    print("\nstarting resource_spec sync\n")
    updated_local_resource_specs = copy.deepcopy(local_resource_specs)
    resources = [spec.resource() for spec in local_resource_specs]
    for ref in remote_resource_specs:
        if ref.resource() in resources:
            for i in range(len(local_resource_specs)):
                if local_resource_specs[i].id == ref.id:
                    updated_local_resource_specs[i] = ref
                    print(f"Updated {local_resource_specs[i].id}")
        else:
            updated_local_resource_specs.append(ref)
            print(f"Appending new resource_spec {ref}")


def generate_resources(resources):
    return [Resource(resource) for resource in resources]


def generate_resource_specs(resource_specs, resources):
    resource_specs = [
        Resource_Spec(resource_spec, resources) for resource_spec in resource_specs
    ]
    checked = {}
    for resource_spec in resource_specs:
        if resource_spec.resource() in checked.keys():
            for checked_resource_spec in checked[resource_spec.resource()]:
                if date_overlap(resource_spec, checked_resource_spec):
                    raise Exception(
                        f"overlapping resource_spec dates for {resource_spec.resource()}"
                    )
            checked[resource_spec.resource()].append(resource_spec)
        else:
            checked[resource_spec.resource()] = [resource_spec]
    return resource_specs


def date_overlap(s1, s2):
    return (
        s1.start_date() <= s2.start_date() <= s1.end_date()
        or s2.start_date() <= s1.start_date() <= s2.end_date()
    )


if __name__ == "__main__":
    
    vsc_sites = [f.name for f in os.scandir("VSC-XDMoD/resource_files/") if f.is_dir()] 
    for vsc_site in vsc_sites:
        print(f">>> {vsc_site} <<<")
        check_resource_configs(vsc_site)
