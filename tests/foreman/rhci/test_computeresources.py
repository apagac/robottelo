from robottelo.test import UITestCase
from robottelo.common import conf
from robottelo.ui.session import Session
from robottelo.common.constants import FOREMAN_PROVIDERS
from robottelo.ui.factory import make_resource
from ddt import data, ddt

@ddt
class ComputeResourceTestCase(UITestCase):

    #TODO create this in config file
    default_org = 'Default Organization'
    default_loc = 'Default Location'

    rhev_name=''
    rhev_hostname_api=''
    rhev_username=''
    rhev_password=''
    rhev_datacenter=''

    def test_create_delete_rhev_compute_resource(self):
        with Session(self.browser) as session:
            make_resource(
                session,
                name=self.rhev_name,
                provider_type=FOREMAN_PROVIDERS['rhev'],
                parameter_list=[
                    ['URL', self.rhev_hostname_api, 'field'],
                    ['Username', self.rhev_username, 'field'],
                    ['Password', self.rhev_password, 'field'],
                    ['Datacenter', self.rhev_datacenter, 'special select']
                ],
                orgs=[self.default_org],
                org_select=False,
                locations=[self.default_loc],
                loc_select=True
            )
            search = self.compute_resource.search(self.rhev_name)
            self.assertIsNotNone(search)
            self.compute_resource.delete(self.rhev_name)
            search = self.compute_resource.search(self.rhev_name)
            self.assertIsNone(search)

    #def test_create_vmware_compute_resource(self):
    #    pass

    #def test_create_osp_compute_resource(self):
    #    pass

    #def test_create_docker_compute_resource(self):
    #    pass

    @data(
        {'name': rhev_name,
         'new_name': '%s-updated' % rhev_name},
        #{'name': 'vmware name'},
        #{'name': 'osp name'},
        #{'name': 'docker name'}
    )
    def test_edit_compute_resource(self, data):
        with Session(self.browser) as session:
            make_resource(
                session,
                name=self.rhev_name,
                provider_type=FOREMAN_PROVIDERS['rhev'],
                parameter_list=[
                    ['URL', self.rhev_hostname_api, 'field'],
                    ['Username', self.rhev_username, 'field'],
                    ['Password', self.rhev_password, 'field'],
                    ['Datacenter', self.rhev_datacenter, 'special select']
                ],
                orgs=[self.default_org],
                org_select=False,
                locations=[self.default_loc],
                loc_select=True
            )
            search = self.compute_resource.search(self.rhev_name)
            self.assertIsNotNone(search)
            self.compute_resource.update(name=data['name'], newname=data['new_name'])
            search = self.compute_resource.search(data['new_name'])
            self.assertIsNotNone(search)
            self.compute_resource.delete(data['new_name'])
            self.assertIsNone(search)

    """
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
    """
