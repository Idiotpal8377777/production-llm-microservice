from google import genai 
from google.genai import types , errors 
from app.core.config import settings
from app.schemas.order import CustomerOrder, RetentionResponse
from tenacity import retry, stop_after_attempt, wait_exponential , retry_if_exception_type
import asyncio 
from fastapi import HTTPException 
from app.core.logger import logger
import time 


class RetensionService:

    def __init__(self):
        self.client = genai.Client(api_key = settings.LLM_API_KEY)
        self.models = ["gemini-3.6-flash" , "gemini-3.5-flash-lite"]

    @retry(
        stop = stop_after_attempt(3),
        wait = wait_exponential(multiplier=1 , min=1 , max=4),
        retry = retry_if_exception_type((errors.APIError , asyncio.TimeoutError )),
        reraise = True
    )

    async def generate_response_with_retry(self ,model_name,user_prompt , system_prompt ) -> RetentionResponse:

        plan = await asyncio.wait_for(
            self.client.aio.models.generate_content(
                model = model_name ,
                contents = user_prompt ,
                config =types.GenerateContentConfig
                (system_instruction = system_prompt ,
                 response_mime_type = "application/json",
                response_schema = RetentionResponse 
            )
        ),
    
        timeout=15)

        return plan  # type: ignore 

    async def airesponse(self , payload : CustomerOrder) -> RetentionResponse:

        system_prompt = ("You are an expert AI FinTech retention analyst. "
                        "Evaluate the customer's churn score and support ticket. "
                        "If churn_score > 0.7 or sentiment is critical, set status to DANGER "
                        "and offer a 15-20%  discount. DO NOT exceed 20%. "
                        "Otherwise set status to SAFE and 0%  discount.")

        user_prompt = (f"Customer ID: {payload.customer_id}\n"
                       f"Churn Score: {payload.churn_score}\n"
                       f"Sentiment: {payload.sentiment}\n"
                       f"Support Ticket: {payload.ticket_text}")



        last_error = None 
        for model in self.models:
            start_time = time.perf_counter()
            try:
                response = await self.generate_response_with_retry(model , user_prompt , system_prompt )
                latency_ms = round((time.perf_counter() - start_time)*1000 , 2)
                plan = response.parsed   # type: ignore 
                if plan.discount_offered_pct > 20:
                    plan.discount_offered_pct = 20

                usage = response.usage_metadata # type: ignore
                logger.info("llm call success ", extra = { 
                    "customer_id": payload.customer_id,
                    "model" :model,
                    "latency_ms": latency_ms,
                    "prompt_tokens": usage.prompt_token_count if usage else 0,
                     "output_tokens": usage.candidates_token_count if usage else 0,
                      "total_tokens": usage.total_token_count if usage else 0,
                     "status": plan.status,
                     "discount_pct": plan.discount_offered_pct, 
                                          })

                return plan 


            except (errors.ServerError, asyncio.TimeoutError) as e:
                latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                logger.warning(
                    "llm_model_failed",
                    extra={
                        "data": {
                            "customer_id": payload.customer_id,
                            "model": model,
                            "latency_ms": latency_ms,
                            "error": repr(e),
                        }
                    },
                )
                last_error = e
                continue
                

           



    

    

        
                
                
            
        
        

    
  



