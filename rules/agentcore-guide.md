# AgentCore 배포 가이드

### 4단계: AgentCore 변환
- `@awslabs.aws-documentation-mcp-server/*` - "bedrock agentcore deployment" 검색
- `@awslabs.code-doc-gen-mcp-server/*` - AWS 공식 저장소의 "bedrock agentcore" 관련 코드 검색
- `fs_read` - 원본 코드 읽기
- 수집된 정보 기반으로 AgentCore 형태로 변환
- `fs_write` - 변환된 코드 저장

#### 변환 규칙 (필수 준수)
**원본 Strands 코드를 AgentCore 형식으로 변환:**
- **원본 Agent 로직은 100% 유지** (중요!)
- `from strands import Agent` 그대로 유지
- `use_aws` 등 기존 도구들 그대로 사용 (boto3로 변환 금지)
- `BedrockAgentCoreApp()` 래퍼만 추가
- `@app.entrypoint` 데코레이터 추가
- **if __name__ == "__main__": 블록 교체** (중요!)
  - 원본: input() 함수로 대화형 테스트
  - AgentCore: app.run()으로 서버 모드 변경

**AgentCore if __name__ == "__main__": 블록:**
```python
if __name__ == "__main__":
    app.run()
```

#### 변환 예시
```python
# 원본 Strands
from strands import Agent
from strands_tools import use_aws

agent = Agent(model="claude-sonnet-4", tools=[use_aws])

# AgentCore 변환 (올바른 방법)
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands_tools import use_aws  # ← 그대로 유지!

app = BedrockAgentCoreApp()
agent = Agent(model="claude-sonnet-4", tools=[use_aws])  # ← 원본 유지!

@app.entrypoint
def agent_invocation(payload, context):
    user_message = payload.get("prompt", "기본 질문")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
```

**참고:** AWS 공식 문서 "Use any agent framework - Strands Agents" 섹션에서도 동일한 패턴 확인 가능

### 5단계: AgentCore 배포 (MCP + execute_bash 조합)
- `@ki.aws-strands-agentcore-venv-mcp-server/prepare_agentcore_environment` - AgentCore 배포 환경 준비
- `execute_bash` - agentcore configure 실시간 실행
- `execute_bash` - agentcore launch 실시간 실행  
- `execute_bash` - agentcore invoke 테스트 (실시간 피드백)

**AgentCore 테스트 명령어:**
```bash
cd ~/[agent-name]-agent && /root/.ki.aws-strands-agentcore-venv/bin/agentcore invoke '{"prompt": "테스트 질문"}'
```

**예시:**
```bash
cd ~/s3_bucket_query-agent && /root/.ki.aws-strands-agentcore-venv/bin/agentcore invoke '{"prompt": "S3 버킷 목록 조회해줘"}'
```

#### 권한 관리 워크플로우
**AgentCore는 기본 권한만으로 배포됩니다. 추가 AWS 서비스 권한은 테스트 후 필요시 추가:**

1. **첫 테스트 실행** - 권한 부족 오류 발생 가능
2. **오류 분석** - 필요한 AWS 서비스 및 권한 식별  
3. **IAM 정책 추가** - `aws iam attach-role-policy` 명령으로 필요한 권한만 추가
4. **재테스트** - 권한 추가 후 정상 동작 확인

**⚠️ 중요:** 최소 권한 원칙에 따라 실제 필요한 권한만 추가하세요.

## 단계별 확인 절차

각 단계 완료 후:
1. 결과를 마크다운으로 정리해서 보고
2. "다음 단계를 진행하시겠습니까?" 명시적으로 질문
3. 사용자 승인 후 다음 단계 진행
4. 실시간 실행 시 "지금 실시간으로 실행 중입니다" 안내
