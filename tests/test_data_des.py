class StringOnly:
    """一个描述器，强制属性值必须是字符串。"""

    def __init__(self):
        self.value = "None"

    def __get__(self, instance, owner):
        if self.value is None:
            return instance.__dict__[self.name]
        return self.value

    # def __set__(self, instance, value):
    #     print(f"__set__ called with value: {value}")
    #     if not isinstance(value, str):
    #         raise TypeError(f"'{self.name}' 必须是字符串")
    #     self.value = value
    #     # instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        """在描述器被绑定到类时自动调用，设置属性名。"""
        self.name = name


class Name:
    first_name = StringOnly()
    last_name = StringOnly()

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


# 测试我们的 Name 类
person = Name("Alice", "Smith")
print(person.first_name)  # 输出：Alice
print(person.last_name)  # 输出：Smith

person.__dict__["first_name"] = "kycool"
print(person.first_name)  # 输出：Alice

print(person.__dict__)


# try:
#     person.first_name = 123  # 这会触发 TypeError
# except TypeError as e:
#     print(e)  # 输出：'first_name' 必须是字符串

# try:
#     person.last_name = True  # 这也会触发 TypeError
# except TypeError as e:
#     print(e)  # 输出：'last_name' 必须是字符串

# del person.first_name  # 这会触发 AttributeError，因为 StringOnly 没有 __delete__ 方法
