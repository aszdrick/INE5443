from classifiers import *
import math
import numpy as np
from scipy.spatial import KDTree
import utils

def kdtree_classify(classifier, entry, class_index=-1, k=1):
    prepared_entry = utils.without_column(entry, class_index)
    result = classifier.descriptor.query([prepared_entry], k=k)
    scoreboard = {}

    indexes = result[1]
    if k > 1:
        indexes = indexes[0]

    for index in indexes:
        category = classifier.categories[index]
        if category not in scoreboard:
            scoreboard[category] = 0
        scoreboard[category] += 1

    winner = (0, None)
    for key, value in scoreboard.items():
        if value > winner[0]:
            winner = (value, key)

    return winner[1]

def classify(self, entry, class_index=-1, k=1):
    max_similarity = -float("inf")
    best_categories = []
    prepared_external_entry = utils.without_column(entry, class_index)
    for i in range(len(self.descriptor)):
        # prepared_internal_entry = utils.without_column(internal_entry, class_index)
        internal_entry = self.descriptor[i]
        class_value = self.categories[i]
        similarity = -euclidian_dist(prepared_external_entry, internal_entry)
        if similarity > max_similarity:
            max_similarity = similarity
            best_categories = [class_value]
        elif similarity == max_similarity:
            best_categories.append(class_value)
    best_category = self.pick_one(best_categories)
    return best_category

class Classifier:
    def __init__(self):
        self.hits = 0
        self.fails = 0
        self.descriptor = []
        self.categories = []

    def classify(self, entry, class_index=-1, k=1):
        return self.on_classify(self, entry, class_index, k)

    def add_random_entry(self, training_set):
        self.descriptor.append(self.pick_one(training_set))

    def pick_index(self, array):
        return round(np.random.uniform(0, len(array) - 1))

    def pick_one(self, array):
        return array[self.pick_index(array)]

    def remove_one(self, array):
        index = self.pick_index(array)
        value = array[index]
        del array[index]
        return value


class IBL1(Classifier):
    def __init__(self, training_set, class_index=-1):
        super(IBL1, self).__init__()
        self.on_classify = kdtree_classify

        if len(self.descriptor) == 0:
            self.add_random_entry(training_set)

        for external_entry in training_set:
            max_similarity = -float("inf")
            best_entries = []
            for internal_entry in self.descriptor:
                prepared_external_entry = utils.without_column(external_entry, class_index)
                prepared_internal_entry = utils.without_column(internal_entry, class_index)
                similarity = -euclidian_dist(prepared_external_entry, prepared_internal_entry)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_entries = [internal_entry]
                elif similarity == max_similarity:
                    best_entries.append(internal_entry)
            best_entry = self.pick_one(best_entries)
            if external_entry[class_index] == best_entry[class_index]:
                self.hits += 1
            else:
                self.fails += 1
            self.descriptor.append(external_entry)

        for i in range(len(self.descriptor)):
            self.categories.append(self.descriptor[i][class_index])
            self.descriptor[i] = utils.without_column(self.descriptor[i], class_index)
        self.descriptor = KDTree(np.array(self.descriptor))

class IBL2(Classifier):
    def __init__(self, training_set, class_index=-1):
        super(IBL2, self).__init__()
        if len(self.descriptor) == 0:
            self.add_random_entry(training_set)

        self.on_classify = kdtree_classify

        for external_entry in training_set:
            max_similarity = -float("inf")
            best_entries = []
            for internal_entry in self.descriptor:
                prepared_external_entry = utils.without_column(external_entry, class_index)
                prepared_internal_entry = utils.without_column(internal_entry, class_index)
                similarity = -euclidian_dist(prepared_external_entry, prepared_internal_entry)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_entries = [internal_entry]
                elif similarity == max_similarity:
                    best_entries.append(internal_entry)
            best_entry = self.pick_one(best_entries)
            if external_entry[class_index] == best_entry[class_index]:
                self.hits += 1
            else:
                self.fails += 1
                self.descriptor.append(external_entry)

        for i in range(len(self.descriptor)):
            self.categories.append(self.descriptor[i][class_index])
            self.descriptor[i] = utils.without_column(self.descriptor[i], class_index)
        self.descriptor = KDTree(np.array(self.descriptor))

class IBL3(Classifier):
    class Register:
        def __init__(self, entry, category):
            self.category = category
            self.entry = entry
            self.hits = 0
            self.fails = 0

    def __init__(self, training_set, class_index=-1):
        super(IBL3, self).__init__()
        self.on_classify = kdtree_classify

        frequency_data = {}
        processed_instances = 0

        # Adds a random instance to the descriptor
        if len(self.descriptor) == 0:
            random_entry = self.remove_one(training_set)
            (entry, class_value) = self.prepare(random_entry, class_index)
            frequency_data[class_value] = 1
            processed_instances += 1;

            register = self.Register(entry, class_value)
            register.hits += 1
            self.descriptor.append(register)

        training_size = len(training_set)

        for external_entry in training_set:
            (entry, class_value) = self.prepare(external_entry, class_index)

            # Updates the frequency data
            # TODO: is this the right place to do it?
            if class_value not in frequency_data:
                frequency_data[class_value] = 0
            frequency_data[class_value] += 1

            # Searches for acceptable instances in the descriptor
            best_acceptable = None
            similarity_table = {}
            for register in self.descriptor:
                category = register.category

                # Populates the similarity table
                similarity = -euclidian_dist(entry, register.entry)
                similarity_table[tuple(register.entry)] = similarity

                # classifying acceptability factor
                z = 0.9

                # Calculates the frequency interval (class)
                p = frequency_data[category] / training_size
                n = processed_instances
                frequency_interval = self.interval(p, z, n)

                # Calculates the precision interval (instance)
                n = register.hits + register.fails
                p = register.hits / n
                precision_interval = self.interval(p, z, n)

                if frequency_interval["sup"] < precision_interval["inf"]:
                    # Accept the instance
                    if not best_acceptable or best_acceptable[1] < similarity:
                        best_acceptable = (register, similarity)

            if not best_acceptable:
                # No acceptable instances were found,
                # so use a random register instead
                random_register = self.pick_one(self.descriptor)

                similarity = similarity_table[tuple(random_register.entry)]
                best_acceptable = (random_register, similarity)

            # Flag that indicates if we learned a new entry
            learned = False

            if best_acceptable[0].category == class_value:
                # Correct evaluation, simply update the hit counters
                best_acceptable[0].hits += 1
                self.hits += 1
            else:
                # Incorrect evaluation, update the fail counters, then learn
                best_acceptable[0].fails += 1
                self.fails += 1

                # Learn the new entry
                new_register = self.Register(entry, class_value)
                new_register.hits += 1
                self.descriptor.append(new_register)
                learned = True

            # Updates the processed instances counter
            # TODO: is this the right place to do it?
            processed_instances += 1

            # Update all registers in range
            descriptor_size = len(self.descriptor)

            # If we just appended a new entry, ignore it
            if learned:
                descriptor_size -= 1

            for i in range(descriptor_size):
                register = self.descriptor[i]

                # Similarity of the register used as the best "acceptable"
                outer_similarity = best_acceptable[1]
                similarity = similarity_table[tuple(register.entry)]

                if similarity >= outer_similarity:
                    category = register.category

                    # Update the current register
                    if category == class_value:
                        register.hits += 1
                    else:
                        register.fails += 1

                    # discard factor
                    z = 0.75

                    # Calculates the frequency interval (class)
                    p = frequency_data[category] / training_size
                    n = processed_instances
                    frequency_interval = self.interval(p, z, n)

                    # Calculates the precision interval (instance)
                    n = register.hits + register.fails
                    p = register.hits / n
                    precision_interval = self.interval(p, z, n)

                    if precision_interval["sup"] < frequency_interval["inf"]:
                        # Discard the instance
                        del self.descriptor[i]
                        descriptor_size -= 1
                        i -= 1

        # Transforms the descriptor into a KD-Tree
        for i in range(len(self.descriptor)):
            self.categories.append(self.descriptor[i].category)
            self.descriptor[i] = self.descriptor[i].entry
        self.descriptor = KDTree(np.array(self.descriptor))

    def prepare(self, entry, class_index=-1):
        return (utils.without_column(entry, class_index), entry[class_index])

    def interval(self, p, z, n):
        d = (1 + (z * z) / n)
        f1 = p + (z * z) / (2 * n)
        f2 = z * math.sqrt(p * (1 - p) / n + (z * z) / (4 * n * n))
        return {
            "inf": (f1 - f2) / d,
            "sup": (f1 + f2) / d
        }

class IBL4(Classifier):
    class Register:
        def __init__(self, entry, category):
            self.category = category
            self.entry = entry
            self.hits = 0
            self.fails = 0

    def __init__(self, training_set, class_index=-1):
        super(IBL4, self).__init__()
        self.on_classify = classify

        frequency_data = {}
        processed_instances = 0
        accumulated_weights = []
        normalized_weights = []
        weights = []

        # Adds a random instance to the descriptor
        if len(self.descriptor) == 0:
            random_entry = self.remove_one(training_set)
            (entry, class_value) = self.prepare(random_entry, class_index)

            # Sets initial values for the weights
            num_attributes = len(entry)
            for i in range(len(entry)):
                accumulated_weights.append(0.01)
                normalized_weights.append(0.01)
                weights.append(1 / num_attributes)

            frequency_data[class_value] = 1
            processed_instances += 1;

            register = self.Register(entry, class_value)
            register.hits += 1
            self.descriptor.append(register)

        training_size = len(training_set)

        for external_entry in training_set:
            (entry, class_value) = self.prepare(external_entry, class_index)

            # Updates the frequency data
            # TODO: is this the right place to do it?
            if class_value not in frequency_data:
                frequency_data[class_value] = 0
            frequency_data[class_value] += 1

            # Searches for acceptable instances in the descriptor
            best_acceptable = None
            similarity_table = {}
            for register in self.descriptor:
                category = register.category

                # Populates the similarity table
                similarity = self.weighted_similarity(entry, register.entry, weights)
                similarity_table[tuple(register.entry)] = similarity

                # classifying acceptability factor
                z = 0.9

                # Calculates the frequency interval (class)
                p = frequency_data[category] / training_size
                n = processed_instances
                frequency_interval = self.interval(p, z, n)

                # Calculates the precision interval (instance)
                n = register.hits + register.fails
                p = register.hits / n
                precision_interval = self.interval(p, z, n)

                # TODO: should we accept in case 3 (overlapping intervals)?
                if frequency_interval["sup"] < precision_interval["inf"]:
                    # Accept the instance
                    if not best_acceptable or best_acceptable[1] < similarity:
                        best_acceptable = (register, similarity)
                    # TODO: should we do something if best_acceptable[1] == similarity?

            if not best_acceptable:
                # No acceptable instances were found,
                # so use a random register instead
                random_register = self.pick_one(self.descriptor)

                similarity = similarity_table[tuple(random_register.entry)]
                best_acceptable = (random_register, similarity)

            # Flag that indicates if we learned a new entry
            learned = False

            if best_acceptable[0].category == class_value:
                # Correct evaluation, simply update the hit counters
                best_acceptable[0].hits += 1
                self.hits += 1
            else:
                # Incorrect evaluation, update the fail counters, then learn
                best_acceptable[0].fails += 1
                self.fails += 1

                # Learn the new entry
                new_register = self.Register(entry, class_value)
                new_register.hits += 1
                self.descriptor.append(new_register)
                learned = True

            # Updates the processed instances counter
            # TODO: is this the right place to do it?
            processed_instances += 1

            # Update all registers in range
            descriptor_size = len(self.descriptor)

            # TODO: should we ignore the new entry?
            # If we just appended a new entry, ignore it
            if learned:
                descriptor_size -= 1

            for i in range(descriptor_size):
                register = self.descriptor[i]

                # Similarity of the register used as the best "acceptable"
                outer_similarity = best_acceptable[1]
                similarity = similarity_table[tuple(register.entry)]

                # TODO: should this inequality be strict?
                if similarity > outer_similarity:
                    category = register.category

                    # Update the current register
                    # TODO: not sure about this part (it makes sense though)
                    if category == class_value:
                        register.hits += 1
                    else:
                        register.fails += 1

                    # discard factor
                    z = 0.75

                    # Calculates the frequency interval (class)
                    p = frequency_data[category] / training_size
                    n = processed_instances
                    frequency_interval = self.interval(p, z, n)

                    # Calculates the precision interval (instance)
                    n = register.hits + register.fails
                    p = register.hits / n
                    precision_interval = self.interval(p, z, n)

                    if precision_interval["sup"] < frequency_interval["inf"]:
                        # Discard the instance
                        del self.descriptor[i]
                        i -= 1

            # Iterates over the attributes, updating its weights
            reference = best_acceptable[0]
            category = reference.category
            for i in range(len(reference.entry)):
                delta = abs(entry[i] - reference.entry[i])

                lambd = max(frequency_data[class_value], frequency_data[category])
                complement = 1 - lambd
                if class_value == reference.entry[i]:
                    accumulated_weights[i] += complement * (1 - delta)
                else:
                    accumulated_weights[i] += complement * delta
                normalized_weights[i] += complement

                acc = accumulated_weights[i]
                norm = normalized_weights[i]
                if norm == 0:
                    print("lambd = %s, comp = %s" % (lambd, complement))
                weights[i] = max(0, acc / norm - 0.5)

        for i in range(len(self.descriptor)):
            self.categories.append(self.descriptor[i].category)
            self.descriptor[i] = self.descriptor[i].entry

    def weighted_similarity(self, first, second, weights):
        result = 0
        for i in range(len(first)):
            result += (weights[i] * (first[i] - second[i])) ** 2
        return -math.sqrt(result)

    def prepare(self, entry, class_index=-1):
        return (utils.without_column(entry, class_index), entry[class_index])

    def interval(self, p, z, n):
        d = (1 + (z * z) / n)
        f1 = p + (z * z) / (2 * n)
        f2 = z * math.sqrt(p * (1 - p) / n + (z * z) / (4 * n * n))
        return {
            "inf": (f1 - f2) / d,
            "sup": (f1 + f2) / d
        }

