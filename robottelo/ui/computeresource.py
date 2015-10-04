# -*- encoding: utf-8 -*-
from robottelo.common.constants import FILTER
from robottelo.ui.base import Base, UINoSuchElementError, UIError
from robottelo.ui.locators import common_locators, locators, tab_locators
from robottelo.ui.navigator import Navigator
from selenium.webdriver.support.select import Select


class ComputeResource(Base):
    """Provides the CRUD functionality for Compute Resources."""

    def _configure_resource_provider(
            self, provider_type=None, parameter_list=None):
        """Provide configuration capabilities for compute resource provider.
        All values should be passed in absolute correspondence to UI. For
        example, we need to input some data to 'URL' field, select checkbox
        'Console Passwords' and choose 'SPICE' value from select list, so next
        parameter list should be passed::

            [
                ['URL', libvirt_url, 'field'],
                ['Display Type', 'SPICE', 'select'],
                ['Console passwords', False, 'checkbox']
            ]

        We have cases when it is necessary to push a button to populate values
        for select list. For such scenarios we have 'special select' parameter
        type. For example, for 'RHEV' provider, we need to click 'Load
        Datacenters' button to get values for 'Datacenter' list::

            [
                ['Description', 'My_Test', 'field'],
                ['URL', libvirt_url, 'field'],
                ['Username', 'admin', 'field'],
                ['Password', 'test', 'field'],
                ['X509 Certification Authorities', 'test', 'field'],
                ['Datacenter', 'test', 'special select'],
            ]

        """
        if provider_type:
            Select(
                self.find_element(locators['resource.provider_type'])
            ).select_by_visible_text(provider_type)
        if parameter_list is None:
            return
        for parameter_name, parameter_value, parameter_type in parameter_list:
            param_locator = '.'.join((
                'resource',
                (parameter_name.lower()).replace(' ', '_')
            ))
            self.wait_until_element(locators[param_locator])
            if parameter_type == 'field':
                self.find_element(
                    locators[param_locator]).send_keys(parameter_value)
            elif parameter_type == 'select':
                Select(
                    self.find_element(locators[param_locator])
                ).select_by_visible_text(parameter_value)
            elif parameter_type == 'checkbox':
                if (self.find_element(locators[param_locator]).is_selected() !=
                        parameter_value):
                    self.click(locators[param_locator])
            elif parameter_type == 'special select':
                button_locator = '.'.join((
                    'resource',
                    (parameter_name.lower()).replace(' ', '_'),
                    'button'
                ))
                self.click(locators[button_locator])
                Select(
                    self.find_element(locators[param_locator])
                ).select_by_visible_text(parameter_value)

    def _configure_orgs(self, orgs, org_select):
        """Provides configuration capabilities for compute resource
        organization. The following format should be used::

            orgs=['Aoes6V', 'JIFNPC'], org_select=True

        """
        self.configure_entity(
            orgs,
            FILTER['cr_org'],
            tab_locator=tab_locators['tab_org'],
            entity_select=org_select
        )

    def _configure_locations(self, locations, loc_select):
        """Provides configuration capabilities for compute resource location

        The following format should be used::

            locations=['Default Location'], loc_select=True

        """
        self.configure_entity(
            locations,
            FILTER['cr_loc'],
            tab_locator=tab_locators['tab_loc'],
            entity_select=loc_select
        )

    def create(self, name, provider_type, parameter_list,
               orgs=None, org_select=None, locations=None, loc_select=None):
        """Creates a compute resource."""
        self.click(locators['resource.new'])
        if self.wait_until_element(locators['resource.name']):
            self.find_element(locators['resource.name']).send_keys(name)
        self._configure_resource_provider(provider_type, parameter_list)
        if locations:
            self._configure_locations(locations, loc_select)
        if orgs:
            self._configure_orgs(orgs, org_select)
        self.click(common_locators['submit'])

    def search(self, name):
        """Searches existing compute resource from UI."""
        Navigator(self.browser).go_to_compute_resources()
        self.wait_for_ajax()
        element = self.search_entity(name, locators['resource.select_name'])
        return element

    def update(self, name, newname=None, parameter_list=None,
               orgs=None, org_select=None, locations=None, loc_select=None):
        """Updates compute resource entity"""
        element = self.search(name)
        if element is None:
            raise UINoSuchElementError(
                'Could not find the resource {0}'.format(name))
        strategy, value = locators['resource.edit']
        self.click((strategy, value % name))
        self.wait_until_element(locators['resource.name'])
        if newname:
            self.field_update('resource.name', newname)
        self._configure_resource_provider(parameter_list=parameter_list)
        if locations:
            self._configure_locations(locations, loc_select)
        if orgs:
            self._configure_orgs(orgs, org_select)
        self.click(common_locators['submit'])

    def delete(self, name, really=True):
        """Removes the compute resource entity"""
        #TODO added to make delete work when called with different context
        Navigator(self.browser).go_to_compute_resources()
        self.delete_entity(
            name,
            really,
            locators['resource.select_name'],
            locators['resource.delete'],
            drop_locator=locators['resource.dropdown']
        )

    def go_to_compute_resource(self, res_name):
        resource = self.search(res_name)
        #TODO if not found
        if resource is None:
            raise UINoSuchElementError(
                'Could not find the resource {0}'.format(res_name))
        strategy, value = locators['resource.get_by_name']
        locator = (strategy, value % res_name)
        self.click(locator)
        #TODO consider better object to wait for
        self.wait_until_element(locators['resource.virtual_machines_tab'])

    def list_vms(self, res_name):
        """
        resource = self.search(res_name)
        #TODO if not found
        strategy, value = locators['resource.get_by_name']
        locator = (strategy, value % res_name)
        self.click(locator)
        self.wait_until_element(locators['resource.virtual_machines_tab'])
        """
        self.go_to_compute_resource(res_name)
        self.click(locators['resource.virtual_machines_tab'])
        #vms = self.find_element(locators['resource.virtual_machines'])
        vms = self.browser.find_elements_by_xpath(
            #TODO needs correcting, see list_images
            "//table[contains(@id, 'DataTables')]//a[contains(@data-id, '%s')]" % res_name)
        return vms

    def add_image(self):
        pass

    def list_images(self, res_name):
        """
        resource = self.search(res_name)
        #TODO if not found
        strategy, value = locators['resource.get_by_name']
        locator = (strategy, value % res_name)
        self.click(locator)
        self.wait_until_element(locators['resource.images_tab'])
        """
        self.go_to_compute_resource(res_name)
        self.click(locators['resource.images_tab'])
        images = self.browser.find_elements_by_xpath(
            #"//table[contains(@id, 'DataTables')]/tbody//tr/td[1]")
            #"//table[contains(@id, 'DataTables')]/tbody/tr/*[1]")
            #TODO what about multiple pages? I need some paginator
            "//table[contains(@id, 'DataTables_Table_0')]/tbody/tr/*[1]")
        return images

    def vm_action_stop(self, res_name, vm_name, really):
        self.go_to_compute_resource(res_name)
        self.click(locators['resource.virtual_machines_tab'])
        #strategy, value = locators['resource.vm.power_off_button']
        strategy, value = locators['resource.vm.power_button']
        #locator = (strategy, value % vm_name)
        locator = (strategy, value % (res_name, vm_name))
        button = self.find_element(locator)
        if 'Off' in button.text:
            self.click(locator, wait_for_ajax=False)
            self.handle_alert(really)
            self.wait_until_element(common_locators['notif.success'])
            #element = self.find_element(common_locators['notif.success'])
            #print element.text
        else:
            raise UIError(
                'Could not stop VM {0}. VM is not running'.format(vm_name)
            )


    def vm_action_start(self, res_name, vm_name):
        self.go_to_compute_resource(res_name)
        self.click(locators['resource.virtual_machines_tab'])
        #strategy, value = locators['resource.vm.power_on_button']
        #locator = (strategy, value % vm_name)
        strategy, value = locators['resource.vm.power_button']
        locator = (strategy, value % (res_name, vm_name))
        button = self.find_element(locator)
        if 'On' in button.text:
            self.click(locator,wait_for_ajax=False)
            self.wait_until_element(common_locators['notif.success'])
        else:
            raise UIError(
                'Could not start VM {0}. VM is already running'.format(vm_name)
            )

    def vm_action_toggle(self, res_name, vm_name, really):
        self.go_to_compute_resource(res_name)
        self.click(locators['resource.virtual_machines_tab'])
        strategy, value = locators['resource.vm.power_button']
        locator = (strategy, value % (res_name, vm_name))
        button = self.find_element(locator)
        if "On" in button.text:
            self.click(locator,wait_for_ajax=False)
            #TODO wait for message
        else:
            self.click(locator, wait_for_ajax=False)
            self.handle_alert(really)
            #TODO wait for message

    def vm_delete(self, res_name, vm_name, really):
        self.go_to_compute_resource(res_name)
        self.click(locators['resource.virtual_machines_tab'])
        #TODO this is power button dropdown
        strategy, value = locators['resource.vm.delete_button_dropdown']
        locator = (strategy, value % (res_name, vm_name))
        self.click(locator)
        strategy, value = locators['resource.vm.delete_button']
        locator = (strategy, value % (res_name, vm_name))
        self.click(locator, wait_for_ajax=False)
        self.handle_alert(really)
        self.wait_until_element(common_locators['notif.success'])

    def list_compute_profiles(self):
        pass