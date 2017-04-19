from classifiers import *
from math import sqrt
import numpy as np
import utils

class Classifier:
    def __init__(self):
        self.hits = 0
        self.fails = 0
        self.descriptor = []

    def classify(self, entry, class_index=-1):
        max_similarity = -float("inf")
        best_entries = []
        for internal_entry in self.descriptor:
            prepared_external_entry = utils.without_column(entry, class_index)
            prepared_internal_entry = utils.without_column(internal_entry, class_index)
            similarity = -euclidian_dist(prepared_external_entry, prepared_internal_entry)
            if similarity > max_similarity:
                max_similarity = similarity
                best_entries = [internal_entry]
            elif similarity == max_similarity:
                best_entries.append(internal_entry)
        best_entry = self.pick_one(best_entries)
        return best_entry[class_index]

    def add_random_entry(self, training_set):
        self.descriptor.append(self.pick_one(training_set))

    def pick_one(self, array):
        return array[round(np.random.uniform(0, len(array) - 1))]

class IBL1(Classifier):
    def __init__(self, training_set, class_index=-1):
        super(IBL1, self).__init__()
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

class IBL2(Classifier):
    def __init__(self, training_set, class_index=-1):
        super(IBL2, self).__init__()
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

class IBL3(Classifier):
    class Register:
        def __init__(self, entry, category):
            self.category = category
            self.entry = entry
            self.hits = 0
            self.precision_data = []

    def __init__(self, training_set, class_index=-1):
        super(IBL3, self).__init__()
        self.frequency_data = {}

        parsed_entries = 0
        for external_entry in training_set:
            similarity_list = {}
            acceptable_list = []
            best_acceptable_similarity = -float("inf")
            best_acceptables = []
            i = 0
            # 1.
            for register in self.descriptor:
                internal_entry = register.entry
                prepared_external_entry = utils.without_column(external_entry, class_index)
                similarity = -euclidian_dist(prepared_external_entry, internal_entry)
                similarity_list[register] = similarity
                if (self.acceptable(register)):
                    acceptable_list.append(register)
                    if similarity > best_acceptable_similarity:
                        best_acceptable_similarity = similarity
                        best_acceptable = [register]
                    elif similarity == best_acceptable_similarity:
                        best_acceptables.append(register)
                i += 1

            # 2.
            best_register = None
            if len(acceptable_list) > 0:
                best_register = self.pick_one(best_acceptables)
            elif len(self.descriptor) > 0:
                best_register = self.pick_one(self.descriptor)

            # 3.
            # best_register is still None if len(self.descriptor) == 0
            if best_register and \
               external_entry[class_index] == best_register.category:
                self.hits += 1
            else:
                self.fails += 1
                without_category = utils.without_column(external_entry, class_index)
                category = external_entry[class_index]
                new_register = self.Register(without_category, category)
                self.descriptor.append(new_register)

            # 4.
            for i in range(len(self.descriptor)):
                register = self.descriptor[i]
                if similarity_list[register] >= similarity_list[best_register]:
                    self.update_register(register, best_register)
                    if self.useless(register):
                        del self.descriptor[i]
                        i -= 1
            parsed_entries += 1

    # Updates the register statistics and the frequency data
    def update_register(self, register, reference):
        self.frequency_data[register.category] -= 1
        self.frequency_data[reference.category] += 1
        register.category = reference.category
        # TODO

    def useless(self, register):
        # TODO
        return False

    def acceptable(self, register):
        freq = self.frequency_data[register.category]
        prec = register.precision_data
        if prec.sup < freq.inf:
            return False
        return True

    def interval(self, p, z, n):
        d = (1 + (z * z) / n)
        f1 = p + (z * z) / (2 * n)
        f2 = z * math.sqrt(p * (1 - p) / n + (z * z) / (4 * n * n))
        return {
            "inf": (f1 - f2) / d,
            "sup": (f1 + f2) / d
        }
