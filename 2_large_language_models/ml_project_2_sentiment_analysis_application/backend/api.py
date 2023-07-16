from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel
from google.cloud import bigquery
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Review(BaseModel):
    review: str

@app.get("/api/review")
def help():
    return {"message": "Send a POST request to /api/review with your review to get sentiment analysis"}
@app.post("/api/review", status_code=200)
def review(review: Review):
    logger.info(f"Retrieved review: {review.review}")
    logger.info("Running Bigquery sentiment analysis..")

    client = bigquery.Client()

    query = f"""
    SELECT
        ml_generate_text_result['predictions'][0]['content'] AS generated_text,
        ml_generate_text_result['predictions'][0]['safetyAttributes'] AS safety_attributes,
        * EXCEPT (ml_generate_text_result)
    FROM
        ML.GENERATE_TEXT(
            MODEL `aiedge_imdb_data.llm_model`,
            (SELECT "perform sentiment analysis on the following text, return one the following categories: positive, negative: {review.review}" AS prompt FROM UNNEST([1])),
            STRUCT(
                0.2 AS temperature,
                10 AS max_output_tokens
            )
        );
    """

    logger.debug(f"Query:\n{query}")


    try:
        query_job = client.query(query)  # Make an API request.
        results = query_job.result()  # Wait for the job to complete.

        df = results.to_dataframe().iloc[0]

        safety_attributes = json.loads(df.loc['safety_attributes'])

        logger.info(f"Results:\n{df}")

        logger.info(safety_attributes)
        logger.info(safety_attributes.get('blocked'))


        if safety_attributes.get('blocked') == True:
            result = "negative"
        else:
            result = df['generated_text']


        logger.info(f"Results:\n{result}")

        logger.info(f"Classified sentiment: {result}")

        # We assume here that the query will return a single row of results.
        # If your query could return multiple rows, consider using results.to_dataframe()

        return {"message": "Review submitted successfully", "success": True, "result": result}

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500, detail="Failed to execute sentiment analysis."
        ) from e
