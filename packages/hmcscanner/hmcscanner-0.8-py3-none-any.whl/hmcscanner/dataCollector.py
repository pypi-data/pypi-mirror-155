import logging

import csv
from io import StringIO
import os


from hmcscanner.hmcClient import HmcClient
from hmcscanner.tqdm_manager import TqdmManager






class DataCollector:
    """Collects and manages data for a specific HMC"""

    # Commands and files to be used by the data collector

    hmc_commands = {
        'date':             ['date +"%Y-%m-%d %H:%M:%S"',       'date.txt'],
        'version':          ['lshmc -V',                        'lshmc-vv.txt'],
        'vpd':              ['lshmc -v',                        'lshmc-v.txt'],
        'bios':             ['lshmc -b',                        'lshmc-b.txt'],
        'network':          ['lshmc -n',                        'lshmc-n.txt'],
        'lslparutil':       ['lslparutil -r config',            'lslparutil-config.txt'],
        'systems':          ['lssyscfg -r sys',                 'lssyscfg-r.txt']
    }

    ms_commands = {
        '_sysProc':         ['lshwres -r proc     --level sys                   -m ',     'system_proc.txt'],
        '_sysMem':          ['lshwres -r mem      --level sys                   -m ',     'system_mem.txt'],
        '_sysIO':           ['lshwres -r io       --rsubtype slot               -m ',     'system.slot.txt'],
        '_lparProc':        ['lshwres -r proc     --level lpar                  -m ',     'lpar_proc.txt'],
        '_procPool':        ['lshwres -r procpool                               -m ',     'procpool.txt'],
        '_lparMem':         ['lshwres -r mem      --level lpar                  -m ',     'lpar_mem.txt'],
        '_memPool':         ['lshwres -r mempool                                -m ',     'mempool.txt'],
        '_lparConf':        ['lssyscfg -r lpar                                  -m ',     'lpar_conf.txt'],
        '_lparProf':        ['lssyscfg -r prof                                  -m ',     'profiles.txt'],
        '_lslic':           ['lslic                                             -m ',     'lslic_syspower.txt'],
        '_vswitch':         ['lshwres -r virtualio --rsubtype vswitch           -m ',     'vswitch.txt'],
        '_veth':            ['lshwres -r virtualio --rsubtype eth --level lpar  -m ',     'veth.txt'],
        '_vscsi':           ['lshwres -r virtualio --rsubtype scsi --level lpar -m ',     'vscsi.txt'],
        '_vfc':             ['lshwres -r virtualio --rsubtype fc --level lpar   -m ',     'vfc.txt'],
        '_slotChildren':    ['lshwres -r io --rsubtype slotchildren             -m ',     'lshwres-slotchilden.txt'],
        '_lscodBillProc':   ['lscod -t bill -r proc                             -m ',     'lscod_bill_proc.txt'],
        '_lscodBillMem':    ['lscod -t bill -r mem                              -m ',     'lscod_bill_mem.txt'],
        '_lscodCapProc':    ['lscod -t cap -r proc -c onoff                     -m ',     'lscod_cap_proc_onoff.txt'],
        '_lscodCapMem':     ['lscod -t cap -r mem -c onoff                      -m ',     'lscod_cap_mem_onoff.txt'],
        '_lscodHist':       ['lscod -t hist                                     -m ',     'lscod_hist.txt'],
        '_sriov_adapter':         ['lshwres -r sriov --rsubtype adapter                 -m ',     'sriov_adapter.txt'],
        '_sriov_logport':         ['lshwres -r sriov --rsubtype logport                 -m ',     'sriov_logport.txt'],
        '_sriov_logport_eth':     ['lshwres -r sriov --rsubtype logport --level eth     -m ',     'sriov_logport_eth.txt'],
        '_sriov_logport_roce':    ['lshwres -r sriov --rsubtype logport --level roce    -m ',     'sriov_logport_roce.txt'],
        '_sriov_physport_eth':    ['lshwres -r sriov --rsubtype physport --level eth    -m ',     'sriov_physport_eth.txt'],
        '_sriov_physport_ethc':   ['lshwres -r sriov --rsubtype physport --level ethc   -m ',     'sriov_physport_ethc.txt'],
        '_sriov_physport_roce':   ['lshwres -r sriov --rsubtype physport --level roce   -m ',     'sriov_physport_roce.txt'],
        '_sriov_vnic':            ['lshwres -r virtualio --rsubtype vnic                -m ',     'vnic.txt'],
        '_sriov_vnic_lpar':       ['lshwres -r virtualio --rsubtype vnic --level lpar   -m ',     'vnic_lpar.txt'],
    }

    vios_commands = {
        'ioslevel':         ['ioslevel',                                    'ioslevel.txt'],
        'npiv':             ['lsmap -all -npiv -fmt :',                     'npiv_data.txt'],
        'vscsi':            ['lsmap -all -fmt :',                           'vscsi.txt'],
        'diskuuid':         ['chkdev -fmt : -field name identifier',        'disk_uuid.txt'],
        'lspv_size':        ['lspv -size -fmt :',                           'lspv_size.txt'],
        'lspv_free':        ['lspv -free -fmt :',                           'lspv_free.txt'],
        'proc0':            ['lsdev -dev proc0 -attr',                      'proc0.txt']
    }

    hmc_vios_scripts = {
        'seaCfg':           ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep "Shared Ethernet Adapter" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev -dev $i -attr" | grep True ; done',   'seacfg.txt'],
        'ethChannel':       ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep "EtherChannel" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev -dev $i -attr" | grep True ; done',              'etherCHannel.txt'],
        'entstatSEA':       ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep "Shared Ethernet Adapter" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "entstat -all $i" ; done',                   'entstatSEA.txt'],
        'entstatEth':       ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep -E "^ent[0-9]+" | grep -vE "Shared|Virtual|VLAN" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "entstat -all $i" ; done',      'entstatEth.txt'],
        'slots':            ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev -vpd" | grep -E "^ *ent[0-9]+ +" | grep -v Virtual',                                                                                                                      'slots.txt'],
        'fcstat':           ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep -E "^fcs[0-9]+" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "fcstat -e $i" ; done',                                'fcstat.txt'],
        'fcattr':           ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep -E "^fcs[0-9]+" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev -attr -dev $i" ; done',                         'fcattr.txt'],
    }

    HMC_PREFIX = 'HMC_'
    #HMC_PREFIX = ''



    def __init__(self, host, user, outDir, 
                    password=None, ssh_key=None, connect=True, tqdmMgr=None, novios=False,
                    j_host=None, j_user=None, j_password=None, j_ssh_key=None):
        self.hmcClient  = HmcClient(host, user, outDir, 
                                    password=password, ssh_key=ssh_key, connect=connect,
                                    j_host=j_host, j_user=j_user, j_password=j_password, j_ssh_key=j_ssh_key)
        self.host        = host
        self.outDir     = outDir
        self.tqdmMgr    = tqdmMgr
        self.novios     = novios
        self.logger     = logging.getLogger(host)

        self.data       = {}


        if self.tqdmMgr:
            self.tqdmMgr.add(host, 4)
            self.tqdmMgr.reset(host, 0, 6)    # Get HMC data, Detect systems, Scan systems, Scan VIOS, Data Parsing, Complete

        if not self.hmcClient.isConnected():
            if self.tqdmMgr:
                self.tqdmMgr.setDescription(host, 0, 'Skipped from scanning')
                self.tqdmMgr.update(host, 0, 4)
            else:
                self.logger.warning(f'HMC {self.host} skipped from scanning.')
            if connect:
                # Connection error
                if self.tqdmMgr:
                    self.tqdmMgr.setDescription(host, 0, 'Connection error')
                    self.tqdmMgr.update(host, 0, 2)
                    self.tqdmMgr.refresh()
                else:
                    self.logger.warning(f'HMC {self.host}: connection error.')
                self.data = None
                return
        else:
            self.logger.info(f'Start scanning HMC {self.host}')
            if self.tqdmMgr:
                self.tqdmMgr.setDescription(host, 0, 'Get HMC data')

            # Run commands related to HMC configuration
            self._download_HMC_data()

            self.logger.info(f'... HMC data collected')
            if self.tqdmMgr:
                self.tqdmMgr.update(host, 0, 1)
                self.tqdmMgr.setDescription(host, 0, 'Detect systems')

            # Detect managed systems
            systems = self._loadFile(DataCollector.HMC_PREFIX + DataCollector.hmc_commands['systems'][1])
            systems = [ row['name'] for row in systems ]

            self.logger.info(f'... Identified {len(systems)} Managed Systems')
            if self.tqdmMgr:
                self.tqdmMgr.update(host, 0, 1)
                self.tqdmMgr.setDescription(host, 0, 'Scan systems')

            # Run commands related to managed system
            self._download_MS_data(systems)

            self.logger.info('... All Managed Systems scanned')
            if novios:
                self.logger.info('... VIOS scan skipped')
            else:
                self.logger.info('... Scanning VIOS data')
            if self.tqdmMgr:
                self.tqdmMgr.update(host, 0, 1)
                if novios:
                    self.tqdmMgr.setDescription(host, 0, 'Scan VIOS skipped')
                else:
                    self.tqdmMgr.setDescription(host, 0, 'Scan VIOS')
                    self.tqdmMgr.reset(host, 1, len(systems))    

            # Detect VIOS and run commands
            if not novios:
                for s in systems:
                    if self.tqdmMgr:
                        self.tqdmMgr.setDescription(host, 1, s)
                    vios = self._loadFile(s+'_'+DataCollector.ms_commands['_lparConf'][1])
                    vios = [ row['name'] for row in vios if row.get('lpar_env', None)=='vioserver']
                    self._download_VIOS_data(s, vios)
                    if self.tqdmMgr:
                        self.tqdmMgr.update(host, 1, 1)

            self.logger.info('Scanning completed. Closing HMC connection.')
            if self.tqdmMgr:
                self.tqdmMgr.update(host, 0, 1)

            self.hmcClient.close()


        self.logger.info('Parsing data')
        if self.tqdmMgr:
            self.tqdmMgr.setDescription(host, 0, 'Data parsing')

        if not os.path.isdir(self.outDir):
            if self.tqdmMgr:
                self.tqdmMgr.setDescription(host, 0, 'Error reading cache data')
                self.tqdmMgr.update(host, 0, 2)
            else:
                self.logger.error(f'HMC {self.host}: error reading cache data')
            return

        self._parseData()

        self.logger.info('Parsing complete')
        if self.tqdmMgr:
            self.tqdmMgr.update(host, 0, 1)
            self.tqdmMgr.setDescription(host, 0, 'Completed')
            self.tqdmMgr.update(host, 0, 1)
            self.tqdmMgr.refresh()


    def _download_HMC_data(self):
        """Run all HMC related commands"""
        if self.tqdmMgr:
            self.tqdmMgr.reset(self.host, 1, len(
                DataCollector.hmc_commands.keys()))
            
        # key, v[0] is the command, v[1] is the name and DataCollector.HMC_PREFIX prefix is applied
        for k, v in DataCollector.hmc_commands.items():
            self.logger.debug(f'HMC: {self.host}, CMD: {v[0]}')
            if self.tqdmMgr:
                self.tqdmMgr.setDescription(self.host, 1, k)
            self.hmcClient.runCommand(v[0], DataCollector.HMC_PREFIX+v[1])
            if self.tqdmMgr:
                self.tqdmMgr.update(self.host, 1, 1)

    
    def _download_MS_data(self, systems):
        if self.tqdmMgr:
            self.tqdmMgr.reset(self.host, 1, len(systems))

        for n, s in enumerate(systems):
            if self.tqdmMgr:
                self.tqdmMgr.setDescription(self.host, 1, s)
                self.tqdmMgr.reset(self.host, 2, len(DataCollector.ms_commands.keys()))

            # key, v[0] is the command, v[1] is the name and managed system name is applied as prefix
            for k, v in DataCollector.ms_commands.items():
                self.logger.debug(f'MS: {s}, CMD: {v[0]+s}')
                if self.tqdmMgr:
                    self.tqdmMgr.setDescription(self.host, 2, k)
                self.hmcClient.runCommand(v[0]+s, s+'_'+v[1])
                if self.tqdmMgr:
                    self.tqdmMgr.update(self.host, 2, 1)
            self.logger.info(f'...... {n+1:3d}/{len(systems):<3d} finished scanning {s}')
            if self.tqdmMgr:
                self.tqdmMgr.update(self.host, 1, 1)


    def _download_VIOS_data(self, ms, vios):
        if self.tqdmMgr:
            self.tqdmMgr.reset(self.host, 2, len(vios))

        for lpar in vios:
            if self.tqdmMgr:
                self.tqdmMgr.setDescription(self.host, 2, lpar)
                self.tqdmMgr.reset(self.host, 3, len(
                    DataCollector.vios_commands.keys()) + len(DataCollector.hmc_vios_scripts.keys()))

            # Run VIOS commands
            for k, v in DataCollector.vios_commands.items():
                self.logger.debug(f'MS: {ms}, VIOS: {lpar} CMD: {v[0]}')
                if self.tqdmMgr:
                    self.tqdmMgr.setDescription(self.host, 3, k)
                self.hmcClient.runCommand('viosvrcmd -m "' + ms + '" -p "' + lpar + '" -c "' + v[0] + '"', ms + '_' + lpar + '_' + v[1])
                if self.tqdmMgr:
                    self.tqdmMgr.update(self.host, 3, 1)

            # Run HMC scripts
            for k, v in DataCollector.hmc_vios_scripts.items():
                cmd = v[0].replace('_MS_', ms).replace('_VIOS_', lpar)

                self.logger.debug(f'MS: {ms}, VIOS: {lpar} CMD: {cmd}')
                if self.tqdmMgr:
                    self.tqdmMgr.setDescription(self.host, 3, k)
                self.hmcClient.runCommand(cmd, ms+'_'+lpar+'_'+v[1])
                if self.tqdmMgr:
                    self.tqdmMgr.update(self.host, 3, 1)

            self.logger.info(f'...... finished scanning {lpar}@{ms}')
            if self.tqdmMgr:
                self.tqdmMgr.update(self.host, 2, 1)
            

    # Read a HMC file and return an array of dictionaries
    def _loadFile(self, fileName):
        result = []
        try:
            with open(os.path.join(self.outDir, fileName), newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0].startswith('No results') or row[0].startswith('HSCL'):
                        return []
                    d = { tuple(elem.split('=', 1)) for elem in row }
                    d = { k:self._splitArray(v) for k, v in d }
                    result.append(d)
        except FileNotFoundError:
            self.logger.warning(
                f'File not found: {os.path.join(self.outDir, fileName)}')
        return result


    # Split a line into CSV elements as array
    def _splitArray(self, s):
        if not ',' in s:
            return s

        f = StringIO(s)
        reader = csv.reader(f)
        for row in reader:
            return row


    def _parseData(self):
        if self.tqdmMgr:
            self.tqdmMgr.reset(self.host, 1, 3)
            self.tqdmMgr.setDescription(self.host, 1, 'HMC')

        hmc = self._parseHMC()

        if self.tqdmMgr:
            self.tqdmMgr.update(self.host, 1, 1)
            self.tqdmMgr.setDescription(self.host, 1, 'Managed Systems')

        ms  = self._parseManagedSystem()

        if self.tqdmMgr:
            self.tqdmMgr.update(self.host, 1, 1)
            self.tqdmMgr.setDescription(self.host, 1, 'VIOS')

        self._parseViosData()

        if self.tqdmMgr:
            self.tqdmMgr.update(self.host, 1, 1)

        #print(json.dumps(self.data, indent=2))


    # Parse data related to HMC and return dictionary
    def _parseHMC(self):
        hmc = { 'scanner_name': self.host }

        base = os.path.join(self.outDir, DataCollector.HMC_PREFIX)

        with open(base + DataCollector.hmc_commands['date'][1]) as f:
            hmc['date'] = f.readline().rstrip()

        with open(base + DataCollector.hmc_commands['version'][1]) as f:
            hmc['fixes'] = []
            for line in f.readlines():
                line = line.strip()
                if 'Service Pack:' in line:
                    hmc['service_pack'] = line.split()[-1]
                if 'HMC Build level' in line:
                    hmc['build_level'] = line.split()[-1]
                if line.startswith('MH'):
                    hmc['fixes'].append(line)
                if 'base_version' in line:
                    hmc['base_version'] = line.split('=')[-1]

        with open(base + DataCollector.hmc_commands['vpd'][1]) as f:
            for line in f.readlines():
                line = line.strip()
                if '*TM' in line:
                    hmc['type_model'] = line.split()[-1]
                if '*SE' in line:
                    hmc['serial'] = line.split()[-1]

        with open(base + DataCollector.hmc_commands['bios'][1]) as f:
            hmc['bios'] = f.readline().rstrip().split('=')[-1]

        net = self._loadFile(DataCollector.HMC_PREFIX + DataCollector.hmc_commands['network'][1])
        hmc.update(net[0])

        self.logger.info('HMC data parsed')
        self.data['hmc'] = hmc


    def _parseManagedSystem(self):
        self.logger.info('Parsing Managed System data.')

        managedSystem = { elem['name']: elem for elem in self._loadFile(DataCollector.HMC_PREFIX + DataCollector.hmc_commands['systems'][1]) }
        lslparutil    = { elem['name']: elem for elem in self._loadFile(DataCollector.HMC_PREFIX + DataCollector.hmc_commands['lslparutil'][1]) }

        for ms in managedSystem:
            managedSystem[ms]['lslparutil'] = lslparutil.get(ms, None)

            for key, value in DataCollector.ms_commands.items():
                managedSystem[ms][key] = self._loadFile(ms+'_'+value[1])

            # fixup data layout
            if len(managedSystem[ms]['_sysProc']):
                managedSystem[ms]['_sysProc'] = managedSystem[ms]['_sysProc'][0]
            if len(managedSystem[ms]['_sysMem']):
                managedSystem[ms]['_sysMem'] = managedSystem[ms]['_sysMem'][0]
            managedSystem[ms]['_procPool'] = { elem['name']:elem for elem in managedSystem[ms]['_procPool'] }
            managedSystem[ms]['_sysIO'] = { elem['drc_name']:elem for elem in managedSystem[ms]['_sysIO'] }
            if len(managedSystem[ms]['_lslic']):
                managedSystem[ms]['_lslic'] = managedSystem[ms]['_lslic'][0]
            managedSystem[ms]['_vswitch'] = { elem['vswitch']:elem for elem in managedSystem[ms]['_vswitch'] }


            for elem in managedSystem[ms]['_slotChildren']:
                if elem['parent_slot_child_id'] == 'none':
                    parent = managedSystem[ms]['_sysIO'][elem['parent']]
                else:
                    parent = self._getParent(managedSystem[ms]['_sysIO'].values(), elem['parent_slot_child_id'])
                if not 'children' in parent:
                    parent['children'] = []
                parent['children'].append(elem)
            del(managedSystem[ms]['_slotChildren'])

            managedSystem[ms]['_lpar'] = { elem['name']:{'conf':elem, 'proc':{}, 'mem':{}, 'profile':{}, 'veth':{}, 'vscsi':{}, 'vfc':{} } for elem in managedSystem[ms]['_lparConf'] }
            del(managedSystem[ms]['_lparConf'])
            for elem in managedSystem[ms]['_lparProc']:
                managedSystem[ms]['_lpar'][elem['lpar_name']]['proc'] = elem
            del(managedSystem[ms]['_lparProc'])
            for elem in managedSystem[ms]['_lparMem']:
                managedSystem[ms]['_lpar'][elem['lpar_name']]['mem'] = elem
            del(managedSystem[ms]['_lparMem'])

            for elem in managedSystem[ms]['_lparProf']:
                key = 'virtual_scsi_adapters'
                elem['vscsi'] = []
                if key in elem:
                    if elem[key] != 'none':
                        if not isinstance(elem[key], list):
                            elem[key] = [elem[key]]
                        name = ['slot', 'type', 'remote_id', 'remote_name', 'remote_slot', 'required']
                        for e in elem[key]:
                            elem['vscsi'].append( { name[n]:v for n,v in enumerate(e.split('/')) })
                    del(elem[key])
                key = 'virtual_fc_adapters'
                elem['vfc'] = []
                if key in elem:
                    if elem[key] != 'none':
                        if not isinstance(elem[key], list):
                            elem[key] = [elem[key]]
                        name = ['slot', 'type', 'remote_id', 'remote_name', 'remote_slot', 'wwpns', 'required']
                        for e in elem[key]:
                            d = { name[n]:v for n,v in enumerate(e.split('/')) }
                            if d['type'] == 'client':
                                d['wwpns'] = d['wwpns'].split(',')
                            else:
                                d['wwpns'] = []
                            elem['vfc'].append(d)
                    del(elem[key])
                key = 'virtual_eth_adapters'
                elem['veth'] = []
                if key in elem:
                    if elem[key] != 'none':
                        if not isinstance(elem[key], list):
                            elem[key] = [elem[key]]
                        name = ['slot', 'isIEEE', 'port_id', 'add_id', 'priority', 'required', 'vswitch', 'mac', 'allowed', 'qos_priority']
                        for e in elem[key]:
                            d = { name[n]:v for n,v in enumerate(e.split('/')) }
                            if d['add_id'] == '':
                                d['add_id'] = []
                            else:
                                d['add_id'] = d['add_id'].split(',')
                            if d['allowed'] == '':
                                d['allowed'] = []
                            else:
                                d['allowed'] = d['allowed'].split(',')
                            elem['veth'].append(d)
                    del(elem[key])
                key = 'virtual_serial_adapters'
                elem['virt_serial'] = []
                if key in elem:
                    if elem[key] != 'none':
                        if not isinstance(elem[key], list):
                            elem[key] = [elem[key]]
                        name = ['slot', 'type', 'supports_hmc', 'remote_id', 'remote_name', 'remote_slot', 'required']  
                        for e in elem[key]:
                            d = { name[n]:v for n,v in enumerate(e.split('/')) }
                            elem['virt_serial'].append(d)
                    del(elem[key])
                key = 'io_slots'
                elem['phy_slots'] = []
                if key in elem:
                    if elem[key] != 'none':
                        if not isinstance(elem[key], list):
                            elem[key] = [elem[key]]
                        name = ['drc_index', 'pool_id', 'required']
                        for e in elem[key]:
                            d = { name[n]:v for n,v in enumerate(e.split('/')) }
                            elem['phy_slots'].append(d)
                    del(elem[key])

                managedSystem[ms]['_lpar'][elem['lpar_name']]['profile'][elem['name']] = elem
            del(managedSystem[ms]['_lparProf'])

            for elem in managedSystem[ms]['_veth']:
                managedSystem[ms]['_lpar'][elem['lpar_name']]['veth'][elem['slot_num']] = elem
            del(managedSystem[ms]['_veth'])
            for elem in managedSystem[ms]['_vscsi']:
                managedSystem[ms]['_lpar'][elem['lpar_name']]['vscsi'][elem['slot_num']] = elem
            del(managedSystem[ms]['_vscsi'])
            for elem in managedSystem[ms]['_vfc']:
                managedSystem[ms]['_lpar'][elem['lpar_name']]['vfc'][elem['slot_num']] = elem
            del(managedSystem[ms]['_vfc'])

            # sriov/vios-lpar-name/vios-lpar-ID/sriov-adapter-ID/sriov-physical-port-ID/
            # sriov-logical-port-ID/current-capacity/desired-capacity/failover-priority/
            # current-max-capacity/desired-max-capacity
            name = ['sriov', 'vios-lpar-name', 'vios-lpar-ID', 'sriov-adapter-ID', 'sriov-physical-port-ID',
                    'sriov-logical-port-ID', 'current-capacity', 'desired-capacity',
                    'failover-priority', 'current-max-capacity', 'desired-max-capacity']
            for vnic in managedSystem[ms]['_sriov_vnic']:
                vnic['backing_devices'] = [
                    { k[0]:k[1]  for n, k in enumerate(zip(name, e.split('/'))) if n>0 } 
                    for e in vnic['backing_devices']
                ]
            for vnic in managedSystem[ms]['_sriov_vnic_lpar']:
                vnic['backing_devices'] = [
                    { k[0]:k[1]  for n, k in enumerate(zip(name, e.split('/'))) if n>0 } 
                    for e in vnic['backing_devices']
                ]

            self.logger.info(f'... finished parsing {ms}')

        self.data['managed_system'] = managedSystem

    def _parseViosData(self):
        for ms, config in self.data['managed_system'].items():
            vioslist = [lpar for lpar, data in config['_lpar'].items() if data['conf']['lpar_env'] == 'vioserver']
            config['_vios'] = {}

            for vios in vioslist:
                viosdata = config['_vios'][vios] = {}

                # NPIV
                keys = ['name', 'physloc', 'clntid', 'clntname', 'clntos', 'status',
                        'fc', 'fcphysloc', 'ports', 'flags', 'vfcclient', 'vfcclientdrc']
                viosdata['npiv'] = {}
                if not self.novios:
                    for item in self._parseFieldData(ms+'_'+vios+'_'+DataCollector.vios_commands['npiv'][1], keys, ':'):
                        viosdata['npiv'][item['name']] = item
                        del(item['name'])

                # vSCSI
                #keys = ['svsa', 'physloc', 'clntid', 'vtd', 'lun', 'status', 'backing', 'pdphysloc', 'mirror']
                keys = ['svsa', 'physloc', 'clntid']
                pattern = ['vtd', 'status', 'lun',
                        'backing', 'bdphysloc', 'mirrored']
                viosdata['vscsi'] = {}
                if not self.novios:
                    for item in self._parseFieldDataPattern(ms+'_'+vios+'_'+DataCollector.vios_commands['vscsi'][1], keys, pattern, ':'):
                        viosdata['vscsi'][item['svsa']] = item
                        del(item['svsa'])

                # ioslevel
                if not self.novios:
                    with open(os.path.join(self.outDir, ms)+'_'+vios+'_'+DataCollector.vios_commands['ioslevel'][1]) as f:
                        viosdata['ioslevel'] = f.readline().strip()
                else:
                    viosdata['ioslevel'] = 'Not detected'

                # disk data: uuid, size, free
                viosdata['disk'] = {}

                keys = ['name', 'id']
                if not self.novios:
                    for disk in self._parseFieldData(ms+'_'+vios+'_'+DataCollector.vios_commands['diskuuid'][1], keys, ':'):
                        viosdata['disk'][disk['name']] = disk
                        viosdata['disk'][disk['name']]['free'] = 'false'

                keys = ['name', 'pvid', 'MB']
                if not self.novios:
                    for disk in self._parseFieldData(ms+'_'+vios+'_'+DataCollector.vios_commands['lspv_size'][1], keys, ':'):
                        viosdata['disk'][disk['name']].update(disk)

                keys = ['name', 'pvid', 'MB']
                if not self.novios:
                    for disk in self._parseFieldData(ms+'_'+vios+'_'+DataCollector.vios_commands['lspv_free'][1], keys, ':'):
                        viosdata['disk'][disk['name']]['free'] = 'true'

                # SEA configuration
                viosdata['SEA'] = {}
                sea = None
                if not self.novios:
                    with open(os.path.join(self.outDir, ms)+'_'+vios+'_'+DataCollector.hmc_vios_scripts['seaCfg'][1]) as f:
                        for line in f:
                            if line.startswith('#'):
                                # New SEA
                                sea = line[1:].strip()
                                viosdata['SEA'][sea] = {}
                                continue
                            # accounting      enabled  Enable
                            # 0123456789012345678901234567890
                            s = line.split()
                            viosdata['SEA'][sea][s[0]] = s[1]

                # Ethernet slots
                viosdata['ent'] = {}
                if not self.novios:
                    with open(os.path.join(self.outDir, ms)+'_'+vios+'_'+DataCollector.hmc_vios_scripts['slots'][1]) as f:
                        for row in f:
                            s = row.split()
                            if not s[0].startswith('ent') or len(s) < 2:
                                self.logger.debug('Skip slots: {row}')
                                continue
                            viosdata['ent'][s[0]] = {'pysloc': s[1]}
                            #ent = { 'name': s[0], 'pysloc': s[1]}
                            #viosdata['ent'].append(ent)

                # Etherchannel configuration
                viosdata['etherChannel'] = {}
                channel = None
                if not self.novios:
                    with open(os.path.join(self.outDir, ms)+'_'+vios+'_'+DataCollector.hmc_vios_scripts['ethChannel'][1]) as f:
                        for line in f:
                            if line.startswith('#'):
                                # New Etherchannel
                                channel = line[1:].strip()
                                viosdata['etherChannel'][channel] = {}
                                continue
                            # adapter_names   ent0,ent4      EtherChannel Adapte
                            # 0123456789012345678901234567890
                            s = line.split()
                            viosdata['etherChannel'][channel][s[0]] = s[1]

                # entstst SEA
                #for sea, value in self._parseEntatSEA(ms+'_'+vios+'_'+DataCollector.hmc_vios_scripts['entstatSEA'][1]).items():
                #    viosdata['SEA'][sea].update(value)
                if not self.novios:
                    for seastat in self._parseEntsatSeaList(ms+'_'+vios+'_'+DataCollector.hmc_vios_scripts['entstatSEA'][1]):
                        viosdata['SEA'][seastat['name']]['stats'] = seastat

                # entstat Eth
                if not self.novios:
                    for ethstat in self._parseEntstatList(ms+'_'+vios+'_'+DataCollector.hmc_vios_scripts['entstatEth'][1]):
                        viosdata['ent'][ethstat['name']]['stats'] = ethstat

                # fcs configuration
                viosdata['fcs'] = {}
                fcs = None
                if not self.novios:
                    with open(os.path.join(self.outDir, ms)+'_'+vios+'_'+DataCollector.hmc_vios_scripts['fcattr'][1]) as f:
                        for line in f:
                            if line.startswith('#'):
                                # New fcs
                                fcs = line[1:].strip()
                                viosdata['fcs'][fcs] = {}
                                continue
                            s = line.split()
                            if len(s) > 2:
                                if s[0] == 'attribute':
                                    continue
                                viosdata['fcs'][fcs][s[0]] = s[1]

                # fcs stats
                if not self.novios:
                    for fcs, value in self._parseFcstat(ms+'_'+vios+'_'+DataCollector.hmc_vios_scripts['fcstat'][1]).items():
                        viosdata['fcs'][fcs].update(value)

                # processor type from VIOS
                if not self.novios:
                    with open(os.path.join(self.outDir, ms)+'_'+vios+'_'+DataCollector.vios_commands['proc0'][1]) as f:
                        for line in f:
                            s = line.split()
                            if not len(s) > 2:
                                continue
                            if s[0] == 'frequency':
                                try:
                                    config['vios_freq'] = int(s[1]) / 1000000000
                                except ValueError:
                                    pass
                            if s[0] == 'type':
                                config['vios_cputype'] = s[1]
                else:
                    config['vios_freq'] = 'N/A'
                    config['vios_cputype'] = 'N/A'


    def _parseFieldData(self, file, headers, delimiter):
        result = []
        with open(os.path.join(self.outDir, file), newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row in reader:
                if len(row) != len(headers): 
                    if len(row)==2 and row[0]=='' and row[1]=='':
                        pass    # no element is present, it is not an error
                    else:
                        self.logger.debug(f'Skip row: >{row}< in file {file} for headers: {headers}')
                    continue
                data = { headers[n]:v for n, v in enumerate(row) }
                result.append(data)
        return result


    # Single row has a fixed pat (headers) plus a pattern (pattern) of fields
    # h1,h2,h3,p1,p2,p1,p2,p1,p2 where pattern has one or more instances
    def _parseFieldDataPattern(self, file, headers, patterns, delimiter):
        result = []
        with open(os.path.join(self.outDir, file), newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row in reader:
                if len(row) < len(headers+patterns) or (len(row)-len(headers))%len(patterns) != 0: 
                    if len(row)==2 and row[0]=='' and row[1]=='':
                        pass    # no element is present, it is not an error
                    else:
                        self.logger.debug(f'Skip row: >{row}< in file {file} for headers: {headers} and patters: {patterns}')
                    continue
                data = { headers[n]:v for n, v in enumerate(row[:len(headers)]) }
                data['data'] = []
                for n in range(len(headers), len(row), len(patterns)):
                    data['data'].append( { patterns[n]:v for n, v in enumerate(row[n:n+len(patterns)]) } )
                if len(data['data']) == 1 and data['data'][0]['vtd'] == ' ':
                    data['data'] = []   # there is no vtd
                result.append(data)
        return result


    def _parseEntatSEA(self, file):
        result = {}

        with open(os.path.join(self.outDir, file), newline='') as f:
            line = f.readline()
            while line:
                if line.startswith('#'):
                    # New SEA data
                    name = line.strip()[1:]
                    result[name] = {}
                    line = f.readline()
                    continue

                if line.startswith('SEA Flags'):
                    result[name]['flags'] = []
                    line = f.readline()
                    while line and line.strip().startswith('<'):
                        result[name]['flags'].append(line.strip()[1:-1].strip())
                        line = f.readline()
                    continue

                if line.startswith('Real Adapter'):
                    result[name]['real'] = line.strip().split()[2]
                    line = f.readline()
                    continue

                if line.startswith('Virtual Adapter') or line.startswith('Control Adapter'):
                    adapter = line.strip().split()[-1]
                    result[name]['virtual'] = result[name].get('virtual', {})
                    result[name]['virtual'][adapter] = {}
                    line = f.readline()
                    continue

                if line.startswith('Trunk Adapter'):
                    result[name]['virtual'][adapter]['trunk'] = line.strip().split()[-1]
                    if result[name]['virtual'][adapter]['trunk'] == 'True':
                        line = f.readline()
                        if not line:
                            continue
                        s = line.strip().split()
                        result[name]['virtual'][adapter]['priority'] = s[1]
                        result[name]['virtual'][adapter]['active'] = s[3]
                    line = f.readline()
                    continue

                if line.startswith('Hypervisor Send Failures'):
                    result[name]['virtual'][adapter]['hyp_send_failures'] = line.strip().split()[-1]
                    line = f.readline()
                    continue

                if line.startswith('Hypervisor Receive Failures'):
                    result[name]['virtual'][adapter]['hyp_receive_failures'] = line.strip().split()[-1]
                    line = f.readline()
                    continue

                if line.startswith('Port VLAN ID'):
                    result[name]['virtual'][adapter]['port_vlan'] = line.strip().split()[-1]
                    line = f.readline()
                    continue

                if line.startswith('VLAN Tag IDs'):
                    result[name]['virtual'][adapter]['vlan'] = line.strip().split()[3:]
                    line = f.readline()
                    continue

                if line.startswith('Switch ID'):
                    result[name]['virtual'][adapter]['switch'] = " ".join(line.strip().split()[2:])
                    line = f.readline()
                    continue

                if line.startswith('Receive Information'):
                    line = f.readline()
                    if not line or not line.strip().startswith('Receive Buffers'):
                            continue
                    line = f.readline()
                    if not line or not line.strip().startswith('Buffer Type'):
                            continue
                    bufType = ['tiny', 'small', 'medium', 'large', 'huge']
                    bufValue = ['Min', 'Max', 'Allocated', 'Registered']
                    buffers = { v:{} for v in bufType }
                    for kind in bufValue:
                        line = f.readline()
                        if not line or line.strip().split()[0] != kind:
                            self.logger.debug(f'Buffer content unexpected: {line}')
                            continue
                        values = line.strip().split()[-5:]
                        for n, key in enumerate(bufType): 
                            buffers[key][kind] = values[n]
                    result[name]['virtual'][adapter]['receive_buf'] = buffers
                    line = f.readline()
                    continue

                line = f.readline()
        return result


    def _parseEntstatAdapterSection(self, f, line, stop):
        # Parse statistics related to a single Adapter
        # Line must start with 'ETHERNET STATISTICS'
        # When a line starts a with an element is stop, return
        # Return last read line and the constructed object
        result = {}
        if not line.startswith('ETHERNET STATISTICS'):
            # ERROR!!!!
            return line, None
        result['name'] = line.split()[2][1:-1]  # Get adapter name
        line = f.readline()
        result['type'] = ' '.join(line.split()[2:])
        if 'Link Aggregation' in result['type'] or 'EtherChannel' in result['type']:
            line, new_result = self._parseEntstatAggrSection(f, line, stop)
            new_result['name'] = result['name']
            return line, new_result

        line = f.readline()
        while line and not any([ line.strip().startswith(s) for s in stop]):
            if 'Hardware Address' in line:
                result['mac'] = line.split()[-1]
                line = f.readline()
                continue
            if 'Link Status' in line:
                result['link_status'] = line.split()[-1]
                line = f.readline()
                continue
            if line.startswith('Physical Port Speed'):
                result['effective_speed'] = ' '.join(line.split()[3:])
                line = f.readline()
                continue
            if line.startswith('Media Speed Running'):
                result['effective_speed'] = ' '.join(line.split()[3:])
                line = f.readline()
                continue
            if line.startswith('Physical Port MTU:'):
                result['MTU'] = ' '.join(line.split()[3:])
                line = f.readline()
                continue
            if line.startswith('Jumbo Frames'):
                result['jumbo_frames'] = ' '.join(line.split()[2:])
                line = f.readline()
                continue
            if line.startswith('Receive TCP Segment Aggregation'):
                result['recv_tcp_segment_aggregation'] = ' '.join(line.split()[4:])
                line = f.readline()
                continue
            if line.startswith('Transmit TCP Segmentation Offload'):
                result['tx_tcp_segmentation_offload'] = ' '.join(line.split()[4:])
                line = f.readline()
                continue
            if line.startswith('TCP Segmentation Offload'):
                result['tx_tcp_segmentation_offload'] = ' '.join(
                    line.split()[3:])
                line = f.readline()
                continue
            if 'Actor State' in line:
                line = f.readline()
                line = f.readline()
                line = f.readline()
                if 'Aggregation' in line:
                    result['actor_aggregation'] = ' '.join(line.strip().split()[1:])
                    line = f.readline()
                    if 'Synchronization' in line:
                        result['actor_sync'] = ' '.join(line.strip().split()[1:])
                        line = f.readline()
                        continue
                    continue
                continue
            if 'Partner State' in line:
                line = f.readline()
                line = f.readline()
                line = f.readline()
                if 'Aggregation' in line:
                    result['partner_aggregation'] = ' '.join(line.strip().split()[1:])
                    line = f.readline()
                    if 'Synchronization' in line:
                        result['partner_sync'] = ' '.join(line.strip().split()[1:])
                        line = f.readline()
                        continue
                    continue
                continue
            if line.startswith('Trunk Adapter'):
                result['trunk_adapter'] = ' '.join(line.split()[2:])
                line = f.readline()
                continue
            if 'Priority' in line and 'Active' in line:
                obj = line.split()
                result['priority'] = obj[1]
                result['active'] = obj[3]
                line = f.readline()
                continue
            if line.startswith('Receive Information'):
                line = f.readline()
                if not line or not line.strip().startswith('Receive Buffers'):
                        continue
                line = f.readline()
                if not line or not line.strip().startswith('Buffer Type'):
                        continue
                bufType = line.strip().split()[2:]
                bufValue = ['Min', 'Max', 'Allocated', 'Registered']
                buffers = {v: {} for v in bufType }
                for kind in bufValue:
                    line = f.readline()
                    if not line or line.strip().split()[0] != kind:
                        self.logger.debug(
                            f'Buffer content unexpected: {line}')
                        continue
                    values = line.strip().split()[-len(bufType):]
                    for n, key in enumerate(bufType):
                        buffers[key][kind] = values[n]
                result['receive_buf'] = buffers
                line = f.readline()
                continue
            if 'Platform Large Send Offload' in line:
                result['platform_largesend_offload'] = line.strip().split()[-1]
                line = f.readline()
                continue
            line = f.readline()
        return line, result





    def _parseEntstatAggrSection(self, f, line, stop):
        # Parse statistics related to a single Link Aggregation
        # Line must start with 'Device Type' and has 'Link Aggregation' in line (name was detected by caller)
        # When a line starts a with an element is stop, return
        # Return last read line and the constructed object
        result = { 'primary_adapters': [], 'backup_adapters':[]}
        if not line.startswith('Device Type') or (not 'Link Aggregation' in line and not 'EtherChannel' in line):
            # ERROR!!!!
            return line, None
        result['type'] = ' '.join(line.strip().split()[2:])

        line = f.readline()
        while line and not any([ line.strip().startswith(s) for s in stop]): 
            if 'Hardware Address' in line:
                result['mac'] = line.split()[-1]
                line = f.readline()
                continue
            if line.startswith('Number of adapters'):
                result['#adapters'] = line.split()[-1]
                line = f.readline()
                continue
            if line.startswith('Number of backup adapters'):
                result['#backup'] = line.split()[-1]
                line = f.readline()
                continue
            if line.startswith('Active channel'):
                result['active_channel'] = ' '.join(line.split()[2:])
                line = f.readline()
                continue
            if line.startswith('Operating mode:'):
                result['mode'] = ' '.join(line.split()[2:])
                line = f.readline()
                continue
            if line.strip().startswith('Primary Aggregation status'):
                result['primary_aggregation_status'] = ' '.join(line.strip().split()[3:])
                line = f.readline()
                continue
            if line.strip().startswith('LACPDU Interval'):
                result['lacpdu_interval'] = ' '.join(line.strip().split()[2:])
                line = f.readline()
                continue
            if line.startswith('Hash mode'):
                result['hash_mode'] = ' '.join(line.split()[2:])
                line = f.readline()
                continue
            if line.startswith('MAC swap'):
                result['mac_swap'] = ' '.join(line.split()[2:])
                line = f.readline()
                continue
            if 'PRIMARY ADAPTERS' in line:
                # skip up to 'ETHERNET STATISTICS'
                while line and not line.startswith('ETHERNET STATISTICS'):
                    line = f.readline()
                if not line:
                    return line, None   # ERROR
                new_stop = stop.copy()
                new_stop.append('ETHERNET STATISTICS')
                new_stop.append('BACKUP ADAPTERS')
                while line.startswith('ETHERNET STATISTICS'):
                    line, obj = self._parseEntstatAdapterSection(f, line, new_stop)
                    result['primary_adapters'].append(obj)
                continue
            if 'BACKUP ADAPTERS' in line:
                # skip up to 'ETHERNET STATISTICS'
                while line and not line.startswith('ETHERNET STATISTICS'):
                    line = f.readline()
                if not line:
                    return line, None   # ERROR
                new_stop = stop.copy()
                new_stop.append('ETHERNET STATISTICS')
                while line.startswith('ETHERNET STATISTICS'):
                    line, obj = self._parseEntstatAdapterSection(f, line, new_stop)
                    result['backup_adapters'].append(obj)
                continue
            line = f.readline()
        return line, result

            

    # DO NOT USE
    def _parseEntstatSection(self, f, line, stop):
        # Parse data of single adapter
        # Detect adapter type and call corresponding function
        # Line must start with 'ETHERNET STATISTICS'
        # When a line starts a with an element is stop, return
        # Return last read line and the constructed object
        result = {}
        if not line.startswith('ETHERNET STATISTICS'):
            # ERROR!!!!
            return line, None
        result['name'] = line.split()[2][1:-1]  # Get adapter name

        device_type = f.readline()     # device type line
        if 'Link Aggregation' in device_type:
            return self._parseEntstatAggrSection(f, line, stop, ' '.join(device_type.split()[2:]))
        return line, self._parseEntstatAdapterSection(f, line, stop)
            

    def _parseEntstatSeaSection(self, f, line, stop):
        # Parse statistics related to a single SEA 
        # Line must start with 'ETHERNET STATISTICS'
        # When a line starts a with an element is stop, return
        # Return last read line and the constructed object
        result = {}
        if not line.startswith('ETHERNET STATISTICS'):
            # ERROR!!!!
            return line, None
        result['name'] = line.split()[2][1:-1]  # Get adapter name

        line = f.readline()
        if not 'Shared Ethernet Adapter' in line:
            # ERROR!!!!
            return line, None
        
        line = f.readline()
        while line and not any([ line.strip().startswith(s) for s in stop]):         
            if line.startswith('SEA Flags'):
                result['flags'] = []
                line = f.readline()
                while line and line.strip().startswith('<'):
                    result['flags'].append(line.strip()[1:-1].strip())
                    line = f.readline()
                continue
            if line.strip().startswith('State:'):
                result['state'] = line.strip().split()[1]
                line = f.readline()
                continue
            if line.strip().startswith('Bridge Mode:'):
                result['bridge_mode'] = line.strip().split()[-1]
                line = f.readline()
                continue
            if line.strip().startswith('High Availability Mode:'):
                result['ha_mode'] = line.strip().split()[-1]
                line = f.readline()
                continue
            if line.strip().startswith('Priority:'):
                result['priority'] = line.strip().split()[-1]
                line = f.readline()
                continue
            if line.startswith('Real Adapter'):
                # skip up to 'ETHERNET STATISTICS'
                while line and not line.startswith('ETHERNET STATISTICS'):
                    line = f.readline()
                if not line:
                    return line, None   # ERROR
                new_stop = stop.copy()
                new_stop.append('Virtual Adapter')
                line, result['real_adapter'] = self._parseEntstatAdapterSection(f, line, new_stop)
                continue
            if line.startswith('Virtual Adapter'):
                # skip up to 'ETHERNET STATISTICS'
                while line and not line.startswith('ETHERNET STATISTICS'):
                    line = f.readline()
                if not line:
                    return line, None   # ERROR
                new_stop = stop.copy()
                new_stop.append('Virtual Adapter')
                new_stop.append('Control Adapter')
                result['virtual_adapter'] = result.get('virtual adapter', [])
                line, obj = self._parseEntstatAdapterSection(f, line, new_stop)
                result['virtual_adapter'].append(obj)
                continue
            if line.startswith('Control Adapter'):
                # skip up to 'ETHERNET STATISTICS'
                while line and not line.startswith('ETHERNET STATISTICS'):
                    line = f.readline()
                if not line:
                    return line, None   # ERROR
                line, result['control_adapter'] = self._parseEntstatAdapterSection(f, line, stop)
                continue
            line = f.readline()
        return line, result  





    def _parseEntsatSeaList(self, file):
        # Parse a list of SEA statistics
        # Open file and read one line at a time
        # When a line starts with '#' the data is related to a new adapter
        # Call specific functions for sections
        result = []
        with open(os.path.join(self.outDir, file), newline='') as f:
            line = f.readline()
            while line:
                if line.startswith('#'):
                    # New SEA data: get to 'ETHERNET STATISTICS' line
                    line = f.readline()
                    while line and not line.startswith('ETHERNET STATISTICS'):
                        line = f.readline()
                    if not line:
                        return result  # end of file
                    stop = ['#']    # Stop reading SEA data when hash is found
                    line, seaData = self._parseEntstatSeaSection(f, line, stop)
                    result.append(seaData)
                    continue
                else:
                    line = f.readline()     # this should never happen....
        return result

    
    def _parseEntstatList(self, file):
        # Parse a list of adapter statistics (NOT FOR SEA!!!)
        # Open file and read one line at a time
        # When a line starts with '#' the data is related to a new adapter
        # Call specific functions for sections
        result = []
        with open(os.path.join(self.outDir, file), newline='') as f:
            line = f.readline()
            while line:
                if line.startswith('#'):
                    # New adapter data: get to 'ETHERNET STATISTICS' line or skip the adapter
                    # Adapters in network aggregation or SEA provide only error messages
                    line = f.readline()
                    while line and not (line.startswith('ETHERNET STATISTICS') or line.startswith('#')):
                        line = f.readline()
                    if not line:
                        return result  # end of file
                    if line.startswith('#'):
                        continue
                    stop = ['#']    # Stop reading adapter data when hash is found
                    line, adapterData = self._parseEntstatAdapterSection(
                        f, line, stop)
                    result.append(adapterData)
                    continue
                else:
                    line = f.readline()     # this should never happen....
        return result





            
    def _parseFcstat(self, file):
        result = {}

        with open(os.path.join(self.outDir, file), newline='') as f:
            line = f.readline()
            while line:
                if line.startswith('#'):
                    # New fcs data
                    name = line.strip()[1:]
                    result[name] = {}
                    line = f.readline()
                    continue

                if line.startswith('ZA:'):
                    result[name]['firmware'] = line.strip().split()[1]
                    line = f.readline()
                    continue

                if line.startswith('World Wide Node Name'):
                    result[name]['wwn'] = line.strip().split()[4]
                    line = f.readline()
                    continue

                if line.startswith('World Wide Port Name'):
                    result[name]['wwpn'] = line.strip().split()[4]
                    line = f.readline()
                    continue

                if line.startswith('Port Speed (supported):'):
                    result[name]['speed_supported'] = line.strip().split()[3]
                    line = f.readline()
                    continue

                if line.startswith('Port Speed (running):'):
                    result[name]['speed_running'] = line.strip().split()[3]
                    line = f.readline()
                    continue
                
                if line.startswith('Port FC ID:'):
                    result[name]['port_fc_id'] = line.strip().split()[3]
                    line = f.readline()
                    continue

                if line.startswith('Port Type:'):
                    result[name]['port_type'] = line.strip().split()[2]
                    line = f.readline()
                    continue

                if line.startswith('Attention Type:'):
                    result[name]['attention'] = ' '.join(line.strip().split()[2:])
                    line = f.readline()
                    continue

                if line.startswith('Adapter Effective max transfer value:'):
                    result[name]['max_transfer_effective'] = line.strip().split()[5]
                    line = f.readline()
                    continue


                line = f.readline()
        return result


    def _getParent(self, group, parent_slot_child_id):
        for g in group:
            if 'slot_child_id' in g and g['slot_child_id'] == parent_slot_child_id:
                return g
            if 'children' in g:
                r = self._getParent(g['children'], parent_slot_child_id)
                if r is not None:
                    return r
        return None

        
