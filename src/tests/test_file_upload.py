import os
import tempfile
from io import BytesIO
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, mock_open

from fairyspace.core import exception


class FileUploadTests(APITestCase):
    """文件上传功能测试用例"""

    def setUp(self):
        """设置测试环境"""
        # 创建临时目录用于测试
        self.temp_media_root = tempfile.mkdtemp()

    def tearDown(self):
        """清理测试环境"""
        # 清理临时文件
        import shutil

        if os.path.exists(self.temp_media_root):
            shutil.rmtree(self.temp_media_root)

    def create_test_file(self, filename="test.txt", content=b"test file content"):
        """创建测试文件"""
        return SimpleUploadedFile(filename, content, content_type="text/plain")

    def create_test_image(self, filename="test.jpg"):
        """创建测试图片文件"""
        # 创建一个简单的图片文件内容（实际项目中可以使用PIL生成真实图片）
        image_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00'
        return SimpleUploadedFile(filename, image_content, content_type="image/jpeg")

    @override_settings(MEDIA_ROOT=None)
    def test_upload_without_media_root_config(self):
        """测试没有配置MEDIA_ROOT时的上传"""
        test_file = self.create_test_file()

        # 模拟一个上传视图（需要根据实际路由调整）
        url = '/fairy/oss/'  # 根据实际路由调整

        response = self.client.post(
            url, {'file': test_file, 'name': 'test upload', 'fairy': 'test fairy param'}, format='multipart'
        )

        # 应该返回配置错误
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('MEDIA_ROOT', str(response.data))

    # @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_successful_file_upload(self):
        """测试成功上传文件"""
        test_file = self.create_test_file("success_test.txt", b"Hello World!")

        url = '/fairy/oss/'  # 根据实际路由调整

        response = self.client.post(
            url,
            {'file': test_file, 'name': 'successful upload', 'fairy': 'test fairy param'},
            format='multipart',
        )

        print(response.data)

        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('file_path', response.data['result'])
        # self.assertIn('file_name', response.data['result'])
        # self.assertIn('relative_path', response.data['result'])
        # self.assertEqual(response.data['result']['file_name'], 'success_test.txt')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_with_default_directory(self):
        """测试使用默认目录上传文件"""
        test_file = self.create_test_file("default_dir_test.txt")

        url = '/fairy/oss/'

        response = self.client.post(url, {'file': test_file, 'name': 'default directory upload'}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('default', response.data['result']['relative_path'])

    def test_upload_without_file(self):
        """测试没有上传文件的情况"""
        url = '/fairy/oss/'

        response = self.client.post(url, {'name': 'no file upload', 'fairy': 'test'}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_large_file(self):
        """测试上传大文件"""
        # 创建一个较大的测试文件 (1MB)
        large_content = b'0' * (1024 * 1024)
        large_file = self.create_test_file("large_file.txt", large_content)

        url = '/fairy/oss/'

        response = self.client.post(
            url, {'file': large_file, 'name': 'large file upload', 'dir_path': 'large_files'}, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['file_name'], 'large_file.txt')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_image_file(self):
        """测试上传图片文件"""
        image_file = self.create_test_image("test_image.jpg")

        url = '/fairy/oss/'

        response = self.client.post(
            url, {'file': image_file, 'name': 'image upload', 'dir_path': 'images'}, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['file_name'], 'test_image.jpg')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_with_special_characters_in_filename(self):
        """测试包含特殊字符的文件名上传"""
        special_file = self.create_test_file("测试文件-2024年.txt", b"Chinese filename test")

        url = '/fairy/oss/'

        response = self.client.post(
            url, {'file': special_file, 'name': 'special characters test', 'dir_path': 'special'}, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['file_name'], '测试文件-2024年.txt')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @patch('builtins.open', mock_open())
    @patch('os.makedirs')
    def test_upload_directory_creation_error(self, mock_makedirs):
        """测试目录创建失败的情况"""
        mock_makedirs.side_effect = OSError("Permission denied")

        test_file = self.create_test_file()
        url = '/fairy/oss/'

        response = self.client.post(
            url, {'file': test_file, 'name': 'directory error test', 'dir_path': 'error_dir'}, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('无法创建上传目录', str(response.data))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @patch('builtins.open')
    def test_upload_file_write_error(self, mock_open):
        """测试文件写入失败的情况"""
        mock_open.side_effect = OSError("Disk full")

        test_file = self.create_test_file()
        url = '/fairy/oss/'

        response = self.client.post(url, {'file': test_file, 'name': 'write error test'}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('文件保存失败', str(response.data))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_serializer_validation(self):
        """测试序列化器验证"""
        from fairyspace.rest.mixins import FileUploadSerializer

        # 测试有效数据
        test_file = self.create_test_file()
        serializer = FileUploadSerializer(data={'file': test_file, 'name': 'test', 'fairy': 'test'})
        self.assertTrue(serializer.is_valid())

        # 测试无效数据（缺少文件）
        serializer = FileUploadSerializer(data={'name': 'test', 'fairy': 'test'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('file', serializer.errors)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_multiple_files_upload_sequence(self):
        """测试连续上传多个文件"""
        url = '/fairy/oss/'

        files_to_upload = [
            ('file1.txt', b'Content 1'),
            ('file2.txt', b'Content 2'),
            ('file3.txt', b'Content 3'),
        ]

        uploaded_files = []

        for filename, content in files_to_upload:
            test_file = self.create_test_file(filename, content)

            response = self.client.post(
                url, {'file': test_file, 'name': f'Upload {filename}', 'dir_path': 'multi_upload'}, format='multipart'
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            uploaded_files.append(response.data['result'])

        # 验证所有文件都上传成功
        self.assertEqual(len(uploaded_files), 3)
        for i, file_data in enumerate(uploaded_files):
            expected_filename = files_to_upload[i][0]
            self.assertEqual(file_data['file_name'], expected_filename)


class FileUploadIntegrationTests(APITestCase):
    """文件上传集成测试"""

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_and_verify_file_exists(self):
        """测试上传文件并验证文件确实存在"""
        test_content = b"Integration test content"
        test_file = SimpleUploadedFile("integration_test.txt", test_content, content_type="text/plain")

        url = '/fairy/oss/'

        response = self.client.post(
            url, {'file': test_file, 'name': 'integration test', 'dir_path': 'integration'}, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证文件确实被保存
        file_path = response.data['result']['file_path']
        self.assertTrue(os.path.exists(file_path))

        # 验证文件内容
        with open(file_path, 'rb') as f:
            saved_content = f.read()
            self.assertEqual(saved_content, test_content)

        # 清理测试文件
        os.remove(file_path)
