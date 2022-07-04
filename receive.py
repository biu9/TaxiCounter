import serial
import time
import _thread   # 导入线程包

data_ser = serial.Serial("COM4",9600,timeout = 5)
data_ser.flushInput()



def get_data():
    while True:
        data_count = data_ser.inWaiting()
        if data_count !=0 :
            #recv = data_ser.read(data_ser.in_waiting).decode("gbk")
            recv = data_ser.read(data_ser.in_waiting).decode("gbk")
            print(time.time()," ---  data_recv  --> ", recv)
        time.sleep(0.1)



if __name__ == '__main__':
    
    _thread.start_new_thread(get_data,())  # 开启线程，执行get_data方法
    print("start")
    while 1:
        print("loop")
        time.sleep(1)  
        #print("send 1")
        #data_ser.write(b'1')  # 发送二进制1
        time.sleep(1)
        #print("send 0")
        #data_ser.write(b'0') # 发送二进制0

