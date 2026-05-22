# 🎰 Django Lotto System (웹 기반 로또 서비스)

Django 프레임워크와 Docker 멀티 컨테이너 아키텍처를 기반으로 구현한 안전하고 편리한 웹 로또 시스템입니다. 
일반 사용자의 티켓 구매부터 시스템 관리자의 실시간 난수 추첨까지 로또 발행의 전체 라이프사이클을 제공합니다.

<br>

## 🛠️ Tech Stack (기술 스택)
* **Backend:** Python 3.11, Django
* **Frontend:** HTML5, Bootstrap 5
* **Database:** SQLite3
* **Infrastructure:** Docker, Docker Compose, Nginx, Gunicorn

<br>

## ✨ Key Features (제공 기능)

### 🙍‍♂️ 1. 일반 사용자 (General User)
* **회원가입 및 인증:** UX를 고려하여 회원가입 즉시 자동 로그인(Auto-login) 처리
* **복권 구매:** * 🎲 **자동 발급:** `random.sample`을 이용한 중복 없는 난수 6개 자동 생성
  * ✍️ **수동 번호 선택:** 사용자가 직접 원하는 번호 6개 지정 가능
* **당첨 확인:** 본인이 구매한 복권 내역만 격리하여 조회하며, 추첨 완료 시 실시간으로 등수(1등~5등, 낙첨) 확인 가능

### 👨‍💻 2. 시스템 관리자 (Administrator)
* **판매 내역 모니터링:** 플랫폼 내에서 발행된 모든 유저의 복권 판매 내역 및 영수증 확인
* **회차 추첨 기능:** 시스템 관리자 권한으로만 접근 가능한 [현재 회차 추첨하기] 기능을 통해 공식 당첨 번호(6개) 및 보너스 번호(1개) 난수 추출
* **당첨 내역 확인:** 추첨 즉시 전체 구매 티켓의 당첨 여부를 판별하여 결과 모니터링

### 🛡️ 3. 시스템 보안 (Security)
* **관리자 페이지 은닉:** 무차별 대입 공격을 방지하기 위해 기본 관리자 경로(`admin/`)를 특수 주소(`/secret-admin-access/`)로 변경
* **접근 제어 리다이렉트:** 비인가 사용자가 은닉된 관리자 페이지로 우회 접근을 시도할 경우, 이를 차단하고 일반 사용자 로그인 창으로 강제 리다이렉트 처리

<br>

## 🐳 System Architecture (시스템 구조)

본 서비스는 가용성과 보안성을 높이기 위해 **Docker 멀티 컨테이너 환경(Multi-container)**으로 배포되었습니다.

1. **Nginx (Web Server):** * 포트 80에서 외부 HTTP 요청을 수신하는 리버스 프록시(Reverse Proxy) 역할을 수행합니다.
2. **Django + Gunicorn (WAS):** * 파이썬 웹 애플리케이션 코드를 실행하며, 내부망의 포트 8000번에서 대기합니다.
3. **네트워크 격리 (Isolated Network):** * Nginx와 Django 컨테이너는 사용자 정의 브릿지 네트워크(`lotto-network`)로만 통신하며, 외부에서 WAS로 직접 타격하는 것을 물리적으로 차단합니다.
4. **데이터 영속성 (Volume Bind Mount):** * 컨테이너가 재시작되거나 파괴되어도 데이터가 유실되지 않도록, 호스트 디렉토리의 `db.sqlite3`를 컨테이너와 마운트하여 데이터 영속성을 보장합니다.

<br>

## 🚀 How to Run (실행 방법)

Docker와 Docker Compose가 설치된 환경에서 아래 명령어를 통해 즉시 가동할 수 있습니다.

```bash
# 1. 저장소 클론
$git clone [https://github.com/minwook6/django-lotto.git$](https://github.com/minwook6/django-lotto.git$) cd django-lotto

# 2. 도커 컴포즈 빌드 및 백그라운드 실행
$ docker-compose up --build -d

# 3. 서비스 접속
# 웹 브라우저에서 아래 주소로 접속합니다.
http://localhost/
