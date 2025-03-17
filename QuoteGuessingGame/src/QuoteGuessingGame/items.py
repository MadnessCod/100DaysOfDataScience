import sqlite3


class QuotesItem:
    """
    this class is used to save scraped data from scraper.py to sqlite3 database
    :param *items: scraped data from scraper.py, items are in specific format
        items = (quotes_string, author, author_link, list(tags), list(tags_link))
    :type *items: list
    """

    def __init__(self, *items) -> None:
        self.items = list(items)
        self.con = sqlite3.connect("quotes.db")
        self.cur = self.con.cursor()
        self.database_initialization()

    def database_initialization(self):
        """
        creates three tables: author, tag, quote using sqlite3 database
        :return: None
        """
        self.cur = self.con.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS tag(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        link TEXT NOT NULL);
        """
        )

        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS author(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        link TEXT NOT NULL,
        born INTEGER,
        location TEXT,
        description TEXT);
        """
        )

        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS quote(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL, 
            author INTEGER,
            FOREIGN KEY (author) REFERENCES author(id) ON DELETE CASCADE);
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS quote_tag(
            quote_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY(quote_id) REFERENCES quote(id) ON DELETE CASCADE,
            FOREIGN KEY(tag_id) REFERENCES tag(id) ON DELETE CASCADE,
            PRIMARY KEY (quote_id, tag_id));
            """
        )



if __name__ == "__main__":
    pass
