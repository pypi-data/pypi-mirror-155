from email.errors import NonPrintableDefect
from paramiko import SSHClient, AutoAddPolicy, ProxyCommand
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException
import logging
import socket
import os
from datetime import datetime
import uuid

logger = logging.getLogger("Main")
BUFSIZE = 10*1024
WRITETEST = str(uuid.uuid4())


class HmcClient:
    """Client to interact with HMC"""

    def __init__(self, host, user, outDir, password=None, ssh_key=None, connect=True,
                    j_host=None, j_user=None, j_password=None, j_ssh_key=None):
        logger.debug(f'HMC: {user}@{host}, outDir: {outDir}, password: {password is not None}, ssh_key: {ssh_key is not None}, connect: {connect}')

        self.host       = host
        self.user       = user
        self.password   = password
        self.ssh_key    = ssh_key
        self.outDir     = outDir
        self.j_host     = j_host
        self.j_user     = j_user
        self.j_password = j_password
        self.j_ssh_key  = j_ssh_key
        self.validDir   = False
        self.client     = None

        if connect:
            self.client     = self._connect()
            try:
                os.mkdir(outDir)
            except FileExistsError:
                if not os.path.isdir(outDir):
                    logger.error(f'File {outDir} exists and it is not a directory')
                    return
            except OSError:
                logger.error(f'Can not create directory {outDir}')
                return
            with open(os.path.join(outDir, WRITETEST), 'wt') as file:
                try:
                    file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    self.validDir = True
                except Exception as e:
                    logger.error(f'Can not write into {outDir}')
                    return
            os.remove(os.path.join(outDir, WRITETEST))
        else:
            # Do nothing!
            pass


    def _connect_old(self):
        if self.ssh_key is not None:
            logger.debug(f'{self.user}@{self.host}: try connection with ssh key only')
            client = self._try_to_connect(None, self.ssh_key)
            if client is not None:
                return client
        logger.debug(f'{self.user}@{self.host}: try connection with password only')
        client = self._try_to_connect(self.password, None)
        if client is None:
            logger.error(f'{self.user}@{self.host}: connection failed')
        return client

    def _connect(self):
        if self.j_host is not None:
            logger.debug(f'Jump host configured: {self.j_host}')
            if self.j_ssh_key is not None:
                logger.debug(f'Try key {self.j_ssh_key} for jump host {self.j_user}@{self.j_host}')
                jumphost = self._try_to_connect(self.j_host, self.j_user, None, self.j_ssh_key)
                if jumphost is None:
                    logger.debug(
                        f'Failed key login on jump host {self.j_user}@{self.j_host}')
                    if self.j_password is not None:
                        logger.debug(f'Try password for jump host {self.j_user}@{self.j_host}')
                        jumphost = self._try_to_connect(self.j_host, self.j_user, self.j_password, None)
                        if jumphost is None:
                            logger.debug(f'Failed password login on jump host {self.j_user}@{self.j_host}. Aborting...')
                            return None
                    else:
                        logger.debug(f'Failed login on jump host {self.j_user}@{self.j_host}. Aborting...')
                        return None
            elif self.j_password is not None:
                logger.debug(
                    f'Try password for jump host {self.j_user}@{self.j_host}')
                jumphost = self._try_to_connect(
                    self.j_host, self.j_user, self.j_password, None)
                if jumphost is None:
                    logger.debug(f'Failed password login on jump host {self.j_user}@{self.j_host}. Aborting...')
                    return None
            else:
                logger.error(f'Jump host defined but no key and no password provided!')
                return None
            transport = jumphost.get_transport()
            destination = (self.host, 22)
            source = ("0.0.0.0", 0)
            try:
                channel = transport.open_channel("direct-tcpip", destination, source)
            except Exception as e:
                logger.error(f'Could not open channel to target. Exception: {e}')
                return None
            logger.debug(f'Starting connection from {self.j_host} to {self.host}')
        else:
            channel = None

        if self.ssh_key is not None:
            logger.debug(
                f'Try key {self.ssh_key} for target host {self.user}@{self.host}, channel={channel}')
            client = self._try_to_connect(self.host, self.user, None, self.ssh_key, sock=channel)
            if client is None:
                logger.debug(f'Failed key login on {self.user}@{self.host} sock={channel}')
                if self.password is not None:
                    logger.debug(f'Try password target host {self.user}@{self.host} sock={channel}')
                    client = self._try_to_connect(self.host, self.user, self.password, None, sock=channel)
                    if client is None:
                        logger.debug(f'Failed password login on {self.user}@{self.host} sock={channel}. Aborting...')
                        return None
                else:
                    logger.debug(f'Failed logging on {self.j_user}@{self.j_host} sock={channel}. Aborting...')
                    return None
        elif self.password is not None:
            logger.debug(
                f'Try password for target host {self.user}@{self.host}, channel={channel}')
            client = self._try_to_connect(self.host, self.user, self.password, None, sock=channel)
            if client is None:
                logger.debug(
                    f'Failed password login on {self.user}@{self.host} sock={channel}. Aborting')
                return None
        else:
            logger.error(f'Target host had no key and no password!')
            return None
        return client


    
    def _try_to_connect(self, host, user, password, ssh_key, sock=None):
        logger.debug(f'Start connection: {user}@{host}, password:{password is not None}, ssh_key: {ssh_key}, sock={sock}')
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                    host,
                    username=user,
                    password=password,
                    key_filename=ssh_key,
                    look_for_keys=True,
                    sock=sock
                )
            logger.debug(f'Connected to {user}@{host}')
        except 	BadHostKeyException as exc:
            logger.error(f"{user}@{host}: server host key could not be verified: {exc}")
            return None
        except AuthenticationException as exc:
            logger.error(f'{user}@{host}: authentication error: {exc}')
            return None
        except SSHException as exc:
            logger.error(f'{user}@{host}: SSH error: {exc}')
            return None
        except socket.error as exc:
            logger.error(f'{user}@{host}: socket error: {exc}')
            return None
        except Exception as exc:
            logger.error(f'{user}@{host}: unexpected error: {exc}')
            return None

        logger.debug(f'{user}@{host}: connection is successful')
        return client


    def isConnected(self):
        return self.client != None


    def close(self):
        if self.client is not None:
            self.client.close()
            logger.debug('Connection closed')
        else:
            logger.debug('Connection was not open')
        self.client = None


    def runCommand(self, command, fileName):
        if self.client is None:
            logger.error('Client was not connected. Command not executed')
            return

        if not self.validDir:
            logger.error('No valid output dir. Command not executed')
            
        try:
            logger.debug(f'{command} -> {fileName}')
            transport = self.client.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            with open(os.path.join(self.outDir, fileName), 'wb') as file:
                session.exec_command('LANG=C ' + command)

                data = session.recv(BUFSIZE)
                while len(data) > 0:
                    file.write(data)
                    data = session.recv(BUFSIZE)
            rc = session.recv_exit_status()
            logger.debug(f'Return code: {rc}')
            #if rc != 0:
            #    logger.warning(f'RC={rc} for {self.user}@{self.host}:{command}')

        except SSHException as exc:
            logger.error(f'SSH error: {exc}')
            return
        except (OSError, IOError) as e:
            logger.error(f'I/O error: {e}')
