import serial
import time
import _thread   # 导入线程包
import time
import matplotlib.pyplot as plt

# goal: 接收串口数据并打印
# feature: 
# 1. 接收串口数据
# 2. 接收到start标志后开始记录串口数据
# 3. 接收到stop标志后结束记录串口数据
# 4. 由于接收到一次信号代表着经过一圈,需要计算总路程&时间&费用
# 5. 按下切换计费模式
# bouns:
# 1. 将路程-时间图在一次结束后打印出来
# 2. 保存每一次的费用时间速度等信息

data_ser = serial.Serial("COM4",9600,timeout = 5)
data_ser.flushInput()

global totalCountNum;
totalCountNum = 0;
# 时间以及路程数组
global timeArray;
global lenArray;
timeArray = [];
lenArray = [];
# count fee
global totalFee
global countMode
#一圈的路程
global lenPerSignal;
lenPerSignal = 1;

def get_data():
    startCountFlag = 0;
    global time_start;
    global time_end;
    global total_time;
    global totalCountNum;
    global totalFee;
    global countMode;

    time_start = 0;
    time_end = 0;
    while True:
        data_count = data_ser.inWaiting()
        if data_count !=0 :
            #recv = data_ser.read(data_ser.in_waiting).decode("gbk")
            recv = data_ser.read(data_ser.in_waiting).decode("gbk")
            print(time.time()," ---  data_recv  --> ", recv)
            if(recv == 'start count'):
                time_start = time.time();
                startCountFlag = 1;
            elif(recv == "403" and startCountFlag == 1):
                print("stop count");
                time_end = time.time();
                total_time = time_end - time_start;
                print("time_start: ", time_start, "time_end: ", time_end, "total_time: ", total_time);
                # 将时间写入日志:
                with open("log.txt", "a") as f:
                    f.write(str(time_start) + "-----" + str(time_end) + "------" + str(total_time) + "\n");
                startCountFlag = 0;
            if(recv == "day"):
                countMode = 0;
            elif(recv == "night"):
                countMode = 1;
            startCountFunc(recv,startCountFlag,countMode);    
        time.sleep(0.1)

def startCountFunc(data,startCountFlag,countMode):
    global timeArray;
    global lenArray;
    # 如果startCountFlag为1,则开始记录接收到的脉冲数
    global totalCountNum;
    if(startCountFlag == 1):
        if(data == '1'):
            totalCountNum = totalCountNum + 1;

        # 将路程-时间图在一次结束后打印出来
        timeArray.append(time.time() - time_start);
        lenArray.append(totalCountNum);

        # 将脉冲数写入日志:
        with open("log.txt", "a") as f:
            f.write("receive " + str(totalCountNum) + " signal | " + "time now: " + str(time.time() - time_start)+ " | total fee now: " + str(totalFee) +"\n");
    elif(startCountFlag == 0):
        print("startCountFlag = 0, totalCountNum: ", str(totalCountNum));
        if(len(timeArray) != 0 and len(lenArray) != 0):        
            print("timeArray: ", timeArray, "lenArray: ", lenArray);
            with open("log.txt", "a") as f:
                f.write("timeArray: " + str(timeArray) + "\n lenArray: " + str(lenArray) + "\n");
            drawTimeAndLen(timeArray,lenArray);
            timeArray = [];
            lenArray = [];
        totalCountNum = 0;

# 等待模式:lenArray连续有三个0的时候开始计时,按间隔时间 * 0.5计费
# 正常模式:按照lenArray中的1的个数 * countModel计费
def countFee(timeArray,lenArray,countModel):
    fee = 0
    global lenPerSignal;
    for i in range(len(timeArray)-2):
        if lenArray[i] == 0:
            if lenArray[i+1] == 0 and lenArray[i+2] == 0:
                fee += ((timeArray[i+2]-timeArray[i]) * 0.5)
                i += 2
        else:
            fee += lenArray[i] * (countModel+1) * lenPerSignal
    print("fee in function: ", fee);
    return int(fee)

# 将收到的数以00开头发送出去,
# 发送的数据为4位数据,不足4位前补0
def pubFee(totalPrice):
    priceStr = str(totalPrice)
    if len(priceStr) < 4:
        priceStr = '0' * (4 - len(priceStr)) + priceStr
    # 发送数据
    for i in range(len(priceStr)):
        time.sleep(1)
        data_ser.write(bytes(priceStr[i], 'utf-8'))
    time.sleep(5);
    data_ser.write(b'0');
    
# 画出速度与时间关系图
def drawTimeAndLen(timeArray,lenArray):
    global lenPerSignal
    vArray = [];
    tArray = [];
    for i in range(len(timeArray)-1): 
        vArray.append((lenArray[i+1]-lenArray[i])*lenPerSignal/(timeArray[i+1]-timeArray[i]));
        tArray.append(timeArray[i]);
    plt.plot(tArray,vArray);
    plt.savefig("timeAndLen.png");
if __name__ == '__main__':
    
    _thread.start_new_thread(get_data,())  # 开启线程，执行get_data方法
    print("start")
    # count fee
    countMode = 0;
    totalFee = 0;
    while 1:
        print("loop | countModel: ", countMode, " | totalFee: ", totalFee);
        time.sleep(1)  
        #print("send 1")
        #data_ser.write(b'2')  # 发送二进制1
        #time.sleep(1)  
        #data_ser.write(b'3') 
        #time.sleep(1)  
        #data_ser.write(b'5') 
        #time.sleep(1)  
        #data_ser.write(b'7') 
        #time.sleep(1)
        #print("send 0")
        #data_ser.write(b'0') # 发送二进制0
        # 计算费用
        totalFee = countFee(timeArray,lenArray,countMode);
        print("totalFee: ", totalFee);
        pubFee(totalFee);

