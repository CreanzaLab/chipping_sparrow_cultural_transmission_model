import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import seaborn as sns; sns.set()
import os
import itertools
import model_functions as fns
import time
import sys

"""
Load in real data to get sampling frequency
"""

chippies = pd.read_csv(
    "C:/Users/abiga/PycharmProjects"
    "/CreanzaLab_chippies_cultural_transmission_model/citizen_science_data"
    "/AnimalBehaviour_SupplementalDataTable2_addedMid.csv")

yrs_freq = chippies.RecordingYear.value_counts().sort_index().reindex(range(
    1950, 2018, 1)).fillna(0)

sample_freq = yrs_freq.to_numpy(dtype='int')

"""
Cultural Transmission Model
"""
save_video = False
save_pdfs = True
home_dir = 'C:/Users/abiga\Box ' \
           'Sync\Abigail_Nicole\ChippiesSyllableModel' \
           '/RealYearlySamplingFreq/TestingDispersal'
runs = {}
model_type = 'conformity'
conformity_factor = 2

iterations = 100
dim = 50

mortality_rate = 0.4
dispersal_rate = 0.005
dispersal_dist = 3
low_syll_type = int(0)  # should not change
high_syll_type = int(dim ** 2 / 500)
low_syll_rate = float(5)  # units of syllables/second
high_syll_rate = float(40)  # units of syllables/second

num_syll_types = high_syll_type
num_samples = len(sample_freq)

# get list of all coordinate pairs of matrix
all_coord = list(itertools.product(range(0, dim), range(0, dim)))

# setup runs with various parameters
# for p in np.arange(1.0, 10.01, 2.0):
for p in [0.05]:
    file_name = model_type + '_' \
                + str(p) + 'error_' \
                + str(int(mortality_rate*100)) + 'mortality_' \
                + str(iterations) + 'iters_' \
                + str(dim) + 'dim_' \
                + str(high_syll_type) + 'initialSylls'
    runs.update({file_name: [model_type, p/100]})

# iterate through each of the runs, each with unique parameters
for run, params in runs.items():
    print(run)
    start_time = time.time()
    path = home_dir + '/' + str(dim) + 'DimMatrix/' + run + '/'
    os.mkdir(path)
    os.chdir(path)

    # create matrix with each element being a bird
    total_territories = dim ** 2
    num_deaths = int(mortality_rate*total_territories)
    # create empty vector w/ more space than expected for num of sylls created
    vector_size = int(total_territories * iterations * params[1] * \
                  mortality_rate * 10)

    # initialize the first set of birds
    bird_matrix, rate_matrix, current_bps, actual_lifetimes, unique_bps, \
        sample_bps, sample_unique_bps, first_sampled, last_sampled = \
        fns.initiate(low_syll_type, high_syll_type, low_syll_rate,
                     high_syll_rate, dim, vector_size)

    # find number of birds that have each syllable type, save initial state
    current_bps = fns.count_type(bird_matrix, vector_size)
    bird_counts_t0 = current_bps.copy()

    # initialize figure for video frames
    if save_video:
        video_name = run + '.mp4'
        dpi = 100
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        frame = ax.imshow(bird_matrix, cmap='gray')
        # cbar = fig.colorbar(frame)
        fig.set_size_inches([5, 5])
        frames = [[frame]]

    if save_pdfs:
        fns.plot_type_distributions(bird_matrix, t=0)

        if model_type == 'directional':
            fns.plot_rates_distributions(rate_matrix, t=0)

    for timestep in range(iterations):
        print('\ntimestep', timestep)

        if save_pdfs and (timestep % 100 == 90):
            fns.plot_type_distributions(bird_matrix, timestep)

            if model_type == 'directional':
                fns.plot_rates_distributions(rate_matrix, timestep)

        # some percent of birds die, find their grid location
        open_territories = fns.locate_dead_birds(ordered_pairs=all_coord,
                                                 num_loc=num_deaths)
        learned_types = []  # list of learned syllable types (could be a new type)
        learned_rates = []  # list of learned syllable rates
        for bird in open_territories:
            if (model_type == 'neutral') or (model_type == 'conformity'):
                # get new sylls for birds that will now occupy empty territories
                neighbor_sylls = fns.get_nearby_sylls(bird_matrix,
                                                      bird[0], bird[1],
                                                      d=1)

                new_type, num_syll_types = fns.get_learned_syll(
                    neighbor_sylls, num_syll_types, rule=params[0],
                    error_rate=params[1], conformity_factor=conformity_factor)
                learned_types.append(new_type)

            elif model_type == 'directional':
                neighbor_sylls, neighbor_rates = \
                    fns.get_nearby_sylls_and_rates(bird_matrix,
                                                   rate_matrix,
                                                   bird[0],
                                                   bird[1],
                                                   d=1)

                new_type, new_rate, num_syll_types = \
                    fns.get_learned_syll_and_rate(neighbor_sylls,
                                                  neighbor_rates,
                                                  num_syll_types,
                                                  error_rate=params[1])

                learned_types.append(new_type)
                learned_rates.append(new_rate)

        # add new birds to the open territories (where old birds died)
        for bird, syll, rate in itertools.zip_longest(open_territories,
                                                      learned_types,
                                                      learned_rates,
                                                      fillvalue=None):
            bird_matrix[bird[0], bird[1]] = syll

            if model_type == 'directional':
                rate_matrix[bird[0], bird[1]] = rate

            # after the first timestep in which we sample, increment the
            # number of birds with a syllable type for each new bird
            if timestep > iterations - num_samples:
                unique_bps[syll] += 1

        # when the timestep is the first year to sample, initiate unique_bps
        if timestep == iterations - num_samples:
            unique_bps = fns.count_type(bird_matrix, vector_size)
            bird_counts_t1950 = unique_bps.copy()

        # sample the birds at this timestep (don't need to sample before 1950)
        if timestep >= iterations - num_samples:
            # sampling
            samples = fns.sample_birds(bird_matrix,
                                       sample_freq[timestep-(iterations-num_samples)])

            # updating information based on sample
            # number of sampled birds with a syllable type
            sample_bps = fns.count_type(samples, vector_size)
            # assume each sampled bird has never been sampled before
            # thus, add the sampled syllables to the count of individual birds that have had that syllable type
            sample_unique_bps += sample_bps
            # store timestep the syllable first appeared
            first_sampled[(first_sampled == 0) & (sample_bps > 0)] = \
                timestep
            # increment timestep the syllable last appeared
            last_sampled[sample_bps > 0] = timestep + 1

            # save the first sample
            if timestep == iterations - num_samples:
                sampled_bird_counts_t1950 = sample_bps.copy()

            # updating information based on full bird matrix
            current_bps = fns.count_type(bird_matrix, vector_size)
            actual_lifetimes[current_bps > 0] += 1

        if save_video:
            new_frame = ax.imshow(bird_matrix, cmap='gray', vmin=0, vmax=6000)
            frames.append([new_frame])

        # adult dispersal
        # get lists of indices of birds to swap places
        print('before dispersal')
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.set_aspect('equal')
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)
        ax1.set_title('before')

        ax1.imshow(bird_matrix, cmap='gray')
        plt.show()
        swap_1, swap_2 = fns.adult_dispersal(dispersal_rate,
                                             dispersal_dist,
                                             max_try=((dispersal_dist + 1)
                                                      ** 2),
                                             matrix_dim=dim)
        print('after dispersal')
        swap_2 = np.asarray(swap_2)
        # go through pairs of indices and swap the bird information
        for b1, b2 in zip(swap_1, swap_2):
            if b2 is None:
                pass
            else:
                print(b1)
                print(b2)
                bird_matrix[b1[0], b1[1]], bird_matrix[b2[0], b2[1]] = \
                    bird_matrix[b2[0], b2[1]], bird_matrix[b1[0], b1[1]]
                rate_matrix[b1[0], b1[1]], rate_matrix[b2[0], b2[1]] = \
                    rate_matrix[b2[0], b2[1]], rate_matrix[b1[0], b1[1]]

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.set_aspect('equal')
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        ax2.set_title('after')

        ax2.imshow(bird_matrix, cmap='gray')
        plt.show()
        quit()
    if save_video:
        video = animation.ArtistAnimation(fig, frames, interval=100, blit=False,
                                          repeat_delay=1000)
        video.save(video_name)
        plt.close()

    # calculate lifespan of sampled syllables
    sampled_lifetimes = last_sampled - first_sampled
    sampled_bird_counts_t2017 = sample_bps.copy()
    bird_counts_t2017 = current_bps.copy()

    # save full matrix information
    np.savetxt('actual_lifetimes_starting_1950.csv', actual_lifetimes,
               delimiter=",")
    np.savetxt('bird_counts_t0.csv', bird_counts_t0, delimiter=",")
    np.savetxt('bird_counts_t1950.csv', bird_counts_t1950, delimiter=",")
    np.savetxt('bird_counts_t2017.csv', bird_counts_t2017, delimiter=",")
    np.savetxt('unique_birds_with_syllables.csv', unique_bps,
               delimiter=",")

    np.savetxt('sampled_lifetimes.csv', sampled_lifetimes, delimiter=",")
    np.savetxt('sampled_bird_counts_t1950.csv', sampled_bird_counts_t1950,
               delimiter=",")
    np.savetxt('sampled_bird_counts_t2017.csv', sampled_bird_counts_t2017,
               delimiter=",")
    np.savetxt('sampled_birds_with_syllables.csv', sample_unique_bps,
               delimiter=",")


    print("--- %s seconds ---" % (time.time() - start_time))
