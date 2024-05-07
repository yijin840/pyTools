while(True):
    x,y = map(float, input("请输入 原价 折扣 进行计算：").split())

    print(f"买入： ", x)
    print(f"卖出： ", y)
    print(f"市场税率为：15% ， 到手： ", y * 0.85)
    print(f"折扣： ", (x / y / 0.85))
    print("==================================================")


