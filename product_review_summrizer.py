import json
import sys
import os
import logging
import operator

from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END


logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("Product Review Summerizer")
logger.info("Starting Product Review Summerizer Agent...")

load_dotenv()
api_secret_key = os.getenv("OPENAI_API_KEY")

if not api_secret_key or api_secret_key.startswith("sk-your"):
    logger.info("Secret key not defined or not found")
    sys.exit(1)
logger.info("Intilized the key")
logger.info("All LANGGRAPH model components are loaded")

logger.info("Initilizing the pydantic class with states")

class ProductReviewState(BaseModel):
    reviews:str=""
    pros:list[str]=[]
    cons:list[str]=[]
    sentiment:str=""
    rating:float=0.0
    sentiment_reason:str=""
    is_recommended:bool=False
    recommendation_reason:str=""
    summary:str=""
    messages: Annotated[list, operator.add] = []

logger.info("Initializing the LLM (OpenAI GPT)...") 
llm_model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    api_key=api_secret_key,
    verbose=True
)

logger.info("Initilized the LLM (OpenAI GPT)...")

def extract_pros(productReviewState: ProductReviewState)->dict:
    response = llm_model.invoke(
        f"You are Product review assistant"
        f"User has entered multiple reviews here:'{productReviewState.reviews}'"
        f"now being assitant please extract the positive reviews from the input reviews"
    )
    return {
        "pros":[response.content],
        "messages": [f"[extract_pros] Done"]
    }

def extract_cons(productReviewState: ProductReviewState)->dict:
    response = llm_model.invoke(
        f"You are Product review assistant"
        f"User has entered multiple reviews here:'{productReviewState.reviews}'"
        f"now being assitant please extract the negative or cons reviews from the input reviews"
    )
    return {
        "cons":[response.content],
        "messages": [f"[extract_cons] Done"]
    }

def gauge_overall_sentiment(productReviewState: ProductReviewState)->dict:
    response = llm_model.invoke(
        f"You are Product review assistant"
        f"User has entered multiple reviews here:'{productReviewState.reviews}'\n"
        f"now being assitant please overall sentiment and overall estimated rating with one liner reason. from the input reviews"
        f"Reply STRICTLY in this JSON format (no other text)\n"
        f'{{"overall_sentiment": Positive/Negative/More Positive/More Negative,"Estimated_rating":"2.3/4/5/1/-1","sentiment_reason": "one sentence explanation"}}'
    )   
    try:
        result = json.loads(response.content)
        sentiment = result["overall_sentiment"]
        rating = result["Estimated_rating"]
        sentiment_reason = result["sentiment_reason"]
        print(f"Response from the overall Sentiments\n{'='*45}\n{response.content}")
    except (json.JSONDecodeError, KeyError):
        sentiment=""
        rating=0.0
        sentiment_reason = "Could not parse decision, defaulting to quick practice."

    return {
        "sentiment": sentiment,
        "rating": rating,
        "sentiment_reason": sentiment_reason,
        "messages": [f"[gauge_overall_sentiment] sentiment={sentiment}"]
    }

def execute_commended_or_not(productReviewState: ProductReviewState)->dict:
    response = llm_model.invoke(
        f"You are Product review assistant"
        f"You have below three outputs from specialist agent with prons,cons and over all sentiment"
        f"OVERALL sentiment:\n{productReviewState.sentiment}\n\n"
        f"OVERALL rating:\n{productReviewState.rating}\n\n"
        f"OVERALL sentiment_reason:\n{productReviewState.sentiment_reason}\n\n"
        f"now being EXPERT please return whether product is recommended or not recommended with the reason"
        f"if the productReviewState.rating is below 3 out of 5 then return false else true"
        f"Reply STRICTLY in this JSON format (no other text)"
        f'{{"isRecommended": True/False, "recommendationReason": "2 to 3 lines explanation why this is not recommended considering input points"}}'
    )   
    try:
        result = json.loads(response.content)
        is_recommended = result["isRecommended"]
        recommendation_Reason = result["recommendationReason"]        
    except (json.JSONDecodeError, KeyError):
        is_recommended=False       
        recommendation_Reason = "Could not parse decision, defaulting to quick practice."

    return {
        "is_recommended": is_recommended,
        "recommendation_reason": recommendation_Reason,
        "messages": [f"[execute_commended_or_not] is_recommended={is_recommended}"]
    }

def recommended_summary(productReviewState: ProductReviewState)->dict:      
    return {
        "summary":productReviewState.recommendation_reason,
        "messages": [f"[recommended_summary] Done"]
    }
def not_recommended_summary(productReviewState: ProductReviewState)->dict:    
    return {
        "summary":productReviewState.recommendation_reason,
        "messages": [f"[recommended_summary] Done"]
    }

def route_after_decision(productReviewState: ProductReviewState) -> str:
    if productReviewState.is_recommended:
        return "recommended"
    else:
        return "not_recommended"

graph = StateGraph(ProductReviewState)

graph.add_node("extract_pros",extract_pros)
graph.add_node("extract_cons",extract_cons)
graph.add_node("gauge_overall_sentiment",gauge_overall_sentiment)
graph.add_node("execute_commended_or_not",execute_commended_or_not)
graph.add_node("recommended_summary", recommended_summary)
graph.add_node("not_recommended_summary", not_recommended_summary)

graph.add_edge(START, "extract_pros")

graph.add_edge("extract_pros", "extract_cons")
graph.add_edge("extract_pros", "gauge_overall_sentiment")

graph.add_edge("gauge_overall_sentiment", "execute_commended_or_not")

graph.add_conditional_edges(
    "execute_commended_or_not",
    route_after_decision,
    {
        "recommended": "recommended_summary",
        "not_recommended": "not_recommended_summary",
    }
)

graph.add_edge("recommended_summary", END)
graph.add_edge("not_recommended_summary", END)

app = graph.compile()

def run_product_review_checker(reviews:str):
    print("=" * 55)
    print(" Product Review Summarizer")
    print(f" Your Reviews: \"{reviews}\"")
    print("=" * 55)
    result = app.invoke({
        "reviews": reviews,
        "messages": [],
    })

    print("\n" + "=" * 55)  
    print("=" * 55)
    for msg in result["messages"]:
        print(f"  {msg}")
    
    print(f"\n{result['summary']}")
    return result['summary']

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print(" Product Review Summarizer Graph")
    print("=" * 55)
    print("\n  Write or paste product reviews")
    print("  Type 'exit' to exit.\n")

    while True:
        productReview = input(" Enter or paste Product reviews( press enter, type EOI and press enter to finish): ").strip()

        if productReview.lower() in ("", "exit"):
            print("\n  Take care of yourself. Goodbye!\n")
            break

        lines = []        

        while True:
            line = input()            
            if line.strip() == "EOI":
                break
            lines.append(line)

        productReviews = "\n".join(lines).strip()
        run_product_review_checker(productReviews)
        print("\n")





