#XDMoD Future Plans

In June 2022 we agreed that it would be beneficial to have a centralized place from where we can access the job & storage data from across all vsc sites.
To manage the data and make it available to both vsc staff and users we will use XDMoD. This XDMoD service will be hosted at the KU Leuven site.

## File Structure for Shared NFS volumes

The UAntwerpen, UGent and VUB VSC sites will create a shared NSF volume.
The KU Leuven VSC site will then mount these shared volumes on their site.
These shared volumes will take on the following file structure.

[institute]
|_[cloud_logs]
|_[storage_logs]
|_[job_logs]
  |_[resource_1]
  | |_[pbs]
  | |_[slurm]
  |_[resource_2]
  |_[...]

To avoid problems of data appearing in the directory while the xdmod shredder and ingestor are running, 
the shredder and ingestor will be ran on local coppies of these shared volumes.
Every day, prior to shredding the data, new logs files will be coppied from the shared volume to the local volume. 

If no new logs were found, or the mount is not working at time of copying, the xdmod managers will be notified via email.

## Resources Maintenance

In order to keep the resources known to XDMoD up-to-date and the production resource files sane, a common git repository will be used to facilitate the maintenance of 
the resource files ("resources.json" and "resource_specs.json"). This way, each VSC site can manage their resources. These files will be parsed (periodically)
and checked for: 
1) new resource definitions added
2) updates to existing resources 
     e.g.
     * added end-date for retired cluster
     * ...
3) overall correctness of the json file and sanity.
     e.g. 
     * a resource match must exist between resources.json and resource_specs.json
     * number of processors should always equal number of nodes * number of processors per node as defined in resource_specs.json
     * if a resource has an end-date, start-date < end-date.
     * ...
4) ...

If all checks pass, the current resource files used by the production instance of XDMoD will be updated programatically.

## Resource Types

Resource Types in XDMoD are used to easily filter resources by certain characteristics. A typical example would be: GPU, Bigmem etc. 
We will repurpose the Resource Type to filter resources by vsc site instead. This is currently implemented.

## Hierarchy

When implementing a hierarchy, there are some things that require extra attention. 
The hierarchy and the mapping are bound to change. Every time a new account/project is created,
it should be added to the mapping. While a hierarchy is less suceptible to change than the mapping,
even the hierarchy will evolve over time. Therefore, every few months the hierarchy should be updated. 
The older hierarchies and mappings are also not disposable as they need to be reingest if a database reset were to occure.

In june we did not reach a consensus about how a common hierarchy should be implemented. We did agree that a 3 level hierarchy would be difficult 
to maintain. For creating and maintaining a common hierarchy we can use the same method as described above for managing the resource files. 

