# CosmosX-NASA

**Team GAsP**, the Gap Analysis System for Space Biology Publications. From keyword to hypothesis in seconds.

### Demonstration video

- **Demonstration**: https://tangerine-licorice-c439e6.netlify.app/
- **Presentation**: https://docs.google.com/presentation/d/1FlGfohdK5_PTNShhhBPBwXhRDZfBd4FB/edit?amp%3Bouid=109074628458883513610&amp%3Bamp%3Brtpof=true&amp%3Bamp%3Bsd=true&amp%3Bslide=id.p5&slide=id.p5#slide=id.p5

### Repositories

- **Backend**: https://github.com/CosmosX-NASA/cosmosx-backend
- **Frontend**: https://github.com/CosmosX-NASA/cosmosx-frontend
- **AI & Data processing**: https://github.com/CosmosX-NASA/cosmosx-ai

GAsP is designed to generate testable hypotheses in seconds. It retrieves up to five papers from NASA Space Biology publications, extracts key summary information and research gaps, and then automatically generates a clear, actionable hypothesis. 1) AI-powered Search & Summarization GAsP leverages LLMs to accelerate literature exploration through retrieval and intelligent summarization, delivering true speed. Each paper is summarized across eight structured categories, including data, methodology, conditions, models, and results, enabling researchers to quickly grasp the core content. 2) LLM-based Research Gap Generation The system automatically identifies research gaps based on predefined agents (Methodological Analyst, Conceptual Analyst, Experimental Analyst), uncovering gaps that human researchers might overlook. 3) LLM-based Hypothesis Generation Selected research gaps are transformed into concrete, testable hypotheses, ready for experimental design. GAsP drastically reduces the time required for hypothesis generation. While conventional methods can take over nine hours, GAsP enables researchers to complete the process in just a few minutes. This efficiency allows scientists to focus more on experimental work and analysis, moving seamlessly from keywords to Hypotheses, and accelerating the overall research process.

>P.S. This README was created after the competition for the purpose of the GitHub entry. The commit history confirms that no other content has been modified.


---

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
