__author__ = "Alexios Nersessian"
__email__ = "nersessian@gmail.com"
__version__ = "v1"

"""
       MIT License

    Copyright (c) [year] [fullname]

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

import json
import requests

class DnacDeviceLocation:
    """
    Class that gets all network devices from DNAC and populates the location and locationName fields. The 3 API
    endpoints below are consumed in order to get the location name and location id.

    /dna/intent/api/v1/network-device
    /dna/intent/api/v1/device-health
    /dna/intent/api/v1/site
    """
    def __init__(self, base_url, token, verify=None):
        self.base_url = base_url
        self.token = token
        self.verify = verify if verify is not None else True

    def get_network_devices(self):
        """
        Function gets all DNAC devices in inventory.
        :return: list of dictionaries
        """
        offset = 1
        limit = 500
        device_list = []

        # Define the new headers to retrieve network devices
        headers = {
            "content-type": "application/json",
            "Accept": "application/json",
            "x-auth-token": self.token
        }

        try:
            while True:
                # Make the GET Request
                url = f"{self.base_url}/dna/intent/api/v1/network-device?offset={offset}&limit={limit}"
                response = requests.request("GET", url, headers=headers, verify=self.verify)

                if response.json()['response']:
                    device_list.extend(response.json()['response'])
                    offset += limit
                else:
                    break

            return device_list  # return the list of dnac devices

        except Exception as e:
            print(e)
            return

    def get_all_device_location(self):  # Device health API
        """
        This function gets all the devices from the device health API in order to get their respective location.
        :return: list of dictionaries
        """
        limit = 1000
        offset = 1
        device_list = []

        headers = {
            "content-type": "application/json",
            "Accept": "application/json",
            "x-auth-token": self.token
        }

        try:
            while True:
                url = f"{self.base_url}/dna/intent/api/v1/device-health?limit={limit}&offset={offset}"
                offset += limit

                response = requests.get(url, headers=headers, verify=self.verify)
                if not response.json()["response"]:
                    break

                device_list.extend(response.json()["response"])

        except Exception as e:
            print(e)

        return device_list

    def get_sites(self):
        """
        This function gets all the sites in DNAC.

        :return: list of dictionaries
        """
        url = f"{self.base_url}/dna/intent/api/v1/site"
        # Define the new headers
        headers = {
            "content-type": "application/json",
            "Accept": "application/json",
            "x-auth-token": self.token
        }

        try:
            response = requests.get(url, headers=headers, verify=self.verify)
            response.raise_for_status()

            return response.json()["response"]

        except requests.exceptions.HTTPError as e:
            print(e)
            return

        except requests.exceptions.SSLError as e:
            print(e)
            return

        except Exception as e:
            print(e)
            return

    def get_device_list_with_location(self):
        """
        This function is the main workflow which calls the appropriate funtions in the correct order
        and constructs a new json body from the network-device API response which now will include the location name
        and location ID.

        :return: string
        """
        # 1. Get all sites
        sites = self.get_sites()
        # print(sites)

        if not sites:
            return

        # 2. Get all devices using network-device API
        devices_no_loc = self.get_network_devices()
        # print(devices_no_loc)

        # 3. Get all devices using device-health API
        device_health_inventory = self.get_all_device_location()
        # print(device_health_inventory)

        # 4. Create site dict
        site_dict = create_site_dict(sites)
        # print(site_dict)

        # 5. map hostname to location from device health api response
        device_health_hostname_location = get_name_location_from_global(device_health_inventory)
        # print(device_health_hostname_location)

        # 6. Construct an appropriate response json object that looks like the original
        response = update_network_device_json(device_health_hostname_location, devices_no_loc, site_dict)

        return json.dumps(response)


def get_name_location_from_global(devices_with_location):
    """
    This function creates a dictionary mapping between hostname (key) and location (value).

    :param devices_with_location: list, from device-health response
    :return: filtered_dev_dict: dictionary
    """
    hostname_to_location_dict = {}

    for device in devices_with_location:
        try:
            hostname_to_location_dict[device.get("name")] = device.get("location")
        except:
            continue

    return hostname_to_location_dict


def update_network_device_json(host_location_dict, device_list, site_dict):
    """
    This function creates a json body that looks almost identical to the json body response returned from
    the network-device API; however this updated body now include information in the location and location name fields.

    :param host_location_dict: this variable is a dict that has hostname to location mappings.
    :param device_list: all devices in dnac returned from network-device API.
    :param site_dict: dict with all sites in DNAC.
    :return: response: dict of all device inventory in DNAC that now includes location and location name.
    """
    response_list = []
    response = {}

    for device in device_list:
        try:
            location_id = get_location_id(site_dict, host_location_dict.get(device.get("hostname")))
            device["location"] = location_id
            device["locationName"] = host_location_dict.get(device.get("hostname"))
            response_list.append(device)

        except:
            continue

    response["response"] = response_list

    return response


def get_location_id(site_dict, location_name):
    """
    This function return a string which is any given sites id.

    :param site_dict: dict
    :param location_name: string
    :return: string
    """
    return site_dict.get(location_name)


def create_site_dict(site_list):
    """
    This function creates a dictioary of location names and their respective ids.

    :param site_list: list of dictionaries
    :return: dictionary
    """
    site_dict = {}
    for site in site_list:
        try:
            site_dict[site["siteNameHierarchy"]] = site["id"]

        except:
            continue

    return site_dict
