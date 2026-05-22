# 🎰 Django Lotto System (웹 기반 로또 서비스)

Django 프레임워크와 Docker 멀티 컨테이너 아키텍처를 기반으로 구현한 안전하고 편리한 웹 로또 시스템입니다. 일반 사용자의 티켓 구매부터 시스템 관리자의 실시간 난수 추첨까지 로또 발행의 전체 라이프사이클을 제공합니다.

<br>

## 🛠️ Tech Stack (기술 스택)
* **Backend:** Python 3.11, Django
* **Frontend:** HTML5, Bootstrap 5
* **Database:** SQLite3
* **Infrastructure:** Docker, Docker Compose, Nginx, Gunicorn

<br>

## ✨ Key Features (제공 기능)

### 🙍‍♂️ 1. 일반 사용자 (General User)
* **회원가입 및 인증:** 사용자 경험(UX)을 고려한 회원가입 즉시 자동 로그인(Auto-Login) 기능
* **복권 구매:** 수동 번호 직접 선택 및 자동 번호 발급 기능 제공
* **당첨 확인:** 본인이 구매한 복권 내역 조회 및 실시간 당첨 여부 확인

### 👨‍💻 2. 시스템 관리자 (Administrator)
* **판매 내역 모니터링:** 플랫폼 내에서 발행된 모든 유저의 복권 판매 내역 및 영수증 확인
* **회차 추첨 기능:** 관리자 권한 전용 [현재 회차 추첨하기] 기능을 통한 당첨 번호 및 보너스 번호 추첨
* **당첨 내역 확인:** 추첨 즉시 전체 구매 티켓의 당첨 등수(1등~5등, 낙첨) 판별 및 모니터링

### 🛡️ 3. 시스템 보안 (Security)
* **관리자 페이지 은닉:** 무차별 대입 공격 방지를 위해 기본 관리자 경로(`admin/`)를 특수 주소(`/secret-admin-access/`)로 변경
* **접근 제어 리다이렉트:** 비인가 사용자의 관리자 페이지 우회 접근 시 일반 사용자 로그인 창으로 강제 리다이렉트 처리

<br>

## 🐳 System Architecture (시스템 구조)

본 서비스는 가용성과 보안성을 높이기 위해 **Docker 멀티 컨테이너 환경(Multi-container)**으로 배포되었습니다.

1. **Nginx (Web Server):** 포트 80에서 외부 HTTP 요청을 수신하는 리버스 프록시(Reverse Proxy) 역할을 수행합니다.
2. **Django + Gunicorn (WAS):** 파이썬 웹 애플리케이션 코드를 실행하며, 내부망의 포트 8000번에서 대기합니다.
3. **네트워크 격리 (Isolated Network):** Nginx와 Django 컨테이너는 사용자 정의 브릿지 네트워크(`lotto-network`)로만 통신하며, 외부에서 WAS로 직접 타격하는 것을 물리적으로 차단합니다.
4. **데이터 영속성 (Volume Bind Mount):** 컨테이너가 재시작되거나 파괴되어도 데이터가 유실되지 않도록, 호스트 디렉토리의 `db.sqlite3`를 컨테이너와 마운트하여 데이터 영속성을 보장합니다.

<br>

## 🧑‍🎓 Developer
* **Name:** 임민욱
* **Contact:** (이메일 주소가 있다면 여기에 작성)
