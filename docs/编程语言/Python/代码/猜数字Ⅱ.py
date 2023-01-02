import random
num = random.randint(1,10)
while True:
    temp = input("输入所猜数字：")
    guess = int(temp)
    if guess == num:
            print("猜对了")
            break
    else:
            if guess > num:
                    print("猜大了")
            else:
                    print("猜小了")