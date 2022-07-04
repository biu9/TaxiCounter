import serial
import time
import _thread   # 导入线程包
import time

# goal: 接收串口数据并打印
# feature: 
# 1. 接收串口数据
# 2. 接收到start标志后开始记录串口数据
# 3. 接收到stop标志后结束记录串口数据
# 4. 由于接收到一次信号代表着经过一圈,需要计算总路程&时间&费用
# bouns:
# 1. 将路程-时间图在一次结束后打印出来
# 2. 保存每一次的费用时间速度等信息

data_ser = serial.Serial("COM4",9600,timeout = 5)
data_ser.flushInput()

time_start = 0;
time_end = 0;
total_time = 0;
startCountFlag = 0;
totalCountNum = 0;

def get_data():
    while True:
        data_count = data_ser.inWaiting()
        if data_count !=0 :
            #recv = data_ser.read(data_ser.in_waiting).decode("gbk")
            recv = data_ser.read(data_ser.in_waiting).decode("gbk")
            print(time.time()," ---  data_recv  --> ", recv)
            if(recv == 'start'):
                time_start = time.time();
                startCountFlag = 1;
            elif(recv == 'end'):
                time_end = time.time();
                total_time = time_end - time_start;
                print("time_start: ", time_start, "time_end: ", time_end, "total_time: ", total_time);
                # 将时间写入日志:
                with open("log.txt", "a") as f:
                    f.write(str(time_start) + " " + str(time_end) + " " + str(total_time) + "\n");
                startCountFlag = 0;
            startCountFunc(recv);    
        time.sleep(0.1)

def startCountFunc(data):
    # 如果startCountFlag为1,则开始记录接收到的脉冲数
    if(startCountFlag == '1'):
        totalCountNum = totalCountNum + 1;
        # 将脉冲数写入日志:
        with open("log.txt", "a") as f:
            f.write("接收到 " + str(totalCountNum) + " 第个脉冲 | " + "当前经过时间: " + str(time.time() - time_start) + "\n");
    elif(startCountFlag == '0'):
        print("totalCountNum: ", totalCountNum);
        totalCountNum = 0;

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

