import click
import requests
import httpx
import logging
import json
import kubernetes

## These two lines enable debugging at httplib level (requests->urllib3->http.client)
## You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
## The only thing missing will be the response.body which is not logged.
#try:
#    import http.client as http_client
#except ImportError:
#    # Python 2
#    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1
#
## You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True


@click.version_option("0.0.1", prog_name="OpenShift Lightspeed CLI")

@click.option('--endpoint', default='', help='URL of OpenShift Lightspeed API server')

# uses the current kubeconfig default token by default, but --token will override
@click.option('--token', default='', help='Authorization token')

@click.command("query")
@click.argument('user_query')
def query(endpoint, token, user_query):

    # default OLS query endpoint path
    DEFAULT_QUERY_PATH='/v1/query'
    url = endpoint + DEFAULT_QUERY_PATH

    click.echo('User query: ' + user_query)
    click.echo('URL: ' + url)

    query_obj = {'conversation_id': '', 'query': user_query}

    if (token != ''):
        auth_obj = {'Authorization': 'Bearer ' + token}
    else:
        auth_obj = kubernetes.config.kube_config.new_client_from_config().configuration.api_key

    #resp = requests.post(url, headers = auth_obj, json = query_obj, verify=False, timeout=30)
    #resp_dict = resp.json()
    #print(resp_dict['response'])
    #click.echo(resp_dict['response'])

    r = httpx.post(url, headers=auth_obj, json=query_obj, verify=False, timeout=30)

    #click.echo("===== debug =====")
    #click.echo(r.text)
    #click.echo("===== debug =====")
    click.echo(json.loads(r.text)['response'])

if __name__ == "__main__":
    query()