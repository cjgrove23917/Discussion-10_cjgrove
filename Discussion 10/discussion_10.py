import json
import unittest
import os
import re

def read_json(filename):
    '''
    Opens file filename, loads content as json object

    Parameters: 
        filename: name of file to be opened

    Returns: 
        json dictionary OR an empty dict if the file could not be opened 
    '''
    try:
        source_dir = os.path.dirname(__file__)
        full_path = os.path.join(source_dir, filename)
        file = open(full_path, 'r')
        contents = file.read()
        file.close()
        data = json.loads(contents)
        return data
    except:
        return {}

def shortest_book(books):
    """
    Returns the title of shortest book (in pages)

    Parameters: 
        books (dict): dict representations of a decoded JSON document

    Returns:
        string: the title of the shortest book
    """
    shortest_title = None
    fewest_pages = None
    for isbn, isbn_dict in books.items():
        inner_key = list(isbn_dict.keys())[0]
        details = isbn_dict[inner_key]['details']
        if 'number_of_pages' not in details:
            continue
        pages = details['number_of_pages']
        title = details['title']
        if fewest_pages is None or pages < fewest_pages:
            fewest_pages = pages
            shortest_title = title
    return shortest_title

def title_by_year(year, books):
    """
    returns a dictionary where the keys are authors and the values are their books, each book should be published in the year.

    Parameters: 
        books (dict): dict representations of a decoded JSON document
        year (int): publication year

    Returns:
        dictionary: a dict of authors and the titles of their books published in the given year
    """
    result = {}
 
    for isbn, isbn_dict in books.items():
        inner_key = list(isbn_dict.keys())[0]
        details = isbn_dict[inner_key]['details']
        if 'publish_date' not in details:
            continue
        publish_date = details['publish_date']
        if str(year) not in publish_date:
            continue
        title = details['title']
        authors = details.get('authors', [])
        for author in authors:
            author_name = author['name']
            if author_name not in result:
                result[author_name] = []
            result[author_name].append(title)
    return result

def publisher_by_letter(letter, books):
    """
    Returns a dictionary where the keys are publishers whose name begins with the letter passed into the function
    and the values are the titles of their books

    Parameters: 
    letter (str): a letter from A-Z
    books (dict): dict representations of a decoded JSON document

    Returns:
        dictionary: publishers whose name begins with the letter and the titles of their books

    """
    result = {}
    for isbn, isbn_dict in books.items():
        inner_key = list(isbn_dict.keys())[0]
        details = isbn_dict[inner_key]['details']
        if 'publishers' not in details:
            continue
        title = details['title']
        publishers = details['publishers']
        for publisher in publishers:
            if publisher.startswith(letter):
                if publisher not in result:
                    result[publisher] = []
                result[publisher].append(title)
    return result

#DO NOT CHANGE TEST CASES
class TestDiscussion11(unittest.TestCase):
    def setUp(self):
        self.books = read_json('books.json')

    def test_read_json(self):
        self.assertEqual(len(self.books), 25)


    def test_shortest_book(self):
        self.assertEqual(shortest_book(self.books), 'Where the Wild Things Are')

    def test_title_by_year(self):
        result = title_by_year(1987, self.books)
        self.assertIn('Stanisław Lem', result)
        self.assertIn('Solaris', result['Stanisław Lem'])
        self.assertEqual(len(result), 1, "There should only be one author with a book published in 1987")

        result2 = title_by_year(2006, self.books)
        self.assertEqual(len(result2), 3, "There should be three authors with books published in 2006")
        self.assertIn('Thomas Pynchon', result2)
        self.assertIn("Gravity's Rainbow (Penguin Classics Deluxe Edition)", result2['Thomas Pynchon'])
        self.assertIn("Gabriel García Márquez", result2)
        self.assertIn("One hundred years of solitude", result2['Gabriel García Márquez'])
        self.assertIn("Kazuo Ishiguro", result2)
        self.assertIn("Never Let Me Go", result2['Kazuo Ishiguro'])

    def test_publisher_by_letter(self):
        result = publisher_by_letter('P', self.books)
        self.assertEqual(len(result), 4)
        self.assertIn('Penguin Classics', result)
        self.assertIn("Gravity's Rainbow (Penguin Classics Deluxe Edition)", result['Penguin Classics'])
        self.assertEqual(len(result['Penguin Books']), 2)

        result2 = publisher_by_letter('H', self.books)
        self.assertEqual(len(result2), 6)
        self.assertIn('Harper Perennial Modern Classics', result2)
        self.assertIn('One hundred years of solitude', result2['Harper Perennial Modern Classics'])
        self.assertEqual(len(result2['HarperOne']), 1)

        result3 = publisher_by_letter('Z', self.books)
        self.assertEqual(result3, {})



def main():
    data = read_json('books.json')
    short_book = shortest_book(data)
    title_2006 = title_by_year(2006, data)

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)