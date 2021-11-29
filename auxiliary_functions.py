import os



FORMAT = 'utf-8'
HEADER = 64
SEND_FILE_MESSAGE = "!SEND_FILE!"
OVER_MESSAGE = "!OVER!"
BUFFER_SIZE = 512 * 1024

def send_msg(msg, conn, needs_encode = False):
    if(needs_encode):
        msg = msg.encode(FORMAT)
    msg_length = str(len(msg))
    msg_length = msg_length.encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))
    conn.send(msg_length)
    conn.send(msg)

def receive_msg(conn, needs_decode = False):
    msg_length = conn.recv(HEADER)
    if(msg_length):
        msg_length = msg_length.decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length)
        if(needs_decode):
            msg = msg.decode(FORMAT)
        return msg
    return ""

def send_file(filename, conn):
    send_msg(SEND_FILE_MESSAGE, conn, True)
    send_msg(filename, conn, True)
    send_msg(str(os.path.getsize(filename)), conn, True)
    with open(filename, "rb") as file:
        bytes_read = file.read(BUFFER_SIZE)
        while(bytes_read):
            #print(bytes_read)
            send_msg(bytes_read, conn)
            bytes_read = file.read(BUFFER_SIZE)

def receive_file(conn):
    filename = receive_msg(conn, True)
    file_size = int(receive_msg(conn, True)) 
    with open(filename, "wb") as file:
        file_part = receive_msg(conn)
        size = 0
        while size < file_size:
            #print(file_part)
            file.write(file_part)
            size += len(file_part)
            file_part = receive_msg(conn)
        
            