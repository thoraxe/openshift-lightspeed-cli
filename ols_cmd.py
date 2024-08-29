import argparse
import cmd2
import httpx
import json
import kubernetes

class OLSShell(cmd2.Cmd):
    """OpenShift Lightspeed Shell"""

    def __init__(self):
        # ignore the command line arguments because we want to use argparse for them
        super().__init__(allow_cli_args=False)

    def do_query(self, line):
        # default OLS query endpoint path
        DEFAULT_QUERY_PATH='/v1/query'

        # construct the URL to hit
        url = self.endpoint + DEFAULT_QUERY_PATH

        # construct the query object
        # TODO: command for getting a new conversation
        query_obj = {'conversation_id': '', 'query': line}

        # use the default kubeconfig token or whatever is specifed from the user via args
        if (self.token != ''):
            auth_obj = {'Authorization': 'Bearer ' + self.token}
        else:
            auth_obj = kubernetes.config.kube_config.new_client_from_config().configuration.api_key

        r = httpx.post(url, headers=auth_obj, json=query_obj, verify=False, timeout=30)

        # output the response from OLS
        # TODO: implement a conversation cache
        print(r)
        print ('===')
        print(json.loads(r.text)['response'])

    def help_query(self):
        print('\n'.join(['query [question]', 'Query is used to ask OpenShift Lightspeed a [question]',
                         'Example: query How do I configure a horizontal pod autoscaler?']))

    def do_EOF(self, line):
        return True

    def do_exit(self, line):
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenShift Lightspeed TUI')

    parser.add_argument('endpoint', help='The URL of your OpenShift Lightspeed endpoint')
    parser.add_argument('-t', '--token', default='', help='uses the current kubeconfig default token by default, but --token will override')
    args = parser.parse_args()

    import sys
    c = OLSShell()
    c.endpoint = args.endpoint
    c.token = args.token
    c.prompt = "OLS: "

    print("Welcome to OpenShift Lightspeed")
    print("Type 'help' to get a list of commands")
    print("Use 'query [question]' to ask OpenShift Lightspeed something")
    sys.exit(c.cmdloop())