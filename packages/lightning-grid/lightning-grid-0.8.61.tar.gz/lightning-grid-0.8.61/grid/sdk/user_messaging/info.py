from typing import Optional, List

from grid.sdk.datastores import DATASTORE_FSX_THROUGHPUT_ALIASES


def datastore_currently_creating_datastore(
    name: str, version: str, cluster: str, all_clusters: Optional[List[str]] = None
) -> str:
    res = f"We are creating {name} datastore (version {version}) on cluster {cluster}"
    if all_clusters is not None:
        res += f" not on these clusters: {all_clusters}."
    else:
        res += "."
    res += " Please use `grid datastore` to check the status."
    return res


def datastore_uploaded_successfully(name: str, version: str, cluster: str) -> str:
    return (
        f"Completed uploading {name} datastore (version {version}) on "
        f"cluster {cluster}. Your datastore will be available for use shortly."
    )


def datastore_fsx_total_throughput(throughput_alias: str, capacity_gib: int) -> str:
    return (
        f"You have created a high-performance datastore with throughput setting [{throughput_alias}] which "
        f"corresponds to {DATASTORE_FSX_THROUGHPUT_ALIASES[throughput_alias]}MB/s/TiB of storage. This means "
        f"that with your selected capacity of {capacity_gib}GiB, the total throughput available for the datastore "
        f"will be {DATASTORE_FSX_THROUGHPUT_ALIASES[throughput_alias] * capacity_gib / 1000}MB/s. Note that "
        f"high-performance datastores may burst over their nominal throughput rating."
    )
