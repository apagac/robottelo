from robottelo.test import UITestCase
from robottelo.config import conf
from robottelo.ui.session import Session
from robottelo.constants import FOREMAN_PROVIDERS
from robottelo.ui.factory import make_resource
from ddt import data, ddt

class ComputeResourceTestCase(UITestCase):

    #TODO create this in config file
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
    def test_create_compute_resource(self, data):
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
            search = self.compute_resource.search(data['name'])
            self.assertIsNotNone(search)

    @data(
        {'name': conf.properties['main.rhev.name'],
         'new_name': '%s-updated' % conf.properties['main.rhev.name']},
        {'name': conf.properties['main.vmware.name'],
         'new_name': '%s-updated' % conf.properties['main.vmware.name']}
    )
    def test_edit_compute_resource(self, data):
        with Session(self.browser) as session:
            search = self.compute_resource.search(data['name'])
            self.assertIsNotNone(search)
            self.compute_resource.update(name=data['name'], newname=data['new_name'])
            search = self.compute_resource.search(data['new_name'])
            self.assertIsNotNone(search)

    @data( #TODO
        {'name': 'placeholder'},
        {'name': 'placeholder'}
    )
    def test_delete_compute_resource(self, data):
        with Session(self.browser) as session:
            search = self.compute_resource.search(data['name'])
            self.assertIsNotNone(search)
            self.compute_resource.delete(data['name'])
            search = self.compute_resource.search(data['name'])
            self.assertIsNone(search)


    def test_retrieve_vm_list(self):
        pass

    def test_retrieve_template_list(self):
        pass

    def test_vm_start_stop(self):
        pass

    def test_delete_vm(self):
        pass

    def test_add_image(self):
        pass

    def test_delete_image(self):
        pass

    def test_provision_image(self):
        pass

    #default and custom compute profile
    def test_provision_image_with_compute_profile(self):
        pass

    #to specific folder, static IP & custom spec,
    # configure DNS & domain settings
    def test_provision_vm(self):
        pass

