# 파이썬 개발 환경이 준비된 기본 베이스 이미지 사용
FROM python:3.11-slim

# 필요한 패키지(장고, Gunicorn)를 설치하는 명령
RUN pip install django gunicorn

# 내 컴퓨터의 로또 소스코드를 컨테이너 내부(/opt/source-code)로 복사
COPY . /opt/source-code

# 컨테이너가 켜질 때 자동으로 장고 서버를 실행하는 명령
# (※ /opt/source-code 폴더 안에서 gunicorn을 실행해 줌)
ENTRYPOINT ["gunicorn", "--chdir", "/opt/source-code", "--bind", "0.0.0.0:8000", "mylottosite.wsgi:application"]
