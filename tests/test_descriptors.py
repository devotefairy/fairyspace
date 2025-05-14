"""测试 Python 描述器的各种类型和行为。

包括以下类型的描述器测试：
- 数据描述器（@property）
- 非数据描述器
- 类方法描述器（@classmethod）
- 静态方法描述器（@staticmethod）
"""

import pytest


class TestPropertyDescriptor:
    """测试@property 数据描述器的行为。"""

    class Person:
        def __init__(self, name: str):
            self._name = name

        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, value: str) -> None:
            if not value:
                raise ValueError("名字不能为空")
            self._name = value

        @name.deleter
        def name(self) -> None:
            self._name = ""

    def test_property_getter(self):
        """测试属性的读取行为。"""
        # Arrange
        person = self.Person("张三")

        # Act
        result = person.name

        # Assert
        assert result == "张三", "属性 getter 应返回正确的值"

    def test_property_setter(self):
        """测试属性的设置行为。"""
        # Arrange
        person = self.Person("张三")

        # Act
        person.name = "李四"

        # Assert
        assert person.name == "李四", "属性 setter 应正确设置值"

    def test_property_setter_validation(self):
        """测试属性设置时的验证。"""
        # Arrange
        person = self.Person("张三")

        # Act & Assert
        with pytest.raises(ValueError, match="名字不能为空"):
            person.name = ""

    def test_property_deleter(self):
        """测试属性的删除行为。"""
        # Arrange
        person = self.Person("张三")

        # Act
        del person.name

        # Assert
        assert person.name == "", "属性 deleter 应清空值"


class TestNonDataDescriptor:
    """测试非数据描述器的行为。"""

    class LazyProperty:
        """延迟加载属性的非数据描述器。"""

        def __init__(self, func):
            self.func = func
            self.name = func.__name__

        def __get__(self, obj, owner=None):
            if obj is None:
                return self
            value = self.func(obj)
            setattr(obj, self.name, value)
            return value

    class Calculator:
        def __init__(self, x: int):
            self.x = x

        @LazyProperty
        def square(self) -> int:
            return self.x * self.x

    def test_lazy_property_computation(self):
        """测试延迟属性的计算。"""
        # Arrange
        calc = self.Calculator(4)

        # Act
        result = calc.square

        # Assert
        assert result == 16, "延迟属性应正确计算结果"
        assert hasattr(calc, "square"), "计算结果应被缓存"


class TestClassMethodDescriptor:
    """测试@classmethod 描述器的行为。"""

    class DateUtil:
        date_format = "%Y-%m-%d"

        def __init__(self, date_str: str):
            self.date_str = date_str

        @classmethod
        def set_format(cls, fmt: str) -> None:
            cls.date_format = fmt

        @classmethod
        def get_format(cls) -> str:
            return cls.date_format

    @pytest.mark.parametrize(
        "new_format,expected",
        [
            ("%Y/%m/%d", "%Y/%m/%d"),
            ("%d-%m-%Y", "%d-%m-%Y"),
        ],
        ids=["斜线格式", "欧洲格式"],
    )
    def test_class_method_format_setting(self, new_format: str, expected: str):
        """测试类方法对类属性的修改。"""
        # Arrange & Act
        self.DateUtil.set_format(new_format)

        # Assert
        assert self.DateUtil.get_format() == expected, "类方法应正确修改类属性"


class TestStaticMethodDescriptor:
    """测试@staticmethod 描述器的行为。"""

    class MathUtil:
        @staticmethod
        def is_even(number: int) -> bool:
            return number % 2 == 0

        @staticmethod
        def is_positive(number: int) -> bool:
            return number > 0

    @pytest.mark.parametrize(
        "number,expected",
        [
            (2, True),
            (3, False),
            (0, True),
            (-2, True),
        ],
        ids=["偶数", "奇数", "零", "负偶数"],
    )
    def test_static_method_even_check(self, number: int, expected: bool):
        """测试静态方法的行为。"""
        # Act
        result = self.MathUtil.is_even(number)

        # Assert
        assert result == expected, f"{number} 的奇偶性判断错误"

    @pytest.mark.parametrize(
        "number,expected",
        [
            (1, True),
            (0, False),
            (-1, False),
        ],
        ids=["正数", "零", "负数"],
    )
    def test_static_method_positive_check(self, number: int, expected: bool):
        """测试多个静态方法的独立性。"""
        # Act
        result = self.MathUtil.is_positive(number)

        # Assert
        assert result == expected, f"{number} 的正负性判断错误"
