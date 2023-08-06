import collections
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import logging
from operator import itemgetter
from datetime import datetime
import re
import tqdm
import sys


logger = logging.getLogger("Main")


class ExcelWriter:
    """Generates an Excel file from scanner data"""

    
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.workbook = None
        self.data = None
        self.forceSingleHMC = False     # if True only summary data is provided
        self.version = ''

    
    def _setFonts(self):
        #self.header = self.workbook.add_format({'bold': True, 'bg_color': '#CCFFCC', 'text_wrap': True})
        self.header = self.workbook.add_format({'text_wrap': True, 'valign': 'top'})
        self.header45 = self.workbook.add_format({'text_wrap': False, 'valign': 'top', 'rotation': 45})
        self.bold = self.workbook.add_format({'bold': True})
        self.normal = self.workbook.add_format()
        self.float2digits = self.workbook.add_format({'num_format': '0.00'})
        self.integer = self.workbook.add_format({'num_format': '0'})
        self.integerThousand = self.workbook.add_format({'num_format': '#,##0'})



    def generate(self, data):
        if not isinstance(data, list):
            data = [data]
        self.data = data
        self.workbook = xlsxwriter.Workbook(self.fileName)
        self._setFonts()
        self._header()
        self._hmc()
        self._systemSummary()

        # if there is a chance that two HMC have a different view of same managed system name
        # do not generate other data. Caller will generate one XLSX for each HMC!
        steps = [
            ['System Details', self._systemDetails(),],
            ['OnOff Bill Data', self._onOffBillData(),],
            ['CoD Capacity Data', self._codCapacityData(),],
            ['CoD History', self._codHistory(),],
            ['System Microcode', self._sysCode(),],
            ['Virtual Switch', self._vSwitch(),],
            ['CPU/RAM Summary', self._system_CPU_RAM(),],
            ['Processor Pool', self._procPool(),],
            ['System I/O', self._systemIO(),],
            ['LPAR CPU/RAM Summary', self._lparCpuRam(),],
            ['LPAR Details', self._LPARdetails(),],
            ['LPAR CPY/RAM Details', self._LPAR_CPURAM_details(),],
            ['Virtual Adapter Details', self._LPAR_vadapter_details(),],
            ['LPAR Profile CPU/RAM', self._LPAR_profile_CPURAM(),],
            ['LPAR Profile Virt Adapter', self._LPAR_profile_vadapter(),],
            ['LPAR Profile Phys Adapter', self._LPAR_profile_physadapter(),],
            ['NPIV', self._VIOS_npiv(),],
            ['vSCSI Map', self._VIOS_vscsi()],
            ['VIOS Disks', self._VIOS_disk(),],
            ['SEA', self._SEA(),],
            ['VIOS Eth Physical', self._VIOS_eth(),],
            ['VIOS EtherChannel', self._VIOS_etherchannel(),],
            ['VIOS Eth Statistics', self._VIOS_eth_stats()],
            ['VIOS Fibre Channel Physical', self._VIOS_fcs(),],
            ['SR-IOV Adapter', self._sriov_adapter(),],
            ['SR-IOV Logical Port', self._sriov_logicalPort(),], 
            ['SR-IOV Logical Port ETH', self._sriov_logicalPort_eth(),],
            ['SR-IOV Logical Port ROCE', self._sriov_logicalPort_roce(),],
            ['SR-IOV Physical Port ETH', self._sriov_physicalPort_eth(),], 
            ['SR-IOV Physical Port ETHC', self._sriov_physicalPort_ethc(),],
            ['SR-IOV Physical Port ROCE', self._sriov_physicalPort_roce(),],          
            ['SR-IOV Physical vNIC', self._sriov_vnic(),],         
        ]
        if not self.forceSingleHMC:
            maxSize = max([len(s[0]) for s in steps])
            progression  = tqdm.tqdm(bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', 
                                    leave=False, 
                                    file=sys.stdout, total=len(steps))
            for s in steps:
                progression.set_description(f'{s[0]:<{maxSize}}')
                s[1]
                progression.update(1)
            progression.close()
            print('\n')
        self.workbook.close()




    def _formatValue(self, value, thousand=False, sortList=False):
        """ Return (formatted value, formatType) """
        if type(value) is list:
            if sortList:
                value = sorted(value)
            value = ','.join(value)
            format = self.normal
            return value, format

        if type(value) is float:
            format = self.float2digits
            return value, format

        if type(value) is int:
            format = self.integer
            if thousand:
                format = self.integerThousand
            return value, format

        format = self.normal
        if 'E' not in value and 'e' not in value:
            try:
                value = int(value)
                format = self.integer
                if thousand:
                    format = self.integerThousand
            except:
                try:
                    value = float(value)
                    format = self.float2digits
                except:
                    pass
        return value, format

    def _header(self):
        worksheet = self.workbook.add_worksheet('Header')
        if self.version:
            worksheet.write(0, 0, f'hmcScanner version {self.version}', self.bold)
        worksheet.write(1, 0, 'Send comments, suggestions or bugs to vagnini@it.ibm.com')
        worksheet.write(3, 0, 'To install hmcscanner run "pip install hmcscanner" or "python -m pip install hmcscanner" (python3 is required)')
        worksheet.write(4, 0, 'To update the hmcscanner run "pip install hmcscanner --upgrade" or "python -m pip install hmcscanner --upgrade"')
        worksheet.write(5, 0, 'To run the scanner with help: "hmcscanner --help"')
        worksheet.write(6, 0, 'Sample scanning of a single HMC: "hmcscanner --hmc <HMC name or IP> --user hscroot --pwd <the password>')
        worksheet.write(7, 0, 'Scanner report generated on', self.bold)
        worksheet.write(7, 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        worksheet.set_column(0, 0, 30)



    def _hmc(self):
        def writeline(title, name, row):
            worksheet.write(row, 0, title, self.bold)
            item = data.get(name, '')
            if not isinstance(item, list):
                item = [item]
            for n, i in enumerate(item):
                worksheet.write(row, 1+n, i)
            return row+1

        def getLineData(title, prefix):
            result = [title]
            for eth in ['eth0', 'eth1', 'eth2', 'eth3']:
                result.append(data.get(prefix+eth, ''))
            return result


        # Create one worksheet for each HMC numbering them from 1
        for n, d in enumerate(self.data):
            data = d['hmc']
            sheet_name = 'HMC ' + data['scanner_name']
            if len(sheet_name) > 31:
                sheet_name = 'HMC ' + data['scanner_name'].split('.')[0]
            if len(sheet_name) > 31:
                sheet_name = 'HMC #' + str(n+1)
            worksheet = self.workbook.add_worksheet(sheet_name)

            # Summary
            row = 0
            row = writeline('Hostname', 'hostname', row)
            row = writeline('Description', 'description', row)
            row = writeline('Date', 'date', row)
            row = writeline('Bios', 'bios', row)
            row = writeline('Type-Model', 'type_model', row)
            row = writeline('Serial', 'serial', row)
            row = writeline('Base Version', 'base_version', row)
            row = writeline('Build level', 'build_level', row)
            row = writeline('Service pack', 'service_pack', row)
            row = writeline('Fixes', 'fixes', row)

            # Adapters
            row += 1
            table = {'autofilter': False}

            table['data'] = []
            table['data'].append(getLineData('Speed', 'speed_'))
            table['data'].append(getLineData('Duplex', 'duplex_'))
            table['data'].append(getLineData('Jumbo frame', 'jumboframe_'))
            table['data'].append(getLineData('TSO', 'tso_'))
            table['data'].append(getLineData('IPV4 Addr', 'ipv4addr_'))
            table['data'].append(getLineData('IPV4 Netmask', 'ipv4netmask_'))
            table['data'].append(getLineData('IPV4 DHCP', 'ipv4dhcp_'))
            table['data'].append(getLineData('IPV6 Auto', 'ipv6auto_'))
            table['data'].append(getLineData('IPV6 Addr', 'ipv6addr_'))
            table['data'].append(getLineData('IPV6 Privacy', 'ipv6privacy_'))
            table['data'].append(getLineData('IPV6 DHCP', 'ipv6dhcp_'))
            table['data'].append(getLineData('LPAR Comm', 'lparcomm_'))
            table['data'].append(getLineData('DHCP Server', 'dhcpserver_'))

            table['columns'] = [{'header': ' '}]
            for colName in ['eth0', 'eth1', 'eth2', 'eth3']:
                table['columns'].append({'header': colName})

            worksheet.add_table(row, 0, row+len(table['data']), 4, options=table)

            # Serial line
            row = row+len(table['data']) + 2
            row = writeline('SLIP IP', 'slipipaddr', row)
            row = writeline('SLIP Netmask', 'slipnetmask', row)
            row = writeline('SLIP Addresses', 'slpipaddrs', row)

            # DNS
            row += 1
            row = writeline('DNS', 'dns', row)
            row = writeline('Domain', 'domain', row)
            row = writeline('Domain suffix', 'domainsuffix', row)
            row = writeline('Nameserver', 'nameserver', row)

            # Network config
            row += 1
            row = writeline('IP', 'ipaddr', row)
            row = writeline('Netmask', 'networkmask', row)
            row = writeline('Geteway', 'gateway', row)

            # LPAR
            row += 1
            row = writeline('IP LPAR', 'ipaddrlpar', row)
            row = writeline('IPV6 LPAR', 'ipv6addrlpar', row)
            row = writeline('Netmask LPAR', 'networkmasklpar', row)

            # Clients
            row += 1
            row = writeline('Clients', 'clients', row)

            worksheet.set_column(0, 4, 14)


    def _systemSummary(self):
        worksheet = self.workbook.add_worksheet('System Summary')


        # Aggregate managed system data by managed system name. Same name may be used on multiple HMCs
        managedSystem = {}
        for hmcData in self.data:
            for ms, value in hmcData['managed_system'].items():
                managedSystem[ms] = managedSystem.get(ms, [])
                managedSystem[ms].append(value)
                value['_HMC'] = hmcData['hmc']['scanner_name']      # SIDE EFFECT: add HMC name into managed system data


        # Column definition
        name_type = [
            ['Managed System', self.normal],
            ['HMC', self.normal],
            ['Status', self.normal],
            ['Type Model', self.normal],
            ['Serial', self.normal],
            ['GHz', self.float2digits],
            ['CPU Type', self.normal],
            ['Tot Cores', self.integer], 
            ['Act Cores', self.integer], 
            ['Deconf Cores', self.integer], 
            ['Curr Avail Cores', self.float2digits],
            ['Pend Avail Cores', self.float2digits], 
            ['VIOS-Linux cores', self.integer], 
            ['General cores', self.integer], 
            ['Tot GB', self.integerThousand], 
            ['Act GB', self.integerThousand], 
            ['Deconf GB', self.integerThousand], 
            ['Firm GB', self.integerThousand], 
            ['Curr Avail GB', self.integerThousand],
            ['Pend Avail GB', self.integerThousand],
            ['Perf Sample Rate', self.integer],
            #['Mgr #1', self.normal], 
            #['Mgr #2', self.normal], 
            ['Prim SP', self.normal], 
            ['Sec SP', self.normal], 
            ['EC Number', self.normal], 
            ['IPL Level', self.normal], 
            ['Active Level', self.normal], 
            ['Deferred Level', self.normal]
        ]
        # Define columns structure for Table creation setting only column names
        columns = [{'header': nt[0]} for nt in name_type]

        # Add table
        worksheet.add_table(0, 0, len(managedSystem), len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, label in enumerate(name_type):
            worksheet.write(0, n, label[0], self.header)

        # Write the rows
        row = 1
        for msName in sorted(managedSystem.keys()):
            #worksheet.write(row, 0, msName, self.bold)
            #colSize[0] = max(colSize[0], len(msName))
            ms = managedSystem[msName]

            # Check that we do not have multiple physical systems with the same name
            serials = [x['serial_num'] for x in ms if 'serial_num' in x]
            if len(set(serials)) != 1:
                worksheet.write_row(
                    row, 0, [msName, 'Multiple serials with same name: scan single HMC!'])
                self.forceSingleHMC = True
                continue

            # Check that we do not have more than 2 HMC knowing the same managed system
            if len(serials) > 2:
                worksheet.write_row(
                    row, 0, [msName, 'More than 2 HMC knowing the same system: scan single HMC!'])
                self.forceSingleHMC = True
                continue

            # Check that managed system status is the same for all HMC
            states = [x['state'] for x in ms if 'state' in x]
            if len(set(states)) != 1:
                worksheet.write_row(
                    row, 0, [msName, 'Multiple states for the same system: scan single HMC!'])
                self.forceSingleHMC = True
                continue

            # We assume now that HMCs see the same data so we show only first instance!
            if ms[0]['state'] != 'Operating':
                data = [
                msName,
                ms[0]['_HMC'],
                ms[0]['state'],
                ms[0]['type_model'],
                ms[0]['serial_num'],
                ms[0].get('vios_freq', 'N/A'),
                ms[0].get('vios_cputype', 'N/A')]
                data = data + [0] * (len(name_type) - len(data))
            else:
                data = [
                    msName,
                    ms[0]['_HMC'],
                    ms[0]['state'],
                    ms[0]['type_model'],
                    ms[0]['serial_num'],
                    ms[0].get('vios_freq', 'N/A'),
                    ms[0].get('vios_cputype', 'N/A'),
                    float(ms[0]['_sysProc']['installed_sys_proc_units']),
                    float(ms[0]['_sysProc']['configurable_sys_proc_units']),
                    float(ms[0]['_sysProc']['deconfig_sys_proc_units']),
                    float(ms[0]['_sysProc']['curr_avail_sys_proc_units']),
                    float(ms[0]['_sysProc']['pend_avail_sys_proc_units']),
                    float(ms[0]['_sysProc'].get('configurable_sys_proc_units_linux_vios', 0)),
                    float(ms[0]['_sysProc'].get('configurable_sys_proc_units_all_os',ms[0]['_sysProc']['configurable_sys_proc_units'])),
                    float(ms[0]['_sysMem']['installed_sys_mem']),
                    float(ms[0]['_sysMem']['configurable_sys_mem']),
                    float(ms[0]['_sysMem']['deconfig_sys_mem']),
                    float(ms[0]['_sysMem']['sys_firmware_mem']),
                    float(ms[0]['_sysMem']['curr_avail_sys_mem']),
                    float(ms[0]['_sysMem']['pend_avail_sys_mem']),
                    float(ms[0]['lslparutil'].get('sample_rate', 0) if ms[0].get('lslparutil', None) is not None else 0),
                    #ms[0]['_HMC'],
                    #ms[1]['_HMC'] if len(ms) > 1 else 'N/A',
                    ms[0].get('ipaddr', 'N/A'),
                    ms[0].get('ipaddr_secondary', 'N/A'),
                    ms[0]['_lslic']['ecnumber'],
                    ms[0]['_lslic']['installed_level'],
                    ms[0]['_lslic']['activated_level'],
                    ms[0]['_lslic']['deferred_level'],
                ]

            # Write each cell using column format
            for n, (value, param) in enumerate(zip(data, name_type)):
                worksheet.write(row, n, value, param[1])

            # Go to next row
            row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed system name
        worksheet.set_column(1, 1, 12)      # HMC
        worksheet.set_column(2, 2, 12)      # Status
        worksheet.set_column(3, 4, 9)      # Type-Model, Serial
        worksheet.set_column(5, 5, 5)      # GHz
        worksheet.set_column(6, 6, 18)      # CPU Type
        worksheet.set_column(7, 13, 8)      # CPU data
        worksheet.set_column(14, 19, 10)      # RAM data
        worksheet.set_column(20, 20, 7)      # Perf data
        worksheet.set_column(21, 22, 12)      # IP
        worksheet.set_column(23, 26, 8)      # LIC
        worksheet.set_column(27, 35, 2)      # Empty


    def _systemDetails(self):
        worksheet = self.workbook.add_worksheet('System Details')
        worksheet.freeze_panes(1, 1)

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value
            
        # Detect variables and number of managed systems
        vars = set()
        for ms, value in managedSystem.items():
            vars = vars.union([k for k, v in value.items() if not k.startswith('_') and type(v) in [int, float, str, list]])
        vars = sorted(vars)
        #vars.remove('_HMC') # we do not it!
        vars.remove('name') # we do not it!

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}] + [{'header': v} for v in vars]

        # Add table
        worksheet.add_table(0, 0, len(managedSystem.keys()), 1+len(vars), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write Managed System data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            worksheet.write(row, 0, ms, self.normal)
            worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
            for n, v in enumerate(vars):
                value, format = self._formatValue(managedSystem[ms].get(v, 'N/A'))
                worksheet.write(row, 2+n, value, format)
            row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 31, 6)
        worksheet.set_column(32, 33, 15)
        worksheet.set_column(34, 38, 6)
        worksheet.set_column(39, 39, 49)
        worksheet.set_column(40, 78, 6)
        worksheet.set_column(79, 79, 18)
        worksheet.set_column(80, 89, 6)
        worksheet.set_column(90, 95, 2)


    def _system_CPU_RAM(self):
        worksheet = self.workbook.add_worksheet('System CPU RAM')
        worksheet.freeze_panes(1, 1)

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                if value['state'] == 'Operating':
                    managedSystem[ms] = value
            
        # Detect variables and number of managed systems
        cpu_vars = set()
        ram_vars = set()
        for ms, value in managedSystem.items():
            cpu_vars = cpu_vars.union( [k for k, v in value['_sysProc'].items()] )
            ram_vars = ram_vars.union( [k for k, v in value['_sysMem'].items()] )
        cpu_vars = sorted(cpu_vars)
        ram_vars = sorted(ram_vars)

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}
                   ] + [{'header': v} for v in cpu_vars+ram_vars]

        # Add table
        worksheet.add_table(0, 0, len(managedSystem), 1+len(cpu_vars)+len(ram_vars), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write Managed System data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            worksheet.write(row, 0, ms, self.normal)
            worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
            for n, v in enumerate(cpu_vars):
                value, format = self._formatValue(managedSystem[ms]['_sysProc'].get(v, 'N/A'))
                worksheet.write(row, 2+n, value, format)
            for n, v in enumerate(ram_vars):
                value, format = self._formatValue(managedSystem[ms]['_sysMem'].get(v, 'N/A'), thousand=True)
                worksheet.write(row, 2+len(cpu_vars)+n, value, format)
            row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      
        worksheet.set_column(1, 1, 15)


      

    def _lparCpuRam(self):
        worksheet = self.workbook.add_worksheet('LPAR CPU RAM')

        # Data: one entry for each managed system. Every entry is a dictionary of lpar data
        managedSystem = {}
        for hmcData in self.data:
            for ms, value in hmcData['managed_system'].items():
                #managedSystem[ms] = { '_HMC': hmcData['hmc']['scanner_name'], 'lpar': value['_lpar'] }
                managedSystem[ms] = value

        # Column definition
        name_type = [
            ['HMC', self.normal],
            ['Managed System', self.normal],
            ['LPAR Name', self.normal],
            ['ID', self.integer],
            ['LPAR Type', self.normal],
            ['OS Version', self.normal],
            ['Proc Mode', self.normal],         # es. POWER9
            ['Active', self.normal],
            ['Proc Type', self.normal],         # es linux_vios
            ['CPU Mode', self.normal],         # Ded, shared
            ['CPUs', self.integer],             # Virtual or Dedicated
            ['Entitled Cap', self.float2digits],     # EC if shared, CPU is ded
            ['Sharing mode', self.normal],
            ['Weight', self.integer],
            ['Pool Name', self.normal],
            ['Memory mode', self.normal],
            ['GB', self.integerThousand],
        ]
        # Define columns structure for Table creation setting only column names
        columns = [{'header': nt[0]} for nt in name_type]

        # Add table
        worksheet.add_table(0, 0, sum([ len(ms['_lpar'].keys()) for ms in managedSystem.values() ]),
                            len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, label in enumerate(name_type):
            worksheet.write(0, n, label[0], self.header)

        # Write the rows
        row = 1
        for msName in sorted(managedSystem.keys()):
            ms = managedSystem[msName]
            for lparName in sorted(ms['_lpar'].keys()):
                lpar = ms['_lpar'][lparName]
                data = [
                    ms['_HMC'],
                    msName,
                    lparName,
                    int(lpar['conf']['lpar_id']),
                    lpar['conf']['lpar_env'],
                    lpar['conf']['os_version'],
                    lpar['conf']['curr_lpar_proc_compat_mode'],
                    lpar['conf']['state'],
                    lpar['proc'].get('proc_type',''),
                    lpar['proc']['curr_proc_mode'],
                    int(lpar['proc']['run_procs']),
                    float(lpar['proc'].get('run_proc_units',
                                     lpar['proc']['run_procs'])),    # if ded cpu put CPU in Ent
                    lpar['proc']['curr_sharing_mode'],
                    #int(lpar['proc'].get('curr_uncap_weight','')),
                    int(lpar['proc']['curr_uncap_weight']) if 'curr_uncap_weight' in lpar['proc'] else '',
                    lpar['proc'].get('curr_shared_proc_pool_name',''),
                    lpar['mem']['mem_mode'],
                    int(lpar['mem']['curr_mem']),
                ]

                # Write each cell using column format
                for n, (value, param) in enumerate(zip(data, name_type)):
                    worksheet.write(row, n, value, param[1])

                # Put a comment where we copy CPU in Ent
                if not 'run_proc_units' in lpar['proc']:
                    worksheet.write_comment(row, 11, 'Dedicated CPU LPAR\nCopy cores into Entitled Capacity')

                # Put a comment on pool cell if not DefaultPool
                pool = lpar['proc'].get('curr_shared_proc_pool_name', 'DefaultPool')
                if  pool != 'DefaultPool':
                    worksheet.write_comment(row, 14, f"Pool size = {ms['_procPool'][pool]['max_pool_proc_units']}")

                # Go to next row
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 12)      # IP
        worksheet.set_column(1, 1, 35)      # Managed system name
        worksheet.set_column(2, 2, 35)      # LPAR name
        worksheet.set_column(3, 3, 5)      # ID
        worksheet.set_column(4, 4, 10)      # LPAR Type
        worksheet.set_column(5, 5, 35)      # OS Version
        worksheet.set_column(6, 6, 18)      # CPU Type
        worksheet.set_column(7, 7, 13)      # Status
        worksheet.set_column(8, 8, 10)      # Proc Type 
        worksheet.set_column(9, 9, 8)      # CPU Mode
        worksheet.set_column(10, 10, 5)      # CPUs
        worksheet.set_column(11, 11, 8)      # Entitled Cap
        worksheet.set_column(12, 12, 23)      # Sharing mode
        worksheet.set_column(13, 13, 7)      # Weight
        worksheet.set_column(14, 14, 12)      # Pool Name
        worksheet.set_column(15, 15, 8)      # Memory mode
        worksheet.set_column(16, 16, 10)      # GB
        worksheet.set_column(17, 20, 2)      # Empty


    # Recursively scan objects's items. The object may have "children" key to scan into
    # Return the number of items
    def _count_IO_lines(self, object):
        result = 0
        if not isinstance(object, list):
            object = [object]
        for item in object:
            result += 1
            if 'children' in item:
                result += self._count_IO_lines(item['children'])
        return result


    # Recursively scan objects's keys. The object may have "children" key to scan into
    # Return a set of keys
    def _scanNames(self, object):
        result = set()
        if not isinstance(object, list):
            object = [object]
        for item in object:
            result = result.union(item.keys())
            if 'children' in result:
                result.remove('children')
                result = result.union(self._scanNames(item['children']))
        return result


    def _write_IO_lines(self, slot, row, object, worksheet, varNames, ms, hmc):
        worksheet.write(row, 0, ms, self.normal)
        worksheet.write(row, 1, hmc, self.normal)
        worksheet.write(row, 2, slot, self.normal)

        if 'ischild' in object:
            worksheet.write(row, 3, 'Y', self.normal)
        else:
            worksheet.write(row, 3, 'N', self.normal)

        for n, v in enumerate(varNames):
            value, format = self._formatValue(object.get(v, 'N/A'))
            worksheet.write(row, 4+n, value, format)
        row += 1

        if 'children' in object:
            byPysLoc = {}
            for obj in object['children']:
                obj['ischild'] = True
                byPysLoc[obj['phys_loc']] = byPysLoc.get(obj['phys_loc'], [])
                byPysLoc[obj['phys_loc']].append(obj)

            #data = { obj['phys_loc']: obj for obj in object['children'] }
            for physLoc in self._slotSort(byPysLoc.keys()):
                for item in byPysLoc[physLoc]:
                    row = self._write_IO_lines(
                        obj['phys_loc'], row, item, worksheet, varNames, ms, hmc)
        
        return row


    def _slotSort(self, data):
        # [ 'U78CB.001.WZS10G7-P1-C15', 'U78CB.001.WZS10G7-P1-T2', 'U78CB.001.WZS10G7-P1-C1']
        dataSplit = [ d.split('-') for d in data ]
        if [ len(d) for d in dataSplit ].count(len(dataSplit[0])) == len(data):
            # all elements have the same structure: sort by prefix and last integer
            data = [['-'.join(d[:-1]) + '-' + d[-1][:1], int(d[-1][1:])]
                    for d in dataSplit]
            data = sorted(data, key=itemgetter(0, 1))
            data = [ d[0]+str(d[1]) for d in data ]
            return data

        # Different structure: just perform lexical sort
        data = sorted(data)
        return data



    def _systemIO(self):
        worksheet = self.workbook.add_worksheet('System IO')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                if value['state'] == 'Operating':
                    managedSystem[ms] = value
            
        # Detect variables
        varNames = set()
        for ms, value in managedSystem.items():
            varNames = varNames.union( *[ self._scanNames(object) for object in value['_sysIO'].values() ] )
        varNames.remove('drc_name')  # we do not it!
        varNames.remove('phys_loc')

        # Force my order
        primaryVars = ['description', 'lpar_name', 'wwpn', 'wwnn', 'mac_address']
        otherVars = sorted( set(varNames)-set(primaryVars) )
        varNames = primaryVars + otherVars

        # Detect the number of lines to be written
        ioslotObj = [ obj['_sysIO'] for obj in managedSystem.values() if '_sysIO' in obj ]
        lines =  [self._count_IO_lines(list(obj.values())) for obj in ioslotObj] 
        lines = sum( lines )

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}, {'header': 'Location'}, {'header': 'is Child'}] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, lines, 3+len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write slotIO data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            if '_sysIO' in managedSystem[ms]:
                slots = self._slotSort(managedSystem[ms]['_sysIO'].keys())
                for slot in slots:
                    row = self._write_IO_lines(
                        slot, row, managedSystem[ms]['_sysIO'][slot], worksheet, varNames, ms, managedSystem[ms]['_HMC'])

        # Static column width
        worksheet.set_column(0, 0, 35)      # Manages System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 5)       # is Child
        worksheet.set_column(3, 3, 30)      # phys_loc
        worksheet.set_column(4, 4, 45)      # description
        worksheet.set_column(5, 5, 35)      # LPAR
        worksheet.set_column(6, 7, 18)      # wwpn, wwnn
        worksheet.set_column(8, 8, 14)      # MAC 


    def _procPool(self):
        worksheet = self.workbook.add_worksheet('Processor Pools')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                if value['state'] == 'Operating':
                    managedSystem[ms] = value
            
        # Detect the number of lines to be written: one line for each pool
        numpools = sum([len(ms['_procPool'].keys()) for ms in managedSystem.values()])

        # Define columns structure for Table creation setting only column names
        nameType = [
            ['Managed System', self.normal],
            ['HMC', self.normal],
            ['Active cores', self.integer],
            ['Deconf cores', self.integer],
            ['Available cores', self.integer],
            ['Ded cores to off LPARs', self.integer],
            ['Ded cores to active LPARs', self.integer],
            ['Default Pool size', self.integer],
            ['Max donating cores', self.integer],
            ['Ent capacity to active LPARs', self.float2digits],
            ['Ent capacity left', self.float2digits],
            ['Virtual Procs for active LPARs', self.integer],
            ['Pool Name', self.normal], 
            ['Size', self.integer],
            ['Curr Resrvd', self.float2digits],
            ['Pend Reservd', self.float2digits],
            ['LPARs', self.normal],
            ['Active LPARs', self.integer],
            ['Ent assigned', self.float2digits],
            ['Ent left', self.float2digits],
            ['Active VPs', self.integer]
        ]

        # Define columns structure for Table creation setting only column names
        columns = [{'header': v[0]} for v in nameType]

        # Add table
        worksheet.add_table(0, 0, numpools, len(nameType)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(nameType):
            worksheet.write(0, n, v[0], self.header45)

        # Write pool data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            pool = ['DefaultPool'] + sorted( [ p for p in managedSystem[ms]['_procPool'].keys() if p != 'DefaultPool'] )
            for p in pool:

                # fixup: managedSystem[ms]['_procPool'][p]['lpar_names'] is not an array if only one LPAR
                if 'lpar_names' in managedSystem[ms]['_procPool'][p] and not isinstance(managedSystem[ms]['_procPool'][p]['lpar_names'], list):
                    managedSystem[ms]['_procPool'][p]['lpar_names'] = [
                        managedSystem[ms]['_procPool'][p]['lpar_names']]

                data = [
                    ms,                                                     # managed system
                    managedSystem[ms]['_HMC'],                              # HMC name
                    # active cores
                    float(managedSystem[ms]['_sysProc']
                          ['configurable_sys_proc_units']),
                    float(managedSystem[ms]['_sysProc']['deconfig_sys_proc_units']),              # deconfigured cores
                    None,                                                   # formula: Available cores
                    sum([int(lpar['proc']['curr_procs'])                         # Ded cores to off LPARs
                            for lpar in managedSystem[ms]['_lpar'].values() 
                            if lpar['conf']['state']=='Not Activated' 
                                and lpar['proc']['curr_proc_mode']=='ded' 
                                and lpar['proc']['curr_sharing_mode'] in ['keep_idle_procs', 'share_idle_procs_active']]),
                    sum([int(lpar['proc']['curr_procs'])                         # Ded cores to active LPARs
                         for lpar in managedSystem[ms]['_lpar'].values()
                         if lpar['conf']['state'] == 'Running'
                         and lpar['proc']['curr_proc_mode'] == 'ded']),
                    None,                                                   # formula: Default Pool size
                    sum([int(lpar['proc']['curr_procs'])                         # Max donating cores
                         for lpar in managedSystem[ms]['_lpar'].values()
                         if lpar['conf']['state'] == 'Running'
                         and lpar['proc']['curr_proc_mode'] == 'ded'
                         and lpar['proc']['curr_sharing_mode'] in ['share_idle_procs_active', 'share_idle_procs_always']]),
                    sum([float(lpar['proc']['curr_proc_units'])                    # Ent capacity to active LPARs
                         for lpar in managedSystem[ms]['_lpar'].values()
                         if lpar['conf']['state'] == 'Running'
                         and lpar['proc']['curr_proc_mode'] == 'shared']),
                    None,                                                   # formula: Ent capacity left
                    sum([int(lpar['proc']['curr_procs'])                    # Virtual Procs for active LPARs
                         for lpar in managedSystem[ms]['_lpar'].values()
                         if lpar['conf']['state'] == 'Running'
                         and lpar['proc']['curr_proc_mode'] == 'shared']),
                    p,                                                      # pool name
                    float(managedSystem[ms]['_procPool'][p]['max_pool_proc_units']) if p != 'DefaultPool' else '', # size of pool
                    float(managedSystem[ms]['_procPool'][p]['curr_reserved_pool_proc_units']) if p != 'DefaultPool' else '',    # curr reserved only if not DefaultPool
                    float(managedSystem[ms]['_procPool'][p]['pend_reserved_pool_proc_units']) if p != 'DefaultPool' else '',    # pend reserved only if not DefaultPool
                    len(managedSystem[ms]['_procPool'][p].get('lpar_names',[])) if p != 'DefaultPool' else '',                  # LPARs in pool
                    sum([1 for name in managedSystem[ms]['_procPool'][p].get('lpar_names',[]) if managedSystem[ms]['_lpar']
                        [name]['conf']['state'] == 'Running']) if p != 'DefaultPool' else '',  # Active LPARs
                    sum([float(managedSystem[ms]['_lpar'][name]['proc']['curr_proc_units']) for name in managedSystem[ms]['_procPool'][p].get('lpar_names', []) if managedSystem[ms]['_lpar']
                        [name]['conf']['state'] == 'Running']) if p != 'DefaultPool' else '',  # Ent assigned
                    None,                                                   # formula: Formula: ent left
                    sum([int(managedSystem[ms]['_lpar'][name]['proc']['curr_procs']) for name in managedSystem[ms]['_procPool'][p].get('lpar_names', []) if managedSystem[ms]['_lpar']
                        [name]['conf']['state'] == 'Running']) if p != 'DefaultPool' else '',  # Active VPs
                ]

                for n, v in enumerate(data):
                    if v is not None:
                        worksheet.write(row, n, v, nameType[n][1])

                # formula: Available cores
                worksheet.write_formula(
                    row, 4, '='+xl_rowcol_to_cell(row, 2)+'-'+xl_rowcol_to_cell(row, 3), nameType[4][1])   
                # formula: Default Pool size   
                worksheet.write_formula(row, 7, '='+xl_rowcol_to_cell(row, 4)+'-'+xl_rowcol_to_cell(row, 5)+'-'+xl_rowcol_to_cell(row, 6), nameType[7][1])
                # formula: Ent capacity left  
                worksheet.write_formula(row, 10, '='+xl_rowcol_to_cell(row, 7)+'-'+xl_rowcol_to_cell(row, 9), nameType[10][1])
                # formula: Formula: ent left
                if p != 'DefaultPool':
                    worksheet.write_formula(row, 19, '='+xl_rowcol_to_cell(row, 13)+'-'+xl_rowcol_to_cell(row, 18)+'-'+xl_rowcol_to_cell(row, 14), nameType[19][1])
                else:
                    worksheet.write(row, 19, '', nameType[19][1])

                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Manages System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 11, 6)      
        worksheet.set_column(12, 12, 20)      # Pool name
        worksheet.set_column(13, 20, 6)      
        worksheet.set_column(21, 30, 2)      # LPAR


    def _sysCode(self):
        worksheet = self.workbook.add_worksheet('System microcode')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value
            
        # Detect variables
        varNames = set()
        for ms, value in managedSystem.items():
            varNames = varNames.union( value['_lslic'].keys() )
        varNames = sorted(varNames)

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, len(managedSystem.keys()), 1+len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write ms data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            worksheet.write(row, 0, ms, self.normal)
            worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
            for n, v in enumerate(varNames):
                value, format = self._formatValue(managedSystem[ms]['_lslic'].get(v, 'N/A'))
                worksheet.write(row, 2+n, value, format)
            row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 5)   
        worksheet.set_column(3, 3, 9)  
        worksheet.set_column(4, 4, 5)     
        worksheet.set_column(5, 7, 9)
        worksheet.set_column(8, 11, 5)
        worksheet.set_column(12, 13, 9)
        worksheet.set_column(14, 14, 5)
        worksheet.set_column(15, 15, 9)
        worksheet.set_column(16, 16, 15)
        worksheet.set_column(17, 17, 9)
        worksheet.set_column(18, 18, 5)
        worksheet.set_column(19, 19, 9)
        worksheet.set_column(20, 20, 16)
        worksheet.set_column(21, 21, 9)
        worksheet.set_column(22, 22, 18)
        worksheet.set_column(23, 24, 7)
        worksheet.set_column(25, 26, 9)
        worksheet.set_column(27, 28, 5)
        worksheet.set_column(29, 30, 9)
        worksheet.set_column(31, 31, 5)
        worksheet.set_column(32, 34, 9)
        worksheet.set_column(35, 36, 5)
        worksheet.set_column(37, 38, 9)
        worksheet.set_column(39, 39, 11)
        worksheet.set_column(40, 41, 5)


    def _vSwitch(self):
        worksheet = self.workbook.add_worksheet('Virtual Switch')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value
            
        # Define columns structure for Table creation setting only column names
        columns = [
                    {'header': 'Managed System'}, 
                    {'header': 'HMC'},
                    {'header': 'Name'},
                    {'header': 'Mode'},
                    {'header': 'Allowed LPAR ids'},
                    {'header': 'VLAN ids'},
        ] 

        # Detect number of vSwitches
        vswNum = sum([ len(ms['_vswitch'].keys()) for ms in managedSystem.values() ])

        # Add table
        worksheet.add_table(0, 0, vswNum, len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write ms data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for name in sorted(managedSystem[ms]['_vswitch'].keys()):
                obj = managedSystem[ms]['_vswitch'][name]
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, name, self.normal)
                worksheet.write(row, 3, obj['switch_mode'], self.normal)

                obj['allowed_lpar_ids'] = obj.get('allowed_lpar_ids', '') 
                if isinstance(obj['allowed_lpar_ids'], list):
                    worksheet.write(row, 4, 
                        ','.join(sorted([ int(n) for n in sorted(obj['allowed_lpar_ids']) ])),
                        self.normal)
                else:
                    worksheet.write(row, 4, obj['allowed_lpar_ids'], self.normal)

                if isinstance(obj['vlan_ids'], list):
                    worksheet.write(row, 5,
                                    ','.join( [ str(n) for n in sorted([int(n) for n in obj['vlan_ids']]) ] ),
                                    self.normal)
                else:
                    worksheet.write(
                        row, 5, obj['vlan_ids'], self.normal)

                row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 30)   
        worksheet.set_column(3, 3, 5)  
        worksheet.set_column(4, 5, 100)     
        worksheet.set_column(6, 10, 2)



    def _onOffBillData(self):
        worksheet = self.workbook.add_worksheet('Elastic CoD Billing')

        numRows = 0

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = {}
                managedSystem[ms]['_HMC'] = value['_HMC']

                # insert resource type and datetime
                for item in value['_lscodBillProc']:
                    item['_type'] = 'processor'
                    item['_datetime'] = datetime( 
                        *([int(n) for n in item['collection_date'].split('-')+item['collection_time'].split(':')])  
                    )
                for item in value['_lscodBillMem']:
                    item['_type'] = 'memory'
                    item['_datetime'] = datetime( 
                        *([int(n) for n in item['collection_date'].split('-')+item['collection_time'].split(':')])  
                    )

                # create a time sorted list of items
                managedSystem[ms]['_data'] = sorted(
                    value['_lscodBillProc'] + value['_lscodBillMem'], 
                    key=itemgetter('_datetime') 
                )

                numRows += len(managedSystem[ms]['_data'])

        if numRows == 0:
            worksheet.write(0, 0, 'No data available')
            return

        # Detect variables
        varNames = set()
        for ms, value in managedSystem.items():
            varNames = varNames.union(
                *[obj.keys() for obj in value['_data']])
        if len(varNames)==0:
            # There is no data, skip tab
            return
        varNames.remove('collection_date')  # we do not it!
        varNames.remove('collection_time')  # we do not it!

        # Force my order
        primaryVars = ['_type', '_datetime']
        otherVars = sorted(set(varNames)-set(primaryVars))
        varNames = primaryVars + otherVars
            
        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}] + [ {'header':v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numRows, len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            if len(managedSystem[ms]['_data']) == 0:
                continue
            hmc = managedSystem[ms]['_HMC']
            for obj in managedSystem[ms]['_data']:
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(row, 1, hmc, self.normal)
                for n, v in enumerate(varNames):
                    worksheet.write(row, 2+n, str(obj.get(v,'')), self.normal)
                row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 9)
        worksheet.set_column(3, 3, 19)
        worksheet.set_column(4, 19, 18)


    def _codCapacityData(self):
        worksheet = self.workbook.add_worksheet('CoD Capacity')

        numRows = 0

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = {}
                managedSystem[ms]['_HMC'] = value['_HMC']
                managedSystem[ms]['_data'] = {}

                # There should be zero ot only one item in the list. Merge proc & mem
                if len(value['_lscodCapProc']) > 0:
                    for k, v in value['_lscodCapProc'][0].items():
                        managedSystem[ms]['_data'][k] = v
                if len(value['_lscodCapMem']):
                    for k, v in value['_lscodCapMem'][0].items():
                        managedSystem[ms]['_data'][k] = v

                if len(managedSystem[ms]['_data'].keys()) > 0:
                    numRows += 1

        if numRows == 0:
            worksheet.write(0, 0, 'No data available')
            return

        # Detect variables
        varNames = set()
        for ms, value in managedSystem.items():
            varNames = varNames.union([k for k in value['_data'].keys()])
        varNames = sorted(varNames)
        if len(varNames) == 0:
            # No data to display
            return

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numRows, len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            if len(managedSystem[ms]['_data'].keys()) == 0:
                continue
            worksheet.write(row, 0, ms, self.normal)
            worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
            for n, v in enumerate(varNames):
                value, format = self._formatValue(
                    managedSystem[ms]['_data'].get(v, ''))
                if v in ['activated_onoff_mem', 'avail_mem_for_onoff', 'unreturned_onoff_mem']:
                    format = self.integerThousand
                worksheet.write(row, 2+n, value, format)
            row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 5, 10)
        worksheet.set_column(6, 6, 18)
        worksheet.set_column(7, 12, 10)
        worksheet.set_column(13, 13, 18)
        worksheet.set_column(14, 15, 10)
        worksheet.set_column(16, 25, 2)



    def _codHistory(self):
        worksheet = self.workbook.add_worksheet('CoD History')

        numRows = 0

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = {}
                managedSystem[ms]['_HMC'] = value['_HMC']
                managedSystem[ms]['_data'] = []


                # insert resource type and datetime
                for item in value['_lscodHist']:
                    #re.split('/| |:',"12/17/2021 18:19:58")
                    time = re.split('/| |:',item['time_stamp'])
                    order = [2, 0, 1, 3, 4, 5]
                    time = [ int(time[i]) for i in order ]
                    managedSystem[ms]['_data'].append(
                        { 'time': datetime(*time),
                          'entry': item['entry'] if isinstance(item['entry'], str) else ','.join(item['entry'])
                        }
                    )
                    numRows += 1

                # sort by time
                managedSystem[ms]['_data'] = sorted(
                    managedSystem[ms]['_data'],
                    key=itemgetter('time') 
                )

        if numRows == 0:
            worksheet.write(0, 0, 'No data available')
            return
            
        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}, {'header': 'Time'}, {'header': 'Entry'}] 

        # Add table
        worksheet.add_table(0, 0, numRows, len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            if len(managedSystem[ms]['_data']) == 0:
                continue
            hmc = managedSystem[ms]['_HMC']
            for obj in managedSystem[ms]['_data']:
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(row, 1, hmc, self.normal)
                worksheet.write(row, 2, str(obj['time']), self.normal)
                worksheet.write(row, 3, obj['entry'], self.normal)
                row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 150)
        worksheet.set_column(4, 10, 2)



    def _LPARdetails(self):
        worksheet = self.workbook.add_worksheet('LPAR details')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value
            
        # Detect variables and LPARs
        varNames = set()
        numLPARs = 0 
        for ms, value in managedSystem.items():
            for lpar in value['_lpar'].values():
                varNames = varNames.union( lpar['conf'].keys() )
            numLPARs += len(value['_lpar'].keys())
        varNames = sorted(varNames)
        varNames.remove('name')

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'}, {'header': 'HMC'}, {'header': 'Name'}] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numLPARs, 2+len(varNames),
                            {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write lpar data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for lparName in sorted(managedSystem[ms]['_lpar'].keys()):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, lparName, self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(managedSystem[ms]['_lpar'][lparName]['conf'].get(v, 'N/A'))
                    worksheet.write(row, 3+n, value, format)
                row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)       # LPAR name
        worksheet.set_column(3, 6, 5)  
        worksheet.set_column(7, 7, 14)     
        worksheet.set_column(8, 8, 35)
        worksheet.set_column(9, 9, 5)
        worksheet.set_column(10, 10, 35)
        worksheet.set_column(11, 11, 9)
        worksheet.set_column(12, 14, 5)
        worksheet.set_column(15, 15, 11)
        worksheet.set_column(16, 16, 5)
        worksheet.set_column(17, 17, 9)
        worksheet.set_column(18, 19, 5)
        worksheet.set_column(20, 20, 18)
        worksheet.set_column(21, 21, 27)
        worksheet.set_column(22, 24, 5)
        worksheet.set_column(25, 25, 43)
        worksheet.set_column(26, 30, 5)
        worksheet.set_column(31, 31, 19)
        worksheet.set_column(32, 32, 5)
        worksheet.set_column(33, 33, 15)
        worksheet.set_column(34, 34, 9)
        worksheet.set_column(35, 36, 5)
        worksheet.set_column(37, 37, 14)
        worksheet.set_column(38, 43, 5)



    def _LPAR_CPURAM_details(self):
        worksheet = self.workbook.add_worksheet('LPAR CPU RAM details')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value
            
        # Detect variables and LPARs
        procVarNames = set()
        memVarNames = set()
        numLPARs = 0 
        for ms, value in managedSystem.items():
            for lpar in value['_lpar'].values():
                procVarNames = procVarNames.union( lpar['proc'].keys() )
                memVarNames = memVarNames.union( lpar['mem'].keys() )
            numLPARs += len(value['_lpar'].keys())
        procVarNames = sorted(procVarNames)
        procVarNames.remove('lpar_name')
        procVarNames.remove('lpar_id')
        memVarNames = sorted(memVarNames)
        memVarNames.remove('lpar_name')
        memVarNames.remove('lpar_id')

        # Define columns structure for Table creation setting only column names
        columns = [ {'header': 'Managed System'},
                    {'header': 'HMC'}, 
                    {'header': 'Name'}] + [{'header': v} for v in procVarNames+memVarNames]

        # Add table
        worksheet.add_table(0, 0, numLPARs, 2+len(procVarNames)+len(memVarNames),
                            {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write lpar data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for lparName in sorted(managedSystem[ms]['_lpar'].keys()):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, lparName, self.normal)
                for n, v in enumerate(procVarNames):
                    value, format = self._formatValue(managedSystem[ms]['_lpar'][lparName]['proc'].get(v, 'N/A'))
                    worksheet.write(row, 3+n, value, format)
                for n, v in enumerate(memVarNames):
                    value, format = self._formatValue(
                        managedSystem[ms]['_lpar'][lparName]['mem'].get(v, 'N/A'), thousand=True)
                    worksheet.write(row, 3+len(procVarNames)+n, value, format)
                row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)       # LPAR name
        worksheet.set_column(3, 6, 5)  
        worksheet.set_column(7, 7, 7)     
        worksheet.set_column(8, 10, 5)
        worksheet.set_column(11, 11, 12)
        worksheet.set_column(12, 17, 5)
        worksheet.set_column(18, 18, 7)
        worksheet.set_column(19, 21, 5)
        worksheet.set_column(22, 22, 12)
        worksheet.set_column(23, 24, 5)
        worksheet.set_column(25, 25, 10)
        worksheet.set_column(26, 32, 5)
        worksheet.set_column(33, 33, 11)
        worksheet.set_column(34, 34, 5)
        worksheet.set_column(35, 35, 11)
        worksheet.set_column(36, 36, 5)
        worksheet.set_column(37, 37, 11)
        worksheet.set_column(38, 39, 5)
        worksheet.set_column(40, 40, 6)
        worksheet.set_column(41, 43, 5)
        worksheet.set_column(44, 44, 11)
        worksheet.set_column(45, 45, 5)
        worksheet.set_column(46, 46, 11)
        worksheet.set_column(47, 47, 5)
        worksheet.set_column(48, 48, 11)
        worksheet.set_column(49, 50, 5)
        worksheet.set_column(51, 52, 11)
        worksheet.set_column(53, 53, 5)



    def _LPAR_vadapter_details(self):
        worksheet = self.workbook.add_worksheet('LPAR vadapter details')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value
            
        # Detect variables and LPARs
        varNames = set()
        numVadapters = 0 
        for ms, value in managedSystem.items():
            for lpar in value['_lpar'].values():
                for item in ['veth', 'vscsi', 'vfc']:
                    varNames = varNames.union(*[set(v.keys()) for v in lpar[item].values()])
                    numVadapters += len(lpar[item].keys())
        varNames = sorted(varNames)
        varNames.remove('lpar_name')
        varNames.remove('slot_num')

        # Define columns structure for Table creation setting only column names
        columns = [ {'header': 'Managed System'},
                    {'header': 'HMC'}, 
                    {'header': 'Name'},
                    {'header': 'Slot'},
                    {'header': 'Type'},
                    {'header': 'Bad configuration'}] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numVadapters, 5+len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write lpar data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for lparName in sorted(managedSystem[ms]['_lpar'].keys()):
                slots = [ 
                    {'slotid': int(s), 'type': k, 'data': v} 
                    for k in ['veth', 'vscsi', 'vfc'] 
                    for s, v in managedSystem[ms]['_lpar'][lparName][k].items()
                ]
                slots = sorted(slots, key=itemgetter('slotid'))
                for s in slots:
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, lparName, self.normal)
                    worksheet.write(row, 3, s['slotid'], self.integer)
                    worksheet.write(row, 4, s['type'], self.normal)
                    for n, v in enumerate(varNames):
                        value, format = self._formatValue(s['data'].get(v, ''))
                        worksheet.write(row, 6+n, value, format)

                    # Match control
                    if s['type'] in ['vscsi', 'vfc']:
                        match = False
                        if s['data']['remote_lpar_name'] in managedSystem[ms]['_lpar'].keys():
                            matching = managedSystem[ms]['_lpar'][s['data']['remote_lpar_name']][s['type']].get(
                                str(s['data']['remote_slot_num']), None)
                            if matching is not None:
                                if s['data']['adapter_type'] != matching['adapter_type'] and matching['remote_lpar_name'] == lparName and int(matching['remote_slot_num']) == s['slotid']:
                                    match = True
                        if not match:
                            worksheet.write(row, 5, 'ERROR', self.bold)
                            worksheet.write_comment(row, 5, 'Client/Server configuration does not match!')                   

                    row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # LPAR name
        worksheet.set_column(3, 3, 5)       # Slot
        worksheet.set_column(4, 4, 7)       # Type
        worksheet.set_column(5, 5, 7)       # ERROR
        
        worksheet.set_column(6, 6, 7)
        worksheet.set_column(7, 7, 50)
        worksheet.set_column(8, 8, 30)
        worksheet.set_column(9, 12, 5)
        worksheet.set_column(13, 13, 15)
        worksheet.set_column(14, 15, 7)
        worksheet.set_column(16, 16, 0)
        worksheet.set_column(17, 17, 35)
        worksheet.set_column(18, 20, 5)
        worksheet.set_column(21, 21, 20)
        worksheet.set_column(22, 22, 40)



    def _LPAR_profile_CPURAM(self):
        worksheet = self.workbook.add_worksheet('LPAR profiles CPU RAM')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value
            
        # Detect variables and LPARs
        varNames = set()
        numProfiles = 0 
        for ms, value in managedSystem.items():
            for lpar in value['_lpar'].values():
                for profile in lpar['profile'].values():
                    varNames = varNames.union( profile.keys() )
                numProfiles += len(lpar['profile'].keys())
        varNames = sorted(varNames)
        for r in ['name', 'lpar_name', 'vscsi', 'vfc', 'veth', 'virt_serial', 'phy_slots']:
            varNames.remove(r)

        # Define columns structure for Table creation setting only column names
        columns = [
            {'header': 'Managed System'}, 
            {'header': 'HMC'}, 
            {'header': 'LPAR Name'},
            {'header': 'Profile Name'}
        ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numProfiles, 3+len(varNames),
                            {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write profile data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for lparName in sorted(managedSystem[ms]['_lpar'].keys()):
                for profileName in sorted(managedSystem[ms]['_lpar'][lparName]['profile'].keys()):
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, lparName, self.normal)
                    worksheet.write(row, 3, profileName, self.normal)
                    for n, v in enumerate(varNames):
                        if v.endswith('mem'):
                            thousand=True
                        else:
                            thousand=False
                        value, format = self._formatValue(managedSystem[ms]['_lpar'][lparName]['profile'][profileName].get(v, ''), thousand=thousand)
                        worksheet.write(row, 4+n, value, format)
                    row += 1 

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # LPAR name
        worksheet.set_column(3, 3, 35)      # profile name
        worksheet.set_column(7, 30, 7)     
      

    def _LPAR_profile_vadapter(self):
        worksheet = self.workbook.add_worksheet('LPAR profiles vadapter')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numVadapters = 0
        for ms, value in managedSystem.items():
            for lpar in value['_lpar'].values():
                for profile in lpar['profile'].values():
                    for item in ['veth', 'vscsi', 'vfc']:
                        varNames = varNames.union(
                            *[set(v.keys()) for v in profile[item]])
                        numVadapters += len(profile[item])
        varNames = sorted(varNames)
        varNames.remove('slot')

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'LPAR Name'},
                   {'header': 'Profile Name'},
                   {'header': 'Slot'},
                   {'header': 'Adapter Type'}
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numVadapters, 5 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for lparName in sorted(managedSystem[ms]['_lpar'].keys()):
                for profileName in sorted(managedSystem[ms]['_lpar'][lparName]['profile'].keys()):
                    slots = [
                        {'slotid': int(s['slot']), 'type': k, 'data': s}
                        for k in ['veth', 'vscsi', 'vfc']
                        for s in managedSystem[ms]['_lpar'][lparName]['profile'][profileName][k]
                    ]
                    slots = sorted(slots, key=itemgetter('slotid'))
                    for s in slots:
                        worksheet.write(row, 0, ms, self.normal)
                        worksheet.write(
                            row, 1, managedSystem[ms]['_HMC'], self.normal)
                        worksheet.write(row, 2, lparName, self.normal)
                        worksheet.write(row, 3, profileName, self.normal)
                        worksheet.write(row, 4, s['slotid'], self.integer)
                        worksheet.write(row, 5, s['type'], self.normal)
                        for n, v in enumerate(varNames):
                            value, format = self._formatValue(s['data'].get(v, ''))
                            worksheet.write(row, 6+n, value, format)

                        row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # LPAR name
        worksheet.set_column(3, 3, 35)      # Profile name
        worksheet.set_column(4, 5, 5)       # Slot id & type
        worksheet.set_column(6, 6, 50)      
        worksheet.set_column(7, 7, 20)       
        worksheet.set_column(8, 8, 5)
        worksheet.set_column(9, 9, 15)
        worksheet.set_column(10, 13, 5)
        worksheet.set_column(14, 14, 35)
        worksheet.set_column(15, 16, 5)
        worksheet.set_column(17, 17, 7)
        worksheet.set_column(18, 18, 22)
        worksheet.set_column(19, 19, 37)
 


    def _LPAR_profile_physadapter(self):
        def search_drc_index(index, ms):
            obj = [ v for v in ms['_sysIO'].values() if v['drc_index']==index ]
            if len(obj) > 1:
                print(f"SEVERE ERROR: drc_index search results in {len(obj)} objects")
                return None
            return obj[0] if len(obj)==1 else None


        worksheet = self.workbook.add_worksheet('LPAR profiles physical adapter')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for lpar in value['_lpar'].values():
                for profile in lpar['profile'].values():
                    varNames = varNames.union(
                        *[set(v.keys()) for v in profile['phy_slots']])
                    numAdapters += len(profile['phy_slots'])
        varNames = sorted(varNames)
        varNames.remove('drc_index')

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'LPAR Name'},
                   {'header': 'Profile Name'},
                   {'header': 'drc_index'},
                ] + [{'header': v} for v in varNames] + [
                   {'header': 'Location'},
                   {'header': 'Description'}
                ]

        # Add table
        worksheet.add_table(0, 0, numAdapters, 6 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for lparName in sorted(managedSystem[ms]['_lpar'].keys()):
                for profileName in sorted(managedSystem[ms]['_lpar'][lparName]['profile'].keys()):
                    slots = [
                        {'slotid': s['drc_index'], 'data': s}
                        for s in managedSystem[ms]['_lpar'][lparName]['profile'][profileName]['phy_slots']
                    ]
                    slots = sorted(slots, key=itemgetter('slotid'))
                    for s in slots:
                        worksheet.write(row, 0, ms, self.normal)
                        worksheet.write(
                            row, 1, managedSystem[ms]['_HMC'], self.normal)
                        worksheet.write(row, 2, lparName, self.normal)
                        worksheet.write(row, 3, profileName, self.normal)
                        worksheet.write(row, 4, s['slotid'], self.integer)
                        for n, v in enumerate(varNames):
                            value, format = self._formatValue(s['data'].get(v, ''))
                            worksheet.write(row, 5+n, value, format)

                        obj = search_drc_index(s['slotid'], managedSystem[ms])
                        if obj is not None:
                            worksheet.write(row, 5+len(varNames), obj['drc_name'], self.normal)
                            worksheet.write(row, 5+len(varNames)+1, obj['description'], self.normal)

                        row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # LPAR name
        worksheet.set_column(3, 3, 35)      # Profile name
        worksheet.set_column(4, 5, 10)
        worksheet.set_column(6, 6, 5)
        worksheet.set_column(7, 7, 30)
        worksheet.set_column(8, 8, 35)
 
 
 
    def _VIOS_npiv(self):
        worksheet = self.workbook.add_worksheet('NPIV')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numVadapters = 0
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for npiv in vios['npiv'].values():
                    varNames = varNames.union(
                        set(npiv.keys()))
                numVadapters += len(vios['npiv'].keys())
        varNames = sorted(varNames)

        if numVadapters == 0:
            worksheet.write(0, 0, 'No NPIV configuration detected')
            return

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'vfchost'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numVadapters, 3 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for vfchost in sorted(managedSystem[ms]['_vios'][viosName]['npiv'].keys()):
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(
                        row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, viosName, self.normal)
                    worksheet.write(row, 3, vfchost, self.normal)
                    for n, v in enumerate(varNames):
                        value, format = self._formatValue(
                            managedSystem[ms]['_vios'][viosName]['npiv'][vfchost].get(v, ''))
                        worksheet.write(row, 4+n, value, format)
                    row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # VIOS name
        worksheet.set_column(3, 3, 10)      # vfchost
        worksheet.set_column(4, 4, 5)       
        worksheet.set_column(5, 5, 35)      
        worksheet.set_column(6, 7, 7)       
        worksheet.set_column(8, 8, 30)
        worksheet.set_column(9, 9, 5)
        worksheet.set_column(10, 10, 30)
        worksheet.set_column(11, 11, 5)
        worksheet.set_column(12, 12, 17)
        worksheet.set_column(13, 13, 8)
        worksheet.set_column(14, 14, 30)
 

 
    def _VIOS_disk(self):
        worksheet = self.workbook.add_worksheet('VIOS Disks')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numVadapters = 0
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for npiv in vios['disk'].values():
                    varNames = varNames.union(
                        set(npiv.keys()))
                numVadapters += len(vios['disk'].keys())
        varNames = sorted(varNames)

        if numVadapters == 0:
            worksheet.write(0, 0, 'No disks detected')
            return

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'VIOS disk'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numVadapters, 3 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for vfchost in sorted(managedSystem[ms]['_vios'][viosName]['disk'].keys()):
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(
                        row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, viosName, self.normal)
                    worksheet.write(row, 3, vfchost, self.normal)
                    for n, v in enumerate(varNames):
                        value, format = self._formatValue(
                            managedSystem[ms]['_vios'][viosName]['disk'][vfchost].get(v, ''), thousand=True)
                        worksheet.write(row, 4+n, value, format)
                    row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # VIOS name
        worksheet.set_column(3, 3, 10)      # disk name
        worksheet.set_column(4, 5, 10)       
        worksheet.set_column(6, 6, 60)      
        worksheet.set_column(7, 7, 10)       
        worksheet.set_column(8, 8, 23)

 
 
    def _SEA(self):
        w_sea = self.workbook.add_worksheet('SEA Config')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        var_sea = set()
        num_sea = 0
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for sea in vios['SEA'].values():
                    var_sea = var_sea.union(
                        set(sea.keys()))
                num_sea += len(vios['SEA'].keys())
        var_sea.discard('stats')
        var_sea = sorted(var_sea)

        if num_sea == 0:
            w_sea.write(0, 0, 'No Shared Ethernet Adapter was detected')
            return

        # Define columns structure for Table creation setting only column names
        columns_sea = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'SEA'},
                ] + [{'header': v} for v in var_sea]

        # Add table
        w_sea.add_table(0, 0, num_sea, 3 +
                            len(var_sea), {'columns': columns_sea})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns_sea):
            w_sea.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row_sea = 1
        for ms in sorted(managedSystem.keys()):
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for seaName in sorted(managedSystem[ms]['_vios'][viosName]['SEA'].keys()):
                    w_sea.write(row_sea, 0, ms, self.normal)
                    w_sea.write(
                        row_sea, 1, managedSystem[ms]['_HMC'], self.normal)
                    w_sea.write(row_sea, 2, viosName, self.normal)
                    w_sea.write(row_sea, 3, seaName, self.normal)
                    for n, v in enumerate(var_sea):
                        value, format = self._formatValue(
                            managedSystem[ms]['_vios'][viosName]['SEA'][seaName].get(v, ''))
                        w_sea.write(row_sea, 4+n, value, format)
                    row_sea += 1
          
        # Static column width
        w_sea.set_column(0, 0, 35)      # Managed System
        w_sea.set_column(1, 1, 15)      # HMC
        w_sea.set_column(2, 2, 35)      # VIOS name
        w_sea.set_column(3, 3, 10)      # SEA
        w_sea.set_column(4, 4, 9)       
        w_sea.set_column(5, 5, 5)      
        w_sea.set_column(6, 6, 9)       
        w_sea.set_column(7, 7, 5)
        w_sea.set_column(8, 9, 10)
        w_sea.set_column(10, 10, 50)
        w_sea.set_column(11, 11, 5)
        w_sea.set_column(12, 12, 9)
        w_sea.set_column(13, 20, 5)
        w_sea.set_column(21, 21, 9)
        w_sea.set_column(22, 23, 5)
        w_sea.set_column(24, 24, 7)
        w_sea.set_column(25, 29, 10)
        w_sea.set_column(30, 31, 5)
        w_sea.set_column(32, 32, 10)




    def _VIOS_eth(self):
        worksheet = self.workbook.add_worksheet('VIOS Eth adapters')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for ent in vios['ent'].values():
                    varNames = varNames.union(
                        set(ent.keys()))
                numAdapters += len(vios['ent'].keys())
        varNames.discard('stats')       
        varNames = sorted(varNames)
        
        if numAdapters == 0:
            worksheet.write(0, 0, 'No Ethernet Adapter was detected')
            return

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'Ethernet Adapter'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numAdapters, 3 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for entID in sorted([ int(vname[3:]) for vname in managedSystem[ms]['_vios'][viosName]['ent'].keys() ]):
                    entName = 'ent' + str(entID)
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(
                        row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, viosName, self.normal)
                    worksheet.write(row, 3, entName, self.normal)
                    for n, v in enumerate(varNames):
                        value, format = self._formatValue(
                            managedSystem[ms]['_vios'][viosName]['ent'][entName].get(v, ''))
                        worksheet.write(row, 4+n, value, format)
                    row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # VIOS name
        worksheet.set_column(3, 3, 10)      # Ethernet adapter
        worksheet.set_column(4, 4, 50)       



    def _VIOS_etherchannel(self):
        worksheet = self.workbook.add_worksheet('VIOS Link Aggregation')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for channel in vios['etherChannel'].values():
                    varNames = varNames.union(
                        set(channel.keys()))
                numAdapters += len(vios['etherChannel'].keys())
        varNames = sorted(varNames)

        # If there are no Etherchannel, return
        if numAdapters == 0:
            worksheet.write(0, 0, 'No link aggregation was detected')
            return

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'EtherChannel Adapter'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numAdapters, 3 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for entID in sorted([ int(vname[3:]) for vname in managedSystem[ms]['_vios'][viosName]['etherChannel'].keys() ]):
                    entName = 'ent' + str(entID)
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(
                        row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, viosName, self.normal)
                    worksheet.write(row, 3, entName, self.normal)
                    for n, v in enumerate(varNames):
                        value, format = self._formatValue(
                            managedSystem[ms]['_vios'][viosName]['etherChannel'][entName].get(v, ''))
                        worksheet.write(row, 4+n, value, format)
                    row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # VIOS name
        worksheet.set_column(3, 3, 10)      # Ethernet adapter
        #worksheet.set_column(4, 4, 50)       



    def _VIOS_eth_stats(self):
        worksheet = self.workbook.add_worksheet('VIOS Eth Statistics')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        seaVars = set()
        aggrVars = set()
        physVars = set()
        virtVars = set()
        numAdapters = 0
        bufVars = set()
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for sea in vios['SEA'].values():
                    seaVars = seaVars.union(set(sea['stats'].keys()))
                    if sea['stats']['real_adapter']['type'] in ['IEEE 802.3ad Link Aggregation', 'EtherChannel']:
                        aggrVars = aggrVars.union(set(sea['stats']['real_adapter'].keys()))
                        numAdapters += 1  # the aggregation
                        numAdapters += len(sea['stats']['real_adapter']['primary_adapters'])
                        numAdapters += len(sea['stats']['real_adapter']['backup_adapters'])
                        for adapter in sea['stats']['real_adapter']['primary_adapters'] + sea['stats']['real_adapter']['backup_adapters']:
                            physVars = physVars.union(adapter.keys())
                    else:
                        physVars = physVars.union(
                            set(sea['stats']['real_adapter'].keys()))
                        numAdapters += 1  # this adapter
                    for virt in sea['stats']['virtual_adapter']:
                        virtVars = virtVars.union(virt.keys())
                        bufVars = bufVars.union(virt['receive_buf'].keys())
                    if 'control_adapter' in  sea['stats']:
                        virtVars = virtVars.union(
                            sea['stats']['control_adapter'].keys())
                        bufVars = bufVars.union(
                            sea['stats']['control_adapter']['receive_buf'].keys())
                    numAdapters += len(sea['stats']['virtual_adapter'])
                    if 'control_adapter' in sea['stats']:
                        numAdapters += 1
                numAdapters += len(vios['SEA'].keys())

                for adapter in vios['ent'].values():
                    if 'stats' in adapter.keys():
                        physVars = physVars.union(adapter['stats'].keys())
                        numAdapters += 1
                
        if numAdapters == 0:
            worksheet.write(0, 0, 'No statistics are available')
            return
        
        seaVars.remove('name')
        seaVars.remove('real_adapter')
        seaVars.remove('virtual_adapter')
        seaVars.remove('control_adapter')
        seaVars.discard('mac')
        seaVars = sorted(seaVars)
        
        aggrVars.discard('type')
        aggrVars.discard('primary_adapters')
        aggrVars.discard('backup_adapters')
        aggrVars.discard('name')
        aggrVars.discard('mac')
        aggrVars = sorted(aggrVars)
        
        physVars.remove('type')
        physVars.remove('name')
        physVars.discard('mac')
        physVars = sorted(physVars)
        
        virtVars.remove('type')
        virtVars.remove('receive_buf')
        virtVars.remove('priority')
        virtVars.discard('mac')
        virtVars.remove('name')
        virtVars = sorted(virtVars)

        myBufOrder = ['Tiny', 'Small', 'Medium', 'Large', 'Huge']
        bufVars = myBufOrder + [ i for i in bufVars if i not in myBufOrder ]

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'Eth Name'},
                   {'header': 'Type'},
                   {'header': 'Owner'},
                   {'header': 'Parent'},
                ] + [
                    {'header': v} for v in seaVars
                ] + [
                    {'header': v} for v in aggrVars
                ] + [
                    {'header': v} for v in physVars
                ] + [
                    {'header': v} for v in virtVars
                ] + [ item for group in
                        [ [ {'header': v+'_min'},
                          {'header': v+'_max'},
                          {'header': v+'_allocated'},
                          {'header': v+'_registered',} ] for v in bufVars ] for item in group
                ]

        # Add table
        worksheet.add_table(0, 0, numAdapters,
                            len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row TODO
        row = 1
        for ms in sorted(managedSystem.keys()):
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for entID in sorted([int(vname[3:]) for vname in managedSystem[ms]['_vios'][viosName]['SEA'].keys()]):
                    entName = 'ent' + str(entID)
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(
                        row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, viosName, self.normal)
                    worksheet.write(row, 3, entName, self.normal)
                    worksheet.write(row, 4, 'SEA', self.normal)
                    worksheet.write(row, 5, 'VIOS', self.normal)
                    worksheet.write(row, 6, 'VIOS', self.normal)
                    for n, v in enumerate(seaVars):
                        value, format = self._formatValue(
                            managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats'].get(v, ''))
                        worksheet.write(row, 7+n, value, format)
                    row += 1

                    if managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']['real_adapter']['type'] in ['IEEE 802.3ad Link Aggregation', 'EtherChannel']:
                        obj = managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']['real_adapter']
                        worksheet.write(row, 0, ms, self.normal)
                        worksheet.write(
                            row, 1, managedSystem[ms]['_HMC'], self.normal)
                        worksheet.write(row, 2, viosName, self.normal)
                        worksheet.write(row, 3, obj['name'], self.normal)
                        worksheet.write(
                            row, 4, managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']['real_adapter']['type'], self.normal)
                        worksheet.write(row, 5, 'SEA '+entName, self.normal)
                        worksheet.write(row, 6, 'SEA '+entName, self.normal)
                        for n, v in enumerate(aggrVars):
                            value, format = self._formatValue(obj.get(v, ''))
                            worksheet.write(row, 7+len(seaVars)+n, value, format)
                        row += 1

                        for adapter in obj['primary_adapters']:
                            worksheet.write(row, 0, ms, self.normal)
                            worksheet.write(
                                row, 1, managedSystem[ms]['_HMC'], self.normal)
                            worksheet.write(row, 2, viosName, self.normal)
                            worksheet.write(row, 3, adapter['name'], self.normal)
                            worksheet.write(row, 4, 'Phys Aggr Primary', self.normal)
                            worksheet.write(row, 5, 'SEA '+entName, self.normal)
                            worksheet.write(row, 6, 'Aggr '+obj['name'], self.normal)
                            for n, v in enumerate(physVars):
                                value, format = self._formatValue(adapter.get(v, ''))
                                worksheet.write(row, 7+len(seaVars)+len(aggrVars)+n, value, format)
                            row += 1

                        for adapter in obj['backup_adapters']:
                            worksheet.write(row, 0, ms, self.normal)
                            worksheet.write(
                                row, 1, managedSystem[ms]['_HMC'], self.normal)
                            worksheet.write(row, 2, viosName, self.normal)
                            worksheet.write(row, 3, adapter['name'], self.normal)
                            worksheet.write(row, 4, 'Phys Aggr Backup', self.normal)
                            worksheet.write(row, 5, 'SEA '+entName, self.normal)
                            worksheet.write(row, 6, 'Aggr '+obj['name'], self.normal)
                            for n, v in enumerate(physVars):
                                value, format = self._formatValue(adapter.get(v, ''))
                                worksheet.write(row, 7+len(seaVars)+len(aggrVars)+n, value, format)
                            row += 1
                    else:
                        # Physical adapter
                        obj = managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']['real_adapter']
                        worksheet.write(row, 0, ms, self.normal)
                        worksheet.write(
                            row, 1, managedSystem[ms]['_HMC'], self.normal)
                        worksheet.write(row, 2, viosName, self.normal)
                        worksheet.write(row, 3, obj['name'], self.normal)
                        worksheet.write(row, 4, 'Physical', self.normal)
                        worksheet.write(row, 5, 'SEA '+entName, self.normal)
                        worksheet.write(row, 6, 'SEA '+entName, self.normal)
                        for n, v in enumerate(physVars):
                            value, format = self._formatValue(obj.get(v, ''))
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+n, value, format)
                        row += 1

                    # Virtual adapters
                    for adapter in managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']['virtual_adapter']:
                        worksheet.write(row, 0, ms, self.normal)
                        worksheet.write(
                            row, 1, managedSystem[ms]['_HMC'], self.normal)
                        worksheet.write(row, 2, viosName, self.normal)
                        worksheet.write(row, 3, adapter['name'], self.normal)
                        worksheet.write(row, 4, 'Virtual Data', self.normal)
                        worksheet.write(row, 5, 'SEA '+entName, self.normal)
                        worksheet.write(row, 6, 'SEA '+entName, self.normal)
                        for n, v in enumerate(virtVars):
                            value, format = self._formatValue(adapter.get(v, ''))
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+n, value, format)
                        for n, bufType in enumerate(bufVars):
                            if not bufType in adapter['receive_buf']:
                                continue
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Min'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4, value, format)
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Max'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4+1, value, format)
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Allocated'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4+2, value, format)
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Registered'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4+3, value, format)
                        row += 1
                    if 'control_adapter' in managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']:
                        adapter = managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']['control_adapter']
                        worksheet.write(row, 0, ms, self.normal)
                        worksheet.write(
                            row, 1, managedSystem[ms]['_HMC'], self.normal)
                        worksheet.write(row, 2, viosName, self.normal)
                        worksheet.write(row, 3, adapter['name'], self.normal)
                        worksheet.write(row, 4, 'Virtual Control', self.normal)
                        worksheet.write(row, 5, 'SEA '+entName, self.normal)
                        worksheet.write(row, 6, 'SEA '+entName, self.normal)
                        for n, v in enumerate(virtVars):
                            value, format = self._formatValue(adapter.get(v, ''))
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+n, value, format)
                        for n, bufType in enumerate(bufVars):
                            if not bufType in adapter['receive_buf']:
                                continue
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Min'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4, value, format)
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Max'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4+1, value, format)
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Allocated'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4+2, value, format)
                            value, format = self._formatValue(adapter['receive_buf'][bufType]['Registered'])
                            worksheet.write(row, 7+len(seaVars)+len(aggrVars)+len(physVars)+len(virtVars)+n*4+3, value, format)
                        row += 1

                for entID in sorted([int(vname[3:]) for vname in managedSystem[ms]['_vios'][viosName]['ent'].keys()]):
                    entName = 'ent' + str(entID)
                    if 'stats' in managedSystem[ms]['_vios'][viosName]['ent'][entName]:
                        if 'Aggregation' in managedSystem[ms]['_vios'][viosName]['ent'][entName]['stats']['type']:
                            obj = managedSystem[ms]['_vios'][viosName]['SEA'][entName]['stats']
                            worksheet.write(row, 0, ms, self.normal)
                            worksheet.write(
                                row, 1, managedSystem[ms]['_HMC'], self.normal)
                            worksheet.write(row, 2, viosName, self.normal)
                            worksheet.write(row, 3, obj['name'], self.normal)
                            worksheet.write(row, 4, 'Aggregation', self.normal)
                            worksheet.write(row, 5, 'VIOS', self.normal)
                            worksheet.write(row, 6, 'VIOS', self.normal)
                            for n, v in enumerate(aggrVars):
                                value, format = self._formatValue(obj.get(v, ''))
                                worksheet.write(row, 7+len(seaVars)+n, value, format)
                            row += 1

                            for adapter in obj['primary_adapters']:
                                worksheet.write(row, 0, ms, self.normal)
                                worksheet.write(
                                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                                worksheet.write(row, 2, viosName, self.normal)
                                worksheet.write(row, 3, obj['name'], self.normal)
                                worksheet.write(row, 4, 'Phys Aggr Primary', self.normal)
                                worksheet.write(row, 5, 'VIOS', self.normal)
                                worksheet.write(row, 6, 'Aggr '+obj['name'], self.normal)
                                for n, v in enumerate(physVars):
                                    value, format = self._formatValue(adapter.get(v, ''))
                                    worksheet.write(row, 7+len(seaVars)+len(aggrVars)+n, value, format)
                                row += 1

                            for adapter in obj['backup_adapters']:
                                worksheet.write(row, 0, ms, self.normal)
                                worksheet.write(
                                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                                worksheet.write(row, 2, viosName, self.normal)
                                worksheet.write(row, 3, obj['name'], self.normal)
                                worksheet.write(row, 4, 'Phys Aggr Backup', self.normal)
                                worksheet.write(row, 5, 'VIOS', self.normal)
                                worksheet.write(row, 6, 'Aggr '+obj['name'], self.normal)
                                for n, v in enumerate(physVars):
                                    value, format = self._formatValue(adapter.get(v, ''))
                                    worksheet.write(row, 7+len(seaVars)+len(aggrVars)+n, value, format)
                                row += 1
                        else:
                            # Physical adapter
                            obj = managedSystem[ms]['_vios'][viosName]['ent'][entName]['stats']
                            worksheet.write(row, 0, ms, self.normal)
                            worksheet.write(
                                row, 1, managedSystem[ms]['_HMC'], self.normal)
                            worksheet.write(row, 2, viosName, self.normal)
                            worksheet.write(row, 3, obj['name'], self.normal)
                            worksheet.write(row, 4, 'Physical', self.normal)
                            worksheet.write(row, 5, 'VIOS', self.normal)
                            worksheet.write(row, 6, 'VIOS', self.normal)
                            for n, v in enumerate(physVars):
                                value, format = self._formatValue(obj.get(v, ''))
                                worksheet.write(row, 7+len(seaVars)+len(aggrVars)+n, value, format)
                            row += 1



        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # VIOS name
        worksheet.set_column(3, 3, 10)      # Ethernet adapter
        worksheet.set_column(4, 4, 50)       




    def _VIOS_fcs(self):
        worksheet = self.workbook.add_worksheet('VIOS Fiber Adapters')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for fcs in vios['fcs'].values():
                    varNames = varNames.union(
                        set(fcs.keys()))
                numAdapters += len(vios['fcs'].keys())
        varNames = sorted(varNames)

        # If there are no fibers, return
        if numAdapters == 0:
            worksheet.write(0, 0, 'No fiber channel adapter was detected')
            return

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'Fibre Channel Adapter'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numAdapters, 3 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for fcsID in sorted([ int(vname[3:]) for vname in managedSystem[ms]['_vios'][viosName]['fcs'].keys() ]):
                    fcsName = 'fcs' + str(fcsID)
                    worksheet.write(row, 0, ms, self.normal)
                    worksheet.write(
                        row, 1, managedSystem[ms]['_HMC'], self.normal)
                    worksheet.write(row, 2, viosName, self.normal)
                    worksheet.write(row, 3, fcsName, self.normal)
                    for n, v in enumerate(varNames):
                        value, format = self._formatValue(
                            managedSystem[ms]['_vios'][viosName]['fcs'][fcsName].get(v, ''))
                        worksheet.write(row, 4+n, value, format)
                    row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # VIOS name
        worksheet.set_column(3, 6, 7)      # fcs adapter
        worksheet.set_column(7, 9, 11) 
        worksheet.set_column(10, 14, 7)
        worksheet.set_column(15, 17, 10)
        worksheet.set_column(18, 20, 7)
        worksheet.set_column(21, 21, 10)
        worksheet.set_column(22, 27, 7)
        worksheet.set_column(28, 29, 22)


 
    def _VIOS_vscsi(self):
        worksheet = self.workbook.add_worksheet('vSCSI MAP')

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numMaps = 0
        for ms, value in managedSystem.items():
            for vios in value['_vios'].values():
                for vscsi in vios['vscsi'].values():
                    #varNames = varNames.union(
                    #    set(vscsi.keys()))
                    for mapping in vscsi['data']:
                        varNames = varNames.union(set(mapping.keys()))
                    numMaps += len(vscsi['data'])
        varNames = sorted(varNames)

        if numMaps == 0:
            worksheet.write(0, 0, 'No vSCSI mapping was detected')
            return

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'VIOS Name'},
                   {'header': 'vSCSI Name'},
                   {'header': 'Virtual adapter'},
                   {'header': 'LPAR id'},
                   {'header': 'LPAR Name'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(0, 0, numMaps, 6 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(0, n, v['header'], self.header45)

        # Write adapter data, by row
        row = 1
        for ms in sorted(managedSystem.keys()):
            id2lpar = { int(v['conf']['lpar_id']): k for k, v in managedSystem[ms]['_lpar'].items() }
            for viosName in sorted(managedSystem[ms]['_vios'].keys()):
                for vscsi in sorted(managedSystem[ms]['_vios'][viosName]['vscsi'].keys()):
                    for mapping in managedSystem[ms]['_vios'][viosName]['vscsi'][vscsi]['data']:
                        worksheet.write(row, 0, ms, self.normal)
                        worksheet.write(
                            row, 1, managedSystem[ms]['_HMC'], self.normal)
                        worksheet.write(row, 2, viosName, self.normal)
                        worksheet.write(row, 3, vscsi, self.normal)
                        worksheet.write(
                            row, 4, managedSystem[ms]['_vios'][viosName]['vscsi'][vscsi]['physloc'], self.normal)
                        worksheet.write(row, 5, managedSystem[ms]['_vios'][viosName]['vscsi'][vscsi]['clntid'], self.normal)
                        worksheet.write(row, 6, id2lpar.get(int(managedSystem[ms]['_vios'][viosName]['vscsi'][vscsi]['clntid'], base=16), 'N/A'), self.normal)
                        for n, v in enumerate(varNames):
                            value, format = self._formatValue(
                                mapping.get(v, ''))
                            worksheet.write(row, 7+n, value, format)
                        row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # VIOS name
        worksheet.set_column(3, 3, 10)      # vSCSI
        worksheet.set_column(4, 4, 27)       
        worksheet.set_column(5, 5, 12)      
        worksheet.set_column(6, 6, 32)       
        worksheet.set_column(7, 8, 65)
        worksheet.set_column(9, 9, 20)
        worksheet.set_column(10, 10, 10)
        worksheet.set_column(11, 11, 11)
        worksheet.set_column(12, 12, 14)

 
 
    def _sriov_adapter(self):
        worksheet = self.workbook.add_worksheet('SR-IOV Adapters')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for adapter in value['_sriov_adapter']:
                varNames = varNames.union(adapter.keys())
            numAdapters += len(value['_sriov_adapter'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV adapter was detected')
            return

        varNames = sorted(varNames)
        varNames.remove('phys_loc') # we use it as a key in display

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'SR-IOV Adapter Location'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 2 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for adapter in sorted(managedSystem[ms]['_sriov_adapter'], key=itemgetter('phys_loc')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, adapter['phys_loc'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(adapter.get(v, ''))
                    worksheet.write(row, 3+n, value, format)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # Adapter location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 

  
    def _sriov_logicalPort(self):
        worksheet = self.workbook.add_worksheet('SR-IOV Logical Port')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for port in value['_sriov_logport']:
                varNames = varNames.union(port.keys())
            numAdapters += len(value['_sriov_logport'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV logical port was detected')
            return

        varNames = sorted(varNames)
        varNames.remove('location_code') # we use it as a key in display

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'SR-IOV Logical Port Location'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 2 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for port in sorted(managedSystem[ms]['_sriov_logport'], key=itemgetter('location_code')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, port['location_code'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(port.get(v, ''))
                    worksheet.write(row, 3+n, value, format)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # Port location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 

  
    def _sriov_logicalPort_eth(self):
        worksheet = self.workbook.add_worksheet('SR-IOV Logical Port ETH')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for port in value['_sriov_logport_eth']:
                varNames = varNames.union(port.keys())
            numAdapters += len(value['_sriov_logport_eth'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV logical port was detected')
            return

        varNames = sorted(varNames)
        varNames.remove('location_code') # we use it as a key in display

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'SR-IOV Logical Port Location'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 2 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for port in sorted(managedSystem[ms]['_sriov_logport_eth'], key=itemgetter('location_code')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, port['location_code'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(port.get(v, ''))
                    worksheet.write(row, 3+n, value, format)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # Port location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 
  
    def _sriov_logicalPort_roce(self):
        worksheet = self.workbook.add_worksheet('SR-IOV Logical Port ROCE')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for port in value['_sriov_logport_roce']:
                varNames = varNames.union(port.keys())
            numAdapters += len(value['_sriov_logport_roce'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV logical port was detected')
            return

        varNames = sorted(varNames)
        varNames.remove('location_code') # we use it as a key in display

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'SR-IOV Logical Port Location'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 2 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for port in sorted(managedSystem[ms]['_sriov_logport_roce'], key=itemgetter('location_code')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, port['location_code'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(port.get(v, ''))
                    worksheet.write(row, 3+n, value, format)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # Port location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 

    def _sriov_physicalPort_eth(self):
        worksheet = self.workbook.add_worksheet('SR-IOV Physical Port ETH')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for port in value['_sriov_physport_eth']:
                varNames = varNames.union(port.keys())
            numAdapters += len(value['_sriov_physport_eth'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV physical port was detected')
            return
            
        varNames = sorted(varNames)
        varNames.remove('phys_port_loc') # we use it as a key in display

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'SR-IOV Physical Port Location'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 2 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for port in sorted(managedSystem[ms]['_sriov_physport_eth'], key=itemgetter('phys_port_loc')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, port['phys_port_loc'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(port.get(v, ''))
                    worksheet.write(row, 3+n, value, format)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # Port location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 

    def _sriov_physicalPort_ethc(self):
        worksheet = self.workbook.add_worksheet('SR-IOV Physical Port ETHC')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for port in value['_sriov_physport_ethc']:
                varNames = varNames.union(port.keys())
            numAdapters += len(value['_sriov_physport_ethc'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV physical port was detected')
            return
            
        varNames = sorted(varNames)
        varNames.remove('phys_port_loc') # we use it as a key in display

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'SR-IOV Physical Port Location'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 2 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for port in sorted(managedSystem[ms]['_sriov_physport_ethc'], key=itemgetter('phys_port_loc')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, port['phys_port_loc'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(port.get(v, ''))
                    worksheet.write(row, 3+n, value, format)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # Port location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 

    def _sriov_physicalPort_roce(self):
        worksheet = self.workbook.add_worksheet('SR-IOV Physical Port ROCE')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        numAdapters = 0
        for ms, value in managedSystem.items():
            for port in value['_sriov_physport_roce']:
                varNames = varNames.union(port.keys())
            numAdapters += len(value['_sriov_physport_roce'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV physical port was detected')
            return
            
        varNames = sorted(varNames)
        varNames.remove('phys_port_loc') # we use it as a key in display

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                   {'header': 'SR-IOV Physical Port Location'},
                ] + [{'header': v} for v in varNames]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 2 +
                            len(varNames), {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for port in sorted(managedSystem[ms]['_sriov_physport_roce'], key=itemgetter('phys_port_loc')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                worksheet.write(row, 2, port['phys_port_loc'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(port.get(v, ''))
                    worksheet.write(row, 3+n, value, format)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        worksheet.set_column(2, 2, 35)      # Port location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 

    def _sriov_vnic(self):
        worksheet = self.workbook.add_worksheet('SR-IOV vNIC')

        worksheet.write(0, 0, 'SR-IOV is under development. Please contact vagnini@it.ibm.com to profide feedback and data sets', self.bold)
        base = 1

        # Extract managed system data
        managedSystem = {}
        for data in self.data:
            for ms, value in data['managed_system'].items():
                managedSystem[ms] = value

        # Detect variables and vadapters
        varNames = set()
        backingVars = set()
        numAdapters = 0
        maxBacking = 0
        for ms, value in managedSystem.items():
            for vnic in value['_sriov_vnic']:
                varNames = varNames.union(vnic.keys())
                backingVars = backingVars.union(*[e.keys() for e in vnic['backing_devices']])
                maxBacking = max([maxBacking, len(vnic['backing_devices'])])
            numAdapters += len(value['_sriov_vnic'])

        if numAdapters == 0:
            worksheet.write(1, 0, 'No SR-IOV vNIC was detected')
            return
            
        varNames = sorted(varNames)
        varNames.remove('backing_devices') # we put them at the end
        varNames.remove('backing_device_states') # I am not sure of its meaning
        backingVars = sorted(backingVars)

        # Define columns structure for Table creation setting only column names
        columns = [{'header': 'Managed System'},
                   {'header': 'HMC'},
                ] + [
                    {'header': v} for v in varNames
                ] + [
                    {'header': '#backing devices'}
                ] 
        for n in range(1, maxBacking+1):
            columns += [{'header': '#'+str(n)+' '+v} for v in backingVars]

        # Add table
        worksheet.add_table(base, 0, base + numAdapters, 
                            len(columns)-1, {'columns': columns})

        # Rewrite headers of the Table to force my settings
        for n, v in enumerate(columns):
            worksheet.write(base, n, v['header'], self.header45)

        # Write adapter data, by row
        row = base + 1
        for ms in sorted(managedSystem.keys()):
            for vnic in sorted(managedSystem[ms]['_sriov_vnic'], key=itemgetter('slot_num')):
                worksheet.write(row, 0, ms, self.normal)
                worksheet.write(
                    row, 1, managedSystem[ms]['_HMC'], self.normal)
                for n, v in enumerate(varNames):
                    value, format = self._formatValue(vnic.get(v, ''))
                    worksheet.write(row, 2+n, value, format)
                backingPos = 2+n+1
                worksheet.write(
                    row, backingPos, len(vnic['backing_devices']), self.integer)
                backingPos += 1
                for device in sorted(vnic['backing_devices'], key=itemgetter('failover-priority')):
                    for n, v in enumerate(backingVars):
                        value, format = self._formatValue(device.get(v, ''))
                        worksheet.write(row, backingPos+n, value, format)
                    backingPos += len(backingVars)
                row += 1

        # Static column width
        worksheet.set_column(0, 0, 35)      # Managed System
        worksheet.set_column(1, 1, 15)      # HMC
        #worksheet.set_column(2, 2, 35)      # Port location
        #worksheet.set_column(3, 3, 35)      
        #worksheet.set_column(4, 5, 10)
        #worksheet.set_column(6, 6, 5)
        #worksheet.set_column(7, 7, 30)
        #worksheet.set_column(8, 8, 35)
 