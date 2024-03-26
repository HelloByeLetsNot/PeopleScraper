import tkinter as tk
from bs4 import BeautifulSoup
import requests
import threading
import webbrowser

# Words to exclude from the output
exclude_words = [
    "Google", "here", "Images", "News", "Videos", "Maps", "Shopping",
    "Books", "Search tools", "Past hour", "Past 24 hours", "Past week",
    "Past month", "Past year", "Verbatim", "Next >", "Learn More", "Sign in", "Settings",
    "Terms", "Dark theme: Off", "email us", "Goggles", "Next", "Brave Search Premium", "Brave Search Help",
    "Transparency Report", "Report a security issue", "Status", "Brave Browser", "Brave Search",
    "Brave Wallet", "Brave Talk", "Mail", "Next", "Past", "Sign out", "Settings", "Settings," "Home",
    " Home", "Mail", "Finance", "Fantasy", "Sports", "Weather", "Lifestyle", "Help", "Settings",
    "Local", "More", "Past day," "Anytime"
]

class SearchEngineScraper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search Engine Scraper")
        self.setup_ui()

    def setup_ui(self):
        # Labels and entry fields
        tk.Label(self, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Additional Criteria:").grid(row=2, column=0, padx=5, pady=5)
        self.criteria_entry = tk.Entry(self)
        self.criteria_entry.grid(row=2, column=1, padx=5, pady=5)

        # Search button
        self.search_button = tk.Button(self, text="Search", command=self.search)
        self.search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Results text widget
        self.results_frame = tk.Text(self, height=20, width=80)
        self.results_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def search(self):
        # Clear previous results
        self.results_frame.delete('1.0', tk.END)

        # Get search terms from entry fields
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        criteria = self.criteria_entry.get()

        # Display search progress
        self.results_frame.insert(tk.END, "Searching...\n")
        self.results_frame.update()

        # Create and start a thread to perform the search
        search_thread = threading.Thread(target=self.do_search, args=(first_name, last_name, criteria))
        search_thread.start()

    def do_search(self, first_name, last_name, criteria):
        search_engines = {
            "Google": "https://www.google.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/html/?q=",
            "Brave": "https://search.brave.com/search?q=",
            "Yahoo": "https://search.yahoo.com/search?p=",
            "AOL": "https://search.aol.com/aol/search?q=",
            "Pastebin": "https://pastebin.com/search?q=",
            "Pst.innomi.net": "https://pst.innomi.net/search.php?q="
            # Add more search engines here
        }

        for engine, url in search_engines.items():
            if engine == "Doxbin":  # Skip Doxbin
                continue
            query = url + f"{first_name}+{last_name}+{criteria}".replace(' ', '+')
            response = requests.get(query)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('a', href=True)
            self.results_frame.insert(tk.END, f"{engine} Results:\n\n")
            for result in results:
                title = result.text
                link = result['href']
                if link.startswith("http"):  # Ensure the link starts with "http" to be valid
                    if title and link and criteria.lower() in title.lower() and not self.is_ad(result) and not any(word in title for word in exclude_words):
                        self.results_frame.tag_config("link", foreground="blue", underline=1)
                        self.results_frame.insert(tk.END, f"{title}\n", "link")
                        self.results_frame.tag_bind("link", "<Button-1>", lambda event, url=link: webbrowser.open_new(url))
                        self.results_frame.insert(tk.END, f"{link}\n\n")
            self.results_frame.update()
        self.results_frame.insert(tk.END, "Search Completed!\n")

    def is_ad(self, result):
        # Check if the result element or its ancestors have classes or attributes commonly associated with ads
        ad_classes = ['ads', 'ad', 'advertisement', 'sponsor']
        for cls in ad_classes:
            if cls in result.get('class', []) or cls in [ancestor.get('class', []) for ancestor in result.parents]:
                return True
        return False

# Create and run the application
if __name__ == "__main__":
    app = SearchEngineScraper()
    app.mainloop()
