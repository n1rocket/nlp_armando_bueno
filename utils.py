import os
import re
import glob
import lxml.etree as ET
from collections import namedtuple


def load_cinema_reviews(datasets_path, corpus_cine_folder):

	# Path de todas las reviews de cine en formato XML
	review_paths = glob.glob(
	    os.path.join(datasets_path, corpus_cine_folder, '*.xml')
	)

	reviews_dict = dict()
	sorted_review_paths = sorted(review_paths, key=lambda x: int(x.split(os.path.sep)[-1].split(".")[0]))

	for idx, srp in enumerate(sorted_review_paths):
	    parser = ET.XMLParser(encoding='ISO-8859-1', recover=True)
	    root = ET.parse(srp, parser=parser).getroot()
	    review = {
	        'author': root.get('author'),
	        'title': root.get('title'),
            'sentiment': root.get('rank'),
	        'summary': root[0].text,
	        'review_text': root[1].text
	    }    
	    reviews_dict.update({idx: review})

	return reviews_dict


def get_lemmas_dict(data_path, lemmas_dict_file):
    lemmas_dict = {}
    with open(os.path.join(data_path, lemmas_dict_file), 'r', encoding='utf-8') as f:
        for line in f:
            (key, val) = line.split()
            lemmas_dict[str(val)] = key
    return lemmas_dict


def load_movie_titles(datasets_path, movie_titles_file):
    '''read a text file containing movie titles, stored as "title (year)" '''
    MT = namedtuple('Movie', 'title year')
    matcher = lambda l: re.match(r'(.*\S)\s+\((\d+)\)', l)
    movie_tuple = lambda m: MT(m.group(1), int(m.group(2)))
    with open(os.path.join(datasets_path, movie_titles_file), 'r', encoding='utf-8') as f:
        titles = [movie_tuple(movie) 
                  for movie in map(matcher, f) if movie]
    return titles
