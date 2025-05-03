class BORROWBOOKS:
    def __init__(self, user_data, book_data):
        self.user_data = user_data
        self.book_data = book_data
        self.current_user = None
        self.borrowed_books = []

    def login(self, account_number, pin):
        # Check if account number exists and the pin matches
        if account_number in self.user_data and \
                self.user_data[account_number].get('pin') == pin:
            self.current_user = account_number
            return True
        return False

    def borrow_book(self, book_id):
        if self.current_user and book_id in self.book_data:
            book = self.book_data[book_id]
            if book.get('available', False):
                # Mark the book as borrowed
                book['available'] = False
                self.user_data[self.current_user]['borrowed_books'].append(
                    book_id
                )
                return True
        return False

    def return_book(self, book_id):
        if self.current_user and book_id in \
                self.user_data[self.current_user]['borrowed_books']:
            book = self.book_data[book_id]
            # Mark the book as returned
            book['available'] = True
            self.user_data[self.current_user]['borrowed_books'].remove(book_id)
            return True
        return False

    def get_borrowed_books(self):
        # Return a list of borrowed books with details
        if self.current_user:
            borrowed_ids = self.user_data[self.current_user]['borrowed_books']
            return [
                {**self.book_data[book_id], 'book_id': book_id}
                for book_id in borrowed_ids
            ]
        return []

    def get_available_books(self):
        # Return a dictionary of available books with their details
        return {
            book_id: book
            for book_id, book in self.book_data.items()
            if book.get('available', False)
        }

    def search_books(self, **filters):
        # Search books by filters like title, author, genre, or year
        results = []
        for book_id, book in self.book_data.items():
            match = all(
                book.get(key) == value for key, value in filters.items()
            )
            if match and book.get('available', False):
                results.append({**book, 'book_id': book_id})
        return results

    def logout(self):
        # Logout current user and reset
        self.current_user = None
        return True
