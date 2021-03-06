# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\xing\xacom.py
# Compiled at: 2016-03-01 17:38:00
# Size of source mod 2**32: 9249 bytes
from datetime import datetime, timedelta
import math, pandas

def parseErrorCode(code):
    """에러코드 메시지

        :param code: 에러 코드
        :type code: str
        :return: 에러코드 메시지를 반환

        ::

            parseErrorCode("00310") # 모의투자 조회가 완료되었습니다
    """
    code = str(code)
    ht = {'-1': '통신소켓 생성에 실패하였습니다', 
     '-2': '서버접속에 실패하였습니다', 
     '-3': '서버주소가 틀렸습니다', 
     '-4': '서버 접속시간이 초과되었습니다', 
     '-5': '이미 서버에 연결중입니다', 
     '-6': '해당TR은 사용할수 없습니다', 
     '-7': '로그인을 해야 사용이 가능합니다', 
     '-8': '시세전용에서는 사용이 불가능합니다', 
     '-9': '해당 계좌번호를 가지고 있지 않습니다', 
     '-10': '패킷의 크기가 잘못되었습니다', 
     '-11': 'Data의 크기가 다릅니다', 
     '-12': '계좌가 존재하지 않습니다', 
     '-13': 'Request ID 부족', 
     '-14': '소켓이 생성되지 않았습니다', 
     '-15': '암호화 생성에 실패했습니다', 
     '-16': '데이터 전송에 실패했습니다', 
     '-17': '암호화(RTN)처리에 실패했습니다', 
     '-18': '공인인증 파일이 없습니다', 
     '-19': '공인인증 Function이 없습니다', 
     '-20': '메모리가 충분하지 않습니다', 
     '-21': 'TR의 시간당 전송제한에 걸렸습니다', 
     '-22': '해당 TR은 해당 함수를 이용할 수 없습니다', 
     '-23': '로그인이 안되었거나, TR에 대한 정보를 찾을 수 없습니다', 
     '-24': '계좌위치가 지정되지 않았습니다', 
     '-25': '계좌를 가지고 있지 않습니다', 
     '-26': '파일 읽기에 실패했습니다 (종목 검색 조회 시, 파일이 없는 경우)', 
     '0000': '정상완료되었습니다', 
     '00310': '모의투자 조회가 완료되었습니다', 
     '00136': '조회가 완료되었습니다', 
     '00020': 'application program exit[TR:CSPAQ]', 
     '03669': '비밀번호 오류입니다. (5회중 4회 남았습니다)', 
     '01796': '비밀번호 연속 오류허용횟수를 초과하였습니다. 콜센터로 문의하시기 바랍니다'}
    if code in ht:
        return ht[code] + ' (%s)' % code
    return code


def parseTR(trCode):
    """요청 TR 코드 파싱

        :param trCode: TR 코드
        :type trCode: str
        :return: TR코드 내역을 반환

        ::

            parseTR("t0425") # 주식체결/미체결
    """
    ht = {'t0424': '주식잔고', 
     't0425': '주식체결/미체결', 
     't8407': '멀티현재가조회', 
     't8412': '주식챠트(N분)', 
     't8413': '주식챠트(일주월)', 
     't8430': '주식종목조회', 
     't1833': '종목검색(씽API용)', 
     't1101': '주식현재가호가조회', 
     't1102': '주식현재가(시세)조회', 
     't1411': '증거금율별종목조회', 
     't1702': '외인기관종목별동향', 
     't1301': '주식시간대별체결조회', 
     't0167': '서버시간조회', 
     't9945': '주식마스터조회API용', 
     'CSPAQ12200': '현물계좌예수금 주문가능금액 총평가 조회', 
     'CSPAT00600': '현물주문', 
     'CSPAT00700': '현물정정주문', 
     'CSPAT00800': '현물취소주문', 
     'CSPBQ00200': '현물계좌 증거금률별 주문가능 수량 조회', 
     'HA_': 'KOSDAQ호가잔량', 
     'H1_': 'KOSPI호가잔량', 
     'SC0': '주식주문접수', 
     'SC1': '주식주문체결', 
     'SC2': '주식주문정정', 
     'SC3': '주식주문취소', 
     'SC4': '주식주문거부', 
     'JIF': '장운영정보'}
    if trCode in ht:
        return ht[trCode]
    return ''


def parseJstatus(jstatus):
    """장 운영시간 파싱

        :param jstatus: 장 운영시간 코드
        :type jstatus: str
        :return: 장 운영시간 내역을 반환

        ::

            parseJstatus("66") # 사이드카 매수발동

        .. note::

            - 코스피로 장시간을 확인해야함.
            - 선물/옵션 장마감 5분전, 1분전, 10초전은 들어오지 않음
    """
    ht = {'11': '장전동시호가개시', 
     '21': '장시작', 
     '22': '장개시10초전', 
     '23': '장개시1분전', 
     '24': '장개시5분전', 
     '25': '장개시10분전', 
     '31': '장후동시호가개시', 
     '41': '장마감', 
     '42': '장마감10초전', 
     '43': '장마감1분전', 
     '44': '장마감5분전', 
     '51': '시간외종가매매개시', 
     '52': '시간외종가매매종료', 
     '53': '시간외단일가매매개시', 
     '54': '시간외단일가매매종료', 
     '61': '서킷브레이크발동', 
     '62': '서킷브레이크해제', 
     '63': '서킷브레이크단일가접수', 
     '64': '사이드카 매도발동', 
     '65': '사이드카 매도해제', 
     '66': '사이드카 매수발동'}
    if jstatus in ht:
        return ht[jstatus]
    return ''


def parseMarket(jangubun):
    """장 구분

        :param jangubun: 시장 구분 코드
        :type jangubun: str
        :return: 시장 내역을 반환

        ::

            parseMarket("1") # 코스피
    """
    ht = {'1': '코스피', 
     '2': '코스닥', 
     '5': '선물/옵션', 
     '7': 'CME야간선물', 
     '8': 'EUREX야간옵션선물'}
    if jangubun in ht:
        return ht[jangubun]
    return ''


def timeType(base=None):
    """장 전,후 시간을 반환

                :param base: 기준일시
                :type base: datetime
                :return: 기준일시에 맞는 타입문자를 반환

                        BEFORE(장시작 전),SHOWTIME(장 운영시간),AFTER(장종료 후)

                ::

                        timeType()
                        timeType(datetime.today())
        """
    today = base if base else datetime.today()
    mainStart = today.replace(hour=8, minute=50, second=0, microsecond=0)
    mainEnd = today.replace(hour=15, minute=0, second=0, microsecond=0)
    if today.weekday() < 5:
        if today >= mainStart and today <= mainEnd:
            return 'SHOWTIME'
        if today < mainStart:
            return 'BEFORE'
        if today > mainEnd:
            return 'AFTER'
    else:
        return 'NONE'


def today():
    """오늘 날자를 yyyymmdd 형태로 반환

                ::

                        today() # 20160101
        """
    return datetime.today().strftime('%Y%m%d')


def latestBusinessDay():
    """가장 최근 영업일을 yyyymmdd 형태로 반환

                ::

                        latestBusinessDay()     # 20160104
        """
    baseday = datetime.today()
    if baseday.weekday() > 4:
        while baseday.weekday() > 4:
            baseday = baseday - timedelta(days=1)

    return baseday.strftime('%Y%m%d')