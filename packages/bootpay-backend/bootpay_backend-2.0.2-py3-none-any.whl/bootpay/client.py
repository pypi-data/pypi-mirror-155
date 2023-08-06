import requests
import uuid
import json
from bootpay import bankcode
import time


class Bootpay:
    base_url = {
        'development': 'https://dev-api.bootpay.co.kr',
        'production': 'https://api.bootpay.co.kr'
    }

    def __init__(self, application_id, private_key, mode='production'):
        self.application_id = application_id
        self.pk = private_key
        self.mode = mode
        self.token = None

    def api_url(self, uri=None):
        if uri is None:
            uri = []
        return '/'.join([self.base_url[self.mode]] + uri)

    # 1. 토큰 발급 
    def get_access_token(self):
        data = {
            'application_id': self.application_id,
            'private_key': self.pk
        }
        response = requests.post(self.api_url(['request', 'token']), data=data)
        result = response.json()
        if result['status'] == 200:
            self.token = result['data']['token']
        return result

    # 2. 결제 검증 
    def verify(self, receipt_id):
        return requests.get(self.api_url(['receipt', receipt_id]), headers={
            'Authorization': self.token
        }).json()

    # 3. 결제 취소 (전액 취소 / 부분 취소)
    #
    # price - (선택사항) 부분취소 요청시 금액을 지정, 미지정시 전액 취소 (부분취소가 가능한 PG사, 결제수단에 한해 적용됨)
    # cancel_id - (선택사항) 부분취소 요청시 중복 요청을 방지하기 위한 고유값
    # refund - (선택사항) 가상계좌 환불요청시, 전제조건으로 PG사와 CMS 특약이 체결되어 있을 경우에만 환불요청 가능, 기본적으로 가상계좌는 결제취소가 안됨 
    #        {
    #            account: '6756010101234', # 환불받을 계좌번호 
    #            accountholder: '홍길동', # 환불받을 계좌주
    #            bankcode: bankcode.dictionary['국민은행'], # 은행 코드 
    #        }
    #
    def cancel(self, receipt_id, price=None, name=None, reason=None, cancel_id=str(uuid.uuid4()), tax_free=None,
               refund=None):
        payload = {'receipt_id': receipt_id,  # 부트페이로부터 받은 영수증 ID
                   'price': price,  # 부분취소시 금액 지정
                   'name': name,  # 취소 요청자 이름
                   'reason': reason,  # 취소 요청 사유
                   'tax_free': tax_free,  # 취소할 비과세 금액
                   'cancel_id': cancel_id,  # 부분취소 중복요청 방지
                   'refund': refund}

        return requests.post(self.api_url(['cancel.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    # 4. 빌링키 발급
    # extra - 빌링키 발급 옵션 
    #      {
    #               subscribe_tst_payment: 0, # 100원 결제 후 결제가 되면 billing key를 발행, 결제가 실패하면 에러
    #               raw_data: 0 //PG 오류 코드 및 메세지까지 리턴
    #      }  
    def get_subscribe_billing_key(self, pg, order_id, item_name, card_no, card_pw, expire_year, expire_month,
                                  identify_number,
                                  user_info=None, extra=None):
        if user_info is None:
            user_info = {}
        payload = {
            'order_id': order_id,  # 개발사에서 관리하는 고유 주문 번호
            'pg': pg,  # PG사의 Alias ex) danal, kcp, inicis 등
            'item_name': item_name,  # 상품명
            'card_no': card_no,  # 카드 일련번호
            'card_pw': card_pw,  # 카드 비밀번호 앞 2자리
            'expire_year': expire_year,  # 카드 유효기간 년
            'expire_month': expire_month,  # 카드 유효기간 월
            'identify_number': identify_number,  # 주민등록번호 또는 사업자번호
            'user_info': user_info,  # 구매자 정보
            'extra': extra  # 기타 옵션
        }
        return requests.post(self.api_url(['request', 'card_rebill.json']), data=json.dumps(payload), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    # 4-1. 발급된 빌링키로 결제 승인 요청 
    # tax_free - 면세 상품일 경우 해당만큼의 금액을 설정 
    # interest - 웰컴페이먼츠 전용, 무이자여부를 보내는 파라미터가 있다
    # quota - 5만원 이상 결제건에 적용하는 할부개월수. 0-일시불, 1은 지정시 에러 발생함, 2-2개월, 3-3개월... 12까지 지정가능
    # feedback_url - webhook 통지시 받으실 url 주소 (localhost 사용 불가)
    # feedback_content_type - webhook 통지시 받으실 데이터 타입 (json 또는 urlencoded, 기본값 urlencoded)
    #####
    def subscribe_billing(self, billing_key, item_name, price, order_id, items=None, user_info=None, extra=None,
                          tax_free=None, quota=None, interest=None, feedback_url=None, feedback_content_type=None):
        if items is None:
            items = []
        payload = {
            'billing_key': billing_key,  # 발급받은 빌링키
            'item_name': item_name,  # 결제할 상품명
            'price': price,  # 결제할 상품금액
            'order_id': order_id,  # 개발사에서 지정하는 고유주문번호
            'items': items,  # 구매할 상품정보, 통계용
            'user_info': user_info,  # 구매자 정보, 특정 PG사의 경우 구매자 휴대폰 번호를 필수로 받는다
            'extra': extra,  # 기타 옵션
            'tax_free': tax_free,  # 면세 상품일 경우 해당만큼의 금액을 설정
            'quota': quota,  # int 형태, 5만원 이상 결제건에 적용하는 할부개월수. 0-일시불, 1은 지정시 에러 발생함, 2-2개월, 3-3개월... 12까지 지정가능
            'interest': interest,  # 웰컴페이먼츠 전용, 무이자여부를 보내는 파라미터가 있다
            'feedback_url': feedback_url,  # webhook 통지시 받으실 url 주소 (localhost 사용 불가)
            'feedback_content_type': feedback_content_type
            # webhook 통지시 받으실 데이터 타입 (json 또는 urlencoded, 기본값 urlencoded)
        }
        return requests.post(self.api_url(['subscribe', 'billing.json']), data=json.dumps(payload), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    # 4-2. 발급된 빌링키로 결제 예약 요청
    # def subscribe_billing_reserve(self, billing_key, item_name, price, order_id, execute_at, feedback_url, items=None):
    def subscribe_billing_reserve(self, billing_key, item_name, price, order_id, execute_at=time.time() + 10,
                                  items=None, user_info=None, extra=None,
                                  tax_free=None, quota=None, interest=None, feedback_url=None,
                                  feedback_content_type=None):
        if items is None:
            items = []
        payload = {
            'billing_key': billing_key,  # 발급받은 빌링키
            'item_name': item_name,  # 결제할 상품명
            'price': price,  # 결제할 상품금액
            'order_id': order_id,  # 개발사에서 지정하는 고유주문번호
            'execute_at': execute_at,  # 결제 수행(예약) 시간, 기본값으로 10초 뒤 결제
            'items': items,  # 구매할 상품정보, 통계용
            'user_info': user_info,  # 구매자 정보, 특정 PG사의 경우 구매자 휴대폰 번호를 필수로 받는다
            'extra': extra,  # 기타 옵션
            'tax_free': tax_free,  # 면세 상품일 경우 해당만큼의 금액을 설정
            'quota': quota,  # int 형태, 5만원 이상 결제건에 적용하는 할부개월수. 0-일시불, 1은 지정시 에러 발생함, 2-2개월, 3-3개월... 12까지 지정가능
            'interest': interest,  # 웰컴페이먼츠 전용, 무이자여부를 보내는 파라미터가 있다
            'feedback_url': feedback_url,  # webhook 통지시 받으실 url 주소 (localhost 사용 불가)
            'feedback_content_type': feedback_content_type,
            # webhook 통지시 받으실 데이터 타입 (json 또는 urlencoded, 기본값 urlencoded)
            'scheduler_type': 'oneshot'
        }
        return requests.post(self.api_url(['subscribe', 'billing', 'reserve.json']), data=json.dumps(payload), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    # 4-2-1. 발급된 빌링키로 결제 예약 - 취소 요청 
    def subscribe_billing_reserve_cancel(self, reserve_id):
        return requests.delete(self.api_url(['subscribe', 'billing', 'reserve', reserve_id]), headers={
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }).json()

    # 4-3. 빌링키 삭제
    def destroy_subscribe_billing_key(self, billing_key):
        return requests.delete(self.api_url(['subscribe', 'billing', billing_key]), headers={
            'Authorization': self.token
        }).json()

    # 5. (부트페이 단독 - 간편결제창, 생체인증 기반의 사용자를 위한) 사용자 토큰 발급
    def get_user_token(self, user_id=None, email=None, name=None, gender=None, birth=None, phone=None):
        payload = {
            'user_id': user_id,  # 개발사에서 관리하는 회원 고유 id
            'email': email,  # 구매자 email
            'name': name,  # 구매자 이름
            'gender': gender,  # 0:여자, 1:남자
            'birth': birth,  # 생일 901004
            'phone': phone  # 01012341234
        }

        return requests.post(self.api_url(['request', 'user', 'token.json']), data=json.dumps(payload), headers={
            'Authorization': self.token
        }).json()

    # 6. 결제링크 생성 
    # user_info # 구매자 모델 설명 
    # { 
    #   id: nil, # 개발사에서 관리하는 회원 고유 id
    #   username: nil, # 구매자 이름
    #   email: nil, # 구매자 email
    #   phone: nil, # 01012341234
    #   gender: nil, # 0:여자, 1:남자
    #   area: nil, # 서울|인천|대구|광주|부산|울산|경기|강원|충청북도|충북|충청남도|충남|전라북도|전북|전라남도|전남|경상북도|경북|경상남도|경남|제주|세종|대전 중 택 1
    #   birth: nil # 생일 901004
    # },
    # item 모델 설명
    # {
    #   item_name: '', # 상품명
    #   qty: 1, # 수량
    #   unique: '', # 상품 고유키
    #   price: 1000, # 상품단가
    #   cat1: '', # 카테고리 상
    #   cat2: '', # 카테고리 중
    #   cat3: '' # 카테고리 하
    # }
    # extra 모델 설명 
    # { 
    #     escrow: false, # 에스크로 연동 시 true, 기본값 false
    #     quota: [0,2,3], #List<int> 형태,  결제금액이 5만원 이상시 할부개월 허용범위를 설정할 수 있음, ex) "0,2,3" 지정시 - [0(일시불), 2개월, 3개월] 허용, 미설정시 PG사별 기본값 적용, 1 지정시 에러가 발생할 수 있음
    #     disp_cash_result: nil, # 현금영수증 노출할지 말지 (가상계좌 이용시)
    #     offer_period: '월 자동결제', # 통합결제창, PG 정기결제창에서 표시되는 '월 자동결제'에 해당하는 문구를 지정한 값으로 변경, 지원하는 PG사만 적용 가능
    #     theme: nil, # 통합결제창 테마, [ red, purple(기본), custom ] 중 택 1
    #     custom_background: nil, # 통합결제창 배경색,  ex) "#00a086" theme가 custom 일 때 background 색상 지정 가능
    #     custom_font_color: nil # 통합결제창 글자색,  ex) "#ffffff" theme가 custom 일 때 font color 색상 지정 가능
    # }
    def request_payment(self, pg=None, method=None, methods=None, price=None, order_id=None, params=None, tax_free=None,
                        name=None,
                        user_info={}, items=None, extra={}):

        if items is None:
            items = []

        payload = {
            'pg': pg,  # PG사의 Alias ex) danal, kcp, inicis 등
            'method': method,  # 'card', # 결제수단 Alias ex) card, phone, vbank, bank, easy 중 1개, 미적용시 통합결제창
            'methods': methods,  # ['card', 'phone'], # 결제수단 array, 통합결제창 사용시 활성화된 결제수단 중 사용할 method array 지정
            'price': price,  # 결제할 상품금액
            'order_id': order_id,  # 개발사에서 지정하는 고유주문번호
            'params': params,  # 전달할 string, 결제 후 다시 되돌려 줌, json string 형태로 활용해도 무방
            'tax_free': tax_free,  # 면세 상품일 경우 해당만큼의 금액을 설정
            'name': name,  # 상품명
            'user_info': user_info,  # 구매자 정보, 특정 PG사의 경우 구매자 휴대폰 번호를 필수로 받는다
            'extra': extra,  # 기타 옵션
            'items': items  # 구매할 상품정보, 통계용
        }

        return requests.post(self.api_url(['request', 'payment.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    # 7. 서버 승인 요청
    def submit(self, receipt_id):
        payload = {
            'receipt_id': receipt_id
        }
        return requests.post(self.api_url(['submit.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    # 8. 본인 인증 결과 검증
    def certificate(self, receipt_id):
        return requests.get(self.api_url(['certificate', receipt_id]), headers={
            'Authorization': self.token
        }).json()

    # deprecated
    def remote_link(self, payload={}, sms_payload=None):
        if sms_payload is None:
            sms_payload = {}
        payload['sms_payload'] = sms_payload
        return requests.post(self.api_url(['app', 'rest', 'remote_link.json']), data=payload).json()

    # deprecated 
    def remote_form(self, remoter_form, sms_payload=None):
        if sms_payload is None:
            sms_payload = {}
        payload = {
            'application_id': self.application_id,
            'remote_form': remoter_form,
            'sms_payload': sms_payload
        }
        return requests.post(self.api_url(['app', 'rest', 'remote_form.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    # deprecated 
    def send_sms(self, receive_numbers, message, send_number=None, extra={}):
        payload = {
            'data': {
                'sp': send_number,
                'rps': receive_numbers,
                'msg': message,
                'm_id': extra['m_id'],
                'o_id': extra['o_id']
            }
        }
        return requests.post(self.api_url(['push', 'sms.json']), data=payload, headers={
            'Authorization': self.token
        }).json()

    # deprecated 
    def send_lms(self, receive_numbers, message, subject, send_number=None, extra={}):
        payload = {
            'data': {
                'sp': send_number,
                'rps': receive_numbers,
                'msg': message,
                'sj': subject,
                'm_id': extra['m_id'],
                'o_id': extra['o_id']
            }
        }
        return requests.post(self.api_url(['push', 'lms.json']), data=payload, headers={
            'Authorization': self.token
        }).json()
