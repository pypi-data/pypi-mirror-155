"""
CUCMToolKit functions incorporated via:
Class to interface with cisco ucm axl api.
Author: Jeff Levensailor
Version: 0.1
Dependencies:
 - zeep: https://python-zeep.readthedocs.io/en/master/
Links:
 - https://developer.cisco.com/site/axl/
"""
import requests
from lxml import etree
from collections import OrderedDict
from xmltodict import unparse
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.exceptions import Fault
import urllib3
import logging.config
import logging
import os
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AXLHistoryPlugin(HistoryPlugin):
    """
        Extends Zeep HistoryPlugin for easy xml extraction
    """

    @staticmethod
    def _parse_envelope(envelope):
        return etree.tostring(envelope, encoding="unicode", pretty_print=True)

    @property
    def last_received_xml(self):
        last_tx = self._buffer[-1]
        if last_tx:
            return self._parse_envelope(last_tx['received']['envelope'])

    @property
    def last_sent_xml(self):
        last_tx = self._buffer[-1]
        if last_tx:
            return self._parse_envelope(last_tx['sent']['envelope'])


class PawsToolkit:
    """
    The PawsToolkit SOAP API class
    This class enables us to connect and make PAWS API calls utilizing Zeep Python Package as the SOAP Client
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param service: The PAWS API service name
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :type username: str
    :type password: str
    :type server_ip: str
    :type service: str
    :type tls_verify: bool
    :type timeout: int
    :returns: return an PawsToolkit object
    :rtype: PawsToolkit
    """

    def __init__(self, username, password, server_ip, service, tls_verify=False, timeout=15):
        """
        Constructor - Create new instance
        """

        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.history = AXLHistoryPlugin(maxlen=1)
        self.wsdl = None
        self.binding = None
        self.endpoint = None
        self.last_exception = None

        self.cache = SqliteCache(path='/tmp/sqlite_paws_{0}.db'.format(server_ip), timeout=60)

        path = os.path.dirname(__file__)

        if service == 'HardwareInformation':
            self.wsdl = os.path.join(path, 'paws/hardware_information_service.wsdl')
            self.binding = "{http://services.api.platform.vos.cisco.com}HardwareInformationServiceSoap11Binding"
            self.endpoint = "https://{0}:8443/platform-services/services/HardwareInformationService.HardwareInformationServiceHttpsSoap11Endpoint/".format(
                server_ip)  # nopep8
        elif service == 'OptionsService':
            self.wsdl = 'https://{0}:8443/platform-services/services/OptionsService?wsdl'.format(server_ip)
            self.binding = "{http://services.api.platform.vos.cisco.com}OptionsServiceSoap12Binding"
            self.endpoint = "https://{0}:8443/platform-services/services/OptionsService.OptionsServiceHttpsSoap12Endpoint/".format(
                server_ip)  # nopep8
        elif service == 'ProductService':
            self.wsdl = 'https://{0}:8443/platform-services/services/ProductService?wsdl'.format(server_ip)
            self.binding = "{http://services.api.platform.vos.cisco.com}ProductServiceSoap12Binding"
            self.endpoint = "https://{0}:8443/platform-services/services/ProductService.ProductServiceHttpsSoap12Endpoint/".format(
                server_ip)  # nopep8
        elif service == 'VersionService':
            self.wsdl = 'https://{0}:8443/platform-services/services/VersionService?wsdl'.format(server_ip)
            self.binding = "{http://services.api.platform.vos.cisco.com}VersionServiceSoap12Binding"
            self.endpoint = "https://{0}:8443/platform-services/services/VersionService.VersionServiceHttpsSoap12Endpoint/".format(
                server_ip)  # nopep8
        elif service == 'ClusterNodesService':
            self.wsdl = 'https://{0}:8443/platform-services/services/ClusterNodesService?wsdl'.format(server_ip)
            self.binding = "{http://services.api.platform.vos.cisco.com}ClusterNodesServiceSoap12Binding"
            self.endpoint = "https://{0}:8443/platform-services/services/ClusterNodesService.ClusterNodesServiceHttpsSoap12Endpoint/".format(
                server_ip)  # nopep8

        self.service = Client(wsdl=self.wsdl, plugins=[self.history], transport=Transport(timeout=timeout,
                                                                                          operation_timeout=timeout,
                                                                                          cache=self.cache,
                                                                                          session=self.session))

        self.service = self.service.create_service(self.binding, self.endpoint)

    def get_service(self):
        return self.service

    def get_cluster_status(self):
        cluster_status = self.service.getClusterStatus()
        return cluster_status

    def get_cluster_replication(self):
        cluster_replication = self.service.isNodeReplicationOK()
        return cluster_replication

    def get_active_options(self):
        active_options = self.service.getActiveOptions()
        return active_options

    def get_active_version(self):
        active_version = self.service.getActiveVersion()
        return active_version

    def get_inactive_version(self):
        inactive_version = self.service.getInactiveVersion()
        return inactive_version

    def get_installed_products(self):
        installed_prod = self.service.getInstalledProducts()
        return installed_prod

    def get_hardware_information(self):
        hw_info = self.service.getHardwareInformation()
        return hw_info


class AxlToolkit:
    """
    The AxlToolkit Common AXL SOAP API class
    This Parent class enables us to connect and make SOAP API calls to CUCM & IM&P utilizing Zeep Python Package as the SOAP Client
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param version: (optional) The major version of CUCM / IM&P Cluster (default: 12.5)
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :param schema_folder_path: (optional) Sub Directory Location for AXL schema versions (default: None)
    :type username: str
    :type password: str
    :type server_ip: str
    :type version: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :type schema_folder_path: str
    :returns: return an AxlToolkit object
    :rtype: AxlToolkit
    """

    def __init__(self, username, password, server_ip, version='12.5', tls_verify=True, timeout=10,
                 logging_enabled=False, schema_folder_path=None):
        """
        Constructor - Create new instance
        """

        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.history = AXLHistoryPlugin(maxlen=1)
        self.wsdl = None
        self.last_exception = None

        filedir = os.path.dirname(__file__)
        if schema_folder_path is not None:
            filedir = schema_folder_path

        self.cache = SqliteCache(path='/tmp/sqlite_axl_{0}.db'.format(server_ip), timeout=60)

        if version == '14.0':
            self.wsdl = os.path.join(filedir, f'schema/{version}/AXLAPI.wsdl')
        elif version == '12.5':
            self.wsdl = os.path.join(filedir, f'schema/{version}/AXLAPI.wsdl')
        elif version == '12.0':
            self.wsdl = os.path.join(filedir, f'schema/{version}/AXLAPI.wsdl')
        elif version == '11.5':
            self.wsdl = os.path.join(filedir, f'schema/{version}/AXLAPI.wsdl')
        elif version == '11.0':
            self.wsdl = os.path.join(filedir, f'schema/{version}/AXLAPI.wsdl')
        elif version == '10.5':
            self.wsdl = os.path.join(filedir, f'schema/{version}/AXLAPI.wsdl')
        elif version == '10.0':
            self.wsdl = os.path.join(filedir, f'schema/{version}/AXLAPI.wsdl')
        else:
            self.wsdl = os.path.join(filedir, 'schema/12.5/AXLAPI.wsdl')

        self.service = Client(wsdl=self.wsdl, plugins=[self.history],
                              transport=Transport(timeout=timeout, operation_timeout=timeout,
                                                  cache=self.cache, session=self.session))

        # Update the Default SOAP API Binding Address Location with server_ip for all API Service Endpoints
        # Default: (https://CCMSERVERNAME:8443/axl/)
        self.service = self.service.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
                                                   "https://{0}:8443/axl/".format(server_ip))
        # Verify the IP/credentials provided work instead of
        session = requests.session()
        session.auth = (username, password)
        session.verify = False
        ConnectivityTest = (session.get(f'https://{server_ip}:8443/axl/'))
        if ConnectivityTest.status_code == 200:
            pass  # Connection was successful.
        elif ConnectivityTest.status_code == 401:
            raise ValueError(
                'Unable to authenticate using the specified credentials and/or ip address. Please verify the information and/or reachability of the server.')
        else:
            print(ConnectivityTest.status_code)

        if logging_enabled:
            self._enable_logging()

    @staticmethod
    def _enable_logging():
        """
        Enables Logging of SOAP Request and Response Payloads to /tmp/axltoolkit.log
        Use http://xmlprettyprint.com/ to help with SOAP XML payloads
        Its a staticmethod in order to allow other classes in this file to utilize it directly
        """
        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'verbose': {
                    'format': '%(asctime)s | %(name)s: %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
                'debug_file_handler': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'verbose',
                    'filename': '/tmp/axltoolkit.log',
                    "maxBytes": 10485760,
                    "backupCount": 20,
                    "encoding": "utf8"
                }
            },
            'loggers': {
                'zeep.transports': {
                    'level': 'DEBUG',
                    'propagate': True,
                    'handlers': ['console', 'debug_file_handler'],
                },
            }
        })
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def get_service(self):
        return self.service

    def last_request_debug(self):
        return {
            'request': self.history.last_sent,
            'response': self.history.last_received
        }

    def run_sql_query(self, query):
        """
        Thin AXL (SQL Queries / Updates)
        """

        result = {'num_rows': 0,
                  'query': query}

        try:
            if any(re.findall(r'<|>|&lt;|&gt;', query)):
                if not re.search(r'^<!\[CDATA\[', query):
                    query = f"<![CDATA[{query}]]>"
            sql_result = self.service.executeSQLQuery(sql=query)
        except Exception as fault:
            self.last_exception = fault
            return None

        num_rows = 0
        result_rows = []

        if sql_result is not None:
            if sql_result['return'] is not None:
                for row in sql_result['return']['row']:
                    result_rows.append({})
                    for column in row:
                        result_rows[num_rows][column.tag] = column.text
                    num_rows += 1

        result['num_rows'] = num_rows
        if num_rows > 0:
            result['rows'] = result_rows

        return result

    def run_sql_update(self, query):
        """
        Thin AXL (SQL Queries / Updates)
        """

        result = {'rows_updated': 0,
                  'query': query}

        try:
            if any(re.findall(r'<|>|&lt;|&gt;', query)):
                if not re.search(r'^<!\[CDATA\[', query):
                    query = f"<![CDATA[{query}]]>"
            sql_result = self.service.executeSQLUpdate(sql=query)
        except Exception as fault:
            self.last_exception = fault
            return None

        if sql_result is not None:
            if sql_result['return'] is not None:
                result['rows_updated'] = sql_result['return']['rowsUpdated']

        return result


# noinspection PyDefaultArgument,PyIncorrectDocstring
class CUCMAxlToolkit(AxlToolkit):
    """
    The CUCMAxlToolkit based on parent class AxlToolkit
    This class enables us to connect and make unique CUCM AXL API requests
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param version: (optional) The major version of CUCM / IM&P Cluster (default: 12.5)
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :param schema_folder_path: (optional) Sub Directory Location for AXL schema versions (default: None)
    :type username: str
    :type password: str
    :type server_ip: str
    :type version: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :type schema_folder_path: str
    :returns: return an CUCMAxlToolkit object
    :rtype: CUCMAxlToolkit
    """

    def __init__(self, username, password, server_ip, version='12.5', tls_verify=False, timeout=10,
                 logging_enabled=False, schema_folder_path=None):
        self.version = version
        if schema_folder_path is None:
            schema_folder_path = os.path.dirname(os.path.realpath(__file__))
            schema_folder_path += "/CUCM/"

        else:
            schema_folder_path += "/CUCM/"

        # Create a super class, where the CUCMAxlToolkit class inherits from the AxlToolkit class.
        # This enables us to extend the parent class AxlToolkit with CUCM AXL API specic methods
        # Reference:  https://realpython.com/python-super/
        super().__init__(username, password, server_ip, version=version, tls_verify=tls_verify, timeout=timeout,
                         logging_enabled=logging_enabled, schema_folder_path=schema_folder_path)

    def listAllLocations(
            self,
            tagfilter={
                "name": "",
                "withinAudioBandwidth": "",
                "withinVideoBandwidth": "",
                "withinImmersiveKbits": "",
            },
    ):
        """
        Get location details
        :param tagfilter:
        :param mini: return a list of tuples of location details
        :return: A list of dictionary's
        """
        try:
            return self.service.listLocation({"name": "%"}, returnedTags=tagfilter, )[
                "return"
            ]["location"]
        except Exception as e:
            raise Exception(e)

    def executeSQLQuery(self, query):
        """
        Execute SQL query
        :param query: SQL Query to execute
        :return: result dictionary
        """
        try:
            sqlResult = self.service.executeSQLQuery(query)['return']
            print(sqlResult)
            sqlDict = {}
            for item in sqlResult['row']:
                print(item[0].text, item[1].text)  # print the DP counts and Device pool name to screen
                sqlDict[str(item[1].text)] = str(item[0].text)  # save in a new dictionary to reference later
            return sqlDict
        except Exception as e:
            raise Exception(e)

    def executeSQLUpdate(self, query):
        """
        Execute SQL update
        :param query: SQL Update to execute
        :return: result dictionary
        """
        try:
            return self.service.executeSQLUpdate(query)["return"]
        except Exception as e:
            raise Exception(e)

    def listAllLdapDirectories(self, tagfilter={"name": "", "ldapDn": "", "userSearchBase": "", "repeatable": "",
                                                "intervalValue": "", "scheduleUnit": "", "nextExecTime": "",
                                                "accessControlGroupInfo": ""}):
        """
        Get LDAP Syncs
        :return: result dictionary
        """
        try:
            LdapDirectoryList = self.service.listLdapDirectory(
                {"name": "%"}, returnedTags=tagfilter,
            )["return"]
            if LdapDirectoryList is not None:
                LdapDirectoryList = LdapDirectoryList["ldapDirectory"]
            return LdapDirectoryList
        except Exception as e:
            raise Exception(e)

    def doLdapSync(self, name):
        """
        Do LDAP Sync
        :param uuid: uuid
        :return: result dictionary
        """
        try:
            return self.service.doLdapSync(name=name, sync=True)
        except Exception as e:
            raise Exception(e)

    def doChangeDNDStatus(self, deviceName, dndStatus):
        """
        Do Change DND Status
        :param deviceName:
        :param dndStatus:
        :type dndStatus: bool
        :type deviceName: str
        :return: result dictionary
        """
        try:
            return self.service.doChangeDNDStatus(userID=deviceName, dndStatus=dndStatus)
        except Exception as e:
            raise Exception(e)

    def doDeviceLogin(self, deviceName, loginDuration, profileName, userId):
        """
        Do Device Login
        :param deviceName:
        :param userId:
        :param profileName:
        :return: result dictionary
        """
        try:
            return self.service.doDeviceLogin(deviceName=deviceName, loginDuration=loginDuration,
                                              profileName=profileName, userId=userId)
        except Exception as e:
            raise Exception(e)

    def doDeviceLogout(self, deviceName):
        """
        Do Device Logout
        :param deviceName:
        :param userId:
        :return: result dictionary
        """
        try:
            return self.service.doDeviceLogout(deviceName=deviceName)
        except Exception as e:
            raise Exception(e)

    def doDeviceReset(self, deviceName="", uuid=""):
        """
        Do Device Reset
        :param deviceName: device name
        :param uuid: device uuid
        :return: result dictionary
        """
        if deviceName != "" and uuid == "":
            try:
                return self.service.doDeviceReset(deviceName=deviceName, isHardReset=True)
            except Fault as e:
                return e
        elif deviceName == "" and uuid != "":
            try:
                return self.service.doDeviceReset(uuid=uuid, isHardReset=True)
            except Fault as e:
                return e

    def resetSipTrunk(self, name="", uuid=""):
        """
        Reset SIP Trunk
        :param name: device name
        :param uuid: device uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.resetSipTrunk(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.resetSipTrunk(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def getLocation(self, name='', uuid=''):
        """
        Get device pool parameters
        :param name: location name
        :param uuid: location uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.getLocation(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.getLocation(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def addLocation(
            self,
            name,
            kbits=512,
            video_kbits=-1,
            within_audio_bw=512,
            within_video_bw=-1,
            within_immersive_kbits=-1,
    ):
        """
        Add a location
        :param name: Name of the location to add
        :param cucm_version: ucm version
        :param kbits: ucm 8.5
        :param video_kbits: ucm 8.5
        :param within_audio_bw: ucm 10
        :param within_video_bw: ucm 10
        :param within_immersive_kbits: ucm 10
        :return: result dictionary
        """
        if (
                self.version == "8.6"
                or self.version == "9.0"
                or self.version == "9.5"
                or self.version == "10.0"
        ):
            try:
                return self.service.addLocation(
                    {
                        "name": name,
                        # CUCM 8.6
                        "kbits": kbits,
                        "videoKbits": video_kbits,
                    }
                )
            except Fault as e:
                return e
        else:
            try:
                betweenLocations = []
                betweenLocation = {}
                RLocationBetween = {}
                RLocationBetween["locationName"] = "Hub_None"
                RLocationBetween["weight"] = 0
                RLocationBetween["audioBandwidth"] = within_audio_bw
                RLocationBetween["videoBandwidth"] = within_video_bw
                RLocationBetween["immersiveBandwidth"] = within_immersive_kbits
                betweenLocation["betweenLocation"] = RLocationBetween
                betweenLocations.append(betweenLocation)

                return self.service.addLocation(
                    {
                        "name": name,
                        # CUCM 10.6
                        "withinAudioBandwidth": within_audio_bw,
                        "withinVideoBandwidth": within_video_bw,
                        "withinImmersiveKbits": within_immersive_kbits,
                        "betweenLocations": betweenLocations,
                    }
                )
            except Fault as e:
                return e

    def removeLocation(self, name='', uuid=''):
        """
        Delete a location
        :param name: The name of the location to delete
        :param uuid: The uuid of the location to delete
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.removeLocation(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.removeLocation(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def updateLocation(self, **args):
        """
        Update a Location
        :param name:
        :param uuid:
        :param newName:
        :param withinAudioBandwidth:
        :param withinVideoBandwidth:
        :param withImmersiveKbits:
        :param betweenLocations:
        :return:
        """
        try:
            return self.service.updateLocation(**args)
        except Exception as e:
            raise Exception(e)

    def listAllRegions(self, tagfilter={"uuid": "", "name": "", "defaultCodec": ""}, ):
        """
        Get region details
        :param mini: return a list of tuples of region details
        :return: A list of dictionary's
        """
        try:
            RegionList = self.service.listRegion({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]
            if RegionList is not None:
                RegionList = RegionList["region"]
            return RegionList
        except Exception as e:
            raise Exception(e)

    def getRegion(self, name='', uuid=''):
        """
        Get region information
        :param name: Region name
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.getRegion(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.getRegion(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def addRegion(self, name):
        """
        Add a region
        :param name: Name of the region to add
        :return: result dictionary
        """
        try:
            return self.service.addRegion({"name": name})
        except Exception as e:
            raise Exception(e)

    def updateRegion(self, name="", newName="", moh_region=""):
        """
        Update region and assign region to all other regions
        :param name:
        :param uuid:
        :param moh_region:
        :return:
        """
        try:
            return self.service.updateRegion(
                name=name,
                newName=newName,
            )
        except Exception as e:
            raise Exception(e)

    def removeRegion(self, name='', uuid=''):
        """
        Delete a location
        :param name: The name of the region to delete
        :param uuid: The uuid of the region to delete
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.removeRegion(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.removeRegion(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def listAllSrst(self,
                    tagfilter={"uuid": "", "name": "", "port": "", "ipAddress": "", "ipv6Address": "", "SipNetwork": "",
                               "SipPort": "", "srstCertificatePort": "", "isSecure": ""}):
        """
        Get all SRST details
        :param mini: return a list of tuples of SRST details
        :return: A list of dictionary's
        """
        try:
            SRSTList = self.service.listSrst({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]
            if SRSTList is not None:
                SRSTList = SRSTList["srst"]
            return SRSTList
        except Exception as e:
            raise Exception(e)

    def getSrst(self, name):
        """
        Get SRST information
        :param name: SRST name
        :return: result dictionary
        """
        try:
            return self.service.getSrst(name=name)['return']['srst']
        except Exception as e:
            raise Exception(e)

    def addSrst(self, name, ip_address, port=2000, sip_port=5060):
        """
        Add SRST
        :param name: SRST name
        :param ip_address: SRST ip address
        :param port: SRST port
        :param sip_port: SIP port
        :return: result dictionary
        """
        try:
            return self.service.addSrst(
                {
                    "name": name,
                    "port": port,
                    "ipAddress": ip_address,
                    "SipPort": sip_port,
                }
            )
        except Exception as e:
            raise Exception(e)

    def removeSrst(self, name):
        """
        Delete a SRST
        :param name: The name of the SRST to delete
        :return: result dictionary
        """
        try:
            return self.service.removeSrst(name=name)
        except Exception as e:
            raise Exception(e)

    def updateSrst(self, name, newName=""):
        """
        Update a SRST
        :param srst: The name of the SRST to update
        :param newName: The new name of the SRST
        :return: result dictionary
        """
        try:
            return self.service.updateSrst(name=name, newName=newName)
        except Exception as e:
            raise Exception(e)

    def listAllDevicePools(
            self,
            tagfilter={
                "name": "",
                "dateTimeSettingName": "",
                "callManagerGroupName": "",
                "mediaResourceListName": "",
                "regionName": "",
                "srstName": "",
                # 'localRouteGroup': [0],
            },
    ):
        """
        Get a dictionary of device pools
        :param mini: return a list of tuples of device pool info
        :return: a list of dictionary's of device pools information
        """
        try:
            DevicePoolList = self.service.listDevicePool({"name": "%"}, returnedTags="", )[
                "return"
            ]
            if DevicePoolList is not None:
                DevicePoolList = DevicePoolList["devicePool"]
            return DevicePoolList
        except Exception as e:
            raise Exception(e)

    def getDevicePool(self, name):
        """
        Get device pool parameters
        :param name: device pool name
        :return: result dictionary
        """
        try:
            return self.service.getDevicePool(name=name)['return']['devicePool']
        except Exception as e:
            raise Exception(e)

    def addDevicePool(
            self,
            name,
            date_time_group="CMLocal",
            region="Default",
            location="Hub_None",
            route_group="",
            media_resource_group_list="",
            srst="Disable",
            cm_group="Default",
            network_locale="",
    ):

        """
        Add a device pool
        :param device_pool: Device pool name
        :param date_time_group: Date time group name
        :param region: Region name
        :param location: Location name
        :param route_group: Route group name
        :param media_resource_group_list: Media resource group list name
        :param srst: SRST name
        :param cm_group: CM Group name
        :param network_locale: Network locale name
        :return: result dictionary
        """
        try:
            return self.service.addDevicePool(
                {
                    "name": name,
                    "dateTimeSettingName": date_time_group,  # update to state timezone
                    "regionName": region,
                    "locationName": location,
                    "localRouteGroup": {
                        "name": "Standard Local Route Group",
                        "value": route_group,
                    },
                    "mediaResourceListName": media_resource_group_list,
                    "srstName": srst,
                    "callManagerGroupName": cm_group,
                    "networkLocale": network_locale,
                }
            )
        except Exception as e:
            raise Exception(e)

    def updateDevicePool(self, **args):
        """
        Update a device pools route group and media resource group list
        :param name:
        :param uuid:
        :param newName:
        :param mediaResourceGroupListName:
        :param dateTimeSettingName:
        :param callManagerGroupName:
        :param regionName:
        :param locationName:
        :param networkLocale:
        :param srstName:
        :param localRouteGroup:
        :param elinGroup:
        :param media_resource_group_list:
        :return:
        """
        try:
            return self.service.updateDevicePool(**args)
        except Exception as e:
            raise Exception(e)

    def removeDevicePool(self, name):
        """
        Delete a Device pool
        :param device_pool: The name of the Device pool to delete
        :return: result dictionary
        """
        try:
            return self.service.removeDevicePool(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllConferenceBridges(
            self,
            tagfilter={
                "name": "",
                "description": "",
                "devicePoolName": "",
                "locationName": "",
            },
    ):
        """
        Get conference bridges
        :param mini: List of tuples of conference bridge details
        :return: results dictionary
        """
        try:
            ConferenceBridgeList = self.service.listConferenceBridge(
                {"name": "%"}, returnedTags=tagfilter,
            )["return"]
            if ConferenceBridgeList is not None:
                ConferenceBridgeList = ConferenceBridgeList["conferenceBridge"]
            return ConferenceBridgeList
        except Exception as e:
            raise Exception(e)

    def getConferenceBridge(self, name):
        """
        Get conference bridge parameters
        :param name: conference bridge name
        :return: result dictionary
        """
        try:
            return self.service.getConferenceBridge(name=name)['return']['conferenceBridge']
        except Exception as e:
            raise Exception(e)

    def addConferenceBridge(
            self,
            name,
            description="",
            device_pool="Default",
            location="Hub_None",
            product="Cisco IOS Enhanced Conference Bridge",
            security_profile="Non Secure Conference Bridge",
    ):
        """
        Add a conference bridge
        :param conference_bridge: Conference bridge name. Cannot be longer than 15 characters
        :param description: Conference bridge description
        :param device_pool: Device pool name
        :param location: Location name
        :param product: Conference bridge type
        :param security_profile: Conference bridge security type
        :return: result dictionary
        """
        try:
            return self.service.addConferenceBridge(
                {
                    "name": name,
                    "description": description,
                    "devicePoolName": device_pool,
                    "locationName": location,
                    "product": product,
                    "securityProfileName": security_profile,
                }
            )
        except Exception as e:
            raise Exception(e)

    def updateConferenceBridge(self, **args):
        """
        Update a conference bridge
        :param name: Conference bridge name. Cannot be longer than 15 characters
        :param newName: New Conference bridge name. Cannot be longer than 15 characters
        :param description: Conference bridge description
        :param device_pool: Device pool name
        :param location: Location name
        :param product: Conference bridge type
        :param security_profile: Conference bridge security type
        :return: result dictionary
        """
        try:
            return self.service.updateConferenceBridge(**args)
        except Exception as e:
            raise Exception(e)

    def removeConferenceBridge(self, name):
        """
        Delete a Conference bridge
        :param name: The name of the Conference bridge to delete
        :return: result dictionary
        """
        try:
            return self.service.removeConferenceBridge(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllTranscoders(
            self, tagfilter={"name": "", "description": "", "devicePoolName": ""}
    ):
        """
        Get transcoders
        :param mini: List of tuples of transcoder details
        :return: results dictionary
        """
        try:
            TranscoderList = self.service.listTranscoder({"name": "%"}, returnedTags=tagfilter, )[
                "return"
            ]
            if TranscoderList is not None:
                TranscoderList = TranscoderList["transcoder"]
            return TranscoderList
        except Exception as e:
            raise Exception(e)

    def getTranscoder(self, name):
        """
        Get conference bridge parameters
        :param name: transcoder name
        :return: result dictionary
        """
        try:
            return self.service.getTranscoder(name=name)
        except Exception as e:
            raise Exception(e)

    def addTranscoder(
            self,
            name,
            description="",
            device_pool="Default",
            product="Cisco IOS Enhanced Media Termination Point",
    ):
        """
        Add a transcoder
        :param transcoder: Transcoder name. Cannot be longer than 15 characters
        :param description: Transcoder description
        :param device_pool: Transcoder device pool
        :param product: Trancoder product
        :return: result dictionary
        """
        try:
            return self.service.addTranscoder(
                {
                    "name": name,
                    "description": description,
                    "devicePoolName": device_pool,
                    "product": product,
                }
            )
        except Exception as e:
            raise Exception(e)

    def updateTranscoder(self, **args):
        """
        Add a transcoder
        :param name: Transcoder name. Cannot be longer than 15 characters
        :param newName: New Transcoder name. Cannot be longer than 15 characters
        :param description: Transcoder description
        :param device_pool: Transcoder device pool
        :param product: Trancoder product
        :return: result dictionary
        """
        try:
            return self.service.updateTranscoder(**args)
        except Exception as e:
            raise Exception(e)

    def removeTranscoder(self, name):
        """
        Delete a Transcoder
        :param name: The name of the Transcoder to delete
        :return: result dictionary
        """
        try:
            return self.service.removeTranscoder(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllMTPs(self, tagfilter={"name": "", "description": "", "devicePoolName": ""}):
        """
        Get mtps
        :param mini: List of tuples of transcoder details
        :return: results dictionary
        """
        try:
            MTPList = self.service.listMtp({"name": "%"}, returnedTags=tagfilter, )[
                "return"
            ]
            if MTPList is not None:
                MTPList = MTPList["mtp"]
            return MTPList
        except Exception as e:
            raise Exception(e)

    def getMtp(self, name):
        """
        Get mtp parameters
        :param name: transcoder name
        :return: result dictionary
        """
        try:
            return self.service.getMtp(name=name)
        except Exception as e:
            raise Exception(e)

    def addMtp(
            self,
            name,
            description="",
            device_pool="Default",
            mtpType="Cisco IOS Enhanced Media Termination Point",
    ):
        """
        Add an mtp
        :param name: MTP name
        :param description: MTP description
        :param device_pool: MTP device pool
        :param mtpType: MTP Type
        :return: result dictionary
        """
        try:
            return self.service.addMtp(
                {
                    "name": name,
                    "description": description,
                    "devicePoolName": device_pool,
                    "mtpType": mtpType,
                }
            )
        except Exception as e:
            raise Exception(e)

    def updateMtp(self, **args):
        """
        Update an MTP
        :param name: MTP name
        :param newName: New MTP name
        :param description: MTP description
        :param device_pool: MTP device pool
        :param mtpType: MTP Type
        :return: result dictionary
        """
        try:
            return self.service.updateMtp(**args)
        except Exception as e:
            raise Exception(e)

    def removeMtp(self, name):
        """
        Delete an MTP
        :param name: The name of the Transcoder to delete
        :return: result dictionary
        """
        try:
            return self.service.removeMtp(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllGateways(
            self,
            tagfilter={
                "domainName": "",
                "description": "",
                "product": "",
                "protocol": "",
                "callManagerGroupName": "",
                "scratch": "",
                "loadInformation": "",

            },
    ):
        """
        Get Gateways
        :param mini: List of tuples of Gateway details
        :return: results dictionary
        """
        try:
            GatewayList = self.service.listGateway({"domainName": "%"}, returnedTags=tagfilter, )[
                "return"
            ]
            if GatewayList is not None:
                GatewayList = GatewayList
            return GatewayList
        except Exception as e:
            raise Exception(e)

    def getGateway(self, deviceName):
        """
        Get Gateway parameters
        :param deviceName: Gateway name
        :return: result dictionary
        """
        try:
            return self.service.getGateway(domainName=deviceName)
        except Exception as e:
            raise Exception(e)

    def getGatewayAnalogAccess(self, name):
        """
        Get Gateway parameters
        :param name: Gateway name
        :return: result dictionary
        """
        try:
            return self.service.getGateway(domainName=deviceName)
        except Exception as e:
            raise Exception(e)

    def listAllH323Gateways(
            self,
            tagfilter={
                "name": "",
                "description": "",
                "devicePoolName": "",
                "locationName": "",
                "sigDigits": "",
            },
    ):
        """
        Get H323 Gateways
        :param mini: List of tuples of H323 Gateway details
        :return: results dictionary
        """
        try:
            H323GatewayList = self.service.listH323Gateway({"name": "%"}, returnedTags=tagfilter, )[
                "return"
            ]
            if H323GatewayList is not None:
                H323GatewayList = H323GatewayList["h323Gateway"]
            return H323GatewayList
        except Exception as e:
            raise Exception(e)



    def getH323Gateway(self, name):
        """
        Get H323 Gateway parameters
        :param name: H323 Gateway name
        :return: result dictionary
        """
        try:
            return self.service.getH323Gateway(name=name)
        except Exception as e:
            raise Exception(e)

    def addH323Gateway(self,
                       **args):  # TODO: Find the correct protocol for use with this function. No combiniations found were successful.
        """
        Add H323 gateway
        :param h323_gateway:
        :param description:
        :param device_pool:
        :param location:
        :param media_resource_group_list: Media resource group list name
        :param prefix_dn:
        :param sig_digits: Significant digits, 99 = ALL
        :param css:
        :param aar_css:
        :param aar_neighborhood:
        :param product:
        :param protocol:
        :param protocol_side:
        :param pstn_access:
        :param redirect_in_num_ie:
        :param redirect_out_num_ie:
        :param cld_party_ie_num_type:
        :param clng_party_ie_num_type:
        :param clng_party_nat_pre:
        :param clng_party_inat_prefix:
        :param clng_party_unknown_prefix:
        :param clng_party_sub_prefix:
        :param clng_party_nat_strip_digits:
        :param clng_party_inat_strip_digits:
        :param clng_party_unknown_strip_digits:
        :param clng_party_sub_strip_digits:
        :param clng_party_nat_trans_css:
        :param clng_party_inat_trans_css:
        :param clng_party_unknown_trans_css:
        :param clng_party_sub_trans_css:
        :return:
        """
        try:
            return self.service.addH323Gateway(**args)
        except Exception as e:
            raise Exception(e)

    def updateH323Gateway(self, **args):
        """
        :param name:
        :return:
        """
        try:
            return self.service.updateH323Gateway(**args)
        except Exception as e:
            raise Exception(e)

    def removeH323Gateway(self, name):
        """
        Delete a H323 gateway
        :param name: The name of the H323 gateway to delete
        :return: result dictionary
        """
        try:
            return self.service.removeH323Gateway(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllRouteGroups(self, tagfilter={"name": "", "distributionAlgorithm": ""}):
        """
        Get route groups
        :param mini: return a list of tuples of route group details
        :return: A list of dictionary's
        """
        try:
            RouteGroupList = self.service.listRouteGroup({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]
            if RouteGroupList is not None:
                RouteGroupList = RouteGroupList["routeGroup"]
            return RouteGroupList
        except Exception as e:
            raise Exception(e)

    def getRouteGroup(self, name='', uuid=''):
        """
        Get route group
        :param name: route group name
        :param uuid: route group uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.getRouteGroup(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.getRouteGroup(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def addRouteGroup(self, name, distribution_algorithm="Top Down", members=[]):
        """
        Add a route group
        :param name: Route group name
        :param distribution_algorithm: Top Down/Circular
        :param members: A list of devices to add (must already exist DUH!)
        """
        req = {
            "name": name,
            "distributionAlgorithm": distribution_algorithm,
            "members": {"member": []},
        }

        if members:
            [
                req["members"]["member"].append(
                    {
                        "deviceName": i,
                        "deviceSelectionOrder": members.index(i) + 1,
                        "port": 0,
                    }
                )
                for i in members
            ]

        try:
            return self.service.addRouteGroup(req)
        except Exception as e:
            raise Exception(e)

    def removeRouteGroup(self, **args):
        """
        Delete a Route group
        :param name: The name of the Route group to delete
        :return: result dictionary
        """
        try:
            return self.service.removeRouteGroup(**args)
        except Exception as e:
            raise Exception(e)

    def updateRouteGroup(self, **args):
        """
        Update a Route group
        :param name: The name of the Route group to update
        :param distribution_algorithm: Top Down/Circular
        :param members: A list of devices to add (must already exist DUH!)
        :return: result dictionary
        """
        try:
            return self.service.updateRouteGroup(**args)
        except Exception as e:
            raise Exception(e)

    def listAllRouteLists(self, tagfilter={"name": "", "description": ""}):
        """
        Get route lists
        :param mini: return a list of tuples of route list details
        :return: A list of dictionary's
        """
        try:
            RouteListList = self.service.listRouteList({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]
            if RouteListList is not None:
                RouteListList = RouteListList["routeList"]
            return RouteListList

        except Exception as e:
            raise Exception(e)

    def getRouteList(self, name='', uuid=''):
        """
        Get route list
        :param name: route list name
        :param uuid: route list uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.getRouteList(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.getRouteList(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def addRouteList(
            self,
            name,
            description="",
            cm_group_name="Default",
            route_list_enabled="true",
            run_on_all_nodes="false",
            members=[],
    ):

        """
        Add a route list
        :param name: Route list name
        :param description: Route list description
        :param cm_group_name: Route list call mangaer group name
        :param route_list_enabled: Enable route list
        :param run_on_all_nodes: Run route list on all nodes
        :param members: A list of route groups
        :return: Result dictionary
        """
        req = {
            "name": name,
            "description": description,
            "callManagerGroupName": cm_group_name,
            "routeListEnabled": route_list_enabled,
            "runOnEveryNode": run_on_all_nodes,
            "members": {"member": []},
        }

        if members:
            [
                req["members"]["member"].append(
                    {
                        "routeGroupName": i,
                        "selectionOrder": members.index(i) + 1,
                        "calledPartyTransformationMask": "",
                        "callingPartyTransformationMask": "",
                        "digitDiscardInstructionName": "",
                        "callingPartyPrefixDigits": "",
                        "prefixDigitsOut": "",
                        "useFullyQualifiedCallingPartyNumber": "Default",
                        "callingPartyNumberingPlan": "Cisco CallManager",
                        "callingPartyNumberType": "Cisco CallManager",
                        "calledPartyNumberingPlan": "Cisco CallManager",
                        "calledPartyNumberType": "Cisco CallManager",
                    }
                )
                for i in members
            ]

        try:
            return self.service.addRouteList(req)
        except Exception as e:
            raise Exception(e)

    def removeRouteList(self, **args):
        """
        Delete a Route list
        :param name: The name of the Route list to delete
        :param uuid: The uuid of the Route list to delete
        :return: result dictionary
        """
        try:
            return self.service.removeRouteList(**args)
        except Exception as e:
            raise Exception(e)

    def updateRouteList(self, **args):
        """
        Update a Route list
        :param name: The name of the Route list to update
        :param uuid: The uuid of the Route list to update
        :param description: Route list description
        :param cm_group_name: Route list call mangaer group name
        :param route_list_enabled: Enable route list
        :param run_on_all_nodes: Run route list on all nodes
        :param members: A list of route groups
        :return: result dictionary
        """
        try:
            return self.service.updateRouteList(**args)
        except Exception as e:
            raise Exception(e)

    def listAllPartitions(self, tagfilter={"name": "", "description": ""}):
        """
        Get partitions
        :param mini: return a list of tuples of partition details
        :return: A list of dictionary's
        """
        try:
            return self.service.listRoutePartition(
                {"name": "%"}, returnedTags=tagfilter
            )["return"]["routePartition"]
        except Exception as e:
            raise Exception(e)

    def getRoutePartition(self, name='', uuid=''):
        """
        Get partition details
        :param partition: Partition name
        :param uuid: UUID name
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.getRoutePartition(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.getRoutePartition(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def addRoutePartition(self, name, description="", timeScheduleName="All the time"):
        """
        Add a partition
        :param name: Name of the partition to add
        :param description: Partition description
        :param time_schedule_name: Name of the time schedule to use
        :return: result dictionary
        """
        try:
            return self.service.addRoutePartition(
                {
                    "name": name,
                    "description": description,
                    "timeScheduleIdName": timeScheduleName,
                }
            )
        except Exception as e:
            raise Exception(e)

    def removeRoutePartition(self, name='', uuid=''):
        """
        Delete a partition
        :param partition: The name of the partition to delete
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.removeRoutePartition(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.removeRoutePartition(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def updateRoutePartition(self, **args):
        """
        Update calling search space
        :param uuid: CSS UUID
        :param name: CSS Name
        :param description:
        :param newName:
        :param timeScheduleIdName:
        :param useOriginatingDeviceTimeZone:
        :param timeZone:
        :return: result dictionary
        """
        try:
            return self.service.updateRoutePartition(**args)
        except Exception as e:
            raise Exception(e)

    def listAllCallingSearchSpaces(self, tagfilter={"name": "", "description": ""}):
        """
        Get calling search spaces
        :param mini: return a list of tuples of css details
        :return: A list of dictionary's
        """
        try:
            SearchSpaceList = self.service.listCss({"name": "%"}, returnedTags=tagfilter)["return"][
                "css"
            ]
            if SearchSpaceList is not None:
                SearchSpaceList = SearchSpaceList["css"]
            return SearchSpaceList
        except Exception as e:
            raise Exception(e)

    def getCallingSearchSpace(self, name='', uuid=''):
        """
        Get Calling search space details
        :param name: Calling search space name
        :param uuid: Calling search space uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.getCss(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.getCss(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def addCallingSearchSpace(self, name, description="", members=[]):
        """
        Add a Calling search space
        :param name: Name of the CSS to add
        :param description: Calling search space description
        :param members: A list of partitions to add to the CSS
        :return: result dictionary
        """
        req = {
            "name": name,
            "description": description,
            "members": {"member": []},
        }
        if members:
            [
                req["members"]["member"].append(
                    {"routePartitionName": i, "index": members.index(i) + 1, }
                )
                for i in members
            ]

        try:
            return self.service.addCss(req)
        except Exception as e:
            raise Exception(e)

    def removeCallingSearchSpace(self, name='', uuid=''):
        """
        Delete a Calling search space
        :param calling_search_space: The name of the partition to delete
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.removeCss(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.removeCss(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def updateCallingSearchSpace(self, **args):
        """
        Update calling search space
        :param uuid: CSS UUID
        :param name: CSS Name
        :param description:
        :param newName:
        :param members:
        :param removeMembers:
        :param addMembers:
        :return: result dictionary
        """
        try:
            return self.service.updateCss(**args)
        except Exception as e:
            raise Exception(e)

    def listAllRoutePatterns(
            self, tagfilter={"pattern": "", "description": "", "uuid": ""}
    ):
        """
        Get route patterns
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            RoutePatternList = self.service.listRoutePattern(
                {"pattern": "%"}, returnedTags=tagfilter,
            )["return"]
            if RoutePatternList is not None:
                RoutePatternList = RoutePatternList["routePattern"]
            return RoutePatternList
        except Exception as e:
            raise Exception(e)

    def getRoutePattern(self, pattern="", uuid=""):
        """
        Get route pattern
        :param pattern: route pattern
        :param uuid: route pattern uuid
        :return: result dictionary
        """
        if uuid == "" and pattern != "":
            # Cant get pattern directly so get UUID first
            try:
                uuid = self.service.listRoutePattern(
                    {"pattern": pattern}, returnedTags={"uuid": ""}
                )
            except Fault as e:
                return e
            if "return" in uuid and uuid["return"] is not None:
                uuid = uuid["return"]["routePattern"][0]["uuid"]
                try:
                    return self.service.getRoutePattern(uuid=uuid)
                except Fault as e:
                    return e

        elif uuid != "" and pattern == "":
            try:
                return self.service.getRoutePattern(uuid=uuid)
            except Fault as e:
                return e

    def addRoutePattern(
            self,
            pattern,
            gateway="",
            route_list="",
            description="",
            partition="",
            blockEnable=False,
            patternUrgency=False,
            releaseClause="Call Rejected",
            req=None
    ):
        """
        Add a route pattern
        :param pattern: Route pattern - required
        :param gateway: Destination gateway - required
        :param route_list: Destination route list - required
               Either a gateway or route list can be used at the same time
        :param description: Route pattern description
        :param partition: Route pattern partition
        :param req: Provide your own dictionary of values to access full features of the AXL call.
        :return: result dictionary
        """
        if req is None:
            req = {
                "pattern": pattern,
                "description": description,
                "destination": {},
                "routePartitionName": partition,
                "blockEnable": blockEnable,
                "releaseClause": releaseClause,
                "useCallingPartyPhoneMask": "Default",
                "networkLocation": "OnNet",
            }

        if gateway == "" and route_list == "":
            return "Either a gateway OR route list, is a required parameter"

        elif gateway != "" and route_list != "":
            return "Enter a gateway OR route list, not both"

        elif gateway != "":
            req["destination"].update({"gatewayName": gateway})
        elif route_list != "":
            req["destination"].update({"routeListName": route_list})
        try:
            return self.service.addRoutePattern(req)
        except Exception as e:
            raise Exception(e)

    def removeRoutePattern(self, pattern, partition):
        """
        Delete a route pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the route to delete
        :param partition: The name of the partition
        :return: result dictionary
        """
        try:
            return self.service.removeRoutePattern(pattern=pattern, partition=partition)
        except Exception as e:
            raise Exception(e)

    def updateRoutePattern(self, **args):
        """
        Update a route pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the route to update
        :param partition: The name of the partition
        :param gateway: Destination gateway - required
        :param route_list: Destination route list - required
               Either a gateway or route list can be used at the same time
        :param description: Route pattern description
        :param partition: Route pattern partition
        :return: result dictionary
        """
        try:
            return self.service.updateRoutePattern(**args)
        except Exception as e:
            raise Exception(e)

    def listAllMediaResourceGroups(self, tagfilter={"name": "", "description": ""}):
        """
        Get media resource groups
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            MediaResourceGroupList = self.service.listMediaResourceGroup(
                {"name": "%"}, returnedTags=tagfilter
            )["return"]
            if MediaResourceGroupList is not None:
                MediaResourceGroupList = MediaResourceGroupList["mediaResourceGroup"]
            return MediaResourceGroupList
        except Exception as e:
            raise Exception(e)

    def getMediaResourceGroup(self, name):
        """
        Get a media resource group details
        :param media_resource_group: Media resource group name
        :return: result dictionary
        """
        try:
            return self.service.getMediaResourceGroup(name=name)
        except Exception as e:
            raise Exception(e)

    def addMediaResourceGroup(
            self, name, description="", multicast="false", members=[]
    ):
        """
        Add a media resource group
        :param name: Media resource group name
        :param description: Media resource description
        :param multicast: Mulicast enabled
        :param members: Media resource group members
        :return: result dictionary
        """
        req = {
            "name": name,
            "description": description,
            "multicast": multicast,
            "members": {"member": []},
        }

        if members:
            [req["members"]["member"].append({"deviceName": i}) for i in members]

        try:
            return self.service.addMediaResourceGroup(req)
        except Exception as e:
            raise Exception(e)

    def updateMediaResourceGroup(self, **args):
        """
        Update a media resource group
        :param name: Media resource group name
        :param description: Media resource description
        :param multicast: Mulicast enabled
        :param members: Media resource group members
        :return: result dictionary
        """
        try:
            return self.service.updateMediaResourceGroup(**args)
        except Exception as e:
            raise Exception(e)

    def removeMediaResourceGroup(self, name):
        """
        Delete a Media resource group
        :param media_resource_group: The name of the media resource group to delete
        :return: result dictionary
        """
        try:
            return self.service.removeMediaResourceGroup(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllMediaResourceGroupLists(self, tagfilter={"name": ""}):
        """
        Get media resource groups
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            MediaResourceListList = self.service.listMediaResourceList(
                {"name": "%"}, returnedTags=tagfilter
            )["return"]
            if MediaResourceListList is not None:
                MediaResourceListList = MediaResourceListList["mediaResourceList"]
            return MediaResourceListList

        except Exception as e:
            raise Exception(e)

    def getMediaResourceList(self, name):
        """
        Get a media resource group list details
        :param name: Media resource group list name
        :return: result dictionary
        """
        try:
            return self.service.getMediaResourceList(name=name)
        except Exception as e:
            raise Exception(e)

    def addMediaResourceList(self, name, members=[]):
        """
        Add a media resource group list
        :param media_resource_group_list: Media resource group list name
        :param members: A list of members
        :return:
        """
        req = {"name": name, "members": {"member": []}}

        if members:
            [
                req["members"]["member"].append(
                    {"order": members.index(i), "mediaResourceGroupName": i}
                )
                for i in members
            ]
        try:
            return self.service.addMediaResourceList(req)
        except Exception as e:
            raise Exception(e)

    def updateMediaResourceList(self, **args):
        """
        Update a media resource group list
        :param name: Media resource group name
        :param description: Media resource description
        :param multicast: Mulicast enabled
        :param members: Media resource group members
        :return: result dictionary
        """
        try:
            return self.service.updateMediaResourceList(**args)
        except Exception as e:
            raise Exception(e)

    def removeMediaResourceList(self, name):
        """
        Delete a Media resource group list
        :param name: The name of the media resource group list to delete
        :return: result dictionary
        """
        try:
            return self.service.removeMediaResourceList(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllDirectoryNumbers(
            self, tagfilter={"pattern": "", "description": "", "routePartitionName": "", }
    ):
        """
        Get directory numbers
        :param mini: return a list of tuples of directory number details
        :return: A list of dictionary's
        """
        try:
            ListLineList = self.service.listLine({"pattern": "%"}, returnedTags=tagfilter, )[
                "return"
            ]
            if ListLineList is not None:
                ListLineList = ListLineList["line"]
            return ListLineList

        except Exception as e:
            raise Exception(e)

    def getDirectoryNumber(self, pattern, partition):
        """
        Get directory number details
        :param name:
        :param partition:
        :return: result dictionary
        """
        try:
            return self.service.getLine(pattern=pattern, routePartitionName=partition)
        except Exception as e:
            raise Exception(e)

    def addDirectoryNumber(
            self,
            pattern,
            partition="",
            description="",
            alerting_name="",
            ascii_alerting_name="",
            shared_line_css="",
            aar_neighbourhood="",
            call_forward_css="",
            vm_profile_name="NoVoiceMail",
            aar_destination_mask="",
            call_forward_destination="",
            forward_all_to_vm="false",
            forward_all_destination="",
            forward_to_vm="false",
    ):
        """
        Add a directory number
        :param pattern: Directory number
        :param partition: Route partition name
        :param description: Directory number description
        :param alerting_name: Alerting name
        :param ascii_alerting_name: ASCII alerting name
        :param shared_line_css: Calling search space
        :param aar_neighbourhood: AAR group
        :param call_forward_css: Call forward calling search space
        :param vm_profile_name: Voice mail profile
        :param aar_destination_mask: AAR destination mask
        :param call_forward_destination: Call forward destination
        :param forward_all_to_vm: Forward all to voice mail checkbox
        :param forward_all_destination: Forward all destination
        :param forward_to_vm: Forward to voice mail checkbox
        :return: result dictionary
        """
        try:
            return self.service.addLine(
                {
                    "pattern": pattern,
                    "routePartitionName": partition,
                    "description": description,
                    "alertingName": alerting_name,
                    "asciiAlertingName": ascii_alerting_name,
                    "voiceMailProfileName": vm_profile_name,
                    "shareLineAppearanceCssName": shared_line_css,
                    "aarNeighborhoodName": aar_neighbourhood,
                    "aarDestinationMask": aar_destination_mask,
                    "usage": "Device",
                    "callForwardAll": {
                        "forwardToVoiceMail": forward_all_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": forward_all_destination,
                    },
                    "callForwardBusy": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardBusyInt": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardNoAnswer": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardNoAnswerInt": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardNoCoverage": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardNoCoverageInt": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardOnFailure": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardNotRegistered": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                    "callForwardNotRegisteredInt": {
                        "forwardToVoiceMail": forward_to_vm,
                        "callingSearchSpaceName": call_forward_css,
                        "destination": call_forward_destination,
                    },
                }
            )
        except Exception as e:
            raise Exception(e)

    def removeDirectoryNumber(self, pattern, routePartitionName):
        """
        Delete a directory number
        :param directory_number: The name of the directory number to delete
        :return: result dictionary
        """
        try:
            return self.service.removeLine(
                pattern=pattern, routePartitionName=routePartitionName
            )
        except Exception as e:
            raise Exception(e)

    def updateDirectoryNumber(self, **args):
        """
        Update a directory number
        :param pattern: Directory number
        :param partition: Route partition name
        :param description: Directory number description
        :param alerting_name: Alerting name
        :param ascii_alerting_name: ASCII alerting name
        :param shared_line_css: Calling search space
        :param aar_neighbourhood: AAR group
        :param call_forward_css: Call forward calling search space
        :param vm_profile_name: Voice mail profile
        :param aar_destination_mask: AAR destination mask
        :param call_forward_destination: Call forward destination
        :param forward_all_to_vm: Forward all to voice mail checkbox
        :param forward_all_destination: Forward all destination
        :param forward_to_vm: Forward to voice mail checkbox
        :return: result dictionary
        """
        try:
            return self.service.updateLine(**args)
        except Exception as e:
            raise Exception(e)

    def listAllCTIRoutePoints(self, tagfilter={"name": "", "description": ""}):
        """
        Get CTI route points
        :param mini: return a list of tuples of CTI route point details
        :return: A list of dictionary's
        """
        try:
            CTIRoutePointList = self.service.listCtiRoutePoint({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]
            if CTIRoutePointList is not None:
                CTIRoutePointList = CTIRoutePointList["ctiRoutePoint"]
            return CTIRoutePointList
        except Exception as e:
            raise Exception(e)

    def getCtiRoutePoint(self, name='', uuid=''):
        """
        Get CTI route point details
        :param name: CTI route point name
        :param uuid: CTI route point uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.service.getCtiRoutePoint(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.service.getCtiRoutePoint(uuid=uuid)
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR name. Not both.")

    def addCtiRoutePoint(
            self,
            name,
            description="",
            device_pool="Default",
            location="Hub_None",
            common_device_config="",
            css="",
            product="CTI Route Point",
            dev_class="CTI Route Point",
            protocol="SCCP",
            protocol_slide="User",
            use_trusted_relay_point="Default",
            lines=[],
    ):
        """
        Add CTI route point
        lines should be a list of tuples containing the pattern and partition
        EG: [('77777', 'AU_PHONE_PT')]
        :param name: CTI route point name
        :param description: CTI route point description
        :param device_pool: Device pool name
        :param location: Location name
        :param common_device_config: Common device config name
        :param css: Calling search space name
        :param product: CTI device type
        :param dev_class: CTI device type
        :param protocol: CTI protocol
        :param protocol_slide: CTI protocol slide
        :param use_trusted_relay_point: Use trusted relay point: (Default, On, Off)
        :param lines: A list of tuples of [(directory_number, partition)]
        :return:
        """

        req = {
            "name": name,
            "description": description,
            "product": product,
            "class": dev_class,
            "protocol": protocol,
            "protocolSide": protocol_slide,
            "commonDeviceConfigName": common_device_config,
            "callingSearchSpaceName": css,
            "devicePoolName": device_pool,
            "locationName": location,
            "useTrustedRelayPoint": use_trusted_relay_point,
            "lines": {"line": []},
        }

        if lines:
            [
                req["lines"]["line"].append(
                    {
                        "index": lines.index(i) + 1,
                        "dirn": {"pattern": i[0], "routePartitionName": i[1]},
                    }
                )
                for i in lines
            ]

        try:
            return self.service.addCtiRoutePoint(req)
        except Exception as e:
            raise Exception(e)

    def removeCtiRoutePoint(self, name):
        """
        Delete a CTI route point
        :param cti_route_point: The name of the CTI route point to delete
        :return: result dictionary
        """
        try:
            return self.service.removeCtiRoutePoint(name=name)
        except Exception as e:
            raise Exception(e)

    def updateCtiRoutePoint(self, **args):
        """
        Add CTI route point
        lines should be a list of tuples containing the pattern and partition
        EG: [('77777', 'AU_PHONE_PT')]
        :param name: CTI route point name
        :param description: CTI route point description
        :param device_pool: Device pool name
        :param location: Location name
        :param common_device_config: Common device config name
        :param css: Calling search space name
        :param product: CTI device type
        :param dev_class: CTI device type
        :param protocol: CTI protocol
        :param protocol_slide: CTI protocol slide
        :param use_trusted_relay_point: Use trusted relay point: (Default, On, Off)
        :param lines: A list of tuples of [(directory_number, partition)]
        :return:
        """
        try:
            return self.service.updateCtiRoutePoint(**args)
        except Exception as e:
            raise Exception(e)

    def listAllPhones(self, query={"name": "%"}, tagfilter={
            "name": "",
            "product": "",
            "description": "",
            "protocol": "",
            "locationName": "",
            "callingSearchSpaceName": ""
        }, returnAllTags=False):
        """
        :param query: returns all phones by default. This can be upated to only return certain phones. Example: query={"name": "A%"}, this would only return phones with device names that begin with A.
        :param tagfilter: The tags that should be returned for each phone. More tags will result in slower processing of the request.
        :param returnAllTags: Boolean to determine if all available tags should be returned. Defaults to False.
        :type returnAllTags: bool
        :return:
        """
        if returnAllTags:
            tagfilter = {
                "name": "",
                "product": "",
                "description": "",
                "model": "",
                "class": "",
                "protocolSide": "",
                "devicePoolName": "",
                "commonPhoneConfigName": "",
                "commonDeviceConfigName": "",
                "networkLocation": "",
                "mediaResourceListName": "",
                "networkHoldMohAudioSourceId": "",
                "automatedAlternateRoutingCssName": "",
                "aarNeighborhoodName": "",
                "loadInformation": "",
                "protocol": "",
                "locationName": "",
                "callingSearchSpaceName": "",
                "traceFlag": "",
                "mlppIndicationStatus": "",
                "preemption": "",
                "useTrustedRelayPoint": "",
                "retryVideoCallAsAudio": "",
                "securityProfileName": "",
                "sipProfileName": "",
                "cgpnTransformationCssName": "",
                "useDevicePoolCgpnTransformCss": "",
                "geoLocationName": "",
                "geoLocationFilterName": "",
                "sendGeoLocation": "",
                "numberOfButtons": "",
                "phoneTemplateName": "",
                "primaryPhoneName": "",
                "ringSettingIdleBlfAudibleAlert": "",
                "ringSettingBusyBlfAudibleAlert": "",
                "userLocale": "",
                "networkLocale": "",
                "idleTimeout": "",
                "authenticationUrl": "",
                "directoryUrl": "",
                "idleUrl": "",
                "informationUrl": "",
                "messagesUrl": "",
                "proxyServerUrl": "",
                "softkeyTemplateName": "",
                "loginUserId": "",
                "defaultProfileName": "",
                "enableExtensionMobility": "",
                "currentProfileName": "",
                "loginTime": "",
                "loginDuration": "",
                "currentConfig": "",
                "singleButtonBarge": "",
                "joinAcrossLines": "",
                "builtInBridgeStatus": "",
                "callInfoPrivacyStatus": "",
                "hlogStatus": "",
                "ownerUserName": "",
                "ignorePresentationIndicators": "",
                "packetCaptureMode": "",
                "packetCaptureDuration": "",
                "subscribeCallingSearchSpaceName": "",
                "rerouteCallingSearchSpaceName": "",
                "allowCtiControlFlag": "",
                "presenceGroupName": "",
                "unattendedPort": "",
                "requireDtmfReception": "",
                "rfc2833Disabled": "",
                "certificateOperation": "",
                "authenticationMode": "",
                "keySize": "",
                "keyOrder": "",
                "ecKeySize": "",
                "authenticationString": "",
                "certificateStatus": "",
                "upgradeFinishTime": "",
                "deviceMobilityMode": "",
                "roamingDevicePoolName": "",
                "remoteDevice": "",
                "dndOption": "",
                "dndRingSetting": "",
                "dndStatus": "",
                "isActive": "",
                "isDualMode": "",
                "mobilityUserIdName": "",
                "phoneSuite": "",
                "phoneServiceDisplay": "",
                "isProtected": "",
                "mtpRequired": "",
                "mtpPreferedCodec": "",
                "dialRulesName": "",
                "sshUserId": "",
                "digestUser": "",
                "outboundCallRollover": "",
                "hotlineDevice": "",
                "secureInformationUrl": "",
                "secureDirectoryUrl": "",
                "secureServicesUrl": "",
                "secureAuthenticationUrl": "",
                "secureIdleUrl": "",
                "alwaysUsePrimeLine": "",
                "alwaysUsePrimeLineForVoiceMessage": "",
                "featureControlPolicy": "",
                "deviceTrustMode": "",
                "earlyOfferSupportForVoiceCall": "",
                "requireThirdPartyRegistration": "",
                "blockIncomingCallsWhenRoaming": "",
                "homeNetworkId": "",
                "AllowPresentationSharingUsingBfcp": "",
                "confidentialAccess": "",
                "requireOffPremiseLocation": "",
                "allowiXApplicableMedia": "",
                "enableCallRoutingToRdWhenNoneIsActive": "",
                "enableActivationID": "",
                "mraServiceDomain": "",
                "allowMraMode": "",

            }
        skip = 0
        a = []

        def inner(skip):
            while True:
                res = self.service.listPhone(
                    searchCriteria=query, returnedTags=tagfilter, first=1000, skip=skip
                )["return"]
                skip = skip + 1000
                if res is not None and 'phone' in res:
                    yield res['phone']
                else:
                    break

        for each in inner(skip):
            a.extend(each)
        return a

    def getPhone(self, deviceName):
        """
        Get device profile parameters
        :param phone: profile name
        :return: result dictionary
        """
        try:
            return self.service.getPhone(name=deviceName)["return"]["phone"]
        except Exception as e:
            raise Exception(e)

    def addPhone(
            self,
            name,
            description="",
            product="Cisco 7841",
            device_pool="Default",
            location="Hub_None",
            phone_template="Standard 8861 SIP",
            common_device_config="",
            css="",
            aar_css="",
            subscribe_css="",
            securityProfileName="",
            lines=[],
            dev_class="Phone",
            protocol="SCCP",
            softkey_template="Standard User",
            enable_em="true",
            em_service_name="Extension Mobility",
            em_service_url=False,
            em_url_button_enable=False,
            em_url_button_index="1",
            em_url_label="Press here to logon",
            ehook_enable=1,
            req=None,
    ):
        """
        lines takes a list of Tuples with properties for each line EG:
                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        Add A phone
        :param name:
        :param description:
        :param product:
        :param device_pool:
        :param location:
        :param phone_template:
        :param common_device_config:
        :param css:
        :param aar_css:
        :param subscribe_css:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param enable_em:
        :param em_service_name:
        :param em_service_url:
        :param em_url_button_enable:
        :param em_url_button_index:
        :param em_url_label:
        :param ehook_enable:
        :return:
        """
        if req is None:
            req = {
                "name": name,
                "description": description,
                "product": product,
                "class": dev_class,
                "protocol": protocol,
                "protocolSide": "User",
                "commonDeviceConfigName": common_device_config,
                "commonPhoneConfigName": "Standard Common Phone Profile",
                "softkeyTemplateName": softkey_template,
                "phoneTemplateName": phone_template,
                "devicePoolName": device_pool,
                "locationName": location,
                "useTrustedRelayPoint": "Off",
                "builtInBridgeStatus": "Default",
                "certificateOperation": "No Pending Operation",
                "packetCaptureMode": "None",
                "deviceMobilityMode": "Default",
                "enableExtensionMobility": enable_em,
                "callingSearchSpaceName": css,
                "automatedAlternateRoutingCssName": aar_css,
                "subscribeCallingSearchSpaceName": subscribe_css,
                "lines": {"line": []},
                "services": {"service": []},
                "vendorConfig": [{"ehookEnable": ehook_enable}],
            }

        if lines:
            [
                req["lines"]["line"].append(
                    {
                        "index": lines.index(i) + 1,
                        "dirn": {"pattern": i[0], "routePartitionName": i[1]},
                        "display": i[2],
                        "displayAscii": i[3],
                        "label": i[4],
                        "e164Mask": i[5],
                    }
                )
                for i in lines
            ]

        if em_service_url:
            req["services"]["service"].append(
                [
                    {
                        "telecasterServiceName": em_service_name,
                        "name": em_service_name,
                        "url": "http://{0}:8080/emapp/EMAppServlet?device=#DEVICENAME#&EMCC=#EMCC#".format(
                            self.cucm
                        ),
                    }
                ]
            )

        if em_url_button_enable:
            req["services"]["service"][0].update(
                {"urlButtonIndex": em_url_button_index, "urlLabel": em_url_label}
            )
        try:
            return self.service.addPhone(req)
        except Exception as e:
            raise Exception(e)

    def removePhone(self, deviceName):
        """
        Delete a phone
        :param phone: The name of the phone to delete
        :return: result dictionary
        """
        try:
            return self.service.removePhone(name=deviceName)
        except Exception as e:
            raise Exception(e)

    def updatePhone(self, **args):

        """
        lines takes a list of Tuples with properties for each line EG:
                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        Add A phone
        :param name:
        :param description:
        :param product:
        :param device_pool:
        :param location:
        :param phone_template:
        :param common_device_config:
        :param css:
        :param aar_css:
        :param subscribe_css:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param enable_em:
        :param em_service_name:
        :param em_service_url:
        :param em_url_button_enable:
        :param em_url_button_index:
        :param em_url_label:
        :param ehook_enable:
        :return:
        """
        try:
            return self.service.updatePhone(**args)
        except Exception as e:
            raise Exception(e)

    def listAllDeviceProfiles(
            self,
            tagfilter={"name": "", "product": "", "protocol": "", "phoneTemplateName": "", },
    ):
        """
        Get device profile details
        :param mini: return a list of tuples of device profile details
        :return: A list of dictionary's
        """
        try:
            DeviceProfileList = self.service.listDeviceProfile(
                {"name": "%"}, returnedTags=tagfilter,
            )["return"]
            if DeviceProfileList is not None:
                DeviceProfileList = DeviceProfileList["deviceProfile"]
            return DeviceProfileList
        except Exception as e:
            raise Exception(e)

    def getDeviceProfile(self, name):
        """
        Get device profile parameters
        :param name: profile name
        :param uuid: profile uuid
        :return: result dictionary
        """
        try:
            return self.service.getDeviceProfile(name=name)
        except Exception as e:
            raise Exception(e)

    def addDeviceProfile(
            self,
            name,
            description="",
            product="Cisco 7962",
            phone_template="Standard 7962G SCCP",
            dev_class="Device Profile",
            protocol="SCCP",
            protocolSide="User",
            softkey_template="Standard User",
            em_service_name="Extension Mobility",
            lines=[],
    ):
        """
        Add A Device profile for use with extension mobility
        lines takes a list of Tuples with properties for each line EG:
                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        :param name:
        :param description:
        :param product:
        :param phone_template:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param em_service_name:
        :return:
        """

        req = {
            "name": name,
            "description": description,
            "product": product,
            "class": dev_class,
            "protocol": protocol,
            "protocolSide": protocolSide,
            "softkeyTemplateName": softkey_template,
            "phoneTemplateName": phone_template,
            "lines": {"line": []},
        }

        if lines:
            [
                req["lines"]["line"].append(
                    {
                        "index": lines.index(i) + 1,
                        "dirn": {"pattern": i[0], "routePartitionName": i[1]},
                        "display": i[2],
                        "displayAscii": i[3],
                        "label": i[4],
                        "e164Mask": i[5],
                    }
                )
                for i in lines
            ]

        try:
            return self.service.addDeviceProfile(req)
        except Exception as e:
            raise Exception(e)

    def removeDeviceProfile(self, name):
        """
        Delete a device profile
        :param profile: The name of the device profile to delete
        :return: result dictionary
        """
        try:
            return self.service.removeDeviceProfile(name=name)
        except Exception as e:
            raise Exception(e)

    def updateDeviceProfile(self, **args):
        """
        Update A Device profile for use with extension mobility
        lines takes a list of Tuples with properties for each line EG:
                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        :param profile:
        :param description:
        :param product:
        :param phone_template:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param em_service_name:
        :return:
        """
        try:
            return self.service.updateDeviceProfile(**args)
        except Exception as e:
            raise Exception(e)

    def listAllUsers(self, tagfilter={"userid": "", "firstName": "", "lastName": ""}):
        """
        Get users details
        :return: A list of dictionary's
        """
        skip = 0
        a = []

        def inner(skip):
            while True:
                res = self.service.listUser(
                    {"userid": "%"}, returnedTags=tagfilter, first=1000, skip=skip
                )["return"]
                skip = skip + 1000
                if res is not None and 'user' in res:
                    yield res['user']
                else:
                    break

        for each in inner(skip):
            a.extend(each)
        return a

    def getUser(self, userid):
        """
        Get user parameters
        :param user_id: profile name
        :return: result dictionary
        """
        try:
            return self.service.getUser(userid=userid)["return"]["user"]
        except Exception as e:
            raise Exception(e)

    def addUser(
            self,
            userid,
            lastName,
            firstName,
            presenceGroupName="Standard Presence group",
            phoneProfiles=[],
    ):
        """
        Add a user
        :param user_id: User ID of the user to add
        :param first_name: First name of the user to add
        :param last_name: Last name of the user to add
        :return: result dictionary
        """

        try:
            return self.service.addUser(
                {
                    "userid": userid,
                    "lastName": lastName,
                    "firstName": firstName,
                    "presenceGroupName": presenceGroupName,
                    "phoneProfiles": phoneProfiles,
                }
            )
        except Exception as e:
            raise Exception(e)

    def updateUser(self, **args):
        """
        Update end user for credentials
        :param userid: User ID
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :return: result dictionary
        """
        try:
            return self.service.updateUser(**args)
        except Exception as e:
            raise Exception(e)

    def updateUserExtensionMobility(
            self, user_id, device_profile, default_profile, subscribe_css, primary_extension
    ):
        """
        Update end user for extension mobility
        :param user_id: User ID
        :param device_profile: Device profile name
        :param default_profile: Default profile name
        :param subscribe_css: Subscribe CSS
        :param primary_extension: Primary extension, must be a number from the device profile
        :return: result dictionary
        """
        try:
            resp = self.service.getDeviceProfile(name=device_profile)
        except Exception as e:
            raise Exception(e)
        if "return" in resp and resp["return"] is not None:
            uuid = resp["return"]["deviceProfile"]["uuid"]
            try:
                return self.service.updateUser(
                    userid=user_id,
                    phoneProfiles={"profileName": {"_uuid": uuid}},
                    defaultProfile=default_profile,
                    subscribeCallingSearchSpaceName=subscribe_css,
                    primaryExtension={"pattern": primary_extension},
                    associatedGroups={"userGroup": {"name": "Standard CCM End Users"}},
                )
            except Fault as e:
                return e
        else:
            return "Device Profile not found for user"

    def updateUserCredentials(self, userid, password="", pin=""):
        """
        Update end user for credentials
        :param userid: User ID
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :return: result dictionary
        """

        if password == "" and pin == "":
            return "Password and/or Pin are required"

        elif password != "" and pin != "":
            try:
                return self.service.updateUser(userid=userid, password=password, pin=pin)
            except Fault as e:
                return e

        elif password != "":
            try:
                return self.service.updateUser(userid=userid, password=password)
            except Fault as e:
                return e

        elif pin != "":
            try:
                return self.service.updateUser(userid=userid, pin=pin)
            except Fault as e:
                return e

    def removeUser(self, userid):
        """
        Delete a user
        :param userid: The name of the user to delete
        :return: result dictionary
        """
        try:
            return self.service.removeUser(userid=userid)
        except Exception as e:
            raise Exception(e)

    def listAllTranslationPatterns(self):
        """
        Get translation patterns
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            TranslationPatternList = self.service.listTransPattern(
                {"pattern": "%"},
                returnedTags={
                    "pattern": "",
                    "description": "",
                    "uuid": "",
                    "routePartitionName": "",
                    "callingSearchSpaceName": "",
                    "useCallingPartyPhoneMask": "",
                    "patternUrgency": "",
                    "prefixDigitsOut": "",
                    "calledPartyTransformationMask": "",
                    "callingPartyTransformationMask": "",
                    "digitDiscardInstructionName": "",
                    "callingPartyPrefixDigits": "",
                    "provideOutsideDialtone": "",
                },
            )["return"]
            if TranslationPatternList is not None:
                TranslationPatternList = TranslationPatternList["transPattern"]
            return TranslationPatternList
        except Exception as e:
            raise Exception(e)

    def getTranslationPattern(self, pattern="", routePartitionName="", uuid=""):
        """
        Get translation pattern
        :param pattern: translation pattern to match
        :param routePartitionName: routePartitionName required if searching pattern
        :param uuid: translation pattern uuid
        :return: result dictionary
        """

        if pattern != "" and routePartitionName != "" and uuid == "":
            try:
                return self.service.getTransPattern(
                    pattern=pattern,
                    routePartitionName=routePartitionName,
                    returnedTags={
                        "pattern": "",
                        "description": "",
                        "routePartitionName": "",
                        "callingSearchSpaceName": "",
                        "useCallingPartyPhoneMask": "",
                        "patternUrgency": "",
                        "provideOutsideDialtone": "",
                        "prefixDigitsOut": "",
                        "calledPartyTransformationMask": "",
                        "callingPartyTransformationMask": "",
                        "digitDiscardInstructionName": "",
                        "callingPartyPrefixDigits": "",
                    },
                )
            except Fault as e:
                return e
        elif uuid != "" and pattern == "" and routePartitionName == "":
            try:
                return self.service.getTransPattern(
                    uuid=uuid,
                    returnedTags={
                        "pattern": "",
                        "description": "",
                        "routePartitionName": "",
                        "callingSearchSpaceName": "",
                        "useCallingPartyPhoneMask": "",
                        "patternUrgency": "",
                        "provideOutsideDialtone": "",
                        "prefixDigitsOut": "",
                        "calledPartyTransformationMask": "",
                        "callingPartyTransformationMask": "",
                        "digitDiscardInstructionName": "",
                        "callingPartyPrefixDigits": "",
                    },
                )
            except Fault as e:
                return e
        else:
            raise Exception("Must specify either uuid OR pattern and partition")

    def addTranslationPattern(
            self,
            pattern,
            partition,
            description="",
            usage="Translation",
            callingSearchSpaceName="",
            useCallingPartyPhoneMask="Off",
            patternUrgency="f",
            provideOutsideDialtone="f",
            prefixDigitsOut="",
            calledPartyTransformationMask="",
            callingPartyTransformationMask="",
            digitDiscardInstructionName="",
            callingPartyPrefixDigits="",
            blockEnable="f",
            routeNextHopByCgpn="f",
    ):
        """
        Add a translation pattern
        :param pattern: Translation pattern
        :param partition: Route Partition
        :param description: Description - optional
        :param usage: Usage
        :param callingSearchSpaceName: Calling Search Space - optional
        :param patternUrgency: Pattern Urgency - optional
        :param provideOutsideDialtone: Provide Outside Dial Tone - optional
        :param prefixDigitsOut: Prefix Digits Out - optional
        :param calledPartyTransformationMask: - optional
        :param callingPartyTransformationMask: - optional
        :param digitDiscardInstructionName: - optional
        :param callingPartyPrefixDigits: - optional
        :param blockEnable: - optional
        :return: result dictionary
        """
        try:
            return self.service.addTransPattern(
                {
                    "pattern": pattern,
                    "description": description,
                    "routePartitionName": partition,
                    "usage": usage,
                    "callingSearchSpaceName": callingSearchSpaceName,
                    "useCallingPartyPhoneMask": useCallingPartyPhoneMask,
                    "patternUrgency": patternUrgency,
                    "provideOutsideDialtone": provideOutsideDialtone,
                    "prefixDigitsOut": prefixDigitsOut,
                    "calledPartyTransformationMask": calledPartyTransformationMask,
                    "callingPartyTransformationMask": callingPartyTransformationMask,
                    "digitDiscardInstructionName": digitDiscardInstructionName,
                    "callingPartyPrefixDigits": callingPartyPrefixDigits,
                    "blockEnable": blockEnable,
                }
            )
        except Exception as e:
            raise Exception(e)

    def removeTranslationPattern(self, pattern="", partition="", uuid=""):
        """
        Delete a translation pattern
        :param pattern: The pattern of the route to delete
        :param partition: The name of the partition
        :param uuid: Required if pattern and partition are not specified
        :return: result dictionary
        """

        if pattern != "" and partition != "" and uuid == "":
            try:
                return self.service.removeTransPattern(
                    pattern=pattern, routePartitionName=partition
                )
            except Fault as e:
                return e
        elif uuid != "" and pattern == "" and partition == "":
            try:
                return self.service.removeTransPattern(uuid=uuid)
            except Fault as e:
                return e
        else:
            return "must specify either uuid OR pattern and partition"

    def updateTranslationPattern(
            self,
            pattern="",
            partition="",
            uuid="",
            newPattern="",
            description="",
            newRoutePartitionName="",
            callingSearchSpaceName="",
            useCallingPartyPhoneMask="",
            patternUrgency="",
            provideOutsideDialtone="",
            prefixDigitsOut="",
            calledPartyTransformationMask="",
            callingPartyTransformationMask="",
            digitDiscardInstructionName="",
            callingPartyPrefixDigits="",
            blockEnable="",
    ):
        """
        Update a translation pattern
        :param uuid: UUID or Translation + Partition Required
        :param pattern: Translation pattern
        :param partition: Route Partition
        :param description: Description - optional
        :param usage: Usage
        :param callingSearchSpaceName: Calling Search Space - optional
        :param patternUrgency: Pattern Urgency - optional
        :param provideOutsideDialtone: Provide Outside Dial Tone - optional
        :param prefixDigitsOut: Prefix Digits Out - optional
        :param calledPartyTransformationMask: - optional
        :param callingPartyTransformationMask: - optional
        :param digitDiscardInstructionName: - optional
        :param callingPartyPrefixDigits: - optional
        :param blockEnable: - optional
        :return: result dictionary
        """

        args = {}
        if description != "":
            args["description"] = description
        if pattern != "" and partition != "" and uuid == "":
            args["pattern"] = pattern
            args["routePartitionName"] = partition
        if pattern == "" and partition == "" and uuid != "":
            args["uuid"] = uuid
        if newPattern != "":
            args["newPattern"] = newPattern
        if newRoutePartitionName != "":
            args["newRoutePartitionName"] = newRoutePartitionName
        if callingSearchSpaceName != "":
            args["callingSearchSpaceName"] = callingSearchSpaceName
        if useCallingPartyPhoneMask != "":
            args["useCallingPartyPhoneMask"] = useCallingPartyPhoneMask
        if digitDiscardInstructionName != "":
            args["digitDiscardInstructionName"] = digitDiscardInstructionName
        if callingPartyTransformationMask != "":
            args["callingPartyTransformationMask"] = callingPartyTransformationMask
        if calledPartyTransformationMask != "":
            args["calledPartyTransformationMask"] = calledPartyTransformationMask
        if patternUrgency != "":
            args["patternUrgency"] = patternUrgency
        if provideOutsideDialtone != "":
            args["provideOutsideDialtone"] = provideOutsideDialtone
        if prefixDigitsOut != "":
            args["prefixDigitsOut"] = prefixDigitsOut
        if callingPartyPrefixDigits != "":
            args["callingPartyPrefixDigits"] = callingPartyPrefixDigits
        if blockEnable != "":
            args["blockEnable"] = blockEnable
        try:
            return self.service.updateTransPattern(**args)
        except Exception as e:
            raise Exception(e)

    def listAllRoutePlans(self, pattern=""):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: results dictionary
        """
        try:
            RoutePlanList = self.service.listRoutePlan(
                {"dnOrPattern": "%" + pattern + "%"},
                returnedTags={
                    "dnOrPattern": "",
                    "partition": "",
                    "type": "",
                    "routeDetail": "",
                },
            )["return"]
            if RoutePlanList is not None:
                RoutePlanList = RoutePlanList["routePlan"]
            return RoutePlanList
        except Exception as e:
            raise Exception(e)

    def getRoutePlan(self, pattern=""):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: results dictionary
        """
        try:
            return self.service.listRoutePlan(
                {"dnOrPattern": pattern},
                returnedTags={
                    "dnOrPattern": "",
                    "partition": "",
                    "type": "",
                    "routeDetail": "",
                },
            )
        except Exception as e:
            raise Exception(e)

    def listAllCalledPartyTransformationPatterns(self):
        """
        Get called party xforms
        :param mini: return a list of tuples of called party transformation pattern details
        :return: A list of dictionary's
        """
        try:
            CalledPartyTransformationPatternList = self.service.listCalledPartyTransformationPattern(
                {"pattern": "%"},
                returnedTags={"pattern": "", "description": "", "uuid": ""},
            )["return"]
            if CalledPartyTransformationPatternList is not None:
                CalledPartyTransformationPatternList = CalledPartyTransformationPatternList[
                    "calledPartyTransformationPattern"]
            return CalledPartyTransformationPatternList
        except Exception as e:
            raise Exception(e)

    def getCalledPartyTransformationPattern(self, **args):
        """
        Get called party xform details
        :param name:
        :param partition:
        :param uuid:
        :return: result dictionary
        """
        try:
            return self.service.getCalledPartyTransformationPattern(**args)
        except Exception as e:
            raise Exception(e)

    def addCalledPartyTransformationPattern(
            self,
            pattern="",
            description="",
            partition="",
            calledPartyPrefixDigits="",
            calledPartyTransformationMask="",
            digitDiscardInstructionName="",
    ):
        """
        Add a called party transformation pattern
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param calledPartyTransformationmask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param calledPartyPrefixDigits:
        :param calledPartyNumberingPlan:
        :param calledPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        """
        try:
            return self.service.addCalledPartyTransformationPattern(
                {
                    "pattern": pattern,
                    "description": description,
                    "routePartitionName": partition,
                    "calledPartyPrefixDigits": calledPartyPrefixDigits,
                    "calledPartyTransformationMask": calledPartyTransformationMask,
                    "digitDiscardInstructionName": digitDiscardInstructionName,
                }
            )
        except Exception as e:
            raise Exception(e)

    def removeCalledPartyTransformationPattern(self, **args):
        """
        Delete a called party transformation pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the transformation to delete
        :param partition: The name of the partition
        :return: result dictionary
        """
        try:
            return self.service.removeCalledPartyTransformationPattern(**args)
        except Exception as e:
            raise Exception(e)

    def updateCalledPartyTransformationPattern(self, **args):
        """
        Update a called party transformation
        :param uuid: required unless pattern and routePartitionName is given
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param calledPartyTransformationmask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param calledPartyPrefixDigits:
        :param calledPartyNumberingPlan:
        :param calledPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        :return: result dictionary
        """
        try:
            return self.service.updateCalledPartyTransformationPattern(**args)
        except Exception as e:
            raise Exception(e)

    def listAllCallingPartyTransformationPatterns(self):
        """
        Get calling party xforms
        :param mini: return a list of tuples of calling party transformation pattern details
        :return: A list of dictionary's
        """
        try:
            CallingPartyTransformationPatternList = self.service.listCallingPartyTransformationPattern(
                {"pattern": "%"},
                returnedTags={"pattern": "", "description": "", "uuid": ""},
            )["return"]
            if CallingPartyTransformationPatternList is not None:
                CallingPartyTransformationPatternList = CallingPartyTransformationPatternList[
                    "callingPartyTransformationPattern"]
            return CallingPartyTransformationPatternList
        except Exception as e:
            raise Exception(e)

    def getCallingPartyTransformationPattern(self, **args):
        """
        Get calling party xform details
        :param name:
        :param partition:
        :param uuid:
        :return: result dictionary
        """
        try:
            return self.service.getCallingPartyTransformationPattern(**args)
        except Exception as e:
            raise Exception(e)

    def addCallingPartyTransformationPattern(
            self,
            pattern="",
            description="",
            partition="",
            callingPartyPrefixDigits="",
            callingPartyTransformationMask="",
            digitDiscardInstructionName="",
    ):
        """
        Add a calling party transformation pattern
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param callingPartyTransformationmask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param callingPartyPrefixDigits:
        :param callingPartyNumberingPlan:
        :param callingPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        """
        try:
            return self.service.addCallingPartyTransformationPattern(
                {
                    "pattern": pattern,
                    "description": description,
                    "routePartitionName": partition,
                    "callingPartyPrefixDigits": callingPartyPrefixDigits,
                    "callingPartyTransformationMask": callingPartyTransformationMask,
                    "digitDiscardInstructionName": digitDiscardInstructionName,
                }
            )
        except Exception as e:
            raise Exception(e)

    def removeCallingPartyTransformationPattern(self, **args):
        """
        Delete a calling party transformation pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the transformation to delete
        :param partition: The name of the partition
        :return: result dictionary
        """
        try:
            return self.service.removeCallingPartyTransformationPattern(**args)
        except Exception as e:
            raise Exception(e)

    def updateCallingPartyTransformationPattern(self, **args):
        """
        Update a calling party transformation
        :param uuid: required unless pattern and routePartitionName is given
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param callingPartyTransformationMask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param calledPartyPrefixDigits:
        :param calledPartyNumberingPlan:
        :param calledPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        :return: result dictionary
        """
        try:
            return self.service.updateCallingPartyTransformationPattern(**args)
        except Exception as e:
            raise Exception(e)

    def listAllSIPTrunks(
            self, tagfilter={"name": "", "sipProfileName": "", "callingSearchSpaceName": ""}
    ):
        try:
            SIPTrunkList = self.service.listSipTrunk({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]
            if SIPTrunkList is not None:
                SIPTrunkList = SIPTrunkList["sipTrunk"]
            return SIPTrunkList
        except Exception as e:
            raise Exception(e)

    def getSipTrunk(self, name):
        """
        Get sip trunk
        :param name:
        :param uuid:
        :return: result dictionary
        """
        try:
            return self.service.getSipTrunk(name=name)
        except Exception as e:
            raise Exception(e)

    def updateSipTrunk(self, **args):
        """
        Update a SIP Trunk
        :param name:
        :param uuid:
        :param newName:
        :param description:
        :param callingSearchSpaceName:
        :param devicePoolName:
        :param locationName:
        :param sipProfileName:
        :param mtpRequired:
        :return:
        """
        try:
            return self.service.updateSipTrunk(**args)
        except Exception as e:
            raise Exception(e)

    def removeSipTrunk(self, name):
        try:
            return self.service.removeSipTrunk(name=name)
        except Exception as e:
            raise Exception(e)

    def getSipTrunkSecurityProfile(self, name):
        try:
            return self.service.getSipTrunkSecurityProfile(name=name)["return"]
        except Exception as e:
            raise Exception(e)

    def getSipProfile(self, name):
        try:
            return self.service.getSipProfile(name=name)["return"]
        except Exception as e:
            raise Exception(e)

    def addSipTrunk(self, **args):
        """
        Add a SIP Trunk
        :param name:
        :param description:
        :param product:
        :param protocol:
        :param protocolSide:
        :param callingSearchSpaceName:
        :param devicePoolName:
        :param securityProfileName:
        :param sipProfileName:
        :param destinations: param destination:
        :param runOnEveryNode:
        :return:
        """
        try:
            return self.service.addSipTrunk(**args)
        except Exception as e:
            raise Exception(e)

    def listAllProcessNodes(self):
        try:
            ProcessNodeList = self.service.listProcessNode(
                {"name": "%", "processNodeRole": "CUCM Voice/Video"},
                returnedTags={"name": ""},
            )["return"]
            if ProcessNodeList is not None:
                ProcessNodeList = ProcessNodeList["processNode"]
                return ProcessNodeList
        except Exception as e:
            raise Exception(e)

    def addCallManagerGroup(self, name, members):
        """
        Add call manager group
        :param name: name of cmg
        :param members[]: array of members
        :return: result dictionary
        """

        try:
            return self.service.addCallManagerGroup({"name": name, "members": members})
        except Exception as e:
            raise Exception(e)

    def getCallManagerGroup(self, name):
        """
        Get call manager group
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            return self.service.getCallManagerGroup(name=name)
        except Exception as e:
            raise Exception(e)

    def listAllCallManagerGroups(self):
        """
        Get call manager groups
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            CallManagerGroupList = self.service.listCallManagerGroup(
                {"name": "%"}, returnedTags={"name": ""}
            )["return"]
            if CallManagerGroupList is not None:
                CallManagerGroupList = CallManagerGroupList["callManagerGroup"]
            return CallManagerGroupList
        except Exception as e:
            raise Exception(e)

    def updateCallManagerGroup(self, **args):
        """
        Update call manager group
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            return self.service.updateCallManagerGroup(**args)
        except Exception as e:
            raise Exception(e)

    def removeCallManagerGroup(self, name):
        """
        Delete call manager group
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            return self.service.removeCallManagerGroup(name=name)
        except Exception as e:
            raise Exception(e)


class IMPAxlToolkit(AxlToolkit):
    """
    The IMPAxlToolkit based on parent class AxlToolkit
    This class enables us to connect and make unique IM&P AXL API requests
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param version: (optional) The major version of CUCM / IM&P Cluster (default: 12.5)
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :param schema_folder_path: (optional) Sub Directory Location for AXL schema versions (default: None)
    :type username: str
    :type password: str
    :type server_ip: str
    :type version: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :type schema_folder_path: str
    :returns: return an IMPAxlToolkit object
    :rtype: IMPAxlToolkit
    """

    def __init__(self, username, password, server_ip, version='11.5', tls_verify=True, timeout=10,
                 logging_enabled=False, schema_folder_path=None):
        schema_folder_path += "IMP/"

        # Create a super class, where the CUCMAxlToolkit class inherits from the AxlToolkit class.
        # This enables us to extend the parent class AxlToolkit with CUCM AXL API specic methods
        # Reference:  https://realpython.com/python-super/
        super().__init__(username, password, server_ip, version=version, tls_verify=tls_verify, timeout=timeout,
                         logging_enabled=logging_enabled, schema_folder_path=schema_folder_path)

    def get_cup_version(self):
        """
        Get CUP Version
        """
        try:
            result = self.service.getCUPVersion()
        except Exception as fault:
            self.last_exception = fault
            return fault
        if result:
            return result['return']['version']
        else:
            return None


class UcmServiceabilityToolkit:
    """
    The UcmServiceabilityToolkit SOAP API class
    This class enables us to connect and make Control Center Services API calls utilizing Zeep Python Package as the SOAP Client
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :type username: str
    :type password: str
    :type server_ip: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :returns: return an UcmServiceabilityToolkit object
    :rtype: UcmServiceabilityToolkit
    """

    def __init__(self, username, password, server_ip, tls_verify=True, timeout=10, logging_enabled=False):
        """
        Constructor - Create new instance
        """

        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.history = AXLHistoryPlugin(maxlen=1)
        self.wsdl = 'https://{0}:8443/controlcenterservice2/services/ControlCenterServices?wsdl'.format(server_ip)
        self.last_exception = None

        self.cache = SqliteCache(path='/tmp/sqlite_serviceability_{0}.db'.format(server_ip), timeout=60)

        self.service = Client(wsdl=self.wsdl, plugins=[self.history], transport=Transport(timeout=timeout,
                                                                                          operation_timeout=timeout,
                                                                                          cache=self.cache,
                                                                                          session=self.session))

        # Update the Default SOAP API Binding Address Location with server_ip for all API Service Endpoints
        # Default: (https://localhost:8443/controlcenterservice2/services/ControlCenterServices)
        control_svc_ip = "https://{0}:8443/controlcenterservice2/services/ControlCenterServices".format(server_ip)
        self.service = self.service.create_service("{http://schemas.cisco.com/ast/soap}ControlCenterServicesBinding",
                                                   control_svc_ip)

        if logging_enabled:
            AxlToolkit._enable_logging()

    def getService(self):
        return self.service

    def getProductInformationList(self):
        return self.service.getProductInformationList

    def soapGetServiceStatus(self):
        return self.service.soapGetServiceStatus

    def soapGetStaticServiceList(self):
        return self.service.soapGetStaticServiceList

    def soapDoControlServices(self):
        return self.service.soapDoControlServices

    def soapDoServiceDeployment(self):
        return self.service.soapDoServiceDeployment

class UcmRisPortToolkit:
    """
    The UcmRisPortToolkit SOAP API class
    This class enables us to connect and make RisPort70 API calls utilizing Zeep Python Package as the SOAP Client
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :type username: str
    :type password: str
    :type server_ip: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :returns: return an UcmRisPortToolkit object
    :rtype: UcmRisPortToolkit
    """

    def __init__(self, username, password, server_ip, tls_verify=True, timeout=30, logging_enabled=False):
        """
        Constructor - Create new instance
        """

        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.history = AXLHistoryPlugin(maxlen=1)
        self.wsdl = 'https://{0}:8443/realtimeservice2/services/RISService70?wsdl'.format(server_ip)
        self.last_exception = None

        self.cache = SqliteCache(path='/tmp/sqlite_risport_{0}.db'.format(server_ip), timeout=60)

        self.service = Client(wsdl=self.wsdl, plugins=[self.history], transport=Transport(timeout=timeout,
                                                                                          operation_timeout=timeout,
                                                                                          cache=self.cache,
                                                                                          session=self.session))

        # Update the Default SOAP API Binding Address Location with server_ip for all API Service Endpoints
        # Default: (https://localhost:8443/realtimeservice2/services/RISService70)
        self.service = self.service.create_service("{http://schemas.cisco.com/ast/soap}RisBinding",
                                                   "https://{0}:8443/realtimeservice2/services/RISService70".format(
                                                       server_ip))

        if logging_enabled:
            AxlToolkit._enable_logging()

    def get_service(self):
        return self.service


class UcmPerfMonToolkit:
    """
    The UcmPerfMonToolkit SOAP API class
    This class enables us to connect and make PerfMon API calls utilizing Zeep Python Package as the SOAP Client
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :type username: str
    :type password: str
    :type server_ip: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :returns: return an UcmPerfMonToolkit object
    :rtype: UcmPerfMonToolkit
    """

    def __init__(self, username, password, server_ip, tls_verify=True, timeout=30, logging_enabled=False):
        """
        Constructor - Create new instance
        """

        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.history = AXLHistoryPlugin(maxlen=1)
        self.wsdl = 'https://{0}:8443/perfmonservice2/services/PerfmonService?wsdl'.format(server_ip)
        self.last_exception = None

        self.cache = SqliteCache(path='/tmp/sqlite_perfmon_{0}.db'.format(server_ip), timeout=60)

        self.service = Client(wsdl=self.wsdl, plugins=[self.history], transport=Transport(timeout=timeout,
                                                                                          operation_timeout=timeout,
                                                                                          cache=self.cache,
                                                                                          session=self.session))

        # Update the Default SOAP API Binding Address Location with server_ip for all API Service Endpoints
        # Default: (https://localhost:8443/perfmonservice2/services/PerfmonService)
        self.service = self.service.create_service("{http://schemas.cisco.com/ast/soap}PerfmonBinding",
                                                   "https://{0}:8443/perfmonservice2/services/PerfmonService".format(
                                                       server_ip))

        if logging_enabled:
            AxlToolkit._enable_logging()

    def get_service(self):
        return self.service

    def perfmon_open_session(self):
        session_handle = self.service.perfmonOpenSession()
        return session_handle

    def perfmon_close_session(self, session_handle):
        return self.service.perfmonCloseSession(SessionHandle=session_handle)

    def perfmon_add_counter(self, session_handle, counters):
        """
        :param session_handle: A session Handle returned from perfmonOpenSession()
        :param counters: An array of counters or a single string for a single counter
        :return: True for Success and False for Failure
        """

        if isinstance(counters, list):
            counter_data = [
                {
                    'Counter': []
                }
            ]

            for counter in counters:
                new_counter = {
                    'Name': counter
                }
                counter_data[0]['Counter'].append(new_counter)

        elif counters is not None:
            counter_data = [
                {
                    'Counter': [
                        {
                            'Name': counters
                        }
                    ]
                }
            ]

        try:
            self.service.perfmonAddCounter(SessionHandle=session_handle, ArrayOfCounter=counter_data)
            result = True
        except Exception:
            result = False

        return result

    def perfmon_collect_session_data(self, session_handle):
        return self.service.perfmonCollectSessionData(SessionHandle=session_handle)

    def perfmon_collect_counter_data(self, host, perfmon_object):
        return self.service.perfmonCollectCounterData(Host=host, Object=perfmon_object)


class UcmLogCollectionToolkit:
    """
    The UcmLogCollectionToolkit SOAP API class
    This class enables us to connect and make Log Collection API calls utilizing Zeep Python Package as the SOAP Client
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :type username: str
    :type password: str
    :type server_ip: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :returns: return an UcmLogCollectionToolkit object
    :rtype: UcmLogCollectionToolkit
    """

    def __init__(self, username, password, server_ip, tls_verify=True, timeout=30, logging_enabled=False):
        """
        Constructor - Create new instance
        """

        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.history = AXLHistoryPlugin(maxlen=1)
        self.wsdl = 'https://{0}:8443/logcollectionservice2/services/LogCollectionPortTypeService?wsdl'.format(
            server_ip)
        self.last_exception = None

        self.cache = SqliteCache(path='/tmp/sqlite_logcollection.db', timeout=60)

        self.service = Client(wsdl=self.wsdl, plugins=[self.history], transport=Transport(timeout=timeout,
                                                                                          operation_timeout=timeout,
                                                                                          cache=self.cache,
                                                                                          session=self.session))

        # Update the Default SOAP API Binding Address Location with server_ip for all API Service Endpoints
        # Default: (https://localhost:8443/logcollectionservice2/services/LogCollectionPortTypeService)
        self.service = self.service.create_service("{http://schemas.cisco.com/ast/soap}LogCollectionPortSoapBinding",
                                                   "https://{0}:8443/logcollectionservice2/services/LogCollectionPortTypeService".format(
                                                       server_ip))

        if logging_enabled:
            AxlToolkit._enable_logging()

    def get_service(self):
        return self.service


class UcmDimeGetFileToolkit:
    """
    The UcmDimeGetFileToolkit SOAP API class
    This class enables us to connect and make DimeGetFileService API calls utilizing Zeep Python Package as the SOAP Client
    :param username: The username used for Basic HTTP Authentication
    :param password: The password used for Basic HTTP Authentication
    :param server_ip: The Hostname / IP Address of the server
    :param tls_verify: (optional) Certificate validation check for HTTPs connection (default: True)
    :param timeout: (optional) Zeep Client Transport Response Timeout in seconds (default: 10)
    :param logging_enabled: (optional) Zeep SOAP message Logging (default: False)
    :type username: str
    :type password: str
    :type server_ip: str
    :type tls_verify: bool
    :type timeout: int
    :type logging_enabled: bool
    :returns: return an UcmDimeGetFileToolkit object
    :rtype: UcmDimeGetFileToolkit
    """

    def __init__(self, username, password, server_ip, tls_verify=True, timeout=30, logging_enabled=False):
        """
        Constructor - Create new instance
        """

        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.history = AXLHistoryPlugin(maxlen=1)
        self.wsdl = 'https://{0}:8443/logcollectionservice/services/DimeGetFileService?wsdl'.format(server_ip)
        self.last_exception = None

        self.cache = SqliteCache(path='/tmp/sqlite_logcollectiondime.db', timeout=60)

        self.service = Client(wsdl=self.wsdl, plugins=[self.history], transport=Transport(timeout=timeout,
                                                                                          operation_timeout=timeout,
                                                                                          cache=self.cache,
                                                                                          session=self.session))

        self.service = self.client.service

        if logging_enabled:
            AxlToolkit._enable_logging()

    def get_service(self):
        return self.service


class RemotePhoneAccess:
    """
    Reference: https://web.archive.org/web/20220119230219/https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cuipph/all_models/xsi/9-1-1/CUIP_BK_P82B3B16_00_phones-services-application-development-notes/CUIP_BK_P82B3B16_00_phones-services-application-development-notes_chapter_0101.html
    """

    def __init__(self, phone_ip, axlUsername, axlPassword, server_ip):
        self.phone_ip = phone_ip
        self.axlUsername = axlUsername
        self.axlPassword = axlPassword
        self.server_ip = server_ip
        ConnectivityTest = (
            requests.get(f'https://{self.axlUsername}:{self.axlPassword}@{self.phone_ip}', verify=False))
        if ConnectivityTest.status_code == 200:
            logging.info(f'Successfully connected to Phone: {self.phone_ip}')
        elif ConnectivityTest.status_code == 401:
            raise Exception(
                'Unable to authenticate using the specified credentials and/or ip address. Please verify the information and/or reachability of the server.')
        else:
            raise Exception(ConnectivityTest.reason)

    def callManagerSetup(self):
        """
        Accesses the phone's webpage to get the MAC address. Then updates the application user specified to include the phone's MAC address so it can be controlled remotely.
        :return:
        """
        CUCMAXL = CUCMAxlToolkit(username=self.axlUsername, password=self.axlPassword, server_ip=self.server_ip)
        phoneWebpageInfo = requests.get(f"http://{self.phone_ip}", verify=False).text
        rex = re.compile('SEP............')
        macAddress = rex.search(phoneWebpageInfo).group()
        appUser = CUCMAXL.get_app_user(userid=self.axlUsername)
        associatedDevices = (appUser['return']['appUser']['associatedDevices'])
        if associatedDevices is not None:
            associatedDevices = associatedDevices['device']
            if macAddress not in associatedDevices:
                associatedDevices.append(macAddress)
                CUCMAXL.update_app_user(userid=self.axlUsername, associatedDevices={'device': associatedDevices})

    def getPhoneScreenshot(self):
        """
        Returns the bytes of the screenshot url request.
        :return:
        """
        url = f'https://{self.axlUsername}:{self.axlPassword}@{self.phone_ip}/CGI/Screenshot'

        r = requests.get(url, allow_redirects=True, verify=False, stream=True).content
        return r

    # Define our function to iterate through our key press list
    # and send the key press to the target device
    def sendKeyPress(self, keyPress):
        """
        Sends button presses to the phone IP specified. Example usage: send_key_press({"Key:KeyPad0"})
        :param keyPress: Key to send to the phone.
        :return:
        """
        messages = []
        for kp in keyPress:
            d = OrderedDict(
                [("CiscoIPPhoneExecute", OrderedDict(
                    [("ExecuteItem", OrderedDict([("@Priority", "0"), ("@URL", kp)])
                      )])
                  )])
            messages.append({"XML": unparse(d)})
            # messages = [{   Code here and below is the XML to send popup messages to a phone!!
            #     'XML': '<?xml version="1.0" encoding="utf-8"?>\n<CiscoIPPhoneText><Prompt>Prompt</Prompt><Text>Text</Text></CiscoIPPhoneText>'}]
        headers = {"content-type": "application/xml"}
        for key_press in messages:
            r = requests.post(
                url="http://" + self.phone_ip + "/CGI/Execute",
                data=key_press, verify=False, headers=headers, auth=(self.axlUsername, self.axlPassword)
            )
        return r.text
