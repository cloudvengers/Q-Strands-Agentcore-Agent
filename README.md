# Q-Strands-Agentcore-Agent

🚀 **AWS 서비스 전용 Agent 자동 개발 및 배포 시스템**

MCP로 환경 준비, execute_bash로 실시간 실행, Bedrock AgentCore 배포까지 완전 자동화

## 0. 들어가기에 앞서

### 사용 중인 MCP 서버

이 프로젝트는 6개의 MCP 서버를 연동하여 완전 자동화를 구현합니다:

| MCP 서버 | 역할 |
|---------|------|
| `awslabs.core-mcp-server` | 명령 이해 및 분석 |
| `strands` | Strands 프레임워크 지원 |
| `awslabs.aws-api-mcp-server` | AWS CLI 명령어 |
| `awslabs.aws-documentation-mcp-server` | AWS 문서 검색 |
| `awslabs.code-doc-gen-mcp-server` | 코드 예제 분석 |
| `ki.aws-strands-agentcore-venv-mcp-server` | 배포 환경 준비 |

### Ki AWS Strands AgentCore Virtual Environment MCP Server

`ki.aws-strands-agentcore-venv-mcp-server`는 이 프로젝트를 위해 특별히 개발된 MCP 서버입니다:

**🚀 주요 기능:**
- **자동 가상환경 생성**: 필요한 패키지들이 설치된 가상환경 자동 생성
- **Agent 환경 준비**: Strands Agent 실행을 위한 환경 정보 제공  
- **AgentCore 환경 준비**: Bedrock AgentCore 배포를 위한 환경 설정

**🛠️ 사용 가능한 도구:**
- `prepare_agent_environment`: Agent 실행 환경 정보 반환
- `prepare_agentcore_environment`: AgentCore 배포 환경 준비

**📦 자동 설치 패키지:**
- `strands-agents`
- `strands-agents-tools`  
- `bedrock-agentcore`
- `bedrock-agentcore-starter-toolkit`

**🔍 가상환경 위치:** `~/.ki.aws-strands-agentcore-venv`

**⚠️ 요구사항:** uvx 설치 필요 (`pip install uvx`)

### Q CLI Agent의 Global 설정

이 Agent는 **글로벌 Agent**로 설정되어 있습니다:

- **위치**: `~/.aws/amazonq/cli-agents/Q-Strands-Agentcore-Agent.json`
- **범위**: 어느 디렉토리에서든 사용 가능
- **용도**: AWS 서비스 전용 Agent 개발 및 배포 전문 도구

### Q CLI 요구사항

- **버전**: Q CLI 1.15.0 이상 필요
- **실험 기능**: 다음 4개 experiment 기능을 모두 활성화해야 합니다
  - Knowledge [ON] - 지속적인 컨텍스트 저장 및 검색 (/knowledge)
  - Thinking [ON] - 단계별 사고 과정을 통한 복잡한 추론
  - Tangent Mode [ON] - 격리된 대화를 위한 임시 모드 (/tangent)
  - Todo Lists [ON] - TODO 리스트 생성 및 관리 (/todo)

### Rules 파일 구조

Agent가 참조하는 가이드 파일들은 다음 위치에 있습니다:

```
/root/.aws/amazonq/rules/
├── strands-agent-guide.md     # Strands Agent 개발 가이드 (1-3단계)
├── agentcore-guide.md         # AgentCore 배포 가이드 (4-5단계)
└── final-response-guide.md    # 최종 답변 형식 가이드
```

### 전체 요구사항 정리

이 프로젝트를 사용하기 위해 다음 사항들이 필요합니다:

**필수 설치:**
- Q CLI 1.15.0 이상
- uvx (`pip install uvx`)

**필수 설정:**
- 4개 experiment 기능 모두 활성화 (Knowledge, Thinking, Tangent Mode, Todo Lists)
- Agent 파일을 글로벌 위치에 배치 (`~/.aws/amazonq/cli-agents/`)

## 1. 프로젝트 상세 소개

### 개요

Q-Strands-Agentcore-Agent는 **Strands Agent 프레임워크**를 사용하여 **AWS 서비스를 활용하는 Agent**를 개발하고, 이를 **Bedrock AgentCore**로 배포하는 완전 자동화 시스템입니다.

### 핵심 개념

- **Strands Agent**: AWS에서 개발한 Agent 프레임워크로, AWS 서비스와의 통합이 최적화되어 있음
- **AWS 서비스 통합**: `use_aws` 도구를 통해 S3, EC2, Lambda 등 모든 AWS 서비스에 접근 가능
- **Bedrock AgentCore**: 개발된 Agent를 AWS 클라우드에 배포하여 서비스화하는 플랫폼

### 주요 특징

- **AWS 서비스 전용**: S3, EC2, RDS, Lambda 등 AWS 서비스를 활용하는 Agent 개발에 특화
- **완전 자동화**: MCP + execute_bash 조합으로 개발부터 배포까지 전체 워크플로우 자동화
- **단계별 승인**: 모든 단계마다 사용자 승인 필수로 안전한 진행
- **실시간 피드백**: execute_bash로 실시간 실행 상황 모니터링
- **6개 MCP 서버 연동**: AWS 생태계 완전 지원
- **한국어 지원**: 모든 응답과 가이드가 한국어로 제공

### 개발 가능한 Agent 예시

- **S3 관리 Agent**: 버킷 생성, 파일 업로드/다운로드, 권한 관리
- **EC2 모니터링 Agent**: 인스턴스 상태 확인, 성능 메트릭 조회
- **Lambda 배포 Agent**: 함수 생성, 업데이트, 로그 분석
- **RDS 관리 Agent**: 데이터베이스 상태 확인, 백업 관리
- **IAM 보안 Agent**: 권한 분석, 정책 검토, 보안 감사

## 2. 작업 흐름

### 1단계: 요구사항 분석
사용자가 원하는 AWS 서비스 Agent의 기능과 목적을 파악합니다.

### 2단계: 사용자 확인
분석한 내용을 정리하여 보고하고 사용자 승인을 받습니다.

### 3단계: Strands Agent 개발
- AWS 서비스 연동을 위한 Strands Agent 코드 자동 생성
- 로컬 환경에서 테스트 실행
- 정상 동작 확인

### 4단계: AgentCore 배포
- Strands Agent를 Bedrock AgentCore 형식으로 변환
- AWS 클라우드에 자동 배포
- 배포된 Agent 테스트 및 검증

### 5단계: 결과 제공
- 생성된 Agent 파일 정보
- 배포된 Agent 접근 방법
- 사용법 및 예시 제공

## 3. 설치 및 설정

### Agent 설치

1. **저장소 클론**
```bash
git clone https://github.com/cloudvengers/Q-Developer-CLI-Strands_Agentcore-Agent.git
cd Q-Developer-CLI-Strands_Agentcore-Agent
```

2. **글로벌 위치에 배치**
```bash
# 디렉토리 생성
mkdir -p ~/.aws/amazonq/cli-agents
mkdir -p ~/.aws/amazonq/rules

# Agent 파일 복사
cp Q-Strands-Agentcore-Agent.json ~/.aws/amazonq/cli-agents/

# Rules 파일들 복사
cp rules/*.md ~/.aws/amazonq/rules/
```

### Agent 활성화

```bash
# cli-agents 폴더로 이동
cd ~/.aws/amazonq/cli-agents

# Agent와 함께 Q CLI 실행
q chat --agent Q-Strands-Agentcore-Agent
```
