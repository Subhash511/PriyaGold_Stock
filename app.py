import streamlit as st
import pandas as pd
import sqlite3

# Initialize connection
conn = sqlite3.connect("stock_data.db", check_same_thread=False)
cursor = conn.cursor()

# Enable foreign key constraint
cursor.execute("PRAGMA foreign_keys = ON;")

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS db_master (
    db_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT,
    ss TEXT,
    db_name TEXT,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS month_table (
    month_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month_name TEXT UNIQUE,
    is_half_month BOOLEAN
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS sku_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku_name TEXT NOT NULL UNIQUE,
    category TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opening INTEGER,
    closing INTEGER,
    purchase INTEGER,
    sales INTEGER,
    db_id INTEGER,
    month_id INTEGER,
    sku_master_id INTEGER,
    FOREIGN KEY (db_id) REFERENCES db_master(db_id),
    FOREIGN KEY (month_id) REFERENCES month_table(month_id),
    FOREIGN KEY (sku_master_id) REFERENCES sku_master(id)
)
''')

conn.commit()


# ---------------- Streamlit UI ---------------- #

st.title("SQLite3 Foreign Key Demo - 4 Table Manager")

menu = st.sidebar.selectbox("Choose Table", ["DB Master", "Month Table","Sku_Master" ,"Stock Master"])

# 1. DB MASTER
if menu == "DB Master":
    st.header("DB Master")
    with st.form("db_form"):
        state = st.text_input("State")
        ss = st.text_input("SS")
        db_name = st.text_input("DB Name")
        password = st.text_input("Password")
        submitted = st.form_submit_button("Add Record")
        if submitted:
            cursor.execute("INSERT INTO db_master (state, ss, db_name, password) VALUES (?, ?, ?, ?)",
                           (state, ss, db_name, password))
            conn.commit()
            st.success("DB Master record added!")
    st.subheader("🔍 View DB Master Record")

    if st.button('Click to Show Db Master Data'):
        df_db = pd.read_sql_query("SELECT * FROM db_master", conn)
        st.dataframe(df_db)
        

    st.subheader('Delete Table')
    delete_id = int(st.number_input('Select id to delete',min_value=1))
    
    if st.button(f'Delete table id {delete_id}'):
        cursor.execute(f"DELETE FROM month_table WHERE month_id ={delete_id}")
        conn.commit()
        
            

# 2. MONTH TABLE
elif menu == "Month Table":
    st.header("Month Table")
    with st.form("month_form"):
        month_name = st.text_input("Month Name")
        is_half_month = st.checkbox("Is Half Month?")
        submitted = st.form_submit_button("Add Month")
        if submitted:
            try:
                cursor.execute("INSERT INTO month_table (month_name, is_half_month) VALUES (?, ?)",
                            (month_name, int(is_half_month)))
                conn.commit()
                st.success("Month record added!")
            except sqlite3.IntegrityError:
                st.error(f"The month '{month_name}' already exists. Please enter a unique name.")
    if st.button('Click to Show Month Table'):
        st.subheader("🔍 View Month Record")
        df_month = pd.read_sql_query("SELECT * FROM month_table", conn)

        st.dataframe(df_month)

                


    st.subheader("All Month Records")

    st.subheader('Delete Table')
    delete_id = int(st.number_input('Select id to delete',min_value=1))
    
    if st.button(f'Delete table id {delete_id}'):
        cursor.execute(f"DELETE FROM month_table WHERE month_id ={delete_id}")
        conn.commit()
        
            
# 3. Sku_Master
elif menu == "Sku_Master":
    st.subheader("➕ Add SKU Master Entry")
    with st.form("add_sku_form"):
        new_sku_name = st.text_input("SKU Name")
        category = ['Bis','Conf','Noodle','Juice']
        new_category = st.selectbox("Select Category",category)
        submitted = st.form_submit_button("Add SKU")
        if submitted:
            try:
                cursor.execute("INSERT INTO sku_master (sku_name, category) VALUES (?, ?)", (new_sku_name, new_category))
                conn.commit()
                st.success("SKU added successfully!")
            except sqlite3.IntegrityError:
                st.error("SKU name must be unique.")
    if st.button('Click to Show Sku Table'):
        st.subheader("🔍 View Sku Record")
        df_stock = pd.read_sql_query("SELECT * FROM sku_master", conn)
        st.dataframe(df_stock) 
    st.subheader('Delete Table')
    delete_id = int(st.number_input('Select id to delete',min_value=1))
    
    if st.button(f'Delete table id {delete_id}'):
        cursor.execute(f"DELETE FROM month_table WHERE month_id ={delete_id}")
        conn.commit()
                      


# 4. STOCK MASTER
elif menu == "Stock Master":
    st.header("Stock Master")
    dbs = cursor.execute("SELECT db_id, db_name FROM db_master").fetchall()
    sku = cursor.execute("SELECT id, sku_name FROM sku_master").fetchall()
    months = cursor.execute("SELECT month_id, month_name FROM month_table").fetchall()

    db_options = {f"{row[1]} (ID:{row[0]})": row[0] for row in dbs}
    sku_options = {f"{row[1]} (ID:{row[0]})": row[0] for row in sku}
    month_options = {f"{row[1]} (ID:{row[0]})": row[0] for row in months}

    with st.form("stock_form"):
        sku_id = st.selectbox('Sku id',sku_options.keys())

        opening = st.number_input("Opening", step=1)
        closing = st.number_input("Closing", step=1)
        purchase = st.number_input("Purchase", step=1)
        sales = st.number_input("Sales", step=1)
        db_id = st.selectbox("DB ID", db_options.keys())
        month_id = st.selectbox("Month ID", month_options.keys())
        submitted = st.form_submit_button("Add Stock Record")
        if submitted:
            cursor.execute('''
                INSERT INTO stock_master (opening, closing, purchase, sales, db_id, month_id,sku_master_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ( opening, closing, purchase, sales, db_options[db_id], month_options[month_id]),sku_options[sku_id])
            conn.commit()
            st.success("Stock record added!")
        
    if st.button('Click to Show Stock Table'):
        st.subheader("🔍 View Stock Record")
        df_stock = pd.read_sql_query("SELECT * FROM stock_master", conn)
        st.dataframe(df_stock)

    st.subheader('Delete Table')
    delete_id = int(st.number_input('Select id to delete',min_value=1))
    
    if st.button(f'Delete table id {delete_id}'):
        cursor.execute(f"DELETE FROM month_table WHERE month_id ={delete_id}")
        conn.commit()
            
                
