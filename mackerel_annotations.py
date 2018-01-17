#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


DOCUMENTATION = """
module: mackerel_annotations
short_description: Send Mackerel annotations
description:
    - The mackerel_annotations  module sends annotations to mackerel service and roles
author: "Ryo Manzoku(@rmanzoku)"
options:
  api_key:
    description:
      - Mackrel API key https://mackerel.io/my?tab=apikeys
    required: True
  title:
    description:
      - Annotation title
    required: True
  description:
    description:
      - Annotation details
    required: False
    default: None
  epoch_from:
    description:
      - Starting time (epoch seconds)
    required: True
  epoch_to:
    description:
      - Ending time (epoch seconds)
    required: True
  service:
    description:
      - Service name
    required: True
  roles:
    description:
      - Role name array (omit this field to register an annotation related to the service)
    required: False
    default: None
"""


def build_payload(module, title, description, epoch_from, epoch_to, service, roles):

    payload = {}

    payload['title'] = title

    if description is not None:
        payload['description'] = description

    payload['from'] = epoch_from
    payload['to'] = epoch_to
    payload['service'] = service

    if roles is not None:
        payload['roles'] = roles

    return module.jsonify(payload)


def do_notify_mackerel_annotations(module, api_key, payload):

    mackerel_annotations_url = 'https://api.mackerelio.com/api/v0/graph-annotations'

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Api-Key': api_key
    }

    response, info = fetch_url(module=module,
                               url=mackerel_annotations_url,
                               headers=headers,
                               method='POST',
                               data=payload)

    if info['status'] != 200:
        module.fail_json(
            msg=" failed to send %s to %s: %s"
            % (payload, mackerel_annotations_url, info['msg'])
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_key=dict(type='str', required=True),
            title=dict(type='str', required=True),
            description=dict(type='str', required=False, default=None),
            epoch_from=dict(type='int', required=True),
            epoch_to=dict(type='int', required=True),
            service=dict(type='str', required=True),
            roles=dict(type='list', required=False, default=None)
        )
    )

    api_key = module.params['api_key']
    title = module.params['title']
    description = module.params['description']
    epoch_from = module.params['epoch_from']
    epoch_to = module.params['epoch_to']
    service = module.params['service']
    roles = module.params['roles']

    payload = build_payload(module, title, description, epoch_from, epoch_to, service, roles)
    do_notify_mackerel_annotations(module, api_key, payload)

    module.exit_json(msg="OK")

if __name__ == '__main__':
    main()
