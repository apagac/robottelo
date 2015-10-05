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

    rhev_name = conf.properties['rhev.name']
    rhev_hostname_api = conf.properties['rhev.hostname']
    rhev_username = conf.properties['rhev.username']
    rhev_password = conf.properties['rhev.password']
    rhev_datacenter = conf.properties['rhev.datacenter']
    #TODO for development purposes
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
            #self.compute_resource.delete(self.rhev_name)
            #search = self.compute_resource.search(self.rhev_name)
            #self.assertIsNone(search)

    vmware_name = conf.properties['vmware.name']
    vmware_vcenter = conf.properties['vmware.vcenter']
    vmware_username = conf.properties['vmware.username']
    vmware_password = conf.properties['vmware.password']
    vmware_datacenter = conf.properties['vmware.datacenter']
    #TODO for development purposes
    def test_create_vmware_compute_resource(self):
        with Session(self.browser) as session:
            make_resource(
                session,
                name=self.vmware_name,
                provider_type=FOREMAN_PROVIDERS['vmware'],
                parameter_list=[
                    ['VCenter/Server', self.vmware_vcenter, 'field'],
                    ['Username', self.vmware_username, 'field'],
                    ['Password', self.vmware_password, 'field'],
                    ['Datacenter', self.vmware_datacenter, 'special select']
                ],
                orgs=[self.default_org],
                org_select=False,
                locations=[self.default_loc],
                loc_select=True
            )
            search = self.compute_resource.search(self.vmware_name)
            self.assertIsNotNone(search)
            #self.compute_resource.delete(self.vmware_name)
            #search = self.compute_resource.search(self.vmware_name)
            #self.assertIsNone(search)

    #def test_create_osp_compute_resource(self):
    #    pass

    #def test_create_docker_compute_resource(self):
    #    pass

    @data(
        {'name': rhev_name,
         'provider': FOREMAN_PROVIDERS['rhev'],
         'url': rhev_hostname_api,
         'username': rhev_username,
         'password': rhev_password,
         'datacenter': rhev_datacenter,
         #this is the name of the URL field for rhev
         'url_name': 'URL'},
        {'name': vmware_name,
         'provider': FOREMAN_PROVIDERS['vmware'],
         'url': vmware_vcenter,
         'username': vmware_username,
         'password': vmware_password,
         'datacenter': vmware_datacenter,
         #this is the name of the URL field for vmware
         'url_name': 'VCenter/Server'}
    )
    def test_create_compute_resource(self):
        with Session(self.browser) as session:
            make_resource(
                session,
                name=data['name'],
                provider_type=data['provider'],
                parameter_list=[
                    [data['url_name'], data['url'], 'field'],
                    ['Username', data['username'], 'field'],
                    ['Password', data['password'], 'field'],
                    ['Datacenter', data['datacenter'], 'special select']
                ],
                orgs=[self.default_org],
                org_select=False,
                locations=[self.default_loc],
                loc_select=True
            )
            search = self.compute_resource.search(data['name'])
            self.assertIsNotNone(search)
            self.compute_resource.delete(data['name'])
            search = self.compute_resource.search(data['name'])
            self.assertIsNone(search)

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

    def test_retrieve_vm_list(self):
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
            for item in self.compute_resource.list_vms(self.rhev_name):
                if item.text:
                    print "VM: %s" % item.text
            self.compute_resource.delete(self.rhev_name)

    def test_retrieve_template_list(self):
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
            for item in self.compute_resource.list_images(self.rhev_name):
                print "Image: %s" % item.text
            self.compute_resource.delete(self.rhev_name)

    #TODO need to set-up the VM on the resource
    vm_name = "apagac2-cfme"

    def test_vm_start_stop(self):
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
            #TODO assuming the VM is powered down when starting this test
            #TODO RFE: find out the status of the VM
            self.compute_resource.vm_action_start(self.rhev_name, self.vm_name)
            self.compute_resource.vm_action_stop(self.rhev_name, self.vm_name, True)
            self.compute_resource.delete(self.rhev_name)

    def test_delete_vm(self):
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
            self.compute_resource.vm_delete(self.rhev_name,
                                            self.vm_name,
                                            True)
            self.compute_resource.delete(self.rhev_name)

    """
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
