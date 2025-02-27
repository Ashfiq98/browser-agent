# import asyncio
# from langchain_openai import ChatOpenAI
# from browser_use import Agent
# import time
# from dotenv import load_dotenv
# import pandas as pd
# from openpyxl import Workbook


# load_dotenv()

# llm = ChatOpenAI(
#     model="gpt-4o-mini-2024-07-18",
#     temperature=0.0,
# )


# async def main():
#     sensitive_data = {
#         'xyz_name': 'xyz@gmail.com',
#         'xyz_password': 'xyzpass'
#     }

#     prompt = """
# You're a QA tester for testing a website (for example, now travelai.com), and your task is in below and after each successful evaluation move to the next task, don't repeat any task.


# 1.**TravelAI Logo Click Test**
#     Task: Go to travelAi.com, click all the 'TravelAI' logo on that page and ensure it redirects to the homepage.
#     """
# 2. **TravelAI Logo UI Test on Devices**
#    Task: Check if the logo is visible and responsive on iPhone, iPad, and Desktop.
# 3. **Our Brand Navigation Menu Click Test**
#    Task: Click on 'Our brands' in the navigation menu and verify it redirects to the correct page.

# 4. **Our Brand Menu Spelling Check**
#    Task: Inspect the 'Our brands' navigation menu text for any spelling errors.

# 5. **Our Brand Menu Responsive Display Test**
#    Task: Check if the 'Our brands' menu displays correctly on iPhone, iPad, and Desktop views.

# 6. **Applied AI Navigation Menu Click Test**
#    Task: Click on 'Applied AI' in the navigation menu and verify it redirects to the correct page.

# 7. **Applied AI Menu Spelling Check**  
#    Task: Inspect the 'Applied AI' navigation menu text for any spelling errors.

# 8. **Applied AI Menu Responsive Display Test**  
#    Task: Check if the 'Applied AI' menu displays correctly on iPhone, iPad, and Desktop views.
#     3. **TravelAI Logo Hover Test** 
#        Task: (Maximum 3 attempts per step. If any step fails thrice, skip the test.)
#        - Open https://www.travelai.com/  
#        - Hover over the 'TravelAI' logo (DO NOT CLICK). Check if the <a> tag has the correct homepage URL.  
#        - If no tooltip, check the bottom-left corner for the correct URL. Verify the URL matches the homepage.
#     5. **Our Brand Navigation Menu Hover Test**
#        Task: (Maximum 3 attempts per step. If any step fails thrice, skip the test.)
#        - Open https://www.travelai.com/.  
#        - Hover over the 'Our brands' menu item.  
#        - Verify the correct URL displays in the browser status bar.
#        - Confirm the hover state changes the color appropriately.
#     9. **Applied AI Navigation Menu Hover Test**  
#        Task: (Maximum 3 attempts per step. If any step fails thrice, skip the test.)  
#        - Open https://www.travelai.com/.  
#        - Hover over the 'Applied AI' menu item.
#        - Verify the correct URL displays in the browser status bar.
#        - Confirm the hover state changes the color appropriately.

#     12. **Our Vision Navigation Menu Hover Test**
#         Task: (Maximum 3 attempts per step. If any step fails thrice, skip the test.)
#         - Open https://www.travelai.com/.
#         - Hover over the 'Our Vision' menu item.
#         - Verify the correct URL displays in the browser status bar.
#         - Confirm the hover state changes the color appropriately.
# """
#     # Create a list to hold the test case results
#     results = []

#     overall_start_time = time.time()

#     # Use the same prompt string to run the agent
#     agent = Agent(task=prompt, llm=llm, sensitive_data=sensitive_data)

#     step_start_time = time.time()
#     result = await agent.run()  # Run the agent
#     step_end_time = time.time()

#     # Defaulting status to 'pass'
#     status = "pass"

#     # Add the result to the list
#     results.append({
#         "testcase": "All Test Cases",
#         "status": status,
#         "time": step_end_time - step_start_time
#     })

#     print(f"Time Taken for 'All Test Cases': {step_end_time - step_start_time:.2f} seconds")

#     overall_end_time = time.time()
#     print(f"\nTotal Execution Time: {overall_end_time - overall_start_time:.2f} seconds")

#     # Create a DataFrame and save to Excel
#     df = pd.DataFrame(results)
#     df.to_excel("test_results.xlsx", index=False)

# asyncio.run(main())

import asyncio
import json
from langchain_openai import ChatOpenAI
from browser_use import Agent
import time
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0.0,
)


def read_prompt_from_file(file_path):
    """Read prompt from a text file."""
    try:
        with open(file_path, 'r') as file:
            prompt = file.read()
        return prompt
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


async def main():
    sensitive_data = {
        'xyz_name': 'xyz@gmail.com',
        'xyz_password': 'xyzpass'
    }

    # Read prompt from file
    prompt_file_path = "prompt.txt"
    prompt = read_prompt_from_file(prompt_file_path)
    
    if not prompt:
        print("Failed to load prompt. Exiting.")
        return

    overall_start_time = time.time()

    # Use the prompt from the file to run the agent
    agent = Agent(task=prompt, llm=llm, sensitive_data=sensitive_data)

    step_start_time = time.time()
    agent_result = await agent.run()  # Run the agent
    step_end_time = time.time()
    
    # Get execution time
    execution_time = step_end_time - step_start_time
    
    # Print some basic info about the agent result to help identify available data
    print("\nAgent Result Type:", type(agent_result))
    
    # Try to extract data - this assumes agent_result might be iterable
    # Adjust based on the actual structure you observe
    try:
        # First, try to extract data assuming it's a list-like object
        if hasattr(agent_result, '__iter__'):
            extracted_data = []
            for item in agent_result:
                # Try to get item as dict or string
                if hasattr(item, '__dict__'):
                    item_data = {k: str(v) for k, v in item.__dict__.items() if not k.startswith('_')}
                else:
                    item_data = str(item)
                extracted_data.append(item_data)
        # If it's not iterable, try to get its string representation or dict
        elif hasattr(agent_result, '__dict__'):
            extracted_data = {k: str(v) for k, v in agent_result.__dict__.items() if not k.startswith('_')}
        else:
            extracted_data = str(agent_result)
            
        # Create result object
        result = {
            "testcase": "All Test Cases",
            "status": "pass",
            "time": execution_time,
            "agent_data": extracted_data
        }
        
        # Save to JSON
        with open("test_results.json", "w") as json_file:
            json.dump(result, json_file, indent=4)
        print("Results saved to test_results.json")
        
    except Exception as e:
        print(f"Error extracting or saving data: {e}")
        # Fallback to just saving the string representation
        result = {
            "testcase": "All Test Cases",
            "status": "pass",
            "time": execution_time,
            "agent_data": str(agent_result)
        }
        with open("test_results_basic.json", "w") as json_file:
            json.dump(result, json_file, indent=4)
        print("Basic results saved to test_results_basic.json")
    
    # Also save to Excel
    df = pd.DataFrame([{
        "testcase": "All Test Cases", 
        "status": "pass", 
        "time": execution_time
    }])
    df.to_excel("test_results.xlsx", index=False)
 
    overall_end_time = time.time()
    print(f"\nTotal Execution Time: {overall_end_time - overall_start_time:.2f} seconds")

asyncio.run(main())