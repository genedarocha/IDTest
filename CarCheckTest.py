
# The is a test using Python with Selenium WebDriver to check the car details on the website

# Test Description:
# Write a test automation suite which does following.
# 1. Reads given input file: car_input.txt
# 2. Extracts vehicle registration numbers based on pattern(s).
# 3. Each number extracted from input file is fed to any car valuation website for e.g. webuyanycar (Perform vehicle details search car valuation page with random mileage details)
# 4. Compare the output returned by car valuation website with given car_output.txt
# 5. Highlight/fail the test for any mismatches. Showcase your skills so it’s easier to add more input files in future. Utilise any JVM based language with browser automation tools. Use
# design patterns where appropriate.

# This is the import file provided

# There are multiple websites available to check current car value in United Kingdom.
# The best of all is webuyanycar.com for instant valuation.
# The other examples are autotrader.com and confused.com.
# Checking example BMW with registration AD58 VNF the value of the car is roughly around £3000.
# However car with registration BW57 BOW is not worth much in current market.
# There are multiple cars available higher than £10k with registrations KT17DLX and SG18 HTN.

# This is the output file provided

# VARIANT_REG,MAKE,MODEL,YEAR
# SG18HTN,Volkswagen, Golf 1.5 TSI EVO SE Nav SG18 HTN,2018
# AD58VNF,BMW,1 SERIES DIESEL COUPE - 120d M Sport 2dr,2008
# BW57BOF,TOYOTA,YARIS HATCHBACK - 1.0 VVT-i T2 3dr,2008
# KT17DLX,SKODA,SUPERB DIESEL ESTATE - 2.0 TDI CR 190 Sport Line 5dr DSG,2017

# The test will check the car details on the website and compare the output with the expected output
# The test will be run using the command: python CarCheckTest.py


# Import the required libraries
import re
import random
import argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Starting the Car Check Test")

# This is a function to get the car registration numbers from the input file
# Step 1: Read the car registration numbers from the input file - car_input.txt
def get_the_car_reg_numbers(file_path):
    # Open the input file car_input.txt and read the content
    with open(file_path, 'r') as file:
        content = file.read()

    # Define a simple pattern to match car registration numbers
    pattern = r'\b[A-Z]{2}\d{2}[A-Z]{3}\b|\b[A-Z]{2}\d{2} [A-Z]{3}\b'

    # Find all registration numbers that match the pattern based on the input file
    registration_numbers = re.findall(pattern, content)
    
    # Return the list of registration numbers from the input file after pattern matching
    return registration_numbers


def check_the_car_value(registration_number, mileage):
    # Create a new browser window in Chrome 
    driver = webdriver.Chrome()

    # Visit the car valuation website
    driver.get("https://www.webuyanycar.com/")
    sleep(4)
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    #going too fast.. need to slow down to allow the page to load
    
    # When we get to this website there are some cookies, so we have to click to accept the cookies first. 
        # Click the button to submit the details
    accept_cookie_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    accept_cookie_button.click()
    
        
    #going too fast.. need to slow down to allow the page to load
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'vehicleReg')))
    
    # Find the input fields for registration and mileage
    registration_input = driver.find_element(By.ID, 'vehicleReg')
    mileage_input = driver.find_element(By.ID, 'Mileage')

    # Type in the registration number and mileage
    registration_input.send_keys(registration_number)
    
    mileage_input.send_keys(mileage)

    # Click the button to submit the details
    submit_button = driver.find_element(By.ID, 'btn-go')
    submit_button.click()
    sleep(5)

    # Wait for the page to load and get the result
    # if this was Cypress, it would do it without this statement, built in wait
    # but in Selenium, we need to wait for the page to load (there is no retry here either)
    # Playwright is another tool that has built in wait
    # Another problem - 7 seconds mayb not be enough, but we can't make it too long 
    # Should add a retry mechanism really 
    
     # Now we need to fill in the new fields (Email, Postcode, Telephone)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'EmailAddress')))
    
    # Find the email address, postcode, and telephone fields
    email_input     = driver.find_element(By.ID, 'EmailAddress')
    postcode_input  = driver.find_element(By.ID, 'Postcode')
    telephone_input = driver.find_element(By.ID, 'TelephoneNumber')

    # Enter the values into the fields
    email_details ='genedarocha@gmail.com'
    postcode1 ='SE18 AAA'       # incorrect postcode 
    postcode2 = 'SE18 7DP'      # correct postcode
    telephone = '07786857444'   # random telephone number
    
    email_input.send_keys(email_details )
    postcode_input.send_keys(postcode1)     # incorrect postcode to check if error occurs 
    
    # try:
    #     error_message0 = driver.find_element(By.XPATH, "//div[contains(text(), 'Please check this has been entered correctly.')]")
    #     return "Existing Postcode is not working, so using a new postcode"
    # except:
    #     return 
    postcode_input.clear()
    postcode_input.send_keys(postcode2)   
    telephone_input.send_keys('07786857444')

    #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'advance-btn')))
    #need to ensure that element is present and I can also see variables in the code.
    sleep(10)
        
    # Click the 'advance_btn' button to submit
    advance_button = driver.find_element(By.ID, 'advance-btn')
    advance_button.click()
    sleep(15)
  
    # Wait for a moment to ensure everything is processed
    sleep(5)

    # Now, extracting the valuation result from the 'amount' class
    try:
        valuation_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'amount')))
        valuation_result = valuation_element.text.strip()  # Extract the text and strip any extra spaces
        
        driver.quit()
        return valuation_result

    except Exception as e:
        print("Error: Could not find the valuation result", e)
        driver.quit()
        return None

    
    # When I manually tried one of the car and also once  that did not exist, I would see the message 'Sorry, we couldn't find your car' message
    # So had to put in some error trapping
    
    try:
        error_message = driver.find_element(By.XPATH, "//div[contains(text(), 'Sorry, we couldn\'t find your car')]")
        # If the message is found, then return the message and close the browser
        driver.quit()
        return "Sorry, we couldn't find your car"
    except:
        # If the message is not found, get the car valuation result
        result = driver.find_element(By.ID, 'valuationResult').text
        driver.quit()
        # Then Return the result of the car valuation
        return result
    

# Next we need to check and compare the actual results with the expected results from the output file as presented above
def compare_values(actual, expected_file):
    # We then Open the output file and read the expected result
    with open(expected_file, 'r') as file:
        expected = file.read().strip()

    # Compare the actual results with the expected results
    return actual == expected

# Next we need to call all the functions and run the test 
def run_test(input_file, output_file):
    
    # Get the list of car registration numbers from the input file
    reg_numbers = get_the_car_reg_numbers(input_file)

    # Loop through each registration number
    for reg_number in reg_numbers:
        # As there are no mileage inputs, we can just use the Python function random to get some unique figures between 5k-100k
        mileage = random.randint(5000, 100000)
        
        # Get the actual valuation from the website using the check_the_car_value function
        actual_value = check_the_car_value(reg_number, mileage)

        # Now compare the actual value with the expected value
        if not compare_values(actual_value, output_file):
           print(f"Test Failed for {reg_number}. The value did not match.")

        else:
           print(f"Test Passed for {reg_number}. The value matched.")
            
# Main function to handle command-line arguments
if __name__ == '__main__':
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Run car check test with input and output files.')

    # Add arguments for input and output file paths
    parser.add_argument('--input', type=str, required=True, help='Path to the input file (e.g. car_input.txt)')
    parser.add_argument('--output', type=str, required=True, help='Path to the output file (e.g. car_output.txt)')

    # Parse the arguments
    args = parser.parse_args()

    # Run the test with the provided input and output file
    run_test(args.input, args.output)
            
# End of Test. 