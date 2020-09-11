from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import sys

nucleo_counts = dict()
index_by_population = dict()
index_by_gender = dict()
num_nucleos = 0
num_persons = 995
color_strings = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
population_strings = {
    "ACB":"African Caribbeans in Barbados (ACB)",
    "GWD":"Gambian in Western Divisions in the Gambia (GWD)",
    "ESN":"Esan in Nigeria (ESN)",
    "MSL":"Mende in Sierra Leone (MSL)",
    "YRI":"Yoruba in Ibadan, Nigeria (YRI)",
    "LWK":"Luhya in Webuye, Kenya (LWK)",
    "ASW":"Americans of African Ancestry in SW USA (ASW)",
}

def main(nucleo_path="./Data/nucleotides.txt", output_path="./Plot"):
    print("\n\tParsing data and generating person list")
    person_list = parse_text(nucleo_path)

    print("\n\tGenerating matrix")
    mat = generate_matrix(person_list)
    centered_mat = mat - np.mean(mat, axis = 0)
    
    pca = PCA(n_components=4)
    print("\n\tFitting PCAs")
    pca.fit(centered_mat)

    print("\n\tGenerating Plots")
    generate_scatter_plot(np.tensordot(centered_mat, pca.components_, axes=([1],[1])), index_by_population, (0,1), ("Population", "Component 1", "Component 2"))
    generate_scatter_plot(np.tensordot(centered_mat, pca.components_, axes=([1],[1])), index_by_gender, (0,1), ("Gender", "Component 1", "Component 2"))
    generate_scatter_plot(np.tensordot(centered_mat, pca.components_, axes=([1],[1])), index_by_population, (0,2), ("Population", "Component 1", "Component 3"))
    generate_scatter_plot(np.tensordot(centered_mat, pca.components_, axes=([1],[1])), index_by_gender, (0,2), ("Gender", "Component 1", "Component 3"))
    generate_scatter_plot(np.tensordot(centered_mat, pca.components_, axes=([1],[1])), index_by_population, (0,3), ("Population", "Component 1", "Component 4"))
    generate_scatter_plot(np.tensordot(centered_mat, pca.components_, axes=([1],[1])), index_by_gender, (0,3), ("Gender", "Component 1", "Component 4"))

    generate_scatter_plot_ind(np.absolute(pca.components_[2]), index_by_population, ("Nucleobase Index", "Component 3 Coefficient"))
    generate_scatter_plot_ind(np.absolute(pca.components_[3]), index_by_population, ("Nucleobase Index", "Component 4 Coefficient"))

    # Investigating Principal Component 3
    nucleobase_split = 9615
    start_mat = np.take(centered_mat, np.arange(nucleobase_split), axis=1)
    start_comp = np.take(pca.components_, np.arange(nucleobase_split), axis=1)
    generate_scatter_plot(np.tensordot(start_mat, start_comp, axes=([1],[1])), index_by_gender, (0,2), ("Gender", "(First {0} Nucleobases) Comp 1".format(nucleobase_split), "Comp 3"))

    end_mat = np.take(centered_mat, np.arange(nucleobase_split,num_nucleos), axis=1)
    end_comp = np.take(pca.components_, np.arange(nucleobase_split,num_nucleos), axis=1)
    generate_scatter_plot(np.tensordot(end_mat, end_comp, axes=([1],[1])), index_by_gender, (0,2), ("Gender", "(Last {0} Nucleobases) Comp 1".format(num_nucleos - nucleobase_split), "Comp 3"))



def generate_scatter_plot(plot_data, ind_lookup, comp_ind_tuple, plot_def):
    fig = plt.figure(figsize = (9,9))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel("Principal Component 1", fontsize = 15)
    ax.set_ylabel("Principal Component 2", fontsize = 15)
    ax.set_title("{1} vs. {2} (by {0})".format(plot_def[0], plot_def[1], plot_def[2]), fontsize = 20)
    key_values = ind_lookup.keys()
    color_subset = color_strings[:len(key_values)]
    for key_val, color in zip(key_values, color_subset):
        ax.scatter(x=np.take(plot_data[:,comp_ind_tuple[0]],ind_lookup[key_val]), y=np.take(plot_data[:,comp_ind_tuple[1]],ind_lookup[key_val]), c=color, s=50)
    ax.legend(key_values)
    ax.grid()
    plt.savefig("PCA_{0}_{1}_vs_{2}.png".format(filename_comp_format(plot_def[0]), filename_comp_format(plot_def[1]), filename_comp_format(plot_def[2])), format = 'png')
    plt.close()

def generate_scatter_plot_ind(plot_data, ind_lookup, plot_def):
    fig = plt.figure(figsize = (9,9))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel("Nucleobase Index", fontsize = 15)
    ax.set_ylabel("Principal Component 3 Coefficient", fontsize = 15)
    ax.set_title("{0} vs. {1}".format(plot_def[0], plot_def[1]), fontsize = 20)
    ax.scatter(x=np.arange(num_nucleos), y=plot_data, c='b', s=50)
    ax.grid()
    plt.savefig("PCA_{0}_vs_{1}.png".format(filename_comp_format(plot_def[0]), filename_comp_format(plot_def[1])), format = 'png')
    plt.close()

def filename_comp_format(component):
    return component.replace(" ", "-")


def generate_matrix(person_list):
    mat = np.zeros((num_persons, num_nucleos))
    for p_ind, person in enumerate(person_list):
        print("\tGenerating matrix row for person {0} of 995".format(p_ind + 1))
        for n_ind, nucleo in enumerate(person.nucleotides):
            #if nucleo != get_mode(n_ind):
            #    mat[p_ind, n_ind] = 1
            #mat[p_ind, n_ind] = nucleo_counts[n_ind][nucleo] / sum(nucleo_counts[n_ind].values())
            mat[p_ind, n_ind] = nucleo_to_num(nucleo)
    return mat

def nucleo_to_num(nucleo):
    if nucleo == 'G':
        return 1
    if nucleo == 'A':
        return 2
    if nucleo == 'C':
        return 3
    if nucleo == 'T':
        return 4
    return 0

def get_mode(ind):
    return max(nucleo_counts[ind], key=nucleo_counts[ind].get)

def parse_text(text_filepath):
    global nucleo_counts
    global num_nucleos
    global index_by_population
    global index_by_gender
    persons = list()
    max_num_nucleos = 0
    with open(text_filepath) as nucleos:
        for ind, person in enumerate(nucleos):
            print("\tParsing data for line {0} of 995".format(ind + 1))
            dna_data = person.split()
            populat = population_strings[dna_data[2]]
            gendr = "male" if int(dna_data[1]) == 1 else "female"
            if populat not in index_by_population:
                index_by_population[populat] = list()
            index_by_population[populat].append(ind)
            if gendr not in index_by_gender:
                index_by_gender[gendr] = list()
            index_by_gender[gendr].append(ind)
            person = Person(id=dna_data[0], gender=gendr, population=populat)
            for nucleo_ind in range(3,len(dna_data)):
                nucleo = dna_data[nucleo_ind]
                person.add_nucleotide(nucleo)
                rebase_ind = nucleo_ind - 3
                if rebase_ind not in nucleo_counts:
                    nucleo_counts[rebase_ind] = dict()
                if nucleo not in nucleo_counts[rebase_ind]:
                    nucleo_counts[rebase_ind][nucleo] = 0
                nucleo_counts[rebase_ind][nucleo] += 1
            if len(dna_data) - 3 > max_num_nucleos:
                max_num_nucleos = len(dna_data) - 3
            persons.append(person)
    num_nucleos = max_num_nucleos
    return persons

class Person:
    def __init__(self, id, gender, population):
        self.id = id
        self.gender = gender
        self.population = population
        self.nucleotides = list()
    
    def add_nucleotide(self, nucleotide):
        self.nucleotides.append(nucleotide)

if __name__ == '__main__':
    main()