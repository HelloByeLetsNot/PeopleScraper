import tkinter as tk
from bs4 import BeautifulSoup
import requests
import threading

def search():
    def do_search():
        # Get search terms from entry fields
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        criteria = criteria_entry.get()

        # Clear previous results
        results_frame.delete('1.0', tk.END)

        # Display search progress
        results_frame.insert(tk.END, "Searching...\n")
        results_frame.update()

        search_engines = {
            "Google": "https://www.google.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/html/?q=",
            "Brave": "https://search.brave.com/search?q=",
            "Yahoo": "https://search.yahoo.com/search?p=",
            "AOL": "https://search.aol.com/aol/search?q=",
            # Add more search engines here
        }
        for engine, url in search_engines.items():
            query = url + f"{first_name}+{last_name}+{criteria}".replace(' ', '+')
            response = requests.get(query)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('a', href=True)
            results_frame.insert(tk.END, f"{engine} Results:\n\n")
            for result in results:
                title = result.text
                link = result['href']
                if title and link and criteria.lower() in title.lower():
                    results_frame.insert(tk.END, f"{title}\n")
                    results_frame.tag_configure("link", foreground="blue", underline=True)
                    results_frame.tag_bind("link", "<Button-1>", lambda event, l=link: callback(l))
                    results_frame.insert(tk.END, "\n\n")
            results_frame.update()
        results_frame.insert(tk.END, "Search Completed!\n")

    # Create a new thread to perform the search
    search_thread = threading.Thread(target=do_search)
    search_thread.start()

def callback(link):
    import webbrowser
    webbrowser.open_new(link)

# GUI setup
root = tk.Tk()
root.title("Search Engine Scraper")

# Labels and entry fields
tk.Label(root, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Additional Criteria:").grid(row=2, column=0, padx=5, pady=5)
criteria_entry = tk.Entry(root)
criteria_entry.grid(row=2, column=1, padx=5, pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=search)
search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Results text widget
results_frame = tk.Text(root, height=20, width=80)
results_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
