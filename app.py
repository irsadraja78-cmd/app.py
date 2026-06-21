import time

class NormalSecurityApp:
    def __init__(self):
        # शुरुआत में हम मान लेते हैं कि कोई पिन सेट नहीं है
        self.saved_pin = "1234"  # यह आपका डिफॉल्ट पिन है
        self.max_attempts = 3    # अधिकतम 3 मौके मिलेंगे

    def login(self):
        print("--- आपका स्वागत है सुरक्षित ऐप में ---")
        attempts = 0

        while attempts < self.max_attempts:
            # यूजर से पिन मांगना
            entered_pin = input("कृपया अपना 4-अंकों का PIN दर्ज करें: ")

            # पिन की जांच करना
            if entered_pin == self.saved_pin:
                print("\n✅ एक्सेस ग्रांटेड! आप ऐप के अंदर आ चुके हैं।")
                self.open_app_dashboard()
                return True
            else:
                attempts += 1
                remaining = self.max_attempts - attempts
                print(f"❌ गलत PIN! आपके पास {remaining} मौके और बचे हैं।\n")
        
        # 3 बार गलत पिन डालने पर सुरक्षा ब्लॉक
        print("🚨 सुरक्षा अलर्ट: 3 बार गलत पिन डाला गया! ऐप को 10 सेकंड के लिए ब्लॉक किया जा रहा है।")
        time.sleep(10) # ऐप को 10 सेकंड के लिए रोक देगा
        print("आप अब फिर से कोशिश कर सकते हैं।")
        return False

    def open_app_dashboard(self):
        # लॉग इन होने के बाद दिखने वाली स्क्रीन
        print("---------------------------------------")
        print("📱 मुख्य डैशबोर्ड: आपकी फाइलें यहाँ सुरक्षित हैं।")
        print("1. सुरक्षित फाइलें देखें")
        print("2. पिन बदलें")
        print("3. लॉग आउट करें")
        print("---------------------------------------")

# ऐप को शुरू करना
app = NormalSecurityApp()
app.login()
