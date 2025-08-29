# TTIs

## How to start the remote monitoring?

- First let's ssh to acd-daq05 as acdcs user:

```bash
ssh -J acdcs@acd-gw06.fnal.gov acdcs@acd-daq05.fnal.gov
```

Go to /home/acd/acdcs/2x2/SlowControls2x2/TTIs an run:

```bash
./run.sh
```

## How to stop the remote monitoring?
just do:

```bash
podman stop tti-monitoring
```
