import numpy as np
import shared
import math

"""
Function to run problem one solution and generate the heat maps.
@param article_path: path to articles file
@param label_path: path to mapping of articles to groups
@param groups_path: path to file mapping of group ids to names
@param output_path: output perfix for heatmaps
"""
def main(article_path="./Data/data50.csv", label_path="./Data/label.csv", groups_path="./Data/groups.csv", output_path="./Heatmap"):
    shared.setup(article_path, label_path, groups_path)
    group_list = list(shared.group_id_to_articles.keys())
    group_names = [shared.group_id_to_name[gid] for gid in group_list]
    num_groups = len(group_list)
    jacc_similarity_vals = np.zeros((num_groups, num_groups))
    l2_similarity_vals = np.zeros((num_groups, num_groups))
    cos_similarity_vals = np.zeros((num_groups, num_groups))
    print("Comparing groupings")

    # Leverage symmetric property of underlying similarity functions for a runtime optimization to avoid unnecessary iterations
    for ind in range(num_groups):
        for ind_two in range(ind, num_groups):
            num_completed_iters = ind
            end_val = num_groups - (num_completed_iters - 1)
            current_iters = (ind_two + 1) - ind
            print("\tComparing group {0} of 210".format(int((num_completed_iters * (num_groups + end_val)/2) + current_iters)))
            jacc_similarity, l2_similarity, cos_similarity = similarity(shared.group_id_to_articles[group_list[ind]], shared.group_id_to_articles[group_list[ind_two]])
            jacc_similarity_vals[ind, ind_two] = jacc_similarity
            l2_similarity_vals[ind, ind_two] = l2_similarity
            cos_similarity_vals[ind, ind_two] = cos_similarity
            
            # set inverse values
            jacc_similarity_vals[ind_two, ind] = jacc_similarity
            l2_similarity_vals[ind_two, ind] = l2_similarity
            cos_similarity_vals[ind_two, ind] = cos_similarity
    print("Plotting Jaccard heatmap")
    shared.makeHeatMap(jacc_similarity_vals, group_names, output_path, "Jaccard")

    print("Plotting L2 heatmap")
    shared.makeHeatMap(l2_similarity_vals, group_names, output_path, "L2", round='%.1f')

    print("Plotting Cosine heatmap")
    shared.makeHeatMap(cos_similarity_vals, group_names, output_path, "Cosine")
    print("Completed plotting")

"""
Function to generate similarity metrics between two article groups.
@param article_list_one: Articles from one group to compare
@param article_list_two: Articles from another group to compare the first list to
@return: Returns a three-tuple of averaged similarities for all three similarity metrics, across all articles in each group.
"""
def similarity(article_list_one, article_list_two):
    counter = 0
    jaccard = 0.0
    l2 = 0.0
    cos = 0.0
    for article_one in article_list_one:
        for article_two in article_list_two:
            if (article_one.id == article_two.id and article_one.group_id == article_two.group_id):
                continue
            jacc_min_sum = 0.0
            jacc_max_sum = 0.0
            l2_diff_sum = 0.0
            cos_prod_sum = 0.0
            cos_x_sum = 0.0
            cos_y_sum = 0.0
            for word in set(article_one.word_counts.keys()).union(set(article_two.word_counts.keys())):
                xi = article_one.get_count(word)
                yi = article_two.get_count(word)

                # Jaccard summation
                jacc_min_sum += min(xi, yi)
                jacc_max_sum += max(xi, yi)

                # L2 summation
                l2_diff_sum += math.pow((xi-yi), 2)

                # Cosine summation
                cos_prod_sum += xi * yi
                cos_x_sum += math.pow(xi, 2)
                cos_y_sum += math.pow(yi, 2)

            # compute jaccard
            jaccard += jacc_min_sum/jacc_max_sum

            # compute l2
            l2 += math.sqrt(l2_diff_sum) * -1.0

            # compute cosine
            cos += cos_prod_sum / (math.sqrt(cos_x_sum) * math.sqrt(cos_y_sum))
            counter += 1
    return jaccard/counter, l2/counter, cos/counter

if __name__ == '__main__':
    main()
