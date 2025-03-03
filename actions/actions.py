from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Link các hướng dẫn
ACTIONS_DATA = {
    "tải phần mềm": {
        "name": "tải phần mềm",
        "link": ""
    },
    "sử dụng phần mềm": {
        "name": "sử dụng phần mềm",
        "link": "https://www.youtube.com/@congtyphanmemtotnhat8496/shorts"
    },
    "hốt hụi": {
        "name": "hốt hụi",
        "link": "https://www.youtube.com/watch?v=Yn8LgiFjy3g"
    },
    "đóng hụi": {
        "name": "đóng hụi",
        "link": "https://www.youtube.com/watch?v=SSxNbCxp1EY"
    },
    "tất toán hụi chết": {
        "name": "tất toán hụi chết",
        "link": "https://www.youtube.com/shorts/jJf87pcf23c"
    },
    "in tất cả bill đóng trong ngày": {
        "name": "in tất cả bill đóng trong ngày",
        "link": "https://www.youtube.com/shorts/nw7WNiRD_RI"
    },
    "xóa hốt hụi": {
        "name": "xóa hốt hụi",
        "link": "https://www.youtube.com/shorts/nxlwQEc61YU"
    },
    "gom hụi viên bị trùng": {
        "name": "gom hụi viên bị trùng",
        "link": "https://www.youtube.com/shorts/9VFWoRkcFXI"
    },
    "thêm số phần hụi trong dây hụi": {
        "name": "thêm số phần hụi trong dây hụi",
        "link": "https://www.youtube.com/shorts/Yuup3Vt0YWU"
    },
    "giảm số phần hụi trong dây hụi": {
        "name": "giảm số phần hụi trong dây hụi",
        "link": "https://www.youtube.com/shorts/Yuup3Vt0YWU"
    },
    "thay đổi hụi viên trong dây hụi": {
        "name": "thay đổi hụi viên trong dây hụi",
        "link": "https://www.youtube.com/shorts/Yuup3Vt0YWU"
    },
    "hốt hụi nhiều người cùng kỳ": {
        "name": "hốt hụi nhiều người cùng kỳ",
        "link": "https://www.youtube.com/shorts/MNswWfmdWHQ"
    },
    "xóa tất toán hụi chết": {
        "name": "xóa tất toán hụi chết",
        "link": "https://www.youtube.com/shorts/8GfCuW9uKZg"
    },
    "tất toán hụi sống": {
        "name": "tất toán hụi sống",
        "link": "https://www.youtube.com/shorts/7TJFDykejAU"
    },
    "tạo dây hụi góp": {
        "name": "tạo dây hụi góp",
        "link": "https://www.youtube.com/shorts/rSyTlHMM_OA"
    },
    "mở dây hụi mãn trở lại đang hoạt động": {
        "name": "mở dây hụi mãn trở lại đang hoạt động",
        "link": "https://www.youtube.com/shorts/HG76fJ1DmQI"
    },
    "mãn dây hụi": {
        "name": "mãn dây hụi",
        "link": "https://www.youtube.com/shorts/SF5m5mQxp1w"
    },
    "đóng lại hụi cũ để tính cân bằng hụi chính xác": {
        "name": "đóng lại hụi cũ để tính cân bằng hụi chính xác",
        "link": "https://www.youtube.com/watch?v=SSxNbCxp1EY"
    },
    "xóa kỳ hốt": {
        "name": "xóa kỳ hốt",
        "link": "https://www.youtube.com/shorts/8i7RiyGiW8c"
    },
    "xóa kỳ đóng bị lỗi": {
        "name": "xóa kỳ đóng bị lỗi",
        "link": "https://www.youtube.com/shorts/8i7RiyGiW8c"
    },
    "xác nhận đóng tất cả hụi": {
        "name": "xác nhận đóng tất cả hụi",
        "link": "https://www.youtube.com/watch?v=SSxNbCxp1EY"
    },
    "cân bằng âm dương": {
        "name": "cân bằng âm dương",
        "link": "https://www.youtube.com/shorts/acgQvk26wQI"
    }
}

# Hàm chung để cung cấp link hướng dẫn
class ActionProvideGuide(Action):
    def name(self) -> Text:
        return "action_provide_guide"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        actions = tracker.get_slot("actions")

        if actions in ACTIONS_DATA:
            video_link = ACTIONS_DATA[actions]["link"]
            message = f"Để {ACTIONS_DATA[actions]['name']}, bạn vui lòng xem video hướng dẫn tại đây: {video_link}"
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Xin lỗi, mình chưa hiểu ý của bạn.")

        return []