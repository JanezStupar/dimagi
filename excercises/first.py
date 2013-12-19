__author__ = 'Janez Stupar'

import math


class NumberConverter(object):
    _words_0 = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    _words_1 = [None, None, 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    _words_2 = '%s hundred'
    _words_3 = '%s thousand'
    _words_6 = '%s million'
    _words_9 = '%s billion'

    def num_to_word(self, number):
        if number == 0:
            return self._words_0[0]

        return self.num_to_word_worker(number)

    def num_to_word_worker(self, number):
        if number == 0:
            return ""

        digits = str(number)
        power = int(math.log10(number))

        # For numbers smaller than hundred...
        if power <= 1:
            # Dont write out zeroes
            if number == 0:
                return ""

            # Numbers smaller than twenty have their own words
            elif number < 20:
                return self._words_0[number]

            # Others are compound statements of two digits
            else:
                d1, d2 = int(digits[0]), int(digits[1])
                if d2 == 0:
                    return self._words_1[d1]
                else:
                    return "%s %s" % (self._words_1[d1], self._words_0[d2])

        # Numbers larger than hundred are always compound statements ("one hundred one")
        else:
            rank = power

            # Not every power of ten has an english name, thus we need to find the largest power
            # that will correspond to the number
            named_rank = getattr(self, "_words_%s" % rank, None)
            while named_rank is None:
                rank -= 1
                named_rank = getattr(self, "_words_%s" % rank, None)

            # Split the digits according to the rank
            first_part = int(digits[:-rank])
            second_part = int(digits[len(digits)-rank:])

            # Two recursive calls for each part
            return "%s %s" % (named_rank % self.num_to_word_worker(first_part), self.num_to_word_worker(second_part))



if __name__ == '__main__':
    nc = NumberConverter()
    print nc.num_to_word(19342)
    print nc.num_to_word(355)
    print nc.num_to_word(750)
    print nc.num_to_word(8000000)
    print nc.num_to_word(75008000000)
    print nc.num_to_word(101)
    print nc.num_to_word(100)
    print nc.num_to_word(99)
    print nc.num_to_word(1)
    print nc.num_to_word(25)
    print nc.num_to_word(30)
    print nc.num_to_word(45)
    print nc.num_to_word(0)
