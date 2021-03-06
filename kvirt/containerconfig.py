#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kvirt containerconfig class
"""

from kvirt.common import pprint
import os


class Kcontainerconfig():
    """

    """
    def __init__(self, config, client=None, namespace=None):
            k8s = False
            default_k8s = False
            client = config.client if client is None else client
            if client == 'local':
                currentconfig = {'host': '127.0.0.1'}
            elif client == 'kubernetes':
                currentconfig = {}
                default_k8s = True
            else:
                currentconfig = config.ini[client]
                if 'containerclient' in currentconfig:
                    if currentconfig['containerclient'] not in config.ini:
                        pprint("No section found for containerclient %s. Leaving" % currentconfig['containerclient'],
                               color='red')
                        os._exit(1)
                    else:
                        currentconfig = config.ini[currentconfig['containerclient']]
            if 'type' in currentconfig and currentconfig['type'] == 'kubevirt':
                default_k8s = True
            k8s = currentconfig.get('k8s', default_k8s)
            host = currentconfig.get('host', '127.0.0.1')
            port = currentconfig.get('port', 22)
            user = currentconfig.get('user', 'root')
            if not k8s:
                from kvirt.docker import Kdocker
                cont = Kdocker(host)
            else:
                ca_file = currentconfig.get('ca_file')
                namespace = currentconfig.get('namespace') if namespace is None else namespace
                context = currentconfig.get('context')
                readwritemany = currentconfig.get('readwritemany', False)
                ca_file = currentconfig.get('ca_file')
                if ca_file is not None:
                    ca_file = os.path.expanduser(ca_file)
                    if not os.path.exists(ca_file):
                        pprint("Ca file %s doesn't exist. Leaving" % ca_file, color='red')
                        os._exit(1)
                token = currentconfig.get('token')
                token_file = currentconfig.get('token_file')
                if token_file is not None:
                    token_file = os.path.expanduser(token_file)
                    if not os.path.exists(token_file):
                        pprint("Token file path doesn't exist. Leaving", color='red')
                        os._exit(1)
                    else:
                        token = open(token_file).read()
                from kvirt.kubernetes import Kubernetes
                cont = Kubernetes(host=host, user=user, port=port, token=token, ca_file=ca_file, context=context,
                                  namespace=namespace, readwritemany=readwritemany)
            self.cont = cont
