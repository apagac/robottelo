from robottelo.test import UITestCase
from robottelo.config import conf
from robottelo.ui.session import Session
from robottelo.constants import FOREMAN_PROVIDERS
from robottelo.ui.factory import make_resource
from ddt import data, ddt

class ComputeResourceTestCase(UITestCase):

    #TODO create this in config file
    #current_rhev_url = conf.properties['main.rhev.hostname']
    #rhev_name = conf.properties['main.rhev.name']
    #rhev_username = conf.properties['main.rhev.username']
    #rhev_password = conf.properties['main.rhev.password']
    #rhev_datacenter = conf.properties['main.rhev.datacenter']
    default_org = 'Default Organization'
    default_loc = 'Default Location'

    @data(
        {'name': conf.properties['main.rhev.name'],
         'type': 'rhev',
         'url': conf.properties['main.rhev.hostname'],
         'username': conf.properties['main.rhev.username'],
         'password': conf.properties['main.rhev.password'],
         'datacenter':conf.properties['main.rhev.datacenter']},
        {'name': conf.properties['main.vmware.name'],
         'type': 'vmware',
         'url': conf.properties['main.vmware.hostname'],
         'username': conf.properties['main.vmware.username'],
         'password': conf.properties['main.vmware.password'],
         'datacenter': conf.properties['main.vmware.datacenter']}
    )
    def test_create_compute_resource(self):
        """Create rhev and vmware compute resource"""
        with Session(self.browser) as session:
            make_resource(
                session,
                name=data['name'],
                provider_type=FOREMAN_PROVIDERS[data['type']],
                parameter_list=[
                    ['URL', data['url'], 'field'],
                    ['Username', data['username'], 'field'],
                    ['Password', data['password'], 'field'],
                    #TODO this is different with rhev and with vmware
                    ['Datacenter', self.rhev_datacenter, 'special select']
                ],
                orgs=[self.default_org],
                org_select=True,
                locations=[self.default_loc],
                loc_select=True
            )
            search = self.compute_resource.search(self.rhev_name)
            self.assertIsNotNone(search)

    def test_edit_compute_resource(self):
        pass

    def test_delete_compute_resource(self):
        pass