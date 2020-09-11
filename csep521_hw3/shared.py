import matplotlib.pyplot as plt
import numpy as np
import math
import warnings

group_id_to_name = dict()
group_id_to_articles = dict()
reduction_matrix = None
num_words = -1

"""
Provided helper function for generating HeatMap Graphs
"""
def makeHeatMap(data, names, outputFileName, mode, accuracy=-1, d=-1, color=plt.cm.Blues, round='%.2f'):
	#to catch "falling back to Agg" warning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
		#code source: http://stackoverflow.com/questions/14391959/heatmap-in-matplotlib-with-pcolor
        fig, ax = plt.subplots(figsize=(12,12))
        title = "{} Similarity Matrix".format(mode)
        if d > 0:
            title += "\nd = {0}".format(d)
        
        if accuracy >= 0.0:
            title += "\naccuracy = {0:.4g}%".format(accuracy)
                
        ax.set_title(title, fontsize=20)
		#create the map w/ color bar legend
        heatmap = ax.pcolor(data, cmap=color)
        cbar = plt.colorbar(heatmap)

		# put the major ticks at the middle of each cell
        ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
        ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

		# want a more natural, table-like display
        ax.invert_yaxis()
        ax.xaxis.tick_top()

        ax.set_xticklabels(names, rotation=45, ha='left')
        ax.set_yticklabels(names)

        for y in range(data.shape[0]):
            for x in range(data.shape[1]):
                plt.text(x + 0.5, y + 0.5, round % data[y, x],
                        horizontalalignment='center',
                        verticalalignment='center',
                        )

        plt.tight_layout()
        filename_suffix = "{0}_{1}".format(mode, d) if d > 0 else mode
        plt.savefig("{0}_{1}.png".format(outputFileName, filename_suffix), format = 'png')
        plt.close()

"""
Function to help steup problems one & two but initiating parse.
@param article_path: the path to the article data
@param label_path: the path to the article to group mapping file
@param groups_path: the path to the group id to name data mapping file
"""
def setup(article_path, label_path, groups_path):
    global group_id_to_name
    group_id_to_name = parse_ind_to_val(groups_path)
    parse_articles(article_path, label_path)
    return num_words


"""
Function to help in fully parsin an article.
@param article_path: the path to the article data
@param label_path: the path to the article to group mapping file
"""
def parse_articles(article_path, label_path):
    global group_id_to_articles
    article_to_group = parse_ind_to_val(label_path)
    article_iterator = open(article_path, "r")
    in_progress = True
    next_line = next(article_iterator).strip()
    while in_progress:
        remaining_content, article, next_line = generate_article(next_line, article_iterator)
        group_id = article_to_group[article.id]
        if group_id not in group_id_to_articles:
            group_id_to_articles[group_id] = []
        article.group_id = group_id
        group_id_to_articles[group_id].append(article)
        in_progress = remaining_content

"""
Function generate dictionary given a file, where the keys are the file indices
@param file_path: the path to the file
@return: the generated dictionary
"""
def parse_ind_to_val(file_path):
    ind_to_val = dict()
    for ind, line in enumerate(open(file_path, "r")):
        split_line = line.strip().split(",")
        ind_to_val[str(ind + 1)] = split_line[0]
    return ind_to_val

"""
Function to generate article given input file data
@param first_line: the first list of the article data in the data file
@param article_iterator: the iterator to iterate over the data file
@return: the generated article
"""
def generate_article(first_line, article_iterator):
    global num_words
    article_id, word_id, count = first_line.strip().split(",")
    article = Article(article_id)
    article.add_word_count(word_id, count)
    while True:
        try:
            next_line = next(article_iterator)
            next_article_id, next_word_id, next_count = next_line.strip().split(",")
            # capture the total number of word (leverging the fact that word ids increment in values of 1)
            if int(next_word_id) > num_words:
                num_words = int(next_word_id)
            if article_id != next_article_id:
                return True, article, next_line
            article.add_word_count(next_word_id, next_count)
        except StopIteration:
            return False, article, None

"""
Function to merge all articles into one flattened list
@return: The flattened list of all articles
"""
def generate_article_list():
    return [art for grp in group_id_to_articles.keys() for art in group_id_to_articles[grp]]


"""
Function to run find the nearest neighbor to an article
@param article_list: The complete list of articles to search for the nearest neighbor in
@param article_one: The article to find the nearest neighbor for
@return: The nearest neighbor to the given article
"""
def find_nearest_neighbor(article_list, article_one):
    max_cos_similarity = 0
    nearest_neighbor = None
    for article_two in article_list:
        if (article_one.id == article_two.id and article_one.group_id == article_two.group_id):
            continue
        cos_prod_sum = 0.0
        cos_x_sum = 0.0
        cos_y_sum = 0.0
        for word in set(article_one.word_counts.keys()).union(set(article_two.word_counts.keys())):
            xi = article_one.get_count(word)
            yi = article_two.get_count(word)
            cos_prod_sum += xi * yi
            cos_x_sum += math.pow(xi, 2)
            cos_y_sum += math.pow(yi, 2)
        denominator = (math.sqrt(cos_x_sum) * math.sqrt(cos_y_sum))
        cos = 0
        if denominator != 0:
            cos = cos_prod_sum / denominator
        if nearest_neighbor == None or cos > max_cos_similarity:
            max_cos_similarity = cos
            nearest_neighbor = article_two
    return nearest_neighbor


"""
Class to hold article objects and perform sumple functions on article data.
"""
class Article:
    def __init__(self, article_id):
        self.id = article_id
        self.group_id = None
        self.word_counts = dict()
    
    def add_word_count(self, word_id, count):
        self.word_counts[word_id] = int(count)
    
    def get_count(self, word_id):
        if word_id in self.word_counts:
            return self.word_counts[word_id]
        else:
            return 0

    def vector_to_count(self, vector):
        self.reset_counts()
        for ind, count in enumerate(vector):
            if count > 0:
                self.word_counts[ind] = count

    def word_count_vector(self):
        count_vector = np.zeros((num_words))
        for word_id, count in self.word_counts.items():
            count_vector[int(word_id) - 1] = count
        return count_vector
        
    def reset_counts(self):
        self.word_counts = dict()