# Strands Agent 개발 가이드

## MCP + execute_bash 조합 원칙
- **MCP 서버**: 자체 가상환경에서 Agent 실행 환경 제공
- **execute_bash**: 실제 실행 담당 (실시간 피드백 제공)
- **수동 단계별 진행**: 각 단계마다 사용자 승인 필요
- **MCP 서버 가상환경 사용**: Agent 디렉토리별 가상환경 생성하지 않음

## MCP 도구 활용 방법

### 1단계: 필수 MCP 워크플로우 (모든 도구 사용 필수)
- `@strands/search_docs` - **Strands 프레임워크** 도구, 사용법, 코드 패턴, 구현 예제, **Strands 에러 처리** 검색 **[필수]**
- `@strands/fetch_doc` - 검색된 **Strands 도구들**의 상세 문서, 완전한 코드 예제, 파라미터 설명, 실제 구현 방법 읽기 **[필수]**
- `@awslabs.aws-documentation-mcp-server/*` - 사용자 요구사항에 맞는 **AWS 서비스**의 사용법, API 호출 방법, 권한 설정, 모범 사례, **AWS 오류 처리** 확인 **[필수]**
- `@awslabs.aws-api-mcp-server/*` - 사용자 요구사항 구현에 필요한 **AWS CLI 명령어** 및 API 호출 방법 파악 **[필수]**
- `@awslabs.code-doc-gen-mcp-server/*` - **AWS 공식 저장소**의 Strands Agent 또는 AgentCore 예제 코드, AWS 통합 구조, 배포 패턴, **실제 예외 처리 구현** 분석 **[필수]**

**⚠️ 중요: 위 5개 MCP 도구를 모두 순차적으로 사용하지 않으면 2단계 진행 금지**

### 2단계: 코드 생성
- `fs_write` - Strands Agent 코드 생성
- 환경변수 `AWS_DEFAULT_REGION=us-east-1` 필수 설정
- 마크다운 출력 형식 적용

#### 필수 코드 구조
**모든 Agent 코드 구성:**
1. test_agent() 함수 포함
2. if __name__ == "__main__": 블록에서 실제 작업 수행

**if __name__ == "__main__": 블록 예시:**
```python
if __name__ == "__main__":
    test_agent()
```

### 3단계: 로컬 테스트 (MCP + execute_bash 조합)
**테스트 실행 방식:**
- 로컬 테스트: MCP 가상환경에서 test_agent() 함수 호출

**테스트 실행 명령어:**
```bash
cd ~/[agent-name]-agent && /root/.ki.aws-strands-agentcore-venv/bin/python -c "from [agent-name] import test_agent; test_agent()"
```

**예시:**
```bash
cd ~/iam_role_analyzer-agent && /root/.ki.aws-strands-agentcore-venv/bin/python -c "from iam_role_analyzer import test_agent; test_agent()"
```

## Strands 코드 패턴 탐색 방법론

### 기본 Agent 패턴 분석
#### Agent 초기화 패턴
```python
from strands import Agent
from strands_tools import use_aws

# 기본 초기화
agent = Agent(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    tools=[use_aws],
    system_prompt="시스템 프롬프트"
)

# 고급 초기화 (상태 관리, 세션 관리 포함)
agent = Agent(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    tools=[use_aws],
    system_prompt="시스템 프롬프트",
    conversation_manager=SlidingWindowConversationManager(),
    state=AgentState({"key": "value"}),
    session_manager=session_manager
)
```

#### 도구 연결 패턴
```python
# 단일 도구
agent = Agent(tools=[use_aws])

# 다중 도구
agent = Agent(tools=[use_aws, calculator, search_tool])

# 도구 직접 호출
result = agent.tool.use_aws(service="s3", operation="list-buckets")
```

#### 응답 처리 패턴
```python
# 기본 호출
result = agent("질문")
print(result.message)

# 스트리밍 처리
async for event in agent.stream_async("질문"):
    if "data" in event:
        print(event["data"])

# 구조화된 출력
from pydantic import BaseModel

class Response(BaseModel):
    answer: str
    confidence: float

structured_result = agent.structured_output(Response, "질문")
```

### 에러 처리 패턴
#### Agent Loop 예외 처리
```python
from strands.exceptions import MaxTokensReachedException, ContextWindowOverflowException

try:
    result = agent("복잡한 질문")
except MaxTokensReachedException:
    # 토큰 한계 도달 시 처리
    print("응답이 너무 길어 중단되었습니다.")
except ContextWindowOverflowException:
    # 컨텍스트 윈도우 초과 시 처리
    print("대화 컨텍스트가 너무 깁니다.")
```

#### 도구 실행 예외 처리
```python
try:
    result = agent.tool.use_aws(service="s3", operation="list-buckets")
except Exception as e:
    print(f"도구 실행 오류: {e}")
    # 대체 로직 실행
```

#### 모델 호출 예외 처리
```python
from strands.models import BedrockModel

try:
    model = BedrockModel(model_id="claude-3-sonnet")
    agent = Agent(model=model)
    result = agent("질문")
except Exception as e:
    print(f"모델 호출 오류: {e}")
    # 대체 모델 사용
```

### 환경 설정 패턴
#### 환경변수 설정
```python
import os

# AWS 리전 설정
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# 모델 설정
os.environ['BEDROCK_MODEL_ID'] = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
```

#### 모델 설정 패턴
```python
# 기본 Bedrock 모델
agent = Agent(model="us.anthropic.claude-sonnet-4-20250514-v1:0")

# 커스텀 모델 설정
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region="us-east-1"
)
agent = Agent(model=model)
```

#### 대화 관리 패턴
```python
from strands.agent.conversation_manager import (
    SlidingWindowConversationManager,
    SummarizingConversationManager,
    NullConversationManager
)

# 슬라이딩 윈도우 (기본)
agent = Agent(
    conversation_manager=SlidingWindowConversationManager(window_size=40)
)

# 요약 기반 관리
agent = Agent(
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.3,
        preserve_recent_messages=10
    )
)

# 관리 없음
agent = Agent(
    conversation_manager=NullConversationManager()
)
```

### 고급 패턴
#### 상태 관리 패턴
```python
from strands.agent.state import AgentState

# 상태 초기화
state = AgentState({"user_id": "123", "session": "abc"})
agent = Agent(state=state)

# 상태 조작
agent.state.set("key", "value")
value = agent.state.get("key")
agent.state.delete("key")
```

#### 멀티모달 처리 패턴
```python
# 이미지 포함 메시지
message = [
    {"text": "이 이미지를 분석해주세요"},
    {"image": {"source": {"bytes": image_bytes}}}
]
result = agent(message)
```

#### 도구 조합 패턴
```python
# 조건부 도구 사용
if user_needs_calculation:
    agent = Agent(tools=[calculator, use_aws])
else:
    agent = Agent(tools=[use_aws])

# 동적 도구 추가
agent.tool_registry.process_tools([new_tool])
```

## 개발 표준

### 파일명 규칙
- 영어 소문자 사용
- 언더스코어(_) 사용, **하이픈(-) 절대 금지**
- 예: `s3_bucket_query.py`

### 디렉토리 구조
```
~/[agent-name]-agent/
├── [agent-name].py
└── requirements.txt
```

### requirements.txt 내용 (필수)
```
strands-agents
strands-agents-tools
bedrock-agentcore
```

### 환경변수 설정
```python
import os
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
```

### 기본 모델 설정
- **기본 모델**: `us.anthropic.claude-sonnet-4-20250514-v1:0`
- **기본 도구**: `use_aws` (AWS 서비스용 Agent이므로 기본 포함)
- **추가 도구**: 사용자 요구사항에 따라 `@strands/*` MCP에서 탐색한 적절한 도구들 선택

### 마크다운 출력 형식
```markdown
## 📊 [서비스명] 조회 결과

### 현재 상태
- 주요 정보

### 💡 권장사항
- 제안사항

### 📝 참고 정보
- 추가 정보
```
