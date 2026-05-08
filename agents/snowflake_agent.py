"""Snowflake Agent SDK - Snowflake Cortex AI content."""

from typing import Optional
import os

from agents.base_agent import BaseAgent, ContentRequest, ContentResult
from core.llm_client import LLMClient, LLMConfig


class SnowflakeAgent(BaseAgent):
    """Snowflake Cortex AI specialist.
    
    Capabilities:
    - SQL query generation
    - Data analysis
    - ML model inference
    - Document AI
    - Time series forecasting
    
    Tools: SnowSQL, Cortex LLM, Cortex Embeddings, Document AI
    Skills: sql, data-analysis, ml-inference, snowpark
    """
    
    def __init__(
        self,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        super().__init__(
            agent_id="snowflake-writer",
            name="Snowflake Cortex Writer",
            description="Snowflake - SQL, ML inference, data analysis",
            capabilities=[
                "sql_generation",
                "data_analysis",
                "ml_inference",
                "document_ai",
                "forecasting",
            ],
            skills=["sql", "snowpark", "data-analysis", "ml-inference"],
            api_key=password or os.getenv("SNOWFLAKE_PASSWORD"),
        )
        
        self.account = account or os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = user or os.getenv("SNOWFLAKE_USER")
        self.llm_config = LLMConfig.from_env()
        self._llm = None
    
    def _get_port(self) -> int:
        return 8012
    
    def _get_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = LLMClient(self.llm_config)
        return self._llm
    
    def _generate_content(self, request: ContentRequest) -> ContentResult:
        ct = request.content_type.lower()
        
        if "sql" in ct:
            return self._sql_generation(request)
        elif "analysis" in ct or "ml" in ct:
            return self._ml_inference(request)
        elif "document" in ct:
            return self._document_ai(request)
        elif "forecast" in ct:
            return self._forecasting(request)
        else:
            return self._sql_generation(request)
    
    def _sql_generation(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''-- SQL for {request.topic}

-- Basic query
SELECT * FROM {request.topic.replace(' ', '_').lower()}
ORDER BY id
LIMIT 100;

-- With aggregation
SELECT 
    date_trunc('month', created_at) AS month,
    COUNT(*) AS count,
    SUM(amount) AS total
FROM {request.topic.replace(' ', '_').lower()}
GROUP BY 1
ORDER BY 1 DESC;

-- Using Snowflake Cortex for AI
SELECT CORTEX_LLM_COMPLETE(
    'Summarize the trends in this data',
    SELECT * FROM {request.topic.replace(' ', '_').lower()}
);
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "sql", "skill": "sql"},
        )
    
    def _ml_inference(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''-- ML Inference for {request.topic}

-- Using pre-trained model
SELECT * FROM PREDICT(
    MODEL => '{request.topic.lower().replace(' ', '_')}_model',
    INPUT => TABLE(my_data)
);

-- Time series forecast
SELECT * FROM FORECAST(
    MODEL => 'forecast_model',
    DATA => my_data,
    TARGET_TIMESTAMP => 'date_col',
    TARGET_VALUE => 'value_col'
);

-- Anomaly detection
SELECT * FROM ANOMALY_DETECTION(
    MODEL => 'anomaly_model',
    DATA => my_data
);
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "ml-inference", "skill": "ml-inference"},
        )
    
    def _document_ai(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''-- Document AI for {request.topic}

-- Extract from PDFs
SELECT parse_document(
    '@mystage/{request.topic.lower().replace(' ', '_')}.pdf',
    'extracted_data'
) AS result;

-- Text classification
SELECT CORTEX_UTILS.CLASSIFY_TEXT(
    text_content,
    ['positive', 'negative', 'neutral']
) AS sentiment;

-- Extract entities
SELECT CORTEX_UTILS.EXTRACT_ENTITIES(
    text_content,
    'PERSON,ORG,LOCATION'
) AS entities;
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "document-ai", "skill": "document-ai"},
        )
    
    def _forecasting(self, request: ContentRequest) -> ContentResult:
        return ContentResult(
            content=f'''-- Forecasting for {request.topic}

-- Create forecasting model
CREATE OR REPLACE MODEL {request.topic.lower().replace(' ', '_')}_forecast
INPUT (date_col DATE, value_col FLOAT)
OUTPUT (forecast FLOAT)
AS SELECT date_col, value_col FROM historical_data;

-- Generate forecast
SELECT date_col, forecast 
FROM {request.topic.lower().replace(' ', '_')}_forecast!FORECAST(
    horizon => 30,
    confidence_level => 0.95
);

-- View results
SELECT * FROM TABLE(RESULT_SCAN(-1));
''',
            agent_id=self.agent_id,
            quality_score=0.85,
            metadata={"type": "forecast", "skill": "time-series"},
        )