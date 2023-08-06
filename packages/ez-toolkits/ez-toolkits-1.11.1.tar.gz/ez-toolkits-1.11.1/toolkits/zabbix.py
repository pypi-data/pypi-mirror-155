import time
from copy import deepcopy

import requests
from loguru import logger


class api(object):
    ''' API '''

    ''' Zabbix API URL, User Login Result '''
    _url, _auth = None, None

    '''
    https://www.zabbix.com/documentation/current/en/manual/api#performing-requests
    The request must have the Content-Type header set to one of these values:
        application/json-rpc, application/json or application/jsonrequest.
    '''
    _header = {'Content-Type': 'application/json-rpc'}

    def __init__(self, url, user, password):
        ''' Initiation '''
        self._url = url
        _user_info = self.request("user.login", {
            "username": user,
            "password": password
        })
        self._auth = _user_info['result']

    def request(self, method, params=None):
        ''' Request '''
        try:
            '''
            Request Data
            https://www.zabbix.com/documentation/current/en/manual/api#authentication
            id - an arbitrary identifier of the request
            id - 请求标识符, 这里使用UNIX时间戳作为唯一标示
            '''
            _data = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "auth": self._auth,
                "id": int(time.time())
            }

            # Request
            _response = requests.post(self._url, headers=self._header, json=_data)

            # Return JSON
            return _response.json()

        except Exception as e:
            logger.exception(e)
            return None

    def logout(self):
        ''' User Logout '''
        try:
            return self.request('user.logout', [])
        except Exception as e:
            logger.exception(e)
            return None

    def logout_exit(self, str='Error'):
        ''' Logout and Exit '''
        logger.info(str)
        try:
            self.logout()
        except:
            exit(1)
        exit(1)

    def get_ids_by_template_name(self, name=''):
        '''
        Get ids by template name
        name: string/array
        example: 'Linux by Zabbix agent' / ['Linux by Zabbix agent', 'Linux by Zabbix agent active']
        如果 name 为 '' (空), 返回所有 template id
        '''
        try:
            _response = self.request('template.get', {'output': 'templateid', 'filter': {'name': name}})
            if type(_response) == dict and _response.get('result') != None and type(_response['result']) == list and _response['result'] != []:
                return [i['templateid'] for i in _response['result']]
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_ids_by_hostgroup_name(self, name=''):
        '''
        Get ids by hostgroup name
        name: string/array
        example: 'Linux servers' / ['Linux servers', 'Discovered hosts']
        如果 name 为 '' (空), 返回所有 hostgroup id
        '''
        try:
            _response = self.request('hostgroup.get', {'output': 'groupid', 'filter': {'name': name}})
            if type(_response) == dict and _response.get('result') != None and type(_response['result']) == list and _response['result'] != []:
                return [i['groupid'] for i in _response['result']]
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_hosts_by_template_name(self, name='', output='extend', **kwargs):
        '''
        Get hosts by template name
        name: string/array
        example: 'Linux by Zabbix agent' / ['Linux by Zabbix agent', 'Linux by Zabbix agent active']
        如果 name 为 '' (空), 返回所有 host
        '''
        try:
            # Get Templates
            _response = self.request('template.get', {'output': ['templateid'], 'filter': {'host': name}})
            # Get Hosts
            if type(_response) == dict and _response.get('result') != None and type(_response['result']) == list and _response['result'] != []:
                _ids = [i['templateid'] for i in _response['result']]
                _hosts = self.request('host.get', {'output': output, 'templateids': _ids, **kwargs})
                if type(_hosts) == dict and _hosts.get('result') != None and type(_hosts['result']) == list:
                    return _hosts['result']
                else:
                    return None
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_hosts_by_hostgroup_name(self, name='', output='extend', **kwargs):
        '''
        Get hosts by hostgroup name
        name: string/array
        example: 'Linux servers' / ['Linux servers', 'Discovered hosts']
        如果 name 为 '' (空), 返回所有 hosts
        '''
        _ids = self.get_ids_by_hostgroup_name(name)
        if _ids == []:
            return None
        try:
            # Get Hosts
            _hosts = self.request('host.get', {'output': output, 'groupids': _ids, **kwargs})
            if type(_hosts) == dict and _hosts.get('result') != None and type(_hosts['result']) == list:
                return _hosts['result']
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_history_by_item_key(self, hosts=[], time_from='', time_till='', item_key='', data_type=3):
        '''
        先根据 item key 获取 item id, 然后通过 item id 获取 item history
        https://www.zabbix.com/documentation/6.0/en/manual/api/reference/history/get
        hosts: Host List
        time_from: Datetime From
        time_till: Datetime Till
        item_key: Item Key
        data_type: Data Type
        '''
        try:

            '''
            Deep Copy (拷贝数据为局部变量)
            父函数中有 hosts 变量, 而此函数对 hosts 的值进行了修改, 所以会导致父函数中 hosts 的值改变
            使用 deepcopy 拷贝一份数据, 就不会改变父函数中 hosts 的值
            '''
            _hosts = deepcopy(hosts)

            # ----------------------------------------------------------------------------------------------------

            # Item Get
            _hostids = [i['hostid'] for i in _hosts]
            _item_params = {
                'output': ['name', 'itemid', 'hostid'],
                'hostids': _hostids,
                'filter': {'key_': item_key}
            }
            _items = self.request('item.get', _item_params)

            # ----------------------------------------------------------------------------------------------------

            # Item IDs
            _itemids = []

            # Put Item ID to Hosts
            # 因为 history 获取的顺序是乱的, 为了使输出和 hosts 列表顺序一致, 将 Item ID 追加到 hosts, 然后遍历 hosts 列表输出
            if type(_items) == dict and _items.get('result') != None and type(_items['result']) == list and _items['result'] != []:
                for host in _hosts:
                    _item = next((item for item in _items['result'] if host['hostid'] == item['hostid']), '')
                    host['itemkey'] = item_key
                    if type(_item) == dict and _item.get('itemid') != None:
                        host['itemid'] = _item['itemid']
                        _itemids.append(_item['itemid'])
                    else:
                        host['itemid'] = ''
            else:
                for host in _hosts:
                    host['itemkey'] = item_key
                    host['itemid'] = ''

            # 如果 ID 列表为空, 则返回 None
            # _itemids = [i['itemid'] for i in _items['result']]
            if _itemids == []:
                return None

            # ----------------------------------------------------------------------------------------------------

            # History Get
            _history_params = {
                'output': 'extend',
                'history': data_type,
                'itemids': _itemids,
                'time_from': time_from,
                'time_till': time_till
            }
            _history = self.request('history.get', _history_params)

            # ----------------------------------------------------------------------------------------------------

            # Put history to hosts
            if type(_history) == dict and _history.get('result') != None and type(_history['result']) == list and _history['result'] != []:
                for host in _hosts:
                    _data = [data for data in _history['result'] if host['itemid'] == data['itemid']]
                    host['history'] = _data
                return _hosts
            else:
                return None

        except Exception as e:
            logger.exception(e)
            return None

    def get_interface_by_host_id(self, hostid='', output='extend'):
        '''
        Get interface by host id
        hostids: string/array
        example: '10792' / ['10792', '10793']
        如果 name 为 '' (空), 则返回 []
        '''
        try:
            _response = self.request('hostinterface.get', {'output': output, 'hostids': hostid})
            if type(_response) == dict and _response.get('result') != None and type(_response['result']):
                return _response['result']
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def create_process_data(self, ips=[], name='', item_type=0, proc_name='', proc_user='', proc_cmdline=''):

        # 测试 (Memory used (rss) 的值要除以 1024)
        # zabbix_get -s 10.25.109.141 -k 'proc.cpu.util[java,circle,,zookeeper-3.4.9.jar]'
        # zabbix_get -s 10.25.109.141 -k 'proc.mem[java,circle,,zookeeper-3.4.9.jar,rss]'
        # zabbix_get -s 10.25.109.141 -k 'proc.mem[java,circle,,zookeeper-3.4.9.jar,pmem]'
        # zabbix_get -s 10.25.109.141 -k 'proc.num[java,circle,run,zookeeper-3.4.9.jar]'

        # https://www.zabbix.com/documentation/6.0/en/manual/api/reference/item/object
        # https://www.zabbix.com/documentation/6.0/en/manual/config/items/itemtypes/zabbix_agent#process-data

        # Process CPU utilization percentage
        # proc.cpu.util[<name>,<user>,<type>,<cmdline>,<mode>,<zone>]
        _proc_cpu_util_item_name = '{} CPU utilization'.format(name)
        _proc_cpu_util_item_key = 'proc.cpu.util[{},{},,{}]'.format(proc_name, proc_user, proc_cmdline)

        # Memory used by process in bytes
        # https://www.zabbix.com/documentation/6.0/en/manual/appendix/items/proc_mem_notes
        # proc.mem[<name>,<user>,<mode>,<cmdline>,<memtype>]
        # pmem: 内存使用量百分比, 即 top 显示的百分比
        # rss: 内存使用量实际数值, 即 总内存 x pmem(百分比)
        # Value Type 要使用 numeric float, 即 0, 否则会报错:
        # Value of type 'string' is not suitable for value type 'Numeric (unsigned)'.
        _proc_mem_rss_item_name = '{} Memory used (rss)'.format(name)
        _proc_mem_rss_item_key = 'proc.mem[{},{},,{},rss]'.format(proc_name, proc_user, proc_cmdline)

        _proc_mem_pmem_item_name = '{} Memory used (pmem)'.format(name)
        _proc_mem_pmem_item_key = 'proc.mem[{},{},,{},pmem]'.format(proc_name, proc_user, proc_cmdline)

        # The number of processes
        # proc.num[<name>,<user>,<state>,<cmdline>,<zone>]
        _proc_num_item_name = '{} Number of processes'.format(name)
        _proc_num_item_key = 'proc.num[{},{},,{}]'.format(proc_name, proc_user, proc_cmdline)

        _proc_num_trigger_name = '{} is down'.format(name)

        # 创建 Item, Trigger, Graph
        for _ip in ips:

            # Host Info
            _hostinterface = self.request('hostinterface.get', {'filter': {'ip': _ip}, 'selectHosts': ['host']})
            _host = _hostinterface['result'][0]['hosts'][0]['host']
            _host_id = _hostinterface['result'][0]['hostid']
            _interface_id = _hostinterface['result'][0]['interfaceid']

            # --------------------------------------------------------------------------------

            # Item Create

            # Process CPU utilization percentage
            _params = {
                'name': _proc_cpu_util_item_name,
                'key_': _proc_cpu_util_item_key,
                'hostid': _host_id,
                'type': item_type,
                'value_type': 0,
                'interfaceid': _interface_id,
                'delay': '1m',
                'history': '7d',
                'trends': '7d'
            }
            _ = self.request('item.create', _params)
            logger.success(_)

            # Memory used (rss)
            _params = {
                'name': _proc_mem_rss_item_name,
                'key_': _proc_mem_rss_item_key,
                'hostid': _host_id,
                'type': item_type,
                'value_type': 0,
                'interfaceid': _interface_id,
                'delay': '1m',
                'history': '7d',
                'trends': '7d'
            }
            _ = self.request('item.create', _params)
            logger.success(_)

            # Memory used (pmem)
            # Units: %
            _params = {
                'name': _proc_mem_pmem_item_name,
                'key_': _proc_mem_pmem_item_key,
                'hostid': _host_id,
                'type': item_type,
                'value_type': 0,
                'interfaceid': _interface_id,
                'units': '%',
                'delay': '1m',
                'history': '7d',
                'trends': '7d'
            }
            _ = self.request('item.create', _params)
            logger.success(_)

            # The number of processes
            _params = {
                'name': _proc_num_item_name,
                'key_': _proc_num_item_key,
                'hostid': _host_id,
                'type': item_type,
                'value_type': 3,
                'interfaceid': _interface_id,
                'delay': '1m',
                'history': '7d',
                'trends': '7d'
            }
            _ = self.request('item.create', _params)
            logger.success(_)

            # --------------------------------------------------------------------------------

            # Trigger Create

            _params = [
                {
                    'description': _proc_num_trigger_name,
                    'priority': '2',
                    'expression': 'last(/{}/{})=0'.format(_host, _proc_num_item_key),
                    'manual_close': '1'
                }
            ]
            _ = self.request('trigger.create', _params)
            logger.success(_)

            # --------------------------------------------------------------------------------

            # Graph Create

            # 如果创建 Graph 后显示 [no data], 可以在 Items 中进入对应的 Item, 然后点击最下方的 Latest data
            # 在 Latest data 的右边的 Info 下面会有黄色感叹号, 将鼠标移动到上面, 可以看到相关的提示

            # --------------------------------------------------------------------------------

            # CPU utilization

            # Item Info
            _item_params = {
                'output': 'extend',
                'hostids': _host_id,
                'search': {'key_': _proc_cpu_util_item_key}
            }
            _item = self.request('item.get', _item_params)
            _item_id = _item['result'][0]['itemid']

            _graph_params = {
                'name': _proc_cpu_util_item_name,
                'width': 900,
                'height': 200,
                'yaxismin': 0,
                'yaxismax': 100,
                'ymin_type': 1,
                'ymax_type': 1,
                'gitems': [{'itemid': _item_id, 'color': '0040FF'}]
            }
            _ = self.request('graph.create', _graph_params)
            logger.success(_)

            # --------------------------------------------------------------------------------

            # Memory used (rss)

            # Total memory
            _vm_params = {
                'output': 'extend',
                'hostids': _host_id,
                'search': {'key_': 'vm.memory.size[total]'}
            }
            _vm_total = self.request('item.get', _vm_params)
            _vm_total_id = _vm_total['result'][0]['itemid']

            # Item Params
            _item_params = {
                'output': 'extend',
                'hostids': _host_id,
                'search': {'key_': _proc_mem_rss_item_key}
            }
            _item = self.request('item.get', _item_params)
            _item_id = _item['result'][0]['itemid']

            # gitems 需要注意顺序
            _graph_params = {
                'name': _proc_mem_rss_item_name,
                'width': 900,
                'height': 200,
                'graphtype': 1,
                'gitems': [
                    {'itemid': _item_id, 'color': '00FF00'},
                    {'itemid': _vm_total_id, 'color': '1E88E5'}
                ]
            }
            _ = self.request('graph.create', _graph_params)
            logger.success(_)

            # --------------------------------------------------------------------------------

            # Memory used (pmem)

            # Item Params
            _item_params = {
                'output': 'extend',
                'hostids': _host_id,
                'search': {'key_': _proc_mem_pmem_item_key}
            }
            _item = self.request('item.get', _item_params)
            _item_id = _item['result'][0]['itemid']

            # Graph Params
            _graph_params = {
                'name': _proc_mem_pmem_item_name,
                'width': 900,
                'height': 200,
                'graphtype': 1,
                'yaxismin': 0,
                'yaxismax': 100,
                'ymin_type': 1,
                'ymax_type': 1,
                'gitems': [
                    {'itemid': _item_id, 'color': '66BB6A'}
                ]
            }
            _ = self.request('graph.create', _graph_params)
            logger.success(_)
