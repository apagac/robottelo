from robottelo.test import UITestCase
from robottelo.common import conf
from robottelo.ui.session import Session
from robottelo.common.constants import FOREMAN_PROVIDERS
from robottelo.ui.factory import make_resource
from ddt import data, ddt

@ddt
class ComputeResourceTestCase(UITestCase):

    default_org = 'Default Organization'
    default_loc = 'Default Location'

    rhev_name = conf.properties['rhev.name']
    rhev_hostname_api = conf.properties['rhev.hostname']
    rhev_username = conf.properties['rhev.username']
    rhev_password = conf.properties['rhev.password']
    rhev_datacenter = conf.properties['rhev.datacenter']
    rhev_vm_name=conf.properties['rhev.vm_name']

    vmware_name = conf.properties['vmware.name']
    vmware_vcenter = conf.properties['vmware.vcenter']
    vmware_username = conf.properties['vmware.username']
    vmware_password = conf.properties['vmware.password']
    vmware_datacenter = conf.properties['vmware.datacenter']
    vmware_vm_name=conf.properties['vmware.vm_name']

    @data(
        #{'name': rhev_name,
        # 'provider': FOREMAN_PROVIDERS['rhev'],
        # 'url': rhev_hostname_api,
        # 'username': rhev_username,
        # 'password': rhev_password,
        # 'datacenter': rhev_datacenter,
         #this is the label of the URL field for rhev
        # 'url_name': 'URL',
         #this is for RHEV datacenter locator
        # 'dc_locator': 'datacenter'},
        {'name': vmware_name,
         'provider': FOREMAN_PROVIDERS['vmware'],
         'url': vmware_vcenter,
         'username': vmware_username,
         'password': vmware_password,
         'datacenter': vmware_datacenter,
         #this is the label of the URL field for vmware
         'url_name': 'vcenterserver',
         #this is for vmware datacenter locator
         'dc_locator': 'datacenter_vsphere'}
    )
    def test_create_compute_resource(self, data):
        """ @Test: Create a compute resource.

        @Assert: A compute resource is created

        @Feature: Compute Resource
        """
        with Session(self.browser) as session:
            make_resource(
                session,
                name=data['name'],
                provider_type=data['provider'],
                parameter_list=[
                    [data['url_name'], data['url'], 'field'],
                    ['Username', data['username'], 'field'],
                    ['Password', data['password'], 'field'],
                    [data['dc_locator'], data['datacenter'], 'special select']
                ],
                orgs=[self.default_org],
                org_select=False,
                locations=[self.default_loc],
                loc_select=True
            )
            search = self.compute_resource.search(data['name'])
            self.assertIsNotNone(search)

    @data(
        {'name': rhev_name,
         'new_name': '%s-updated' % rhev_name},
        {'name': vmware_name,
         'new_name': '%s-updated' % vmware_name}
        #{'name': 'osp name'},
        #{'name': 'docker name'}
    )
    def test_edit_compute_resource(self, data):
        """ @Test: Edit a compute resource.

        @Assert: A compute resource with new name exists

        @Feature: Compute Resource
        """
        search = self.compute_resource.search(data['name'])
        self.assertIsNotNone(search)
        self.compute_resource.update(name=data['name'],
                                     newname=data['new_name'])
        search = self.compute_resource.search(data['new_name'])
        self.assertIsNotNone(search)
        self.compute_resource.update(name=data['new_name'],
                                     newname=data['name'])
        search = self.compute_resource.search(data['name'])
        self.assertIsNotNone(search)

    @data(
        {'name': rhev_name},
        {'name': vmware_name}
        #{'name': 'osp name'},
        #{'name': 'docker name'}
    )
    def test_retrieve_vm_list(self, data):
        """ @Test: Retrieve list of VMs.

        @Feature: Compute Resource
        """
        print "%s:" % data['name']
        for item in self.compute_resource.list_vms(data['name']):
            if item.text:
                print "VM: %s" % item.text

    @data(
        {'name': rhev_name},
        {'name': vmware_name}
        #{'name': 'osp name'},
        #{'name': 'docker name'}
    )
    def test_retrieve_template_list(self, data):
        """ @Test: Retrieve list of templates..

        @Feature: Compute Resource
        """
        print "%s:" % data['name']
        for item in self.compute_resource.list_images(data['name']):
            print "Image: %s" % item.text

    @data(
        {'name': rhev_name,
         'vm_name': rhev_vm_name},
        {'name': vmware_name,
         'vm_name': vmware_vm_name}
    )
    def test_vm_start_stop(self, data):
        """ @Test: Start & Stop a VM.

        @Feature: Compute Resource

        note: assuming the VM is powered down when starting this test
        """
        self.compute_resource.vm_action_start(data['name'], data['vm_name'])
        self.compute_resource.vm_action_stop(data['name'], data['vm_name'],
                                             True)

    @data(
        {'name': rhev_name,
         'vm_name': rhev_vm_name},
        {'name': vmware_name,
         'vm_name': vmware_vm_name}
    )
    def test_delete_vm(self, data):
        """ @Test: Deletes a VM.

        @Feature: Compute Resource
        """
        self.compute_resource.vm_delete(data['name'], data['vm_name'], True)

    res = rhev_name
    image_name = 'test_auto_img'
    os = 'CentOS 6.6'
    arch = 'i386'
    uname = 'testing'
    passw = 'testing'
    img = 'Blank'

    @data(
        {'name': rhev_name,
         'img_name': conf.properties['rhev.img_name'],
         'img_os': conf.properties['rhev.img_os'],
         'img_arch': conf.properties['rhev.img_arch'],
         'img_uname': conf.properties['rhev.img_username'],
         'img_passw': conf.properties['rhev.img_password'],
         'img_img': conf.properties['rhev.img_image']},
        {'name': vmware_name,
         'img_name': conf.properties['vmware.img_name'],
         'img_os': conf.properties['vmware.img_os'],
         'img_arch': conf.properties['vmware.img_arch'],
         'img_uname': conf.properties['vmware.img_username'],
         'img_passw': conf.properties['vmware.img_password'],
         'img_img': conf.properties['vmware.img_image']}
    )
    def test_add_image(self, data):
        """ @Test: Adds an image to compute resource.

        @Assert: Image added is on the first page

        @Feature: Compute Resource
        """
        parameter_list=[
            ['Name', data['img_name'], 'field'],
            ['Operatingsystem', data['img_os'], 'select'],
            ['Architecture', data['img_arch'], 'select'],
            ['Username', data['img_uname'], 'field'],
            ['Password', data['img_passw'], 'field'],
            ['Image', data['img_img'], 'select']
        ]
        self.compute_resource.add_image(data['name'], parameter_list)
        for item in self.compute_resource.list_images(data['name']):
            if item.text == data['img_name']:
                search = True
        self.assertIsNotNone(search)


    @data(
        {'name': rhev_name},
        {'name': vmware_name}
    )
    def test_delete_compute_resource(self, data):
        """ @Test: Edit a compute resource.

        @Assert: A compute resource with new name exists

        @Feature: Compute Resource
        """
        search = self.compute_resource.search(data['name'])
        self.assertIsNotNone(search)
        self.compute_resource.delete(data['name'])
        search = self.compute_resource.search(data['name'])
        self.assertIsNone(search)
