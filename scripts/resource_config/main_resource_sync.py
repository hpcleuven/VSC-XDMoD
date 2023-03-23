import copy
import json
import os

from xdmod_resource_manager import Resource, Resource_Spec

def sync_resource_config(vsc_site, resource_files):
    
    local_resources_path = resource_files + "resources.json"
    local_resource_specs_path = resource_files + "resource_specs.json"
    remote_resources_path = resource_files + vsc_site + "/resources.json"
    remote_resource_specs_path = resource_files + vsc_site + "/resource_specs.json"

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
    local_resources = generate_resources(local_resources)
    remote_resources = generate_resources(remote_resources)
    print("\nstarting resource sync\n")
    updated_local_resources = copy.deepcopy(local_resources)
    resources = [res.resource() for res in local_resources]
    for ref in remote_resources:
        if ref.resource() in resources:
            for i in range(len(local_resources)):
                if local_resources[i].resource() == ref.resource():
                    updated_local_resources[i] = ref
                    print(f"Updated {local_resources[i].resource()}")
        else:
            updated_local_resources.append(ref)
            print(f"Appending new resource {ref.resource()}")
            print(ref)

    # sync resource_specs.json
    local_resource_specs = generate_resource_specs(
        local_resource_specs, local_resources
    )
    remote_resource_specs = generate_resource_specs(
        remote_resource_specs, updated_local_resources
    )
    print("\nstarting resource_spec sync\n")
    updated_local_resource_specs = copy.deepcopy(local_resource_specs)
    resource_spec_ids = [spec.id for spec in local_resource_specs]
    for ref in remote_resource_specs:
        if ref.id in resource_spec_ids:
            for i in range(len(local_resource_specs)):
                if local_resource_specs[i].id == ref.id:
                    updated_local_resource_specs[i] = ref
                    print(f"Updated {local_resource_specs[i].id}")
        else:
            updated_local_resource_specs.append(ref)
            print(f"Appending new resource_spec {ref}")

    # overwrite local resources.json and resource_specs.json
    with open(local_resources_path, "w") as o1, open(
        local_resource_specs_path, "w"
    ) as o2:
        print(f"\nwriting to {local_resources_path}\n")
        json.dump(
            [resource.get() for resource in updated_local_resources], o1, indent=4
        )
        print(f"\nwriting to {local_resource_specs_path}\n")
        json.dump(
            [resource_spec.get() for resource_spec in updated_local_resource_specs],
            o2,
            indent=4,
        )


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
    
    resource_files = "./resource_files/"

    vsc_sites = [f.name for f in os.scandir(resource_files) if f.is_dir()] 
    for vsc_site in vsc_sites:
        print(f">>> {vsc_site} <<<")
        sync_resource_config(vsc_site, resource_files)

