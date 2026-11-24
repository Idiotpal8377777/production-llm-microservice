from google import genai 
from google.genai import types 
from app.core.config import settings
from app.schemas.order import CustomerOrder , RetentionResponse

class RetentionAIresponse:
    def __init__(self)->None:
        self.model_name = "gemini-3.5-flash-lite"
        self.client = genai.Client(api_key=settings.LLM_API_KEY)

    async def airesponse(
        self, payload : CustomerOrder ) -> RetentionResponse:


        user_prompt = f"Customer ID : {payload.customer_id},Churn score:{payload.churn_score},sentiment:{payload.sentiment},ticket text:{payload.ticket_text}."


        system_prompt = f"You are a customer retention expert."
        f"You will be given a customer ID, churn score, sentiment, and ticket text."
        f"If the churn score is above 0.7 or the sentiment is 'citical' set status to 'DANGER' and offer 15-20% discount , DO NOT EXCEED 20% discount. "
        f"Otherwise set status to 'SAFE' and offer 0% discount."


        response = await self.client.aio.models.generate_content(
            model=self.model_name, 
            contents = user_prompt,
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type ="application/json",
                response_schema = RetentionResponse


            )

        )


        return response.parsed # type: ignore

retension_service = RetentionAIresponse()
                     
