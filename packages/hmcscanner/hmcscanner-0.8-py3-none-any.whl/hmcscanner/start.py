import argparse
from argparse import RawDescriptionHelpFormatter
import sys
from pathlib import Path
import yaml
import json
import os
import logging
from datetime import datetime
from multiprocessing.pool import ThreadPool
from hmcscanner.dataCollector import DataCollector
from hmcscanner.tqdm_manager import TqdmManager
from hmcscanner.excelWriter import ExcelWriter
import traceback


__version__ = '0.8'             # Used for PyPi versioning


SAMPLE_YAML = 'config.yaml'
DEF_USER = 'hscroot'
DEF_KEY = str(Path.home()/'.ssh'/'id_rsa')
CWD = str(os.getcwd())
DEF_TASKS = 2
EXCEL_FILE = 'hmcScanner_' + datetime.now().strftime("%Y%m%d%H%M%S")+'.xlsx'
LOGFILE = 'hmcScanner.log'



def read_yaml_configuration(file):
    with open(file, "r") as stream:
        try:
            configuration = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f'Error in reading YAML file {SAMPLE_YAML}. Please check following lines:',
                    file=sys.stderr)
            print(exc, file=sys.stderr)
            sys.exit(1)

    # Check that configuration is valid
    error = None
    if not isinstance(configuration, list) or len(configuration) == 0:
        error = 'Configuration should be a list of at least one element'
    else:
        valid_keys = ['ip', 'user', 'password', 'ssh-key', 'jump-host', 'jump-user', 'jump-password', 'jump-ssh-key']
        required_keys = ['ip', 'user']
        minimum_one = ['password', 'ssh-key']
        for n, elem in enumerate(configuration):
            if not isinstance(elem, dict):
                error = f'Element #{n+1} is not correctly parsed'
                break
            invalid_keys = [k for k in elem.keys() if k not in valid_keys]
            missing_keys = [
                k for k in required_keys if k not in elem.keys()]
            minimum_present = [k for k in minimum_one if k in elem.keys()]
            if invalid_keys:
                error = f'Element #{n+1}: the following keys are invalid: {",".join(invalid_keys)}'
                break
            if missing_keys:
                error = f'Element #{n+1}: the following keys are missing: {",".join(missing_keys)}'
                break
            if not minimum_present:
                error = f'Element #{n+1}: one of the following keys must be present: {",".join(minimum_one)}'
    if error:
        print(f'Error in reading YAML file {SAMPLE_YAML}. Please check following lines:',
                file=sys.stderr)
        print(error, file=sys.stderr)
        print('---', file=sys.stderr)
        yaml.dump(elem, sys.stderr, default_flow_style=False)
        sys.exit(1)
    return configuration




def scan(parallel, configuration):
    logger = logging.getLogger("Main")

    # Pool of threads, one for each HMC scan
    pool = ThreadPool(parallel)
    # Scan all HMCs
    logger.debug(f'Starting scanning with {parallel} threads on {len(configuration)} HMCs')
    hmcData = pool.imap(get_data, configuration)
    pool.close()
    pool.join()
    logger.debug(f'Scanning completed')

    # skip empty data
    hmcData = [ d for d in hmcData if d is not None ] 
    return hmcData


def generate(dir, name, hmcData):
    logger = logging.getLogger("Main")

    # Generate Excel data
    logger.debug('Generating single Excel file:')
    excelWriter = ExcelWriter(str(Path(dir) / name))
    excelWriter.version = __version__
    excelWriter.generate(hmcData)
    if excelWriter.forceSingleHMC:
        # A single excel file can not be generated. Produce one file for each HMC
        logger.debug(
            'A single Excel file can not be generated with reliable data.')
        logger.debug('Generating one Excel file for each HMC:')
        for data in hmcData:
            fileName = data['hmc']['scanner_name'] + '_' + name
            excelWriter = ExcelWriter(str(Path(dir) / fileName))
            excelWriter.generate(data)
            logger.debug(f'{str(Path(dir) / fileName)}')
    logger.debug(f'{str(Path(dir) / name)}')


def dump_data(hmcData, dir):
    for data in hmcData:
        with open(str(Path(dir) / f"{data['hmc']['scanner_name']}.txt"), 'w') as outfile:
            outfile.write(json.dumps(data, indent=2))


def main():
    print(f'hmcscanner version {__version__}')

    parser = argparse.ArgumentParser(
        description='Scan one or more HMC and produce a report.',
        epilog='When scanning multiple HMCs avoid selecting two HMCs that manage the same system.\nSend suggestions to vagnini@it.ibm.com',
        formatter_class=RawDescriptionHelpFormatter
    )

    grp0 = parser.add_argument_group("Choose one of these options")
    exgroup1 = grp0.add_mutually_exclusive_group(required=True)
    exgroup1.add_argument('--hmc', action="store", help='Single target HMC')
    exgroup1.add_argument('--file', action="store", help='YAML file with multiple target HMCs')
    exgroup1.add_argument('--generate', action="store_true", help=f'Generate sample YAML file {SAMPLE_YAML} and quit')
    
    grp1 = parser.add_argument_group("Provide the following when pointing to a single HMC from command line")
    grp1.add_argument('--user', action="store", default='hscroot',
                      help=f'Single HMC user. Default is {DEF_USER}')
    exgroup2 = grp1.add_mutually_exclusive_group()
    exgroup2.add_argument('--pwd', action="store", help='Single HMC password')
    exgroup2.add_argument('--ssh-key', default=DEF_KEY, action="store",
                            help = f'Single HMC ssh private key. Default is {DEF_KEY}')

    grp2 = parser.add_argument_group("Customization")
    grp2.add_argument('--dir', action="store", default=CWD,
                      help=f'Base directory containing cache and results. Default current dir: {CWD}')
    grp2.add_argument('--name', action="store", default=EXCEL_FILE,
                      help=f'Name of generated Excel file. Default is hmcScanner_<date>.xlsx. Example: {EXCEL_FILE}')
    grp2.add_argument('--readlocal', action='store_true', help='Do not contact HMC. Parse cached files')
    grp2.add_argument('--parallel', action='store', type=int, default=DEF_TASKS, 
                        help=f'Parallel scans when using YAML on multiple HMCs. Default is {DEF_TASKS}')
    grp2.add_argument('--novios', action='store_true', help=f'Skip VIOS scanning')

    parser.add_argument('--debug', action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # If no param is provided, just show usage
    if not len(sys.argv) > 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.generate:
        with open(SAMPLE_YAML, 'w') as outfile:
            outfile.write('# This is a comment\n')
            outfile.write('# Each HMC is defined by a list of keys, the first starting with a "-"\n')
            outfile.write('# Keep the lines belonging to the same HMC correctly aligned\n')
            outfile.write('# You must provide at least one HMC\n')
            outfile.write('- ip: 10.10.1.1\n')
            outfile.write('  user: hscroot\n')
            outfile.write('  password: abc123\n')
            outfile.write('# The other HMCs should have the same pattern. The order of keys is not relevant\n')
            outfile.write('# You can provide your private key file for authentication\n')
            outfile.write('- ip: 10.20.1.1\n')
            outfile.write('  user: hmcscanner\n')
            outfile.write('  ssh-key: my-secret-key-in-local-disk\n')
            outfile.write('# You can provide both password and secret key. Key will be tried first, then password\n')
            outfile.write('# You can set a JumpServer. Connect to JumpServer in SSH and from there to HMC\n')
            outfile.write('# For JumpServer add jump-host, jump-user, jump-password and/or jump-ssh-key\n')
            outfile.write('# If you provide both password and key for JumpServer, key will be tried first\n')
            outfile.write('# Using keys, both ssh-key and jump-ssh-key must be in local disk\n')
            outfile.write('# You can use any combination of password, ssh-key, jump-password, jump-ssh-key\n')
            outfile.write('- ip: 10.30.1.1\n')
            outfile.write('  user: hscroot\n')
            outfile.write('  password: abc123\n')
            outfile.write('  ssh-key: my-key\n')
            outfile.write('  jump-host: jumphost.mydomain\n')
            outfile.write('  jump-user: federico\n')
            outfile.write('  jump-password: 123abc\n')
            outfile.write('  jump-ssh-key: jump-key\n')
            outfile.write('# This is a valid file that will scan 3 HMC: 10.10.1.1, 10.20.1.1, 10.30.1.1\n')
            outfile.write('# See --parallel flag to define parallel scanning\n')
        sys.exit(0)


    configuration = []

    if args.file is not None:
        configuration = read_yaml_configuration(args.file)
    else:
        hmc = {
            'ip': args.hmc,
            'user': args.user,
            'password': args.pwd,
            'ssh-key': args.ssh_key,
        }
        configuration.append(hmc)

    # Create directory if it does not exists
    try:
        os.mkdir(args.dir)
    except FileExistsError:
        if not os.path.isdir(args.dir):
            print(
                f'File {args.dir} exists and it is not a directory. Aborting.', file=sys.stderr)
            sys.exit(1)
    except OSError:
        print(
            f'Can not create directory {args.dir}. Aborting.', file=sys.stderr)
        return
    with open(os.path.join(args.dir, LOGFILE), 'wt') as file:
        try:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            print(f'Can not write into {args.dir}. Aborting.', file=sys.stderr)
            sys.exit(1)
    
    # Manager of multiple tqdm queues. Skip if readlocal
    if args.readlocal:
        tqdmMrg = None
    else:
        tqdmMrg = TqdmManager()

    # Update configuration data
    for elem in configuration:
        elem['dir'] = args.dir
        elem['connect'] = not args.readlocal
        elem['tqdmMgr'] = tqdmMrg
        elem['novios'] = args.novios
    
    # Setup logging
    logger = logging.getLogger("Main")
    logger.setLevel(logging.DEBUG)

    #formatter_short = logging.Formatter('{asctime} ({levelname:8s}) {message}', style='{')
    formatter_short = logging.Formatter('{message}', style='{')
    formatter_long = logging.Formatter(
        '{asctime} ({levelname:8s}) {filename:15s}:{lineno:5.0f}:{funcName:15s} - {message}', style='{')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter_short)
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(
        os.path.join(args.dir, LOGFILE), mode='w')
    file_handler.setFormatter(formatter_long)
    file_handler.setLevel((logging.DEBUG))

    #logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Log input parameters
    argstring = [str(k)+'='+str(v) if k not in ['pwd']
                 else str(k)+':<HIDDEN>' for k, v in vars(args).items()]
    logger.debug("Args: " +  " ".join(argstring))
    argstring = []
    for elem in configuration:
        s = '{' + ' '.join([str(k)+'='+str(v) if k not in ['password']
                            else str(k)+':<HIDDEN>' for k, v in elem.items()]) + '}'
        argstring.append(s)
    logger.debug("Configuration: " + " ".join(argstring))

    if args.debug:
        hmcData = scan(args.parallel, configuration)
        if tqdmMrg:
            print('\n'*tqdmMrg.freePosition)
        dump_data(hmcData, args.dir)    # Dump data, one file for each HMC
        logger.addHandler(console_handler)  # Enable console logging
        if len(hmcData) == 0:
            logger.warning("No data has been collected.")
            return
        generate(args.dir, args.name, hmcData)
    else:
        try:
            hmcData = scan(args.parallel, configuration)
            if tqdmMrg:
                print('\n'*tqdmMrg.freePosition)
            dump_data(hmcData, args.dir)    # Dump data, one file for each HMC
            logger.addHandler(console_handler)  # Enable console logging
            if len(hmcData) == 0:
                logger.warning("No data has been collected.")
                logger.warning(f"Check log file {os.path.join(args.dir, LOGFILE)}")
                return
            generate(args.dir, args.name, hmcData)
        except Exception as err:
            print()
            logger = logging.getLogger("Main")
            logger.exception(f'Error during execution:')
            print()
            print('Try first to upgrade the code: pip install hmcscanner --upgrade')
            print('Then send a mail to vagnini@it.ibm.com')
            print('Include the log file and the collected data:')
            print(f'- FILE: {os.path.join(args.dir, LOGFILE)}')
            for e in configuration:
                print(f"- DIR : {Path(e['dir']) / e['ip']}")
            sys.exit(1)

    if len(hmcData) != len(configuration):
        logger.warning(
            f'WARNING: only {len(hmcData)} of {len(configuration)} HMCs were scanned.')

    
    






def get_data(config):
    """
    Create DataCollector object that manages data collection (if not disabled) and file parsing. 
    Returns parsed data.
    """
    dc = DataCollector(config['ip'], config['user'], Path(config['dir']) / config['ip'],
                       ssh_key=config.get('ssh-key', None), password=config.get('password', None), connect=config['connect'], 
                       tqdmMgr=config['tqdmMgr'], novios=config['novios'],
                       j_host = config.get('jump-host', None), j_user = config.get('jump-user', None) , 
                       j_password = config.get('jump-password', None), j_ssh_key = config.get('jump-ssh-key', None))
    
    result = dc.data
    if isinstance(result, dict) and len(result.keys())==0:
        result = None

    return result




if __name__ == '__main__':
    main()