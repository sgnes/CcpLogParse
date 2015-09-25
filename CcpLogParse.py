__author__ = 'DZMP8F'

Ccp_command_dit = {1: 'CONNECT', 2: 'SET_MTA', 3: 'DNLOAD',
                   4: 'UPLOAD', 5: 'TEST', 6: 'START_STOP',
                   7: 'DISCONNECT', 8: 'START_STOP_ALL',
                   9: 'GET_ACTIVE_CAL_PAGE', 12: 'SET_S_STATUS',
                   13: 'GET_S_STATUS', 14: 'BUILD_CHKSUM',
                   15: 'SHORT_UP', 16: 'CLEAR_MEMORY',
                   17: 'SELECT_CAL_PAGE', 18: 'GET_SEED',
                   19: 'UNLOCK', 20: 'GET_DAQ_SIZE',
                   21: 'SET_DAQ_PTR', 22: 'WRITE_DAQ',
                   23: 'EXCHANGE_ID', 24: 'PROGRAM',
                   25: 'MOVE', 27: 'GET_CCP_VERSION',
                   32: 'DIAG_SERVICE', 33: 'ACTION_SERVICE',
                   34: 'PROGRAM_6', 35: 'DNLOAD_6',
                   254:'Eveent Message', 255:'CRM'}

import os
import sys
import re

if len(sys.argv) == 2:
    log_file = open(sys.argv[1])
    if log_file:
        text = log_file.read()
        log_file.close()
        last_command = 0
        match_re_list = re.findall(r"\d{2,8}\.\d{2,8}\s1\s+([A-Z0-9]{1,3})\s+([A-Z])x\s+d\s8\s([A-Z0-9\s]{23})", text)
        if match_re_list:
            for line in match_re_list:
                msg_id = line[0]
                msg_type = line[1]
                msg_data = line[2]
                msg_data_list = msg_data.split()
                ccp_command = int(msg_data_list[0], 16)
                if ccp_command in Ccp_command_dit:

                    if Ccp_command_dit[ccp_command] == "SET_MTA":
                        ctr = int(msg_data_list[1], 16)
                        mta_num = int(msg_data_list[2], 16)
                        extaddr = int(msg_data_list[3], 16)
                        mtaaddr = int(msg_data_list[4] + msg_data_list[5] + msg_data_list[6] + msg_data_list[7], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}  MtaNO:{} Address extension:{} Address 0X:{:08x}".format(msg_id, "SET_MTA", msg_data, mta_num, extaddr,mtaaddr))
                    elif Ccp_command_dit[ccp_command] == "BUILD_CHKSUM":
                        ctr = int(msg_data_list[1], 16)
                        block_size = int(msg_data_list[2] + msg_data_list[3] + msg_data_list[4] + msg_data_list[5], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}   block size 0X:{:08x}".format(msg_id, "BUILD_CHKSUM",msg_data, block_size))
                    elif Ccp_command_dit[ccp_command] == "SELECT_CAL_PAGE":
                        ctr = int(msg_data_list[1], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}  ".format(msg_id, "SELECT_CAL_PAGE", msg_data))
                    elif Ccp_command_dit[ccp_command] == "GET_S_STATUS":
                        ctr = int(msg_data_list[1], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}  ".format(msg_id, "GET_S_STATUS", msg_data))
                    elif Ccp_command_dit[ccp_command] == "DNLOAD":
                        ctr = int(msg_data_list[1], 16)
                        block_size = int(msg_data_list[2], 16)
                        data_tran = int(msg_data_list[3] + msg_data_list[4] + msg_data_list[5] + msg_data_list[6] + msg_data_list[7], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}   block size 0X:{:08x} dnload data 0X:{:08x}".format(msg_id, "DNLOAD", msg_data, block_size, data_tran))
                    elif Ccp_command_dit[ccp_command] == "CONNECT":
                        ctr = int(msg_data_list[1], 16)
                        station_add = int(msg_data_list[3] + msg_data_list[2], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}   station addres: 0X:{:08x}".format(msg_id, "CONNECT", msg_data, station_add))
                    elif Ccp_command_dit[ccp_command] == "DISCONNECT":
                        ctr = int(msg_data_list[1], 16)
                        action = int(msg_data_list[2], 16)
                        action_dict = {0:"temporary", 1:"end of session"}
                        station_add = int(msg_data_list[5] + msg_data_list[4], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}   station addres: 0X:{:08x} action:{}".format(msg_id, "DISCONNECT", msg_data, station_add, action_dict[action]))
                    elif Ccp_command_dit[ccp_command] == "EXCHANGE_ID":
                        ctr = int(msg_data_list[1], 16)
                        master_id = int(msg_data_list[2] + msg_data_list[3] + msg_data_list[4] + msg_data_list[5] + msg_data_list[6] + msg_data_list[7], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}   master id: 0X:{:010x}".format(msg_id, "EXCHANGE_ID", msg_data, master_id))
                    elif Ccp_command_dit[ccp_command] == "GET_CCP_VERSION":
                        ctr = int(msg_data_list[1], 16)
                        ccp_version = msg_data_list[2] + msg_data_list[3]
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}   station addres: 0X:{}".format(msg_id, "GET_CCP_VERSION", msg_data, ccp_version))
                    elif Ccp_command_dit[ccp_command] == "UPLOAD":
                        ctr = int(msg_data_list[1], 16)
                        block_size = int(msg_data_list[2], 16)
                        print("MsgID:0X:{} CcpCommand:{:20} CAN Data:{}   upload size: 0X:{:02x}".format(msg_id, "UPLOAD", msg_data, block_size))
                    else:
                        print(msg_id, msg_type, Ccp_command_dit[ccp_command], msg_data)
                last_command = ccp_command
