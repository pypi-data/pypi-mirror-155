import logging
from hmcClient import HmcClient
import csv
from io import StringIO
import os
import json


logger = logging.getLogger("Main")


hmc_commands = {
    'date':         ['date +"%Y-%m-%d %H:%M:%S"',       'date.txt'],
    'version':      ['lshmc -V',                        'lshmc-vv.txt'],
    'vpd':          ['lshmc -v',                        'lshmc-v.txt'],
    'bios':         ['lshmc -b',                        'lshmc-b.txt'],
    'network':      ['lshmc -n',                        'lshmc-n.txt'],
    'lslparutil':   ['lslparutil -r config',            'lslparutil-config.txt'],
    'systems':      ['lssyscfg -r sys',                 'lssyscfg-r.txt']
}

ms_commands = {
    '_sysProc':          ['lshwres -r proc     --level sys                   -m ',     'system_proc.txt'],
    '_sysMem':           ['lshwres -r mem      --level sys                   -m ',     'system_mem.txt'],
    '_sysIO':            ['lshwres -r io       --rsubtype slot               -m ',     'system.slot.txt'],
    '_lparProc':         ['lshwres -r proc     --level lpar                  -m ',     'lpar_proc.txt'],
    '_procPool':         ['lshwres -r procpool                               -m ',     'procpool.txt'],
    '_lparMem':          ['lshwres -r mem      --level lpar                  -m ',     'lpar_mem.txt'],
    '_memPool':          ['lshwres -r mempool                                -m ',     'mempool.txt'],
    '_lparConf':         ['lssyscfg -r lpar                                  -m ',     'lpar_conf.txt'],
    '_lparProf':         ['lssyscfg -r prof                                  -m ',     'profiles.txt'],
    '_lslic':            ['lslic                                             -m ',     'lslic_syspower.txt'],
    '_vswitch':          ['lshwres -r virtualio --rsubtype vswitch           -m ',     'vswitch.txt'],
    '_veth':             ['lshwres -r virtualio --rsubtype eth --level lpar  -m ',     'veth.txt'],
    '_vscsi':            ['lshwres -r virtualio --rsubtype scsi --level lpar -m ',     'vscsi.txt'],
    '_vfc':              ['lshwres -r virtualio --rsubtype fc --level lpar   -m ',     'vfc.txt'],
    '_slotChildren':     ['lshwres -r io --rsubtype slotchildren             -m ',     'lshwres-slotchilden.txt'],
    '_lscodBillProc':    ['lscod -t bill -r proc                             -m ',     'lscod_bill_proc.txt'],
    '_lscodBillMem':     ['lscod -t bill -r mem                              -m ',     'lscod_bill_mem.txt'],
    '_lscodCapProc':     ['lscod -t cap -r proc -c onoff                     -m ',     'lscod_cap_proc_onoff.txt'],
    '_lscodCapMem':      ['lscod -t cap -r mem -c onoff                      -m ',     'lscod_cap_mem_onoff.txt'],
    '_lscodHist':        ['lscod -t hist                                     -m ',     'lscod_hist.txt']
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
    'slots':            ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev -vpd" | grep -E "^ *ent[0-9]+ +"',                                                                                                                      'slots.txt'],
    'fcstat':           ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep -E "^fcs[0-9]+" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "fcstat -e $i" ; done',                                'fcstat.txt'],
    'fcattr':           ['viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev" | grep -E "^fcs[0-9]+" | while read i j ; do echo "#$i"; viosvrcmd -m \'_MS_\' -p \'_VIOS_\' -c "lsdev -attr -dev $i" ; done',                         'fcattr.txt'],
}





# Split a line into CSV elements as array
def splitArray(s):
    if not ',' in s:
        return s

    f = StringIO(s)
    reader = csv.reader(f)
    for row in reader:
        return row


# Read a HMC file and return an array of dictionaries
def loadFile(fileName):
    result = []
    with open(fileName, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].startswith('No results') or row[0].startswith('HSCL'):
                return None
            d = { tuple(elem.split('=', 1)) for elem in row }
            d = { k:splitArray(v) for k, v in d }
            result.append(d)
    return result

    


# Collect data from HMC
def collect_data(host, user, outDir, password=None, ssh_key=None):
    ssh = HmcClient(host, user, outDir, password=password, ssh_key=ssh_key)
    if not ssh.isConnected():
        return False

    logger.info(f'Connected with HMC {host} as user {user}')

    # print('.', end='', flush=True)

    # Run commands related to HMC configuration
    for k, v in hmc_commands.items():
        logger.debug(f'HMC: {host}, CMD: {v[0]}')
        ssh.runCommand(v[0], host+'_'+v[1])

    logger.info(f'... HMC data collected')

    # Detect managed systems
    systems = loadFile(os.path.join(outDir, host+'_'+hmc_commands['systems'][1]))
    systems = [ row['name'] for row in systems ]

    logger.info(f'... Identified {len(systems)} Managed Systems')

    # Run commands related to managed system
    for n, s in enumerate(systems):
        for k, v in ms_commands.items():
            logger.debug(f'MS: {s}, CMD: {v[0]+s}')
            ssh.runCommand(v[0]+s, s+'_'+v[1])
        logger.info(f'...... {n+1:3d}/{len(systems):<3d} finished scanning {s}')

    logger.info('... Scanning VIOS data')

    # Detect VIOS and run commands
    for s in systems:
        vios = loadFile(os.path.join(outDir, s+'_'+ms_commands['_lparConf'][1]))
        vios = [ row['name'] for row in vios if row.get('lpar_env', None)=='vioserver']

        for lpar in vios:
            # Run direct commands
            for k, v in vios_commands.items():
                logger.debug(f'MS: {s}, VIOS: {lpar} CMD: {v[0]}')
                ssh.runCommand('viosvrcmd -m "'+s+'" -p "'+lpar+'" -c "'+v[0]+'"', s+'_'+lpar+'_'+v[1])
            # Run HMC scripts
            for k, v in hmc_vios_scripts.items():
                cmd = v[0].replace('_MS_', s).replace('_VIOS_', lpar)
                logger.debug(f'MS: {s}, VIOS: {lpar} CMD: {cmd}')
                ssh.runCommand(cmd, s+'_'+lpar+'_'+v[1])
            logger.info(f'...... finished scanning {lpar}@{s}')
        
    logger.info('Scanning completed. Closing HMC connection.')

    ssh.close()


# Parse data related to HMC and return dictionary
def _parseHMC(host, outDir):
    hmc = {}

    base = os.path.join(outDir, host+'_')

    with open(base + hmc_commands['date'][1]) as f:
        hmc['date'] = f.readline().rstrip()

    with open(base + hmc_commands['version'][1]) as f:
        for line in f.readlines():
            line = line.strip().split()
            if line[0] == 'Release:':
                hmc['release'] = line[1]
            if line[0] == 'Service Pack:':
                hmc['service_pack'] = line[1]
            if line[0] == 'HMC':
                hmc['buld_level'] = line[-1]

    with open(base + hmc_commands['vpd'][1]) as f:
        for line in f.readlines():
            line = line.strip().split()
            if line[0] == '*TM:':
                hmc['type_model'] = line[1]
            if line[0] == '*SE':
                hmc['serial'] = line[1]

    with open(base + hmc_commands['bios'][1]) as f:
        hmc['bios'] = f.readline().rstrip().split('=')[-1]

    net = loadFile(base+hmc_commands['network'][1])
    hmc.update(net[0])

    logger.info('HMC data parsed')

    return hmc





def _parseManagedSystem(host, outDir):
    logger.info('Parsing Managed System data.')

    base = os.path.join(outDir, host+'_')
    managedSystem = { elem['name']: elem for elem in loadFile(base+hmc_commands['systems'][1]) }

    lslparutil = { elem['name']: elem for elem in loadFile(base+hmc_commands['lslparutil'][1]) }

    for ms in managedSystem:
        managedSystem[ms]['lslparutil'] = lslparutil[ms]

        for key, value in ms_commands.items():
            managedSystem[ms][key] = loadFile(os.path.join(outDir, ms+'_'+value[1]))

        # fixup data layout
        managedSystem[ms]['_sysProc'] = managedSystem[ms]['_sysProc'][0]
        managedSystem[ms]['_sysMem'] = managedSystem[ms]['_sysMem'][0]
        managedSystem[ms]['_procPool'] = { elem['name']:elem for elem in managedSystem[ms]['_procPool'] }
        managedSystem[ms]['_sysIO'] = { elem['drc_name']:elem for elem in managedSystem[ms]['_sysIO'] }
        managedSystem[ms]['_lslic'] = managedSystem[ms]['_lslic'][0]
        managedSystem[ms]['_vswitch'] = { elem['vswitch']:elem for elem in managedSystem[ms]['_vswitch'] }

        managedSystem[ms]['_slot'] = {}
        for elem in managedSystem[ms]['_slotChildren']:
            if not elem['parent'] in managedSystem[ms]['_slot']:
                managedSystem[ms]['_slot'][elem['parent']] = {}
            managedSystem[ms]['_slot'][elem['parent']][elem['phys_loc']] = elem
        del(managedSystem[ms]['_slotChildren'])


        managedSystem[ms]['_lpar'] = { elem['name']:{'conf':elem, 'proc':{}, 'mem':{}, 'profile':{}, 'veth':{} } for elem in managedSystem[ms]['_lparConf'] }
        del(managedSystem[ms]['_lparConf'])
        for elem in managedSystem[ms]['_lparProc']:
            managedSystem[ms]['_lpar'][elem['lpar_name']]['proc'] = elem
        del(managedSystem[ms]['_lparProc'])
        for elem in managedSystem[ms]['_lparMem']:
            managedSystem[ms]['_lpar'][elem['lpar_name']]['mem'] = elem
        del(managedSystem[ms]['_lparMem'])

        for elem in managedSystem[ms]['_lparProf']:
            key = 'virtual_scsi_adapters'
            if key in elem:
                elem['vscsi'] = []
                if elem[key] != 'none':
                    if not isinstance(elem[key], list):
                        elem[key] = [elem[key]]
                    name = ['slot', 'type', 'remote_id', 'remote_name', 'remote_slot', 'required']
                    for e in elem[key]:
                        elem['vscsi'].append( { name[n]:v for n,v in enumerate(e.split('/')) })
                #del(elem[key])
            key = 'virtual_fc_adapters'
            if key in elem:
                elem['vfc'] = []
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
                #del(elem[key])
            key = 'virtual_eth_adapters'
            if key in elem:
                elem['veth'] = []
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
                #del(elem[key])
            key = 'virtual_serial_adapters'
            if key in elem:
                elem['virt_serial'] = []
                if elem[key] != 'none':
                    if not isinstance(elem[key], list):
                        elem[key] = [elem[key]]
                    name = ['slot', 'type', 'supports_hmc', 'remote_id', 'remote_name', 'remote_slot', 'required']  
                    for e in elem[key]:
                        d = { name[n]:v for n,v in enumerate(e.split('/')) }
                        elem['virt_serial'].append(d)
                #del(elem[key])
            key = 'io_slots'
            if key in elem:
                elem['phy_slots'] = []
                if elem[key] != 'none':
                    if not isinstance(elem[key], list):
                        elem[key] = [elem[key]]
                    name = ['drc_index', 'pool_id', 'required']
                    for e in elem[key]:
                        d = { name[n]:v for n,v in enumerate(e.split('/')) }
                        elem['phy_slots'].append(d)
                #del(elem[key])

            managedSystem[ms]['_lpar'][elem['lpar_name']]['profile'][elem['name']] = elem
        del(managedSystem[ms]['_lparProf'])

        for elem in managedSystem[ms]['_veth']:
            managedSystem[ms]['_lpar'][elem['lpar_name']]['veth'][elem['slot_num']] = elem
        del(managedSystem[ms]['_veth'])
        for elem in managedSystem[ms]['_vscsi']:
            managedSystem[ms]['_lpar'][elem['lpar_name']]['veth'][elem['slot_num']] = elem
        del(managedSystem[ms]['_vscsi'])
        for elem in managedSystem[ms]['_vfc']:
            managedSystem[ms]['_lpar'][elem['lpar_name']]['veth'][elem['slot_num']] = elem
        del(managedSystem[ms]['_vfc'])

        logger.info(f'... finished parsing {ms}')

          
    return managedSystem



def _parseFieldData(file, headers, delimiter):
    result = []
    with open(file, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if len(row) != len(headers): 
                logger.debug(f'Skip row: >{row}< in file {file} for headers: {headers}')
                continue
            data = { headers[n]:v for n, v in enumerate(row) }
            result.append(data)
    return result

# Single row has a fixed pat (headers) plus a pattern (pattern) of fields
# h1,h2,h3,p1,p2,p1,p2,p1,p2 where pattern has one or more instances
def _parseFieldDataPattern(file, headers, patterns, delimiter):
    result = []
    with open(file, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if len(row) < len(headers+patterns) or (len(row)-len(headers))%len(patterns) != 0: 
                logger.debug(f'Skip row: >{row}< in file {file} for headers: {headers} and patters: {patterns}')
                continue
            data = { headers[n]:v for n, v in enumerate(row[:len(headers)]) }
            data['data'] = []
            for n in range(len(headers), len(row), len(patterns)):
                data['data'].append( { patterns[n]:v for n, v in enumerate(row[n:n+len(patterns)]) } )
            if len(data['data']) == 1 and data['data'][0]['vtd'] == ' ':
                data['data'] = []   # there is no vtd
            result.append(data)
    return result


def _parseEntatSEA(file):
    result = {}

    with open(file, newline='') as f:
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
                        logger.debug(f'Buffer content unexpected: {line}')
                        continue
                    values = line.strip().split()[-5:]
                    for n, key in enumerate(bufType): 
                        buffers[key][kind] = values[n]
                result[name]['virtual'][adapter]['receive_buf'] = buffers
                line = f.readline()
                continue

            line = f.readline()
    return result

            

def _parseFcstat(file):
    result = {}

    with open(file, newline='') as f:
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






def _parseViosData(host, outDir, data):
    for ms, config in data.items():
        vioslist = [ lpar for lpar, data in config['_lpar'].items() if data['conf']['lpar_env']=='vioserver' ]
        base = os.path.join(outDir, ms)

        if len(vioslist):
            config['_vios'] = {}

        for vios in vioslist:
            viosdata = config['_vios'][vios] = {}

            # NPIV
            keys = ['name', 'physloc', 'clntid', 'clntname', 'clntos', 'status', 'fc', 'fcphysloc', 'ports', 'flags', 'vfcclient', 'vfcclientdrc']
            viosdata['npiv'] = {}
            for item in _parseFieldData(base+'_'+vios+'_'+vios_commands['npiv'][1], keys, ':'):
                viosdata['npiv'][item['name']] = item
                del(item['name'])

            # vSCSI
            #keys = ['svsa', 'physloc', 'clntid', 'vtd', 'lun', 'status', 'backing', 'pdphysloc', 'mirror']
            keys = ['svsa', 'physloc', 'clntid']
            pattern = ['vtd', 'status', 'lun', 'backing', 'bdphysloc', 'mirrored']
            viosdata['vscsi'] = {}
            for item in _parseFieldDataPattern(base+'_'+vios+'_'+vios_commands['vscsi'][1], keys, pattern, ':'):
                viosdata['vscsi'][item['svsa']] = item
                del(item['svsa'])

            # ioslevel
            with open(base+'_'+vios+'_'+vios_commands['ioslevel'][1]) as f:
                viosdata['ioslevel'] = f.readline().strip()

            # disk data: uuid, size, free
            viosdata['disk'] = {}

            keys = ['name', 'id']
            for disk in _parseFieldData(base+'_'+vios+'_'+vios_commands['diskuuid'][1], keys, ':'):
                viosdata['disk'][disk['name']] = disk
                viosdata['disk'][disk['name']]['free'] = 'false'
 
            keys = ['name', 'pvid', 'MB']
            for disk in _parseFieldData(base+'_'+vios+'_'+vios_commands['lspv_size'][1], keys, ':'):
                viosdata['disk'][disk['name']].update(disk)

            keys = ['name', 'pvid', 'MB']
            for disk in _parseFieldData(base+'_'+vios+'_'+vios_commands['lspv_free'][1], keys, ':'):
                viosdata['disk'][disk['name']]['free'] = 'true'
           
            # SEA configuration
            viosdata['SEA'] = {}
            sea = None
            with open(base+'_'+vios+'_'+hmc_vios_scripts['seaCfg'][1]) as f:
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
            with open(base+'_'+vios+'_'+hmc_vios_scripts['slots'][1]) as f:
                for row in f:
                    s = row.split()
                    if not s[0].startswith('ent') or len(s)<2: 
                        logger.debug('Skip slots: {row}')
                        continue
                    viosdata['ent'][s[0]] = { 'pysloc': s[1]}
                    #ent = { 'name': s[0], 'pysloc': s[1]}
                    #viosdata['ent'].append(ent)

            # Etherchannel configuration
            viosdata['etherChannel'] = {}
            channel = None
            with open(base+'_'+vios+'_'+hmc_vios_scripts['ethChannel'][1]) as f:
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
            for sea, value in _parseEntatSEA(base+'_'+vios+'_'+hmc_vios_scripts['entstatSEA'][1]).items():
                viosdata['SEA'][sea].update(value)


            # fcs configuration
            viosdata['fcs'] = {}
            fcs = None
            with open(base+'_'+vios+'_'+hmc_vios_scripts['fcattr'][1]) as f:
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
            for fcs, value in _parseFcstat(base+'_'+vios+'_'+hmc_vios_scripts['fcstat'][1]).items():
                viosdata['fcs'][fcs].update(value)

            # processor typr from VIOS
            with open(base+'_'+vios+'_'+vios_commands['proc0'][1]) as f:
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


    

def parseData(host, outDir):
    hmc = _parseHMC(host, outDir)
    ms = _parseManagedSystem(host, outDir)

    _parseViosData(host, outDir, ms)

    print(json.dumps(ms, indent=2))
            
    





def main(host, user, outDir, password=None, ssh_key=None):
    collect_data(host, user, outDir, password=password, ssh_key=ssh_key)
    parseData(host, outDir)


















if __name__ == "__main__":
    # execute only if run as a script

    logger = logging.getLogger("Main")
    logger.setLevel(logging.DEBUG)

    #formatter_short = logging.Formatter('{asctime} ({levelname:8s}) {message}', style='{')
    formatter_short = logging.Formatter('{message}', style='{')
    formatter_long  = logging.Formatter('{asctime} ({levelname:8s}) {lineno:5.0f}:{funcName:15s} - {message}', style='{')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter_short)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('test.log', mode='w')
    file_handler.setFormatter(formatter_long)
    file_handler.setLevel((logging.DEBUG))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    main('172.17.251.4', 'hscroot', 'data', password='abc1234')
