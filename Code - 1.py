# Author : Shekhar Gosavi
# This code creates a GUI for easily raising tickets at help.ti.com.
# For Suggestions reach out at s-gosavi@ti.com
# TTA Revision 3 : Added the Final Check Pop Up. Soldering + ATE HW

import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from tkinter import Scrollbar
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import threading
import queue



condition = threading.Condition()
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
#options.add_argument("--start-minimized")
# Function to create gradient background
def create_gradient(canvas, width, height, color1, color2):
    limit = height
    (r1, g1, b1) = canvas.winfo_rgb(color1)
    (r2, g2, b2) = canvas.winfo_rgb(color2)
    r_ratio = float(r2 - r1) / limit
    g_ratio = float(g2 - g1) / limit
    b_ratio = float(b2 - b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
        canvas.create_line(0, i, width, i, fill=color, tags=("gradient",))

def start_web_scraping(lab, Selected_Option, short_dis_text, detailed_dis_text, q):
    global proceed
    global driver
    
    if(Selected_Option == "Soldering Help-Minor" or Selected_Option == "Soldering Help-Major"):
        soldering_value = 6 if Selected_Option == "Soldering Help-Minor" else 5
    elif(Selected_Option == "Requesting ATE hardware"):
        soldering_value = "Check Out"
    elif(Selected_Option == "Data Collection"):
        soldering_value = 3 

    if(Selected_Option == "Soldering Help-Minor" or Selected_Option == "Soldering Help-Major" or Selected_Option == "Data Collection" or Selected_Option == "Thermostream Setup"):
        lab_name = 1 if lab == "BTP 3F" else 3
    elif(Selected_Option == "Requesting ATE hardware"):
        lab_name = lab
  
  
    driver = webdriver.Chrome()
    # driver = webdriver.Edge(options=options)
    driver.set_window_size(800, 700)
    # driver.minimize_window()
    q.put("Opening TI Help Page...")
    driver.get("https://help.ti.com/")
    print(driver.page_source)
    q.put(f"Opened {driver.title}")

    try:
        search_box = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="stars-button"]'))
        )
    except:
        driver.refresh()
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="stars-button"]'))
        )
    driver.execute_script('arguments[0].click()', search_box)
    q.put("Clicked on the Submit Ticket...")

    try:
        search_box = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@title="SEARCH:"]'))
        )
        driver.execute_script('arguments[0].click()', search_box)
    except:
        driver.refresh()
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@title="SEARCH:"]'))
        )
        driver.execute_script('arguments[0].click()', search_box)


    if(Selected_Option == "Soldering Help-Minor" or Selected_Option == "Soldering Help-Major"):
        search_box.send_keys("Soldering")
        search_box.send_keys(Keys.RETURN)
        q.put("Searching for Soldering Help...")

        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@title="Request Soldering Help"]'))
        )
        driver.execute_script('arguments[0].click()', link)
        time.sleep(0.5)
        q.put("Clicked on Request Soldering Help link...")

        short_dis = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div[3]/div[1]/div/textarea[2]'))
        )
        driver.execute_script('arguments[0].click()', short_dis)
        short_dis.send_keys(short_dis_text)
        q.put("Entered short description...")

        Dis = driver.find_element(by=By.XPATH, value='//iframe[@frameborder="0"]')
        driver.execute_script('arguments[0].click()', Dis)
        time.sleep(0.5)
        Dis.send_keys(Keys.F8)
        time.sleep(1.5)
        Dis.send_keys(detailed_dis_text)
        q.put("Entered detailed description...")
        time.sleep(1)
        Save = driver.find_element(by=By.XPATH, value='//*[@class="k-primary k-button k-primary-hover k-button-focus"]')
        Save.click()
        q.put("Saved the description...")

        lab = driver.find_element(by=By.XPATH, value='//*[@style="height: 18px; border-style: solid; border-width: 1px; border-color: darkred; line-height: 18px;"]')
        driver.execute_script('arguments[0].click()', lab)

        time.sleep(1)
        lab1 = driver.find_element(by=By.XPATH, value=f'//*[@data-offset-index="{lab_name}"]')
        driver.execute_script('arguments[0].click()', lab1)
        q.put("Lab setting done...")

        lab = driver.find_element(by=By.XPATH, value='//*[@style="height: 18px; border-style: solid; border-width: 1px; border-color: darkred; line-height: 18px;"]')
        driver.execute_script('arguments[0].click()', lab)
        time.sleep(1)
        lab1 = driver.find_element(by=By.XPATH, value=f'//*[@data-offset-index="{soldering_value}"]')
        driver.execute_script('arguments[0].click()', lab1)
        q.put("Soldering help setting done...")

        lab1 = driver.find_element(by=By.XPATH, value=f'//*[@data-offset-index="{soldering_value}"]')
        driver.execute_script('arguments[0].click()', lab1)
        q.put("Soldering help setting done...")
   
    elif(Selected_Option == "Data Collection" ):
        search_box.send_keys("Data Collection")
        search_box.send_keys(Keys.RETURN)
        q.put("Searching for Data Collection Help...")

        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@title="Request Data Collection Support"]'))
        )
        time.sleep(0.5)
        driver.execute_script('arguments[0].click()', link)
        q.put("Clicked on Request Data Collection Support link...")

       
        short_dis = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div[3]/div[1]/div/textarea[2]'))
        )
        driver.execute_script('arguments[0].click()', short_dis)
        short_dis.send_keys(short_dis_text)
        q.put("Entered short description...")

        Dis = driver.find_element(by=By.XPATH, value='//iframe[@frameborder="0"]')
        driver.execute_script('arguments[0].click()', Dis)
        Dis.send_keys(Keys.F8)
        time.sleep(2)
        Dis.send_keys(detailed_dis_text)
        q.put("Entered detailed description...")
        time.sleep(1)
        Save = driver.find_element(by=By.XPATH, value='//*[@class="k-primary k-button k-primary-hover k-button-focus"]')
        Save.click()
        q.put("Saved the description...")

        No = driver.find_element(by=By.XPATH, value='//*[@test-id="CD:943146cf9640dd9bc33a424085a798cef408a1c5f4,Radio"]')
        driver.execute_script('arguments[0].click()', No)

        Yes = driver.find_element(by=By.XPATH, value='//*[@test-id="CD:943146cf96589300280a30430da68c3064fd9d77e0,Radio"]')
        driver.execute_script('arguments[0].click()', Yes)

        lab = driver.find_element(by=By.XPATH, value='//*[@style="height: 18px; border-style: solid; border-width: 1px; border-color: darkred; line-height: 18px;"]')
        driver.execute_script('arguments[0].click()', lab)

        time.sleep(1)
        lab1 = driver.find_element(by=By.XPATH, value=f'//*[@data-offset-index="{lab_name}"]')
        driver.execute_script('arguments[0].click()', lab1)
        q.put("Lab setting done...")

        lab = driver.find_element(by=By.XPATH, value='//*[@tabindex="3001"]')
        driver.execute_script('arguments[0].click()', lab)
        time.sleep(0.5)
        lab.send_keys("Data collection")
        lab.send_keys(Keys.RETURN)
        q.put("Soldering help setting done...")

        time.sleep(0.5)
       

        support = driver.find_element(by=By.XPATH, value=f'//*[@tabindex="3002"]')
        driver.execute_script('arguments[0].click()', support)
        time.sleep(0.5)
        support.send_keys("ATE Day")
        support.send_keys(Keys.RETURN)
        
        q.put("support setting done...")
        
    elif(Selected_Option == "Thermostream Setup" ):
        search_box.send_keys("Data Collection")
        search_box.send_keys(Keys.RETURN)
        q.put("Searching for Data Collection Help...")

        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@title="Request Data Collection Support"]'))
        )
        time.sleep(0.5)
        driver.execute_script('arguments[0].click()', link)
        q.put("Clicked on Request Data Collection Support link...")

       
        short_dis = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div[3]/div[1]/div/textarea[2]'))
        )
        driver.execute_script('arguments[0].click()', short_dis)
        short_dis.send_keys(short_dis_text)
        q.put("Entered short description...")

        Dis = driver.find_element(by=By.XPATH, value='//iframe[@frameborder="0"]')
        driver.execute_script('arguments[0].click()', Dis)
        Dis.send_keys(Keys.F8)
        time.sleep(2)
        Dis.send_keys(detailed_dis_text)
        q.put("Entered detailed description...")
        time.sleep(1)
        Save = driver.find_element(by=By.XPATH, value='//*[@class="k-primary k-button k-primary-hover k-button-focus"]')
        Save.click()
        q.put("Saved the description...")

        No = driver.find_element(by=By.XPATH, value='//*[@test-id="CD:943146cf9640dd9bc33a424085a798cef408a1c5f4,Radio"]')
        driver.execute_script('arguments[0].click()', No)

        Yes = driver.find_element(by=By.XPATH, value='//*[@test-id="CD:943146cf96589300280a30430da68c3064fd9d77e0,Radio"]')
        driver.execute_script('arguments[0].click()', Yes)

        lab = driver.find_element(by=By.XPATH, value='//*[@style="height: 18px; border-style: solid; border-width: 1px; border-color: darkred; line-height: 18px;"]')
        driver.execute_script('arguments[0].click()', lab)

        time.sleep(1)
        lab1 = driver.find_element(by=By.XPATH, value=f'//*[@data-offset-index="{lab_name}"]')
        driver.execute_script('arguments[0].click()', lab1)
        q.put("Lab setting done...")

        lab = driver.find_element(by=By.XPATH, value='//*[@tabindex="3001"]')
        driver.execute_script('arguments[0].click()', lab)
        time.sleep(0.5)
        lab.send_keys("Characterization")
        lab.send_keys(Keys.RETURN)
        q.put("Soldering help setting done...")

        time.sleep(0.5)
       

        support = driver.find_element(by=By.XPATH, value=f'//*[@tabindex="3002"]')
        driver.execute_script('arguments[0].click()', support)
        time.sleep(0.5)
        support.send_keys("ATE Day")
        support.send_keys(Keys.RETURN)
        
        q.put("support setting done...")
        
    else:
        search_box.send_keys("ATE Hardware")
        search_box.send_keys(Keys.RETURN)
        q.put("Searching for Requesting ATE Hardware Help...")

        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Request ATE Hardware, Click here to submit ticket"]'))
        )
        time.sleep(0.5)
        link.click()
        q.put("Clicked on Request ATE Hardware Help link...")

       
        short_dis = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div[3]/div[1]/div/textarea[2]'))
        )
        short_dis.click()
        short_dis.send_keys(short_dis_text)
        q.put("Entered short description...")
        time.sleep(4)

        Dis = driver.find_element(by=By.XPATH, value='//iframe[@frameborder="0"]')
        Dis.click()
        Dis.send_keys(Keys.F8)
        time.sleep(5)
        Dis.send_keys(detailed_dis_text)
        q.put("Entered detailed description...")
        Save = driver.find_element(by=By.XPATH, value='//*[@class="k-primary k-button k-primary-hover k-button-focus"]')
        driver.execute_script('arguments[0].click()', Save)
        q.put("Saved the description...")

        lab = driver.find_element(by=By.XPATH, value='//*[@style="height: 18px; border-style: solid; border-width: 1px; border-color: darkred; line-height: 18px;"]')
        driver.execute_script('arguments[0].click()', lab)

        time.sleep(1)
        lab1 = driver.find_element(by=By.XPATH, value=f'//*[text()="{lab_name}"]')
        driver.execute_script('arguments[0].click()', lab1)
        q.put("Lab setting done...")

        No = driver.find_element(by=By.XPATH, value='//*[@test-id="CD:943146cf9640dd9bc33a424085a798cef408a1c5f4,Radio"]')
        driver.execute_script('arguments[0].click()', No)

        Yes = driver.find_element(by=By.XPATH, value='//*[@test-id="CD:943146cf96589300280a30430da68c3064fd9d77e0,Radio"]')
        driver.execute_script('arguments[0].click()', Yes)

        lab = driver.find_element(by=By.XPATH, value='//*[@style="top: 88px; left: 12.57143px; position: absolute; width: 253.7143px; height: 20.57143px; padding: 0px; visibility: Visible"]/span/span')
        driver.execute_script('arguments[0].click()', lab)
        time.sleep(1)
        lab1 = driver.find_element(by=By.XPATH, value=f'//*[text()="{soldering_value}"]')
        driver.execute_script('arguments[0].click()', lab1)
        q.put("Check Out setting done...")



    

    q.put("All fields are filled, please review")

    with condition:
        condition.wait()
    time.sleep(0.5)
    #SUBMIT TICKET
    # time.sleep(5)
    # submit = driver.find_element(by=By.XPATH, value=f'//*[text()="SUBMIT TICKET"]')
    # driver.execute_script('arguments[0].click()', submit)
    # q.put("Submitted")

    time.sleep(2)
    q.put("Ticket raised Successfully !")
    q.put("popup")
    time.sleep(20)      

def on_submit():

    selected_lab = lab_var.get()
    selected_soldering = soldering_var.get()
    short_dis_text = short_dis_var.get()
    detailed_dis_text = detailed_dis_var.get("1.0", tk.END).strip()

    if not selected_lab or not selected_soldering:
        messagebox.showwarning("Input Required", "Please select both the lab and the help required.")
        return
    
    q.put("Starting...")
    threading.Thread(target=start_web_scraping, args=(selected_lab, selected_soldering, short_dis_text, detailed_dis_text, q)).start()

def check_queue():
    global proceed

    while not q.empty():
        msg = q.get_nowait()
        if msg == "popup":
            messagebox.showinfo("Success", "Ticket raised Successfully!")
        elif msg == "All fields are filled, please review":
            ans = messagebox.askokcancel("Please Check and Review", "Click ok to submit")
            q.put("Please Check and Review")
            if ans:
                with condition:
                    proceed = False
                    condition.notify()
            else :
                q.put("Ticket Submission Cancelled")
                driver.quit()
                break
        else:
             progress_label.config(text=msg)

    root.after(100, check_queue)

# Function to update description fields based on selection
def update_descriptions(event):
    selected_option = soldering_var.get()
    if selected_option == "Requesting ATE hardware":
        short_dis_var.set("Requesting ATE Hardware")
        detailed_dis_var.delete("1.0", tk.END)
        detailed_dis_var.insert("1.0", "Requesting ATE Hardware")

    elif selected_option == "Data Collection":
        short_dis_var.set("Requesting Data Collection Support")
        detailed_dis_var.delete("1.0", tk.END)
        detailed_dis_var.insert("1.0", "Requesting Data Collection Support")

    elif selected_option == "Thermostream Setup":
        short_dis_var.set("Requesting for Thermostream Setup")
        detailed_dis_var.delete("1.0", tk.END)
        detailed_dis_var.insert("1.0", "Requesting for Thermostream Setup")

    else:
        short_dis_var.set("Component Soldering")
        detailed_dis_var.delete("1.0", tk.END)
        detailed_dis_var.insert("1.0", "Soldering some components on PCB")

# GUI setup
root = tk.Tk()
root.title("TI Ticket Automation")
root.geometry("400x650+850+10")

# Create canvas for gradient background
canvas = tk.Canvas(root, width=400, height=620)
canvas.pack(fill="both", expand=True)
create_gradient(canvas, 400, 650, "#ff6347", "#b22222")

# Create a frame on top of the canvas
frame = tk.Frame(canvas, bg="#ffffff")
frame.place(relwidth=0.8, relheight=0.98, relx=0.1, rely=0.02)

# Add content to the frame
lab_label = tk.Label(frame, text="Select Lab", bg="#ffffff")
lab_label.pack(pady=8)
lab_var = tk.StringVar()
lab_dropdown = ttk.Combobox(frame, textvariable=lab_var)
lab_dropdown['values'] = ("BTP 3F", "BTP GF")
lab_dropdown.pack(pady=8)

soldering_label = tk.Label(frame, text="Select the help required", bg="#ffffff")
soldering_label.pack(pady=8)
soldering_var = tk.StringVar()
soldering_dropdown = ttk.Combobox(frame, textvariable=soldering_var)
soldering_dropdown['values'] = ("Soldering Help-Minor", "Soldering Help-Major","Requesting ATE hardware","Data Collection","Thermostream Setup")
soldering_dropdown.pack(pady=8)
soldering_dropdown.bind("<<ComboboxSelected>>", update_descriptions)

short_dis_label = tk.Label(frame, text="Short Description", bg="#ffffff")
short_dis_label.pack(pady=8)
short_dis_var = tk.StringVar(value="Component Soldering")
short_dis_entry = tk.Entry(frame, textvariable=short_dis_var, width=40,highlightbackground="black", highlightcolor="black", highlightthickness=1)
short_dis_entry.pack(pady=8)

detailed_dis_label = tk.Label(frame, text="Detailed Description", bg="#ffffff")
detailed_dis_label.pack(pady=8)
detailed_dis_var = tk.Text(frame, height=15,width=35,font="SegoeUI 9",highlightbackground="black", highlightcolor="black", highlightthickness=1 )
detailed_dis_var.insert("1.0", "Soldering some components on PCB")
detailed_dis_var.pack(pady=8)


submit_button = ttk.Button(frame, text="Submit", command=on_submit)
submit_button.pack(pady=8)

progress_label = tk.Label(frame, text="", bg="#ffffff")
progress_label.pack(pady=8)

# Apply style to the button
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=8)

# Set up queue
q = queue.Queue()
root.after(100, check_queue)

root.mainloop()
