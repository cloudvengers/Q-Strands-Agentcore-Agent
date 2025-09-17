# Ki AWS Strands AgentCore Virtual Environment MCP Server

AWS Strands Agent 개발 및 Bedrock AgentCore 배포를 위한 가상환경을 자동으로 관리하는 MCP 서버입니다.

## 🚀 주요 기능

- **자동 가상환경 생성**: MCP 서버 시작 시 필요한 패키지들이 설치된 가상환경 자동 생성
- **Agent 환경 준비**: Strands Agent 실행을 위한 환경 정보 제공  
- **AgentCore 환경 준비**: Bedrock AgentCore 배포를 위한 환경 설정

## 📦 설치 및 사용

### MCP 설정
```json
{
  "mcpServers": {
    "ki.aws-strands-agentcore-venv-mcp-server": {
      "command": "uvx",
      "args": [
        "ki-aws-strands-agentcore-venv-mcp-server@latest"
      ]
    }
  }
}
```

## 🛠️ 사용 가능한 도구

### 1. prepare_agent_environment
Agent 실행을 위한 환경 정보를 반환합니다.

**매개변수:**
- `agent_path`: Agent 파일이 있는 디렉토리 경로

**반환값:**
- 환경 상태, 메시지, Agent 경로, 가상환경 경로, Python 경로

### 2. prepare_agentcore_environment  
AgentCore 배포를 위한 환경을 준비합니다.

**매개변수:**
- `agent_path`: Agent 파일이 있는 디렉토리 경로

**반환값:**
- 환경 상태, 메시지, Agent 경로, 가상환경 경로, Python 경로, AgentCore 경로

## 📁 자동 설치되는 패키지

MCP 서버가 시작될 때 다음 패키지들이 자동으로 설치됩니다:

- `strands-agents`
- `strands-agents-tools`  
- `bedrock-agentcore`
- `bedrock-agentcore-starter-toolkit`

## 🔍 가상환경 위치

가상환경은 `~/.ki.aws-strands-agentcore-venv` 경로에 생성됩니다.

## 📝 버전 정보

- **현재 버전**: 0.1.9
- **Python 요구사항**: >= 3.8
