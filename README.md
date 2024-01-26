# GPU Resource Monitor

The ISE group has 3 servers with GPU facilities which we use for teaching and research.
There are talks about moving to a hosted shared facility, and to estimate capacity requirements we woud like to monitor current usage.
To do this we would like to start by logging the usage of the GPU instances on the servers to a sqlite database.

We would like to make a tool that periodically reads the output of the nvidia-smi tool and record it in a log. Ideally the pid output of the tool should also be used to then lookup the info on that running process (see: https://github.com/giampaolo/psutil ) and record more information that could be useful.

For example:
```bash
nvidia-smi  --query-compute-apps=pid,used_memory --format=csv
```

pid, used_gpu_memory [MiB]

/usr/local/bin/python -m ipykernel_launcher -f /root/.local/share/jupyter/runtime/kernel-17748908-32ab-4310-9149-6f75784a799d.json, 1711 MiB


Open Questions
What frequency to do the queries?
Which fields qo query (depends on what is available)
What does the log database schema look like? (bonuspoints for doing it in RDF… ;-)
Which format to use for queries from nvidia-smi tool: csv or xml ?
