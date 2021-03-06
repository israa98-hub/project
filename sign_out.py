import random

import util


def log_out_server(socket, ident, data, key_iv, log_in_list):
    try:
        print ("%s wants to log out" %(data.Sender_name))
        key = key_iv[ident][0]
        iv = key_iv[ident][1]

        cha1 = data.C1
        logout_user = data.Sender_name
        logout_request = protobuf_pb2.MyProtocol()
        logout_request.TypeNumber = 100
        logout_request.Type = "Log out request from server"
        logout_request.Sender_name = logout_user

        for name1 in log_in_list: # check name in list
            ident1 = log_in_list[name1][0]
            if name1 == logout_user:
                continue
            cha2 = random.randint(1,10001)
            logout_request.C2 = cha2
            flag = 0
            while flag == 0:
                key1 = key_iv[ident1][0]
                iv1 = key_iv[ident1][1]
                send_message = util.aes_en(key1, iv1, logout_request.SerializeToString())
                socket.send_multipart([ident1, send_message])

                logout_res = socket.recv_multipart()
                logout_res_de = util.rsa_de(logout_res[1])
                logout_response = protobuf_pb2.MyProtocol()
                logout_response.ParseFromString(logout_res_de)

                if logout_response.TypeNumber == 101:
                    if logout_response.C2 == cha2 + 1:
                        flag = 1

        msg_logout_rp = protobuf_pb2.MyProtocol()
        msg_logout_rp.TypeNumber = 102
        msg_logout_rp.C1 = cha1 + 1
        cha2 = random.randint(1,10001)
        msg_logout_rp.C2 = cha2
        socket.send_multipart([ident, util.aes_en(key, iv, msg_logout_rp.SerializeToString())])

        msg_logout_con = socket.recv_multipart()
        msg_logout_con_de = util.rsa_de(msg_logout_con[1])
        msg_logout_confirm = protobuf_pb2.MyProtocol()
        msg_logout_confirm.ParseFromString(msg_logout_con_de)

        if msg_logout_confirm.TypeNumber == 103:
            if msg_logout_confirm.C2 == cha2 + 1:
                del log_in_list[data.Sender_name]
                print ("%s have logged off" %(data.Sender_name))

    except: # Error
        key = key_iv[ident][0]
        iv = key_iv[ident][1]
        msg_logout_rp = protobuf_pb2.MyProtocol()
        msg_logout_rp.TypeNumber = 0
        msg_logout_rp.Error = "Log out Error happen"
        s_msg = util.aes_en(key, iv, msg_logout_rp.SerializeToString())
        socket.send_multipart([ident, s_msg])