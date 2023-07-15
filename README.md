# dnac_device_list

dnac_device_list is a Python library that makes your life easier when you want to programatically find out 
the location name and location id of any given device that is managed by Cisco DNA Center.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dnac_device_list.

```bash
pip install dnac_device_list
```

## Use Case 1 (Use existing token for authorization)

```python
from dnac_device_list import device_list

token = "eyJhbRciOiJSUzI1NiIsInR5cGI6IkpXVCJ9.eyJzdWIiOiI2MTE2YmI0YWU3YjUwODZiNTLjMTI5ZjQiLCJhdXRoU291cmNlIjoiaW50ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVzIjpbIjYxMTZiYjQ4ZTliNTA4NmI1M2MxMjlmMyJdLCJ0ZW5hbnRJZCI6IjYxMTZiYjQ4ZTliNTA4NmI1M2MxMjlmMSIsImV4cCI6MTY4ODQwMzMxMSwiaWF0IjoxNjg4Mzk5NzExLCJqdGkiOiJhNzliMjgwMC04NjdkLTRiZmQtYWJmMy02NjJiOGUzNmY4OTgiLCJ1c2VybmFtZSI6ImFkbWluIn0.hqvLkQL-07Oiwjy_RzEj5b556nlDiNpIZw-78xmEUu9FLIBuE0bWvoLgmK-2AIdAsB2bbPZ61uDmrE4YK__IINDNl6zeK6NfBGSDCzpJ9VvT_ywnLdqSpGfBArcnGcr2Wwa1DRSmGBn5uF7o0SBcE-K2--KneGsIKjZblCAPD4G1F8QwmL_FgNv6cVI-FMdhLxtYuM2pCYpE23oBmHaSIm-0xyPc71vlQiAYbZ1vnQVx64zdVNA5SPvyAvOZUY5YTixhOU0qw3rcABSk0GbVO8jZlE-QJLuC6hhh5LwM6yDnWPekWS7KPqdhXGTAEzPhxNvnAmZlXrY0nrJFJBpkkg"

# initializes class
dnac = device_list.Dnac(base_url="https://dnac.example.com", token=token, verify=False)

# returns 'list of devices'
devices = dnac.get_device_list_with_location()


```

## Use Case 2 (Use username and password for authorization)

```python
from dnac_device_list import device_list

# initializes class
dnac = device_list.Dnac(base_url="https://dnac.example.com", username="admin", password="Cisco123", verify=False)

# returns 'list of devices'
devices = dnac.get_device_list_with_location()
```

## Response json (devices variable)
```json
{
	"response": [
		{
			"reachabilityFailureReason": "string",
			"reachabilityStatus": "string",
			"series": "string",
			"snmpContact": "string",
			"snmpLocation": "string",
			"tagCount": "string",
			"tunnelUdpPort": {},
			"uptimeSeconds": "integer",
			"waasDeviceMode": {},
			"serialNumber": "string",
			"lastUpdateTime": "integer",
			"macAddress": "string",
			"upTime": "string",
			"deviceSupportLevel": "string",
			"hostname": "string",
			"type": "string",
			"memorySize": "string",
			"family": "string",
			"errorCode": "string",
			"softwareType": "string",
			"softwareVersion": "string",
			"description": "string",
			"roleSource": "string",
			"location": "string",
			"role": "string",
			"collectionInterval": "string",
			"inventoryStatusDetail": "string",
			"apEthernetMacAddress": {},
			"apManagerInterfaceIp": "string",
			"associatedWlcIp": "string",
			"bootDateTime": "string",
			"collectionStatus": "string",
			"errorDescription": "string",
			"interfaceCount": "string",
			"lastUpdated": "string",
			"lineCardCount": "string",
			"lineCardId": "string",
			"locationName": "string",
			"managedAtleastOnce": "boolean",
			"managementIpAddress": "string",
			"platformId": "string",
			"managementState": "string",
			"instanceTenantId": "string",
			"instanceUuid": "string",
			"id": "string"
		}]
}
```

## Contributing

Pull requests are welcome. For major changes, please reach out to author via email first.
to discuss what you would like to change.
https://github.com/alekos3/DNAC_Device_Location


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors
Alexios Nersessian
email: nersessian@gmail.com
