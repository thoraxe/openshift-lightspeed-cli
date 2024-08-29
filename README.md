# OpenShift Lightspeed CLI
This is a simple Python implementation of a cmd2 shell for conversing with
OpenShift Lightspeed.

## Requirements
* Python 3.11
* The dependencies in `requirements.txt`

## Usage
`ols_cmd.py` takes one command-line argument, which should be the URL of your 
OpenShift Lightspeed endpoint. You will need to expose the OpenShift Lightspeed
API server service via a `Route` in your OpenShift cluster.

`ols_cmd.py` optionally accepts a token via a command-line argument in the form
of `sha-...` which you can determine via `oc whoami -t`. If the argument is not
supplied, `ols_cmd.py` will use whatever the current default token is in your
system `.kubeconfig` via the Python `kubernetes` library.

Use the `query [question]` command inside the shell to interact with OpenShift
Lightspeed.

When you want to start a new conversation with OpenShift Lightspeed, use the
`clear` command inside the shell.

## Future
* Attachment support