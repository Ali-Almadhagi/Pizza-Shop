from tkinter import *
from tkinter import messagebox
import json
from datetime import datetime
from tkinter.ttk import Combobox
import requests
from tkinter.ttk import Treeview

#==============================================================================================================================================================================================
# A function to resize Images in the Application
def resizeImage(img, newWidth, newHeight):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x * oldWidth / newWidth)
            yOld = int(y * oldHeight / newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage
#==============================================================================================================================================================================================

# setting up client
def client(username, password):
    url = "https://pizzadev.cis294.hfcc.edu/api/login"

    data = {

        "username": username,
        "password": password,
    }

    response = requests.post(url, json=data)

    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
    
    body = response.json()
    
    return response

#==============================================================================================================================================================================================
# Creat window object
app = Tk()
app.title("Momma Maglione's Pizza")
app.geometry('980x480')
app.configure(background='black')
app.resizable(0, 0)

#==============================================================================================================================================================================================
# this function is to check the log in credintials (if the log in information is correct it takes the user to the main page where he can pick which functionality they want to use)    
def signin():
    global username
    global password
    username = user.get()
    password = code.get()
    response = client(username, password) 

    if response.status_code == 200:
        app.destroy()
        main()
        

    else:
        messagebox.showerror("Error", "You entered wrong credintals")

def get_username():
    
    username1 = username

    return username1
def get_password():
    password1 = password

    return password1
#==============================================================================================================================================================================================
# Log in page
img = PhotoImage(file='C:\Pizzashop\images\logo.PNG')

Label(app, image=img, bg='black').place(x=10, y=40)

frame = Frame(app, width=350, height=350, bg="white")
frame.place(x=550, y=70)

heading = Label(frame, text='Sign In', fg='black', bg='white', font=('', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    if user.get() == 'Username':
        user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter(e):
    if code.get() == "Password":
        code.delete(0, 'end')


def on_leave(e):
    passowrd = code.get()
    if passowrd == '':
        code.insert(0, 'Password')


code = Entry(frame, width=25, fg='black', border=0, bg='#fffafa', font=('', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

btn = Button(frame, width=15, height=2, text='Submit', bg='white', font=('', 13, 'bold'), command=signin).place(x=80,
                                                                                                                y=210)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)





#==============================================================================================================================================================================================
# this function is for the punch in punch out system
def punch_inout():
    screen = Tk()
    screen.title("Punch In and Punch Out")
    screen.state('zoomed')

    screen.configure(background='#f8f8ff')

   

    def punch_out():
        
        id1 = id.get()

        if id1 == '' or id1 == "Enter your ID":
            messagebox.showerror("Error", "you need to enter your Id to punch out")
        else:
            url = "https://pizzadev.cis294.hfcc.edu/api/timeOut"

            res = client(username, password)

            token = res.json()['token']
            head = {'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'}
            data = {
                "username": username,
                "userId": id1,
                "password": password
            }

            response = requests.post(url, json=data, headers=head)

            print("Status Code", response.status_code)
            print("JSON Response ", response.json())

            try:
                if (response.json()['message']):
                    messagebox.showinfo("Success", "punched out Successfully")
            except KeyError:
                messagebox.showerror("error", "punch out did not work!")    



    def punch_in():
        
        id1 = id.get()

        if  id1 == '' or id1 == "Enter your ID":
            messagebox.showerror("Error", "you need to enter your ID to punch in")
        else:
            url = "https://pizzadev.cis294.hfcc.edu/api/timeIn"

            res = client(username, password)

            token = res.json()['token']
            head = {'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'}
            data = {
                "username": username,
                "userId": id1,
                "password": password
            }

            response = requests.post(url, json=data, headers=head)

            print("Status Code", response.status_code)
            print("JSON Response ", response.json())

            try:
                if (response.json()['message']):
                    messagebox.showinfo("Success", "punched in Successfully")
            except KeyError:
                messagebox.showerror("error", "punch in did not work!")

          
                

            

           


    canvas = Canvas(

        width=1500,
        height=1500,
        bg='white'
    )
    canvas.pack(fill='both', expand=True)

    img = PhotoImage(file='C:\Pizzashop\images\pizza.PNG')
    img = resizeImage(img, 750, 800)

    canvas.create_image(
        0,
        0,
        anchor=NW,
        image=img
    )

    Label(canvas, text='Welcome to the punch in/ punch out system', fg='black', bg='white', font=('', 25, 'bold')).pack(anchor='ne', pady=5, padx=50)

    frame = Frame(canvas,bd=5, relief='solid', width=770, height=800, bg="white")
    frame.pack(anchor="e", padx=10, pady=10)

    Label(frame, text="Enter your ID, and then select clock-in or clock-out:", fg='black', border=0,
          bg='white', font=('', 18, 'bold')).place(x=50, y=50)

    

    def on_enter(e):
        if id.get() == "Enter your ID":
            id.delete(0, 'end')

    def on_leave(e):
        name1 = id.get()
        if name1 == '':
            id.insert(0, 'Enter your ID')


    id = Entry(frame, width=25, fg='black', border=0, bg='white', font=('', 18))
    id.place(x=180, y=170)
    id.insert(0, 'Enter your ID')
    id.bind('<FocusIn>', on_enter)
    id.bind('<FocusOut>', on_leave)
    Frame(frame, width=250, height=2, bg='black').place(x=180, y=200)

    clock_in_image = PhotoImage(file='C:\Pizzashop\images\clockin.PNG')

    clock_out_image = PhotoImage(file='C:\Pizzashop\images\clockout.PNG')

    Button(frame, width=150, height=100, image=clock_in_image, text='Clock In', font=('', 15, 'bold'), border=0, bg='white', command=punch_in).place(x=150, y=270)
    Button(frame, width=150, height=100, image=clock_out_image, text='Clock Out', font=('', 15, 'bold'), border=0, bg='white', command=punch_out).place(x=400, y=270)

    
    
    def exit_():
        screen.destroy()
        main()
        
        
    Button(frame, width=16, height=4, text='Exit', font=('', 15, 'bold'), command=exit_).place(x=270, y=520)

    

    screen.mainloop()
    

#==============================================================================================================================================================================================
# this function is for input the orders 
def input_order():
    screen = Tk()
    screen.title("Input Orders")
    screen.state('zoomed')

    screen.configure(background='#f8f8ff')

    canvas = Canvas(

        width=1500,
        height=1500,
        bg='white'
    )
    canvas.pack(fill='both', expand=True)

    img = PhotoImage(file='C:\Pizzashop\images\lasagna.PNG')
    img = resizeImage(img, 750, 800)

    canvas.create_image(
        0,
        0,
        anchor=NW,
        image=img
    )

    frame = Frame(canvas, bd=5, relief='solid', width=770, height=800, bg="#fff")
    frame.pack(anchor="ne", padx=10, pady=10)

    Label(frame, text='Input Customer orders', fg='black', bg='white', font=('', 20, 'bold')).place(x=190, y=10)

    add_button = PhotoImage(file='C:\Pizzashop\images\_add.PNG')

    Frame(frame, bd=5, relief='groove', width=760, height=100, bg="#fff").place(y=150)
    Frame(frame, bd=5, relief='groove', width=760, height=100, bg="#fff").place(y=250)
    Frame(frame, bd=5, relief='groove', width=760, height=100, bg="#fff").place(y=350)
    Frame(frame, bd=5, relief='groove', width=760, height=100, bg="#fff").place(y=450)
    Frame(frame, bd=5, relief='groove', width=760, height=100, bg="#fff").place(y=550)
    frame6 = Frame(frame, bd=5, relief='groove', width=760, height=100, bg="#fff").place(y=650)
    Frame(frame, bd=5, relief='groove', width=760, height=100, bg="#fff").place(y=50)

    cart = []

    

    def add_regular():

        customer_Address = customer_address.get().split(',')
        
        size = regular_size.get()
        topping = regular_toppings.get()
        type = order_type.get()
        quantity = qty.get()
        name = customer_name.get()
        phone = customer_phone.get()
        #address = customer_Address[0]
        #city = customer_Address[1]
        #state = customer_Address[2]
        #zipcode = customer_Address[3]


        if size != '12” Small' and size != '14” Medium' and size != '16” Large':

            messagebox.showerror("Error", "You have to enter pizza size!!")
        else:
            if size == '12” Small':
                order_id = 1
            elif size == '14” Medium':
                order_id = 2
            else:
                order_id = 3


        url = "https://pizzadev.cis294.hfcc.edu/api/order/add"

        username = get_username()
        password = get_password()
        

        res = client(username, password)

        employee_id = res.json()['user']

        token = res.json()['token']
        head = {'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'}

        data = {
        "id": order_id,
        "orderType": type,
        "CustomerId": 12,
        "EmployeeId": employee_id,
        "quantity": quantity,
        "toppings": topping
        }

        response = requests.post(url, json=data, headers=head)

        print("Status Code", response.status_code)
        print("JSON Response ", response.json())    

        if response.status_code == 200:
            messagebox.showinfo("Successfully","Successfully added to cart")
        else:
            messagebox.showerror("Error","Error while adding to cart")


    Label(frame, text="One Topping Pizza:", fg='black', bg='#fff', font=('', 16, 'bold')).place(y=60, x=20)
    Label(frame, text="Pizza Size:", fg='black', bg='#fff', font=('', 14)).place(y=90, x=80)
    regular_size = Combobox(frame, values=['12” Small', '14” Medium', '16” Large'])
    regular_size.place(y=95, x=180)
    Label(frame, text="Toppings:", fg='black', bg='#fff', font=('', 14)).place(y=90, x=350)
    regular_toppings = Combobox(frame,
                                values=['Bacon', 'Ham', 'Italian Sausage', 'Pepperoni', 'Ham', 'Bacon', 'Black Olives',
                                        'Fresh Tomatoes', 'Green Olives', 'Green Peppers', 'Pepperoncini', 'Jalapeños',
                                        'Mushrooms', 'Pineapple', 'Red Onions'])
    regular_toppings.place(y=95, x=450)
    Button(frame, image=add_button, text='Add', height=75, borderwidth=0, width=100, command=add_regular,
           font=('', 13, 'bold')).place(y=63,
                                        x=620)
    qty = Combobox(frame,width=4,
                                values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    qty.place(y=95, x=20)                                                                


    def add_toppings():
        
        
        size = toppings_size.get()
        topping = toppings.get().split(",")
        num_of_toppings = len(topping)

        if size == '12” Small $13' or size == '14” Medium $16' or size == '16” Large $19':
            if size == '12” Small $13':
                price = 13 + 2 * num_of_toppings
                size = '12” Small'
            elif size == '14” Medium $16':
                price = 16 + (2.5 * num_of_toppings)
                size = '14” Medium'
            else:
                price = 19 + (3 * num_of_toppings)
                size = '16” Large'

            regular = size + ' pizza topping: ' + toppings.get() + "  price: " + "$" + str(price) 
            messagebox.showinfo("Item added", "You have added the following item!\n" + regular)
            cart.append(regular)

        else:
            messagebox.showerror("Error", "You have to enter pizza size!!")

    Label(frame, text="Pizza with more toppings:", fg='black', bg='white', font=('', 16, 'bold')).place(y=160, x=20)
    Label(frame, text="Pizza Size:", fg='black', bg='#fff', font=('', 14)).place(y=190, x=80)
    toppings_size = Combobox(frame, values=['12” Small $13', '14” Medium $16', '16” Large $19'])
    toppings_size.place(y=195, x=180)
    Label(frame, text="Toppings:", fg='black', bg='#fff', font=('', 14)).place(y=190, x=340)
    toppings = Entry(frame, width=13, fg='black', bg='white', font=('', 14))
    toppings.place(y=190, x=440)
    Button(frame, image=add_button, text='Add', height=75, borderwidth=0, width=100, command=add_toppings,
           font=('', 13, 'bold')).place(y=163,
                                        x=620)
    qty1 = Combobox(frame,width=4,
                                values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    qty1.place(y=195, x=20)                                       

    def add_special():
        
        size = speciality_size.get()
        speciality = speciality_type.get()
        type = order_type.get()
        quantity = qty2.get()

        if speciality == 'Supreme' or speciality == 'Meat Lovers' or speciality == 'Checkin BBQ' or speciality == 'Hawaiian' or speciality == 'Vegitarian':
            if size == '12" Small $18' or size == '14" Medium $20' or size == '16" Large $22':
                if size == '12" Small $18':
                    if speciality == 'Supreme':
                        id = 4
                    elif speciality == 'Meat Lovers':
                        id = 7 
                    elif speciality == 'Checkin BBQ':
                        id = 10  
                    elif speciality == 'Hawaiian':
                        id = 13
                    else:
                        id = 16            
                elif size == '14" Medium $20':
                    if speciality == 'Supreme':
                        id = 5
                    elif speciality == 'Meat Lovers':
                        id = 8 
                    elif speciality == 'Checkin BBQ':
                        id = 11 
                    elif speciality == 'Hawaiian':
                        id = 14 
                    else:
                        id = 17                
                else:
                    if speciality == 'Supreme':
                        id = 6
                    elif speciality == 'Meat Lovers':
                        id = 9
                    elif speciality == 'Checkin BBQ':
                        id = 12 
                    elif speciality == 'Hawaiian':
                        id = 15 
                    else:
                        id = 18                  
            else:
                messagebox.showerror("Error", "You have to select pizza size!!")
        else:
            messagebox.showerror("Error", "You have to select pizza type!!")  

        url = "https://pizzadev.cis294.hfcc.edu/api/order/add"

        username = get_username()
        password = get_password()

        res = client(username, password)

        employee_id = res.json()['user']

        token = res.json()['token']
        head = {'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'}

        data = {
        "id": id,
        "orderType": type,
        "CustomerId": 12,
        "EmployeeId": employee_id,
        "quantity": quantity,
        "toppings": ""
        }

        response = requests.post(url, json=data, headers=head)

        print("Status Code", response.status_code)
        print("JSON Response ", response.json())    

        if response.status_code == 200:
            messagebox.showinfo("Successfully","Successfully added to cart")
        else:
            messagebox.showerror("Error","Error while adding to cart")             

    Label(frame, text="Specialty Pizza:", fg='black', bg='white', font=('', 16, 'bold')).place(y=260, x=20)
    Label(frame, text="Pizza Size:", fg='black', bg='#fff', font=('', 14)).place(y=290, x=80)
    speciality_size = Combobox(frame, values=['12" Small $18', '14" Medium $20', '16" Large $22'])
    speciality_size.place(y=295, x=180)
    Label(frame, text="Pizza Type:", fg='black', bg='#fff', font=('', 14)).place(y=290, x=350)
    speciality_type = Combobox(frame, values=['Supreme', 'Meat Lovers', 'Checkin BBQ', 'Hawaiian', 'Vegitarian'])
    speciality_type.place(y=295, x=450)
    Button(frame, image=add_button, text='Add', height=75, borderwidth=0, width=100, command=add_special,
           font=('', 13, 'bold')).place(y=263,
                                        x=620)
    qty2 = Combobox(frame,width=4,
                                values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    qty2.place(y=295, x=20)                                     

    def add_lasagna():
        order_id = 19
        type = order_type.get()
        quantity = qty2.get()

        url = "https://pizzadev.cis294.hfcc.edu/api/order/add"

        username = get_username()
        password = get_password()

        res = client(username, password)

        employee_id = res.json()['user']

        token = res.json()['token']
        head = {'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'}
            
        data = {
        "id": order_id,
        "orderType": type,
        "CustomerId": 12,
        "EmployeeId": employee_id,
        "quantity": quantity,
        "toppings": ""
        }

        response = requests.post(url, json=data, headers=head)

        print("Status Code", response.status_code)
        print("JSON Response ", response.json())    

        if response.status_code == 200:
            messagebox.showinfo("Successfully","Successfully added to cart")
        else:
            messagebox.showerror("Error","Error while adding to cart")
        

    Label(frame, text="Lasagna  $25", fg='black', bg='white', font=('', 16, 'bold')).place(y=379, x=100)
    Button(frame, image=add_button, text='Add', borderwidth=0, height=75, width=100, command=add_lasagna,
           font=('', 13, 'bold')).place(y=363,
                                        x=620)
    qty3 = Combobox(frame,width=4,
                                values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    qty3.place(y=395, x=20)                                     

    def add_breadsticks():
        size = breadsticks_size.get()
        quantity = qty4.get()
        type = order_type.get()
        bs_price = 0
        if size == '6 pc $5' or size == '12 pc $8':
            if size == '6 pc $5':
                id = 20
            elif size == '12 pc $8':
                id = 21
            url = "https://pizzadev.cis294.hfcc.edu/api/order/add"

            username = get_username()
            password = get_password()

            res = client(username, password)

            employee_id = res.json()['user']

            token = res.json()['token']
            head = {'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'}
                
            data = {
            "id": id,
            "orderType": type,
            "CustomerId": 12,
            "EmployeeId": employee_id,
            "quantity": quantity,
            "toppings": ""
            }

            response = requests.post(url, json=data, headers=head)

            print("Status Code", response.status_code)
            print("JSON Response ", response.json())    

            if response.status_code == 200:
                messagebox.showinfo("Successfully","Successfully added to cart")
            else:
                messagebox.showerror("Error","Error while adding to cart")
            
        else:
            messagebox.showerror("Error", "You have to select bread stick's size !!")

    Label(frame, text="Bread Sticks", fg='black', bg='white', font=('', 16, 'bold')).place(y=479, x=100)
    breadsticks_size = Combobox(frame, values=['6 pc $5', '12 pc $8'])
    breadsticks_size.place(y=495, x=250)
    Button(frame, image=add_button, text='Add', height=75, borderwidth=0, width=100, command=add_breadsticks,
           font=('', 13, 'bold')).place(y=463,
                                        x=620)
    qty4 = Combobox(frame,width=4,
                                values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    qty4.place(y=495, x=20)                                     

    def clear():
        speciality_size.delete(0, 'end')
        speciality_type.delete(0, 'end')
        regular_size.delete(0, 'end')
        regular_toppings.delete(0, 'end')
        toppings_size.delete(0, 'end')
        toppings.delete(0, 'end')
        breadsticks_size.delete(0, 'end')
        customer_name.delete(0, 'end')
        customer_phone.delete(0, 'end')
        customer_phone.insert(0, "Customer phone")
        customer_name.insert(0, 'Customer Name')
        qty.delete(0, 'end')
        qty1.delete(0, 'end')
        qty2.delete(0, 'end')
        qty3.delete(0, 'end')
        qty4.delete(0, 'end')
        order_type.delete(0, 'end')
        cart.clear()

    def show_order():
        display = Toplevel(screen)

        Label(display, text='Order Information: ', font=('', 14)).pack(side='top', anchor='w')
        for x in cart:
            Label(display, text=x, font=('', 14)).pack(side='top', anchor='w')

    clear_button = PhotoImage(file='C:\Pizzashop\images\clear.PNG')
    submit_button = PhotoImage(file='C:\Pizzashop\images\submit.PNG')
    print_button = PhotoImage(file='C:\Pizzashop\images\print.PNG')

    Button(frame, image=clear_button, text='', height=75, width=100, borderwidth=0, command=clear,
           font=('', 13, 'bold')).place(
        y=660, x=50)
    Button(frame, image=print_button, text='', height=75, width=125, borderwidth=0, command=show_order,
           font=('', 13, 'bold')).place(
        y=660, x=200)
    Button(frame, image=submit_button, text='', height=75, width=125, borderwidth=0, font=('', 13, 'bold')).place(
        y=660, x=375)

    def on_enter(e):
        if customer_name.get() == "Customer Name":
            customer_name.delete(0, 'end')

    def on_leave(e):
        name = customer_name.get()
        if name == '':
            customer_name.insert(0, 'Customer Name')

    Label(frame, text="Customer Information: ", fg='black', bg='white', font=('', 16, 'bold')).place(y=555, x=20)
    customer_name = Entry(frame, width=23, fg='black', bg='white', font=('', 14))
    customer_name.place(y=583, x=30)
    customer_name.insert(0, "Customer Name")
    customer_name.bind('<FocusIn>', on_enter)
    customer_name.bind('<FocusOut>', on_leave)

    Label(frame, text="pick up / delivery", fg='black', bg='white', font=('', 16, 'bold')).place(y=570, x=350)
    order_type = Combobox(frame,width=8,
                                values=['pick up', 'delivery'])
    order_type.place(y=575, x=530)    

    def on_enter(e):
        if customer_phone.get() == "Customer phone":
            customer_phone.delete(0, 'end')

    def on_leave(e):
        phone = customer_phone.get()
        if phone == '':
            customer_phone.insert(0, 'Customer phone')

    customer_phone = Entry(frame, width=23, fg='black', bg='white', font=('', 14))
    customer_phone.place(y=613, x=30)
    customer_phone.insert(0, "Customer phone")
    customer_phone.bind('<FocusIn>', on_enter)
    customer_phone.bind('<FocusOut>', on_leave)

    def on_enter(e):
        if customer_address.get() == "Customer Address":
            customer_address.delete(0, 'end')

    def on_leave(e):
        phone = customer_address.get()
        if phone == '':
            customer_address.insert(0, 'Customer Address')

    customer_address = Entry(frame, width=23, fg='black', bg='white', font=('', 14))
    customer_address.place(y=613, x=350)
    customer_address.insert(0, "Customer Address")
    customer_address.bind('<FocusIn>', on_enter)
    customer_address.bind('<FocusOut>', on_leave)

    def exit_():
        screen.destroy()
        main()
        
        
    Button(frame, width=15, height=2, text='Exit', font=('', 15, 'bold'), command=exit_).place(x=550, y=660)

    screen.mainloop()

#==============================================================================================================================================================================================
# this function is for displaying all the orders that has been placed 
def display_order():
    screen = Tk()
    screen.title("display orders")
    screen.state('zoomed')
    

    screen.configure(background='white')

    frame = Frame(screen, bd=5, relief='solid' , width=1570, height=800, bg="#fff")
    frame.pack(anchor="ne", padx= 10, pady=10)

    

    




    screen.mainloop()

#==============================================================================================================================================================================================
# this function is for displaying the Time Card
def display_timecard():
    screen = Tk()
    screen.title("display Time Report")

    screen.configure(background='white')

    url = "https://pizzadev.cis294.hfcc.edu/api/timecards"

    username = get_username()
    password = get_password()

    res = client(username, password)

    token = res.json()['token']
    head = {'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'}

    response = requests.get(url, headers=head)

    data = response.json()['data']
    data = json.dumps(data)
    data = json.loads(data)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
    print(data)


    trv = Treeview(screen, columns=(1, 2, 3, 4, 5), show='headings')
    trv.pack(anchor='ne')

    trv.heading(1, text='id', anchor='center')
    trv.heading(2, text='total hours', anchor='center')
    trv.heading(3, text='punch in', anchor='center')
    trv.heading(4, text='punch out', anchor='center')
    trv.heading(5, text='userId', anchor='center')

    trv.column("#1", anchor='center', width=140, stretch=False)
    trv.column("#2", anchor='center', width=140, stretch=True)
    trv.column("#3", anchor='center', width=160, stretch=True)
    trv.column("#4", anchor='center', width=160, stretch=True)
    trv.column("#5", anchor='center', width=140, stretch=True)


    for item in trv.get_children():
        trv.delete(item)

    rowIndex=1

    for key in data:
        id = key['id']
        totalhours = key['totalHours']
        punch_in = key['punchIn']
        punch_out = key['punchOut']
        username = key['userId']['username']
        trv.insert('', index='end', iid=rowIndex.__str__(), text="", values=(id, totalhours, punch_in, punch_out, username))
        rowIndex = rowIndex+1






   # dataFrame = pd.DataFrame.from_dict(response.json()['data'])
   # Label(screen, text=data.head().to_string(), fg='black', bg='white', font=('', 20, 'bold')).place(anchor='nw')

    screen.mainloop()

#==============================================================================================================================================================================================
# this function is for the main page after the user log in
def main():
    def punch_in_out():
        main.destroy()
        punch_inout()

    def order_input():
        main.destroy()
        input_order()    

    def order_display():
        main.destroy()
        display_order()
        
    
    main = Tk()
    main.title("Momma Maglione's Pizza")
    main.state('zoomed')

    
    

    main.configure(background='white')

    canvas = Canvas(

        width=1500,
        height=1500
    )
    canvas.pack(fill='both', expand=True)

    img = PhotoImage(file='C:\Pizzashop\images\main.PNG')

    img = resizeImage(img, 1550, 1400)

    canvas.create_image(
        0,
        0,
        anchor=NW,
        image=img
    )


    

   
    
    

    Button(canvas, width=17, height=5, text='Punch In/Out', fg='black', font=('', 15, 'bold'),
            command=punch_in_out).pack(side='left', padx=40, pady=100, expand=True)
    Button(canvas, width=17, height=5, text='Input Orders', bg='white', fg='black', font=('', 15, 'bold'),
           command=order_input).pack(side='left', padx=40, pady=100, expand=True)
    Button(canvas, width=17, height=5, text='Display Orders', bg='white', fg='black', font=('', 15, 'bold'),
           command=order_display).pack(side='left', padx=40, pady=100, expand=True)
    Button(canvas, width=17, height=5, text='Time Report', bg='white', fg='black', font=('', 15, 'bold'),
           command=display_timecard).pack(side='left', padx=40, pady=100, expand=True)
   

    main.mainloop()


#==============================================================================================================================================================================================

# Start the program
app.mainloop()
