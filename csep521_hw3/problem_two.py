import numpy as np
import shared
import math
import sys

"""
Function to run problem two solution and generate the accuracy & heat maps.
@param d: the dimension d to reduce the full dimensions to
@param article_path: path to articles file
@param label_path: path to mapping of articles to groups
@param groups_path: path to file mapping of group ids to names
@param output_path: output perfix for heatmaps
"""
def main(d=-1, article_path="./Data/data50.csv", label_path="./Data/label.csv", groups_path="./Data/groups.csv", output_path="./Heatmap"):
    shared.setup(article_path, label_path, groups_path)
    d = -1
    if (len(sys.argv) > 1):
        d = int(sys.argv[1])
        print("Running dimensionality reduction for dimension {0}".format(d))
        dimension_reduction(d)
    print("Generating article list")
    articles_list = shared.generate_article_list()
    num_articles = len(articles_list)
    neighbor_group_counts = dict()
    print("Building nearest neighbor classification")
    correct_count = 0
    article_count = 0
    for ind, article in enumerate(articles_list):
        print("\tFinding nearest neighbor for {0} of {1} articles".format(ind, num_articles))
        nearest_neighbor = shared.find_nearest_neighbor(articles_list, article)
        
        if article.group_id not in neighbor_group_counts:
            neighbor_group_counts[article.group_id] = dict()
        
        if nearest_neighbor.group_id not in neighbor_group_counts[article.group_id]:
            neighbor_group_counts[article.group_id][nearest_neighbor.group_id] = 0
        
        neighbor_group_counts[article.group_id][nearest_neighbor.group_id] += 1
        
        if article.group_id == nearest_neighbor.group_id:
            correct_count += 1
        article_count += 1
    accuracy = (correct_count/article_count) * 100.0
    group_names = [shared.group_id_to_name[str(gid + 1)] for gid in range(len(shared.group_id_to_name))]
    num_groups = len(group_names)
    classify_matrix = np.zeros((num_groups, num_groups))

    print("Building classification matrix")
    for group_id, group_counts in neighbor_group_counts.items():
        total_count = sum(group_counts.values())
        for neighbor_group_id, neighbor_count in group_counts.items():
            classify_matrix[int(group_id) - 1, int(neighbor_group_id) - 1] = neighbor_count/total_count
    
    print("Plotting classification heatmap")
    shared.makeHeatMap(classify_matrix, group_names, output_path, "Classify", accuracy, d)
    print("Accuracy: {0}%".format(accuracy))


"""
Function to reduce dimensionality of the input data
@param d: the dimensionality to reduce to
"""
def dimension_reduction(d):
    global reduction_matrix
    reduction_matrix = np.random.normal(0.0, 1.0, (d, shared.num_words))
    
    for article_list in shared.group_id_to_articles.values():
        for article in article_list:
            article.vector_to_count(reduction_matrix.dot(article.word_count_vector()))

if __name__ == '__main__':
    main()