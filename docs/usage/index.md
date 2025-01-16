# Hướng dẫn sử dụng

## Yêu cầu chung

- [Tesseract OCR CLI](https://tesseract-ocr.github.io/tessdoc/Installation.html) và [Tesseract data set](https://github.com/tesseract-ocr/tessdata) _(Không bắt buộc)_(1)
  { .annotate }

      1. Sử dụng để giải captcha đối với API `csgt.vn`

!!! warning

    - API `checkphatnguoi.vn` không cho truy cập từ IP nước ngoài? (Ảnh hưởng github action)
    - API `csgt.vn` không đảm bảo hoạt động ổn định vì tesseract giải captcha có tỉ lệ sai, cũng như máy chủ `csgt.vn` không đảm bảo đáp ứng. Vì thế không khuyến khích sử dụng API này.

---

## Thiết lập file config

!!! note

    Thiết lập file config trước khi chạy chương trình

---

## Cài đặt

- Từ mã nguồn

!!! info

    Hiện repo chưa cung cấp file thực thi nên chỉ có thể chạy từ mã nguồn
