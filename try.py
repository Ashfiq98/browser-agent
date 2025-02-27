import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
import time
from dotenv import load_dotenv
import pandas as pd
from openpyxl import Workbook
from sentence_transformers import SentenceTransformer, util

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0.0,
)

# Load the pre-trained model for Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')


async def main():
    sensitive_data = {
        'xyz_name': 'xyz@gmail.com',
        'xyz_password': 'xyzpass'
    }

    test_cases = [
        # {
        #     "name": "TravelAI Logo UI Test on Devices",
        #     "task": """(Maximum 3 attempts per step. If it fails thrice, skip and do not repeat.)
        #        Open the TravelAI website. Check if the logo is visible and undistorted on iPhone, iPad, and Desktop."""
        # },
        {
            "name": "Our Brand Navigation Menu Click Test",
            "task": "Open the TravelAI website. Click on 'Our brands' in the navigation menu and verify it redirects to the correct page."
        }
    ]

    # Create a list to hold the test case results
    results = []

    overall_start_time = time.time()

    for test in test_cases:
        print(f"\nExecuting: {test['name']}")
        agent = Agent(task=test["task"], llm=llm, sensitive_data=sensitive_data)

        step_start_time = time.time()
        result = await agent.run()  # Run the agent
        step_end_time = time.time()

        # Now we need to check if the result has an attribute or a message that indicates success or failure.
        # Assuming result is an object, you can access its attributes:
        # For example: result.success, result.status, or any other relevant property

        # Check if the agent run was successful or not.
        print(dir(result))

        # Extract the actual data (the response from the agent)
        actual_data = result.all_results[-1].extracted_content if result.all_results else "N/A"

        # Define expected data (this is the reference you want to compare)
        expected_data = test["task"]

        # Use Sentence-BERT to calculate similarity between actual and expected data
        embedding_actual = model.encode(actual_data, convert_to_tensor=True)
        embedding_expected = model.encode(expected_data, convert_to_tensor=True)

        # Calculate cosine similarity between the embeddings
        cosine_similarity = util.pytorch_cos_sim(embedding_actual, embedding_expected)

        # Set a threshold for cosine similarity to determine pass or fail
        threshold = 0.7  # You can adjust this value based on your needs
        status = "pass" if cosine_similarity.item() > threshold else "fail"

        # Add the result to the list
        results.append({
            "testcase": test["name"],
            "status": status,
            "cosine_similarity": cosine_similarity.item(),
            "actual_data": actual_data,
            "expected_data": expected_data
        })

        print(f"Time Taken for '{test['name']}': {step_end_time - step_start_time:.2f} seconds")
        print(f"Cosine Similarity: {cosine_similarity.item():.4f}")
        print(f"Status: {status}")

    overall_end_time = time.time()
    print(f"\nTotal Execution Time: {overall_end_time - overall_start_time:.2f} seconds")

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(results)
    df.to_excel("test_results.xlsx", index=False)

asyncio.run(main())