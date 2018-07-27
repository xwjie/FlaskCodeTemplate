
# 实现方法
def invoke(data):
    print("user invoke, data:" , data)

    if(data['name'] == ""):
        raise Exception("name is null")

    return 12345
