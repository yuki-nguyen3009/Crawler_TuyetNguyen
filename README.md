# Crawler_TuyetNguyen

Ý tưởng::

  - Get source của trang web về bằng lệnh curl.
  
  - Lọc các đường link css và js file, thay thế nó bằng đường dẫn của source trên web.
  
  - Lưu các dữ liệu đã chrnh sửa vảo file index.html trong đường dẫn: 'D/codeCamp'.
  
  - file css, js được downdload về nằm trong đường dẫn D:/codeCamp/files
  
  
 Issue:

  - Khi trang web hoặt động offline vẫn chưa lấy về được các hình ảnh => các hình ảnh chưa load được.
