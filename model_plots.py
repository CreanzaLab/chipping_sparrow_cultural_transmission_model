import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import seaborn as sns; sns.set()
import os
import sys
from glob import glob


"""
Load in counts from run
"""

home_path = 'C:/Users/abiga\Box ' \
            'Sync\Abigail_Nicole\ChippiesSyllableModel' \
            '/RealYearlySamplingFreq/Testing4_new/500DimMatrix' \
            '/EstablishedEquilibrium'

folders = glob(home_path + "/*/")

for f in folders:
    print(f)

    os.chdir(f)

    birds_t0 = np.genfromtxt('bird_counts_t0.csv',
                                     dtype='int32', delimiter=',')
    birds_t1950 = np.genfromtxt('bird_counts_t1950.csv',
                                     dtype='int32', delimiter=',')
    birds_t2017 = np.genfromtxt('bird_counts_t2017.csv',
                                     dtype='int32', delimiter=',')

    print('no. nonzero t0: ', np.sum(birds_t0 > 0))
    print('no. nonzero t1950: ', np.sum(birds_t1950 > 0))
    print('no. nonzero t2017: ', np.sum(birds_t2017 > 0))

    actual_lifetimes = np.genfromtxt('actual_lifetimes_starting_1950.csv',
                                     dtype='int32', delimiter=',')
    actual_counts = np.genfromtxt('unique_birds_with_syllables.csv',
                                  dtype='int32', delimiter=',')
    sampled_lifetimes = np.genfromtxt('sampled_lifetimes.csv', dtype='int32',
                                      delimiter=',')
    sample_counts = np.genfromtxt('sampled_birds_with_syllables.csv',
                                  dtype='int32', delimiter=',')

    print('total number of syllable types: ', np.sum(actual_counts > 0))

    print('(sampled) total number of syllable types: ', np.sum(
        sample_counts > 0))

    """
    Plotting results
    """

    save_plots = True

    #
    # # random uniform distribution (beginning syllable types)
    # plt.figure(1)
    # plt.bar(range(len(init_counts)), init_counts[:, 0])
    # plt.xlabel('syllable type')
    # plt.ylabel('number of birds with syllable type')
    # plt.title('random initial song types: discrete uniform distribution')
    #
    # if save_plots:
    #     plt.tight_layout()
    #     plt.savefig(
    #         "initial_bird_matrix"
    #         + '.pdf', type='pdf', bbox_inches='tight',
    #         transparent=True)
    #     plt.close()
    # else:
    #     plt.show()
    #     plt.close()
    #
    # beg_syll_counts = prop_counts[:, 0]
    # end_syll_counts = prop_counts[:, -1]
    #
    # # x = syllable type, y = number of birds
    # plt.figure(2)
    # my_dpi = 96
    # sns.set(style='white')
    # sns.set_context({"figure.figsize": (20, 7)})
    # plt.bar(np.arange(len(beg_syll_counts)), beg_syll_counts)
    # plt.title('beginning')
    # plt.xlabel('syllable type')
    # plt.ylabel('number of birds')
    #
    # if save_plots:
    #     plt.tight_layout()
    #     plt.savefig(
    #         "num_birds_singing_each_syll_beg"
    #         + '.pdf', type='pdf', bbox_inches='tight',
    #         transparent=True)
    #     plt.close()
    # else:
    #     plt.show()
    #     plt.close()
    #
    # plt.figure(3)
    # my_dpi = 96
    # sns.set(style='white')
    # sns.set_context({"figure.figsize": (20, 7)})
    # plt.bar(np.arange(len(end_syll_counts)), end_syll_counts)
    # plt.title('ending')
    # plt.xlabel('syllable type')
    # plt.ylabel('number of birds')
    #
    # if save_plots:
    #     plt.tight_layout()
    #     plt.savefig(
    #         "num_birds_singing_each_syll_end"
    #         + '.pdf', type='pdf', bbox_inches='tight',
    #         transparent=True)
    #     plt.close()
    # else:
    #     plt.show()
    #     plt.close()
    #
    #
    #
    #

    my_dpi = 96
    sns.set(style='white')
    sns.set_context({"figure.figsize": (20, 7)})
    plt.figure(4)

    num_syll_types = np.sum(sample_counts > 0)
    x = np.arange(max(sampled_lifetimes))
    y = np.bincount(sampled_lifetimes)

    # don't include no. with 0 lifespan (will be a lot since vector was made
    # much larger than needed)
    plt.bar(x + 1, y[1:])
    plt.title('Sampled: ' + ' total number of syll types: ' + str(
        num_syll_types))
    plt.xlabel('lifespan')
    plt.ylabel('number of syllable types')
    # plt.xlim(0, 80)
    # plt.xticks(range(1, 201))
    # plt.ylim(0, 450)

    if save_plots:
        plt.tight_layout()
        plt.savefig(
            "num_sylls_with_lifespan_sampled"
            + '.pdf', type='pdf', bbox_inches='tight',
            transparent=True)
        plt.close()
    else:
        plt.show()
        plt.close()


    # # x = number of birds singing a syll type, y = number of syllable types
    # plt.figure(4)
    # my_dpi = 96
    # sns.set(style='white')
    # sns.set_context({"figure.figsize": (20, 7)})
    #
    # dataset = np.sum(sample_counts[:, 33:], axis=1)
    # total_sylls = np.count_nonzero(dataset)
    # lifespans = []
    # for row in sample_counts[:, 33:]:
    #     yrs_with_sylls = np.nonzero(row)[0]
    #     if len(yrs_with_sylls) > 0:
    #         yrs = yrs_with_sylls[-1] - yrs_with_sylls[0] + 1
    #         lifespans.append(yrs)
    #     else:
    #         lifespans.append(0)
    #
    # num_syll_types = np.bincount(lifespans)
    # x = np.arange(len(num_syll_types))
    # y = num_syll_types
    # plt.bar(x[1:], y[1:])
    # plt.title('67 yrs' + ' total number of sylls: ' + str(total_sylls))
    # plt.xlabel('lifespan')
    # plt.ylabel('number of syllable types')
    # # plt.xlim(0, 80)
    # # plt.xticks(range(1, 201))
    # # plt.ylim(0, 450)
    #
    # if save_plots:
    #     plt.tight_layout()
    #     plt.savefig(
    #         "num_sylls_with_lifespan_67yrs"
    #         + '.pdf', type='pdf', bbox_inches='tight',
    #         transparent=True)
    #     plt.close()
    # else:
    #     plt.show()
    #     plt.close()


    my_dpi = 96
    sns.set(style='white')
    sns.set_context({"figure.figsize": (20, 7)})
    plt.figure(5)

    num_syll_types = np.sum(sample_counts > 0)
    bin_count_syll_types = np.bincount(sample_counts)
    x = np.arange(len(bin_count_syll_types))
    y = bin_count_syll_types/num_syll_types

    plt.bar(x[1:], y[1:])
    plt.title('Sampled: ' + ' total number of syll types: ' + str(
        num_syll_types))
    plt.xlabel('number of birds with a syllable type')
    plt.ylabel('fraction of syllable types')
    # plt.xlim(0, 45)
    # plt.xticks(range(1, 201))
    plt.ylim(0, 1)

    if save_plots:
        plt.tight_layout()
        plt.savefig(
            "num_sylls_with_num_birds_sampled"
            + '.pdf', type='pdf', bbox_inches='tight',
            transparent=True)
        plt.close()
    else:
        plt.show()
        plt.close()


    # actual distribution (not sampled)

    my_dpi = 96
    sns.set(style='white')
    sns.set_context({"figure.figsize": (20, 7)})
    plt.figure(6)

    num_syll_types = np.sum(actual_counts > 0)
    bin_count_syll_types = np.bincount(actual_counts)[1:]  # don't plot syllables that never existed

    count_binned = [bin_count_syll_types[n:n + 10] for n in range(0, len(bin_count_syll_types), 10)]
    count_binned = [np.sum(count_binned[i]) for i in range(0, len(count_binned))]

    x = np.arange(len(count_binned))
    y = count_binned / num_syll_types

    plt.bar(x, y)
    plt.title('After 1950: ' + ' total number of syll types: ' + str(
        num_syll_types))
    plt.xlabel('number of birds with a syllable type (x10)')
    plt.ylabel('fraction of syllable types')
    # plt.xlim(0, 45)
    # plt.xticks(range(1, 201))
    plt.ylim(0, 1)

    if save_plots:
        plt.tight_layout()
        plt.savefig(
            "num_sylls_with_num_birds_actual"
            + '.pdf', type='pdf', bbox_inches='tight',
            transparent=True)
        plt.close()
    else:
        plt.show()
        plt.close()




    # # x = number of birds singing a syll type, y = number of syllable types
    # plt.figure(6)
    # my_dpi = 96
    # sns.set(style='white')
    # sns.set_context({"figure.figsize": (20, 7)})
    #
    # # print(np.sum(bird_counts, axis=1))
    # print('before bincount')
    # num_sylls = np.bincount(np.sum(bird_counts, axis=1))
    # print('after bincount')
    # x = np.arange(len(num_sylls))
    # y = num_sylls/len(bird_counts[:, 0])
    # plt.bar(x[1:], y[1:])
    # plt.title('all iterations' + ' total number of sylls: ' + str(len(bird_counts)))
    # plt.xlabel('number of birds with a syllable type')
    # plt.ylabel('number of syllable types')
    # # plt.xlim(0, 100)
    # # plt.xticks(range(1, 71))
    # # plt.ylim(0, 1)
    #
    # if save_plots:
    #     plt.tight_layout()
    #     print('before save')
    #     plt.savefig(
    #         "num_sylls_with_num_birds_all_time"
    #         + '.pdf', type='pdf', bbox_inches='tight',
    #         transparent=True)
    #     print('after save')
    #     plt.close()
    # else:
    #     plt.show()
    #     plt.close()



    #
    #
    # plt.figure(7)
    # my_dpi = 96
    # sns.set(style='white')
    # sns.set_context({"figure.figsize": (20, 7)})
    # # plt.bar(np.arange(len(np.bincount(beg_syll_counts)))[1:], (np.bincount(beg_syll_counts)/100)[1:])
    # plt.bar(np.arange(len(np.bincount(beg_syll_counts)))[1:], (np.bincount(beg_syll_counts)/np.count_nonzero(beg_syll_counts))[1:])
    # plt.title('beginning')
    # plt.xlabel('number of birds with a syllable type')
    # plt.ylabel('number of syllable types')
    # # plt.xlim(0, 100)
    # # plt.xticks(range(1, 71))
    # # plt.ylim(0, 0.35)
    #
    # if save_plots:
    #     plt.tight_layout()
    #     plt.savefig(
    #         "num_sylls_with_num_birds_beg"
    #         + '.pdf', type='pdf', bbox_inches='tight',
    #         transparent=True)
    #     plt.close()
    # else:
    #     plt.show()
    #     plt.close()
    #
    #
    # plt.figure(8)
    # my_dpi = 96
    # sns.set(style='white')
    # sns.set_context({"figure.figsize": (20, 7)})
    # # plt.bar(np.arange(len(np.bincount(end_syll_counts)))[1:], (np.bincount(end_syll_counts)/len(end_syll_counts))[1:])
    # plt.bar(np.arange(len(np.bincount(end_syll_counts)))[1:], (np.bincount(end_syll_counts)/np.count_nonzero(end_syll_counts))[1:])
    # plt.title('ending' + ' total number of sylls: ' + str(len(end_syll_counts)))
    # plt.xlabel('number of birds with a syllable type')
    # plt.ylabel('number of syllable types')
    # # plt.xlim(0, 100)
    # # plt.xticks(range(1, 71))
    # # plt.ylim(0, 0.35)
    #
    # if save_plots:
    #     plt.tight_layout()
    #     plt.savefig(
    #         "num_sylls_with_num_birds_end"
    #         + '.pdf', type='pdf', bbox_inches='tight',
    #         transparent=True)
    #     plt.close()
    # else:
    #     plt.show()
    #     plt.close()

    # plt.hist(beg_syll_counts)
    # plt.title('beginning')
    # plt.xlabel('number of birds with a syllable type')
    # plt.ylabel('number of syllable types')
    # # plt.show()
    #
    # plt.hist(end_syll_counts)
    # plt.title('end')
    # plt.xlabel('number of birds with a syllable type')
    # plt.ylabel('number of syllable types')
    # # plt.show()
