#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Populate testapi with testscases - api connection.
"""

import requests
from .output import (print_job, print_success, print_failed_and_exit,
                     print_skipped)

def populate_pod(pod_name, testapi_uri):
    """Create the project in testapi if not exists."""
    print_job(f'🤖 populate pod "{pod_name}"')
    base_uri = f'{testapi_uri}/pods'
    populate(pod_name, base_uri)

def populate_project(project_name, testapi_uri):
    """Create the project in testapi if not exists."""
    print_job(f'📦 populate project "{project_name}"')
    base_uri = f'{testapi_uri}/projects'
    populate(project_name, base_uri)

def populate_case(project_name, case_name, testapi_uri):
    """Create the project test case in testapi if not exists."""
    print_job(f'📋 populate case "{case_name}"')
    base_uri = f'{testapi_uri}/projects/{project_name}/cases'
    populate(case_name, base_uri)

def populate(ressource, base_uri):
    """Populate the testapi with a generic ressource."""
    req = requests.get(f'{base_uri}/{ressource}')
    if req.status_code == 200:
        print_skipped()
        return None
    if req.status_code == 404:
        payload = {'name': ressource}
        req = requests.post(f'{base_uri}', json=payload)
        if req.status_code == 200:
            print_success()
            return None
    print_failed_and_exit(req.text)
    return None
