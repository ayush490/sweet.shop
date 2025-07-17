import unittest
import pandas as pd
from sweet_app import (
    get_sweets,
    price_filter_sweets,
    category_filter_sweets,
    get_sorted,
    get_category,
    get_price,
    enter_new,
    delete_sweet,
    buy_sweets,
    restock
)

class TestSweetShop(unittest.TestCase):
    def setUp(self):
        # Use mock data instead of actual CSV
        self.df = pd.DataFrame([
            {'id': 1, 'name': 'Kaju Katli', 'category': 'Nut-based', 'price': 120, 'quantity': 50},
            {'id': 2, 'name': 'Rasgulla', 'category': 'Milk-based', 'price': 80, 'quantity': 100},
            {'id': 3, 'name': 'Gulab Jamun', 'category': 'Milk-based', 'price': 90, 'quantity': 80},
            {'id': 4, 'name': 'Soan Papdi', 'category': 'Flour-based', 'price': 70, 'quantity': 60},
            {'id': 5, 'name': 'Besan Ladoo', 'category': 'Flour-based', 'price': 85, 'quantity': 90},
            {'id': 6, 'name': 'Jalebi', 'category': 'Syrup-based', 'price': 75, 'quantity': 70},
            {'id': 7, 'name': 'Mysore Pak', 'category': 'Ghee-based', 'price': 100, 'quantity': 40},
            {'id': 8, 'name': 'Peda', 'category': 'Milk-based', 'price': 95, 'quantity': 60},
            {'id': 9, 'name': 'Lauki Halwa', 'category': 'Vegetable-based', 'price': 90, 'quantity': 45},
        ])

    def test_get_sweets(self):
        result = get_sweets(self.df)
        self.assertIn("Kaju Katli", result)
        self.assertIn("Rasgulla", result)

    def test_price_filter_sweets(self):
        result = price_filter_sweets(self.df, "70", "85")
        self.assertIn("Soan Papdi", result)
        self.assertIn("Jalebi", result)
        self.assertNotIn("Kaju Katli", result)

    def test_category_filter_sweets_valid(self):
        result = category_filter_sweets(self.df, "Nut-based")
        self.assertIn("Kaju Katli", result)

    def test_category_filter_sweets_invalid(self):
        result = category_filter_sweets(self.df, "NonExistent")
        self.assertIn("Incorrect Category", result)

    def test_get_sorted_by_price(self):
        result = get_sorted(self.df, 4, 1)  # sort by price ascending
        self.assertIn("Soan Papdi", result)

    def test_get_category(self):
        result = get_category(self.df)
        self.assertIn("Milk-based", result)
        self.assertIn("Flour-based", result)

    def test_get_price_valid(self):
        result = get_price(self.df, "Jalebi")
        self.assertIn("Rs. 75", result)

    def test_get_price_invalid(self):
        result = get_price(self.df, "Donut")
        self.assertIn("Sweet not available", result)

    def test_enter_new_existing_id(self):
        result = enter_new(self.df.copy(), 1, "New Sweet", "Other", 50, 10)
        self.assertIn("ID already exists", result)

    def test_enter_new_new_sweet(self):
        df_copy = self.df.copy()
        df_copy = df_copy[df_copy['id'] != 10]
        result = enter_new(df_copy, 10, "Donut", "Fried", 60, 20)
        self.assertIn("Successfully added Donut", result)

    def test_delete_sweet_valid(self):
        df_copy = self.df.copy()
        result = delete_sweet(df_copy, 2)
        self.assertIn("Successfully deleted", result)
        self.assertNotIn("Rasgulla", result)

    def test_delete_sweet_invalid(self):
        result = delete_sweet(self.df.copy(), 999)
        self.assertIn("Please enter a valid ID", result)

    def test_buy_sweets_valid(self):
        df_copy = self.df.copy()
        result = buy_sweets(df_copy, "Jalebi", 10)
        self.assertIn("Thank you for buying Jalebi", result)

    def test_buy_sweets_invalid_quantity(self):
        df_copy = self.df.copy()
        result = buy_sweets(df_copy, "Jalebi", 1000)
        self.assertIn("Sorry! Only", result)

    def test_buy_sweets_invalid_name(self):
        result = buy_sweets(self.df.copy(), "Donut", 2)
        self.assertIn("Invalid sweet name", result)

    def test_restock_valid(self):
        result = restock(self.df.copy(), "Jalebi", 5)
        self.assertIn("Stock updated successfully", result)

    def test_restock_invalid_sweet(self):
        result = restock(self.df.copy(), "Donut", 5)
        self.assertIn("Invalid sweet", result)

    def test_restock_invalid_quantity(self):
        result = restock(self.df.copy(), "Jalebi", -5)
        self.assertIn("Please enter a valid quantity", result)

if __name__ == '__main__':
    unittest.main()
