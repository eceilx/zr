import requests
import json
import yaml

# ---URL---
BASE_URL = 'http://123.57.222.123:9901'
USER_URL = BASE_URL+'/userInfo'
SELECT_URL = BASE_URL+'/selectInfo'
RESERVE_URL = BASE_URL+'/reservation'
SCAN_URL = BASE_URL + '/scan'

# ----------------Base Requests-----------------


class BaseRequest:
    def __init__(self):
        self.__session = requests.Session()

    def set_bearer_token(self, bearer_token):
        self.__auth_header = {
            'Authorization': bearer_token
        }

    def _post(self, url):
        # print(url)
        return self.__session.post(url).text

    def _post_with_bearer(self, url):
        return self.__session.post(url, headers=self.__auth_header).text

    # ----Other ...-----

    def check_update(self):
        return self._post(f'{BASE_URL}/version/android')

    def query_school(self):
        return self._post(f'{BASE_URL}/school/selectSchool')

    def query_systime(self):
        return self._post(f'{BASE_URL}/getTime/getSystemTime')

    # ----USER----

    def login(self, username, password, school_id):
        return self._post(f'{USER_URL}/login?userNum={username}&userPwd={password}&schoolNum={school_id}')

    def change_password(self, user_id, oldpwd, newpwd):
        return self._post_with_bearer(f'{USER_URL}/current/password?userInfoId={user_id}&oldPassword={oldpwd}&newPassword={newpwd}')

    # ---- Reservation----
    # ---core---

    def reserve(self, user_id, seat_id, begin, end, not_arrive):
        return self._post_with_bearer(f'{RESERVE_URL}/addReservationBychoose?userInfoId={user_id}&seatId={seat_id}&reservationBeginTime={begin}&reservationEndTime={end}&notArrive={not_arrive}')

    def reserve_random(self, user_id, begin, end, campus_id, building_id, floor, room_id):
        return self._post_with_bearer(f'{RESERVE_URL}/addSeatByrandom?campusId={campus_id}&buildingId={building_id}&floor={floor}&classroomId={room_id}&reservationBeginTime={begin}&reservationEndTime={end}&userInfoId={user_id}')

    def extend_reserve(self, resevation_id, user_id, new_end):
        return self._post_with_bearer(f'{RESERVE_URL}/extendSeatTime?reservationId={resevation_id}&userInfoId={user_id}&reservationEndTime={new_end}')

    def cancel_reserve(self, reservation_id):
        return self._post_with_bearer(f'{RESERVE_URL}/cancelReservation?reservationId={reservation_id}')

    def get_seat_reservation(self, seat_id, not_arrive):
        return self._post_with_bearer(f'{RESERVE_URL}/selectReservation?seatId={seat_id}&notArrive={not_arrive}')

    def get_all_reservation(self, user_id):
        return self._post_with_bearer(f'{RESERVE_URL}/selectReservationByUser?userInfoId={user_id}')

    def query_history(self, user_id, state, now_page, page_size):
        return self._post_with_bearer(f'{RESERVE_URL}/selectReservation?userInfoId={user_id}&state={state}&nowPage={now_page}&pageSize={page_size}')

    # ---other---

    def query_config(self, compus_id):
        return self._post_with_bearer(f'{BASE_URL}/configuration/selectConfig?campusId={compus_id}')

    def query_building(self, user_id):
        return self._post_with_bearer(f'{SELECT_URL}/selectBuildingContainResearchRoom?userId={user_id}')

    def query_library(self, user_id):
        return self._post_with_bearer(f'{SELECT_URL}/selectCampusAndBuildingInfomation?userInfoId={user_id}')

    def query_room(self, user_id, library_id):
        return self._post_with_bearer(f'{BASE_URL}/classroom/selectClassroomByBuilding?buildingId={library_id}&userId={user_id}')

    def query_seat_status(self, room_id, begin, end):
        return self._post_with_bearer(f'{SELECT_URL}/selectEachClassroom_SeatsInfo?classroomId={room_id}&reservationBeginTime={begin}&reservationEndTime={end}')

    def get_recommend(self, seat_id, begin):
        return self._post_with_bearer(f'{BASE_URL}/seat/getRecommendReservationTime?seatId={seat_id}&reservationBeginTime={begin}')

    # ---scan QR Code---

    def scan_to_sit(self, user_id, seat_id):
        return self._post_with_bearer(f'{SCAN_URL}/scanQrCode?userInfoId={user_id}&seatId={seat_id}')

    def change_seat(self, seat_id, reservation_id):
        return self._post_with_bearer(f'{SCAN_URL}/seatInfo?seatId={seat_id}&reservationId={reservation_id}')


# ----------------Model .----------------------
HUAT_SCHOOL_ID = '3df715dc-e177-4b71-907c-af530ff9f8ca'


class User():

    def __init__(self, username, pwd, school_id):
        self.username = username
        self.password = pwd
        self.school_id = school_id
        self.user_id = None
        self.base_request = BaseRequest()

    def login(self):
        resp = self.base_request.login(
            self.username, self.password, self.school_id)
        m = json.loads(resp)
        if not m['success']:
            return False

        # main param
        obj = m['object']
        self.user_id = obj['userInfoId']
        self.campus_id = obj['campusId']
        self.head_portrait = obj['headPortrait']
        self.sex = obj['userSex']
        self.name = obj['userName']
        self.school_name = obj['schoolName']
        self.school_id = obj['schoolNum']
        self.campus_name = obj['campusName']
        self.student_year = obj['studentYear']
        self.major = obj['major']
        self.phone_num = obj['phoneNum']
        self.email = obj['userEmail']
        self.credential = obj['credential']
        self.auth_token = obj['token']

        # 设置auth
        self.base_request.set_bearer_token(self.auth_token)
        return True

    def change_pwd(self, new_pwd):
        resp = self.base_request.change_password(
            self.user_id, self.password, new_pwd)
        m = json.loads(resp)
        # print(self, m['message'])
        return m['success']

    def reserve(self, seat_id, begin_time, end_time):
        resp = self.base_request.reserve(
            self.user_id, seat_id, begin_time, end_time, 1)
        m = json.loads(resp)
        # print(m)
        return m

    def reserve_random(self,  begin_time, end_time, building_id, floor, room_id):
        resp = self.base_request.reserve_random(
                                                self.user_id, begin_time, end_time, self.campus_id, building_id, floor, room_id)
        m = json.loads(resp)

    def get_reservation_times(self):
        resp = self.base_request.query_history(self.user_id, 0, 1, 1)
        # print(self, resp)
        m = json.loads(resp)
        return m['sumReservation'] if m['success'] else 0

    def get_history(self):
        resp = self.base_request.query_history(
            self.user_id, 0, 1, self.get_reservation_times())
        # print(self, resp)
        m = json.loads(resp)
        if m['success']:
            return m['list']
        return None

    def get_current_reservation(self):
        resp = self.base_request.get_all_reservation(self.user_id)
        m = json.loads(resp)
        if m['success']:
            return m
            # todo ...
        return None

    def scan_to_sit(self, seat_id):
        resp = self.base_request.scan_to_sit(self.user_id, seat_id)
        m = json.loads(resp)
        return m

    def scan_to_change(self, reservation_id, new_seat_id):
        resp = self.base_request.change_seat(new_seat_id, reservation_id)
        m = json.loads(resp)


# -----------------------function function-----------------------
def time_url_encode(time):
    return (time+":00").replace(':', '%3A')


def load_cfg():
    with open('config.yaml') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        return cfg