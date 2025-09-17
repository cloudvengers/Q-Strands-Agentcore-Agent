# 최종 답변 가이드

## 🎉 최종 답변 형식 (모든 작업 완료 시)

작업 완료 시 다음 형식으로 체계적으로 정리하여 답변:

### ✅ 전체 작업 완료 요약
- 주요 달성 사항 요약

### 📊 최종 결과

#### 🎯 생성된 파일들
- 구체적인 파일명과 용도

#### 🚀 배포된 Agent 정보 (해당 시)
- Agent ARN, 상태, 기능 등

#### 🔧 주요 특징
- 핵심 기능과 장점들

#### 💡 사용 방법
Q CLI Agent에게 다음과 같이 요청하세요:
"배포된 [Agent명]을 호출해서 [원하는 작업]을 해주세요"

예시: "배포된 S3 버킷 조회 Agent를 호출해서 S3 버킷 목록을 조회해주세요"

## 📋 추가 옵션

**사용자에게 질문:**
"Bedrock AgentCore 직접 사용법도 알려드릴까요?"

**사용자가 원할 경우에만 제공:**

### 🔧 Bedrock AgentCore 직접 사용법

#### 1. Starter Toolkit 명령어
```bash
# Agent 호출
agentcore invoke '{"prompt": "원하는 질문"}'

# Agent 상태 확인
agentcore status

# 로그 확인
agentcore logs
```

#### 2. AWS SDK (Python)
```python
import boto3
import json

agent_core_client = boto3.client('bedrock-agentcore')
payload = json.dumps({"prompt": "원하는 질문"}).encode()

response = agent_core_client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:...",
    runtimeSessionId="session-id",
    payload=payload
)
```

#### 3. AWS CLI
```bash
# Agent 호출
aws bedrock-agentcore invoke-agent-runtime \
  --agent-runtime-arn "arn:aws:bedrock-agentcore:..." \
  --payload '{"prompt": "원하는 질문"}'

# Agent 목록 조회
aws bedrock-agentcore list-actors
```

#### 4. HTTP API 직접 호출
```bash
curl -X POST https://agent-endpoint/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "원하는 질문"}'
```

#### 주의사항
- **권한**: `bedrock-agentcore:InvokeAgentRuntime` 필요
- **페이로드**: JSON 형식, 최대 100MB
- **응답**: 스트리밍 방식으로 실시간 반환
- **세션**: `runtimeSessionId`로 대화 컨텍스트 유지 가능
