import time

def pubFee(totalPrice):
    priceStr = str(totalPrice)
    if len(priceStr) < 4:
        priceStr = '0' * (4 - len(priceStr)) + priceStr
    # 发送数据
    for i in range(len(priceStr)):
        time.sleep(1)
        data_ser.write(bytes(priceStr[i], 'utf-8'))

