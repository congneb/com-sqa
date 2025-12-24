
## Set-top-box (STB)

Testing: Gồm test HW và SW

🖥️ 1. Kiểm thử phần cứng (Hardware Test)

    - Khởi động thiết bị: Kiểm tra thời gian boot, hiển thị logo, trạng thái đèn báo.
    
    - Cổng kết nối: HDMI, AV, USB, Ethernet, thẻ nhớ – đảm bảo nhận diện và hoạt động đúng.
    
    - Remote control: Độ nhạy, phạm vi, phản hồi phím bấm.
    
    - Nguồn điện: Hoạt động ổn định, kiểm tra khi mất điện đột ngột.

📡 2. Kiểm thử tín hiệu và giải mã (Signal & Decoding Test)

    - Nhận tín hiệu: Cáp, vệ tinh, IPTV – kiểm tra khả năng bắt tín hiệu.
    
    - Chất lượng hình ảnh/âm thanh: Độ phân giải (SD, HD, 4K), độ trễ, đồng bộ audio/video.
    
    - Chuyển kênh: Thời gian chuyển kênh, có bị giật/lỗi hình.
    
    - Mất tín hiệu: Hiển thị thông báo lỗi, tự động reconnect.

📲 3. Kiểm thử phần mềm (Software Test)

    - Giao diện người dùng (UI): Menu, danh sách kênh, cài đặt – dễ dùng, không crash.
    
    - Chức năng tìm kiếm: Tìm kênh, tìm nội dung theo từ khóa.
    
    - Cập nhật firmware: OTA update, rollback khi lỗi.
    
    - Ứng dụng tích hợp: YouTube, Netflix, IPTV app – khả năng cài đặt và chạy.

🌐 4. Kiểm thử kết nối mạng (Network Test)

    - Wi-Fi/Ethernet: Kết nối ổn định, tốc độ truyền tải.
    
    - Streaming: Xem video online, kiểm tra buffering.
    
    - Bảo mật: Kiểm tra đăng nhập, mã hóa dữ liệu.

🎥 5. Kiểm thử tính năng nâng cao

    - Ghi lại chương trình (PVR): Lưu, phát lại, kiểm tra dung lượng.
    
    - Time-shift: Tạm dừng và tiếp tục chương trình đang phát.
    
    - Parental control: Khóa kênh, kiểm tra mật khẩu.
    
    - Đa ngôn ngữ: Subtitle, audio track.

⚙️ 6. Kiểm thử hiệu năng (Performance Test)

    - Thời gian phản hồi: Menu, chuyển kênh, mở ứng dụng.
    
    - Đa nhiệm: Chạy nhiều ứng dụng song song.

    - Stress test: Chạy liên tục nhiều giờ, kiểm tra nhiệt độ và độ ổn định.

🧪 7. Kiểm thử bảo mật và tuân thủ

    - Bảo mật dữ liệu người dùng: Tài khoản, thông tin cá nhân.
    
    - Tuân thủ chuẩn: DVB, MPEG, DRM.
    
    - Kiểm thử lỗi: Xử lý khi nhập sai mật khẩu, khi không có tín hiệu.


## 📜 Robot Framework Example

Kịch bản chuyển kênh trên Set-top box (STB)

```
*** Settings ***
Library           OperatingSystem
Library           BuiltIn
Library           Collections
Library           RequestsLibrary   # nếu STB có API HTTP
Library           Process

*** Variables ***
${STB_IP}         192.168.1.100
${STB_PORT}       8080
@{CHANNELS}       1    5    10    20

*** Test Cases ***
Switch Channel Test
    [Documentation]    Kiểm tra thời gian chuyển kênh và tín hiệu hình/âm thanh
    FOR    ${ch}    IN    @{CHANNELS}
        ${start}=    Get Time    epoch
        Send Channel Change Command    ${ch}
        Wait Until Keyword Succeeds    3s    1s    Verify Signal OK
        ${end}=    Get Time    epoch
        ${switch_time}=    Evaluate    ${end} - ${start}
        Should Be True    ${switch_time} <= 2    Chuyển kênh quá chậm: ${switch_time}s
    END

*** Keywords ***
Send Channel Change Command
    [Arguments]    ${channel}
    # Ví dụ gọi API giả định: http://STB_IP:STB_PORT/change_channel?ch=xx
    ${resp}=    Get Request    ${STB_IP}:${STB_PORT}    /change_channel?ch=${channel}
    Should Be Equal As Strings    ${resp.status_code}    200

Verify Signal OK
    # Giả định có API kiểm tra tín hiệu video/audio
    ${resp}=    Get Request    ${STB_IP}:${STB_PORT}    /signal_status
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Contain    ${resp.text}    video_ok
    Should Contain    ${resp.text}    audio_ok

```

🛠️ Giải thích

    RequestsLibrary: dùng để gửi lệnh HTTP tới STB (nếu có API).
    
    FOR loop: chạy qua danh sách kênh cần test.
    
    Get Time: đo thời gian chuyển kênh.
    
    Wait Until Keyword Succeeds: chờ tín hiệu ổn định trong vòng 3 giây.
    
    Should Be True: kiểm tra thời gian chuyển kênh ≤ 2 giây.
    
    Custom Keywords: Send Channel Change Command và Verify Signal OK mô phỏng thao tác remote và kiểm tra tín hiệu.
