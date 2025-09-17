import os
from strands import Agent
from strands_tools import use_aws

# 환경변수 설정
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# 시스템 프롬프트 정의
SECURITY_SYSTEM_PROMPT = """당신은 AWS 보안 서비스 상태를 확인하는 전문 Agent입니다.

주요 기능:
1. AWS 보안 서비스들의 활성화/비활성화 상태 확인
2. us-east-1 리전에서만 조회
3. 마크다운 형식으로 결과 출력

확인 대상 보안 서비스:
- GuardDuty: 위협 탐지 서비스
- Security Hub: 중앙 집중식 보안 상태 관리
- Inspector: 취약점 스캔
- Macie: 민감 데이터 보안
- WAF: 웹 애플리케이션 방화벽
- Shield: DDoS 보호
- Config: 리소스 구성 관리
- CloudTrail: API 호출 로깅

출력 형식:
## 📊 AWS 보안 서비스 상태 (us-east-1)

### ✅ 활성화된 서비스
- 서비스명: 상태 설명

### ❌ 비활성화된 서비스  
- 서비스명: 상태 설명

### 💡 권장사항
- 보안 강화를 위한 제안사항

각 서비스 확인 시 적절한 AWS CLI 명령어를 사용하여 상태를 조회하세요.
"""

def test_agent():
    """Agent 테스트 함수"""
    try:
        # Agent 초기화
        agent = Agent(
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",
            tools=[use_aws],
            system_prompt=SECURITY_SYSTEM_PROMPT
        )
        
        # 테스트 질문
        test_query = "AWS 보안 서비스들의 활성화 상태를 확인해주세요."
        
        print("🔍 AWS 보안 서비스 상태 확인 Agent 테스트 시작...")
        print(f"📝 질문: {test_query}")
        print("=" * 50)
        
        # Agent 실행
        result = agent(test_query)
        
        print("📊 Agent 응답:")
        print(result.message)
        
        return result
        
    except Exception as e:
        print(f"❌ Agent 테스트 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    test_agent()
