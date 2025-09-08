# FastAPI-practice

## Project setup

```bash
uv init
uv venv --python 3.11.10
uv sync
```

## 커밋 단계별 설명

#### 1. 기본 CRUD

- todo를 기반으로 CRUD를 구현.
- schemas(dto), services, apis로 구분함으로서 MVC 패턴을 따름.
- 3요소를 명확하게 구분함. apis에서는 services의 의존성을 명시적으로 주입함.

#### 2. 타입/입력 값 규칙 검증

- pydantic을 통한 입력값 검증을 수행함.
- 크게 두 가지 방법으로 검증을 수행할 수 있음.
  - CreateTodoInput 예제: 각각의 schemas에서 필드 단위로 검증
  - UpdateTodoInput 예제: root_validator를 통한 객체 단위로 검증

#### 3. (복습) User CRUD

- user를 기반으로 CRUD를 구현하며 복습함.
- user의 password는 해싱하여 저장하며 기본적으로 사용자에게 반환하지 않음.

#### 4. 예외 처리

- HttpException을 통한 직접적인 예외처리를 CustomException과 전역 예외 핸들러로 처리함.

#### 5. Logging

- print문이 아닌 logging 모듈을 통한 로그 관리.

#### 6. env/JWT

- 환경변수 관리를 위한 env 설정
- JWT를 통한 인증 구현.
  - Router 단위의 인증과 각 endpoint 단위의 인증 구현.
  - Cookie를 통한 인증 구현이 대세이지만, 빠른 구현을 위해 Bearer를 통한 인증 구현.

#### 7. DB 연동

- SQLite + SQLAlchemy를 통한 DB 연동.
- DB Session 관리를 위한 Dependency Injection 구현.

#### 8. Static file 처리

- Static file을 제공하기 위한 FastAPI의 StaticFiles 사용법.

#### 9. ML 연동

- FastAPI와 ML 모델 연동 실습.
- 사전 학습된 RandomForest 모델로 업로드 받은 이미지 분류.

## 앞으로의 TODO

- AWS EC2 배포
- AWS S3 연동
- DB 호스팅. 필요시 AWS RDS 사용
- Dockerization
- AWS에 GPU를 요구하는 무거운 ML 모델 배포
