
import requests
import json

# Thông tin cấu hình từ bạn
FB_PAGE_TOKEN = "EAAUTbY2aZAOQBOZCRLexNdLhz6qsR3NIZBwgEkG5scRYBnPuLuJYAEmZAuMWoqN8jkWydNFnFHxQp7nvrArTJq1HuPZCEyL6RFx9UOZAzXLCYcJ3sXC60dTZCGP4EQEuC2z6wZCcZCmArsZCGkEvBGqZAR4R4QePzmZCxHqpfgSgjXZAbZA1TJiMsQZApxxfDs4VQd0iL5SAmOD5dlLMOVCa3UqZAMUZD"
GEMINI_API_KEY = "AIzaSyCoj4fjCMm7r3NsHJ1rxh0J8nH6gv5mhrg"
FB_API_URL = "https://graph.facebook.com/v20.0"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"  # URL Gemini API chính thức

# Hàm lấy nội dung bình luận từ Facebook
def get_comment(comment_id):
    url = f"{FB_API_URL}/{comment_id}?fields=message&access_token={FB_PAGE_TOKEN}"
    response = requests.get(url)
    data = response.json()
    return data.get("message")

# Hàm tạo phản hồi từ Gemini API
def generate_reply(comment_text):
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{"parts": [{"text": f"Trả lời bình luận sau một cách thân thiện và tự nhiên: '{comment_text}'"}]}],
    }
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    # Lấy nội dung phản hồi từ Gemini
    return data["candidates"][0]["content"]["parts"][0]["text"]

# Hàm đăng phản hồi lên Facebook
def post_reply(comment_id, reply_text):
    url = f"{FB_API_URL}/{comment_id}/comments?access_token={FB_PAGE_TOKEN}"
    payload = {"message": reply_text}
    response = requests.post(url, data=payload)
    return response.status_code == 200

# Xử lý bình luận mới
def handle_new_comment(comment_id):
    comment_text = get_comment(comment_id)
    if comment_text:
        reply_text = generate_reply(comment_text)
        if post_reply(comment_id, reply_text):
            print(f"Đã trả lời: {reply_text}")
        else:
            print("Lỗi khi đăng phản hồi")
    else:
        print("Không lấy được nội dung bình luận")

# Thử nghiệm với một comment_id cụ thể
comment_id = "648985731088308"  # Thay bằng ID bình luận thực tế
handle_new_comment(comment_id)
