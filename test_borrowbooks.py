import unittest
from borrowbooks import BORROWBOOKS
from data import users, books


class TestBORROWBOOKS(unittest.TestCase):
    def setUp(self):
        # Initialize BORROWBOOKS with a fresh copy of user and book data
        self.library = BORROWBOOKS(users.copy(), books.copy())

    def test_login_success(self):
        # Test successful login with correct account number and PIN
        self.assertTrue(self.library.login("raejohn", "1234"))
        self.assertEqual(self.library.current_user, "raejohn")

    def test_login_fail_wrong_pin(self):
        # Test login failure with incorrect PIN
        self.assertFalse(self.library.login("raejohn", "0000"))
        self.assertIsNone(self.library.current_user)

    def test_login_fail_nonexistent_user(self):
        # Test login failure with non-existent account number
        self.assertFalse(self.library.login("nonexistent_user", "1234"))
        self.assertIsNone(self.library.current_user)

    def test_borrow_book_success(self):
        # Test successful borrowing of an available book
        self.library.login("raejohn", "1234")
        result = self.library.borrow_book("book1")
        self.assertTrue(result)
        self.assertIn("book1", 
                      self.library.user_data["raejohn"]["borrowed_books"])
        self.assertFalse(self.library.book_data["book1"]["available"])

    def test_borrow_book_fail_unavailable(self):
        # Test failure to borrow a book that is already borrowed
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        self.library.logout()

        self.library.login("regie", "4321")
        result = self.library.borrow_book("book1")
        self.assertFalse(result)
        self.assertNotIn("book1", 
                         self.library.user_data["regie"]["borrowed_books"])

    def test_borrow_book_fail_not_logged_in(self):
        # Test failure to borrow a book when not logged in
        result = self.library.borrow_book("book1")
        self.assertFalse(result)

    def test_return_book_success(self):
        # Test successful return of a borrowed book
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        result = self.library.return_book("book1")
        self.assertTrue(result)
        self.assertNotIn("book1", 
                         self.library.user_data["raejohn"]["borrowed_books"])
        self.assertTrue(self.library.book_data["book1"]["available"])

    def test_return_book_fail_unborrowed(self):
        # Test failure to return a book that was not borrowed
        self.library.login("123456", "1234")
        result = self.library.return_book("book2")
        self.assertFalse(result)

    def test_return_book_fail_not_logged_in(self):
        # Test failure to return a book when not logged in
        result = self.library.return_book("book1")
        self.assertFalse(result)

    def test_get_borrowed_books(self):
        # Test retrieval of borrowed books list
        self.library.login("123456", "1234")
        self.library.borrow_book("book1")
        self.library.borrow_book("book2")
        borrowed_books = self.library.get_borrowed_books()
        self.assertEqual(len(borrowed_books), 2)
        self.assertIn("book1", [book["book_id"] for book in borrowed_books])
        self.assertIn("book2", [book["book_id"] for book in borrowed_books])

    def test_get_borrowed_books_empty(self):
        # Test retrieval of borrowed books list when none are borrowed
        self.library.login("123456", "1234")
        borrowed_books = self.library.get_borrowed_books()
        self.assertEqual(len(borrowed_books), 0)

    def test_get_available_books(self):
        # Test retrieval of available books
        self.library.login("123456", "1234")
        self.library.borrow_book("book1")
        available_books = self.library.get_available_books()
        self.assertNotIn("book1", available_books)
        self.assertIn("book2", available_books)

    def test_search_books_by_title(self):
        # Test searching books by title
        results = self.library.search_books(title="1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "1984")

    def test_search_books_by_author(self):
        # Test searching books by author
        results = self.library.search_books(author="J.R.R. Tolkien")
        self.assertEqual(len(results), 2)
        self.assertIn("The Lord of the Rings", 
                      [book["title"] for book in results])
        self.assertIn("The Hobbit", 
                      [book["title"] for book in results])

    def test_search_books_no_results(self):
        # Test searching books with no matching results
        results = self.library.search_books(title="Nonexistent Book")
        self.assertEqual(len(results), 0)

    def test_logout(self):
        # Test logging out
        self.library.login("123456", "1234")
        self.library.logout()
        self.assertIsNone(self.library.current_user)

    def test_borrow_book_multiple_users(self):
        # Test borrowing books with multiple users
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        self.library.logout()

        self.library.login("regie", "4321")
        result = self.library.borrow_book("book2")
        self.assertTrue(result)
        self.assertIn("book2", self.library.user_data["regie"]["borrowed_books"])

    def test_return_book_multiple_users(self):
        # Test returning books with multiple users
        self.library.login("raejohn", "1234")
        self.library.borrow_book("book1")
        self.library.logout()

        self.library.login("regie", "4321")
        result = self.library.return_book("book1")
        self.assertFalse(result)

        self.library.login("raejohn", "1234")
        result = self.library.return_book("book1")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
