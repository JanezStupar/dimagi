__author__ = 'Janez Stupar'


def range_generator(first, second=None):
    """
    This is a generator version of range(), which is not a generator in Python 2.7.x

    This approach was taken because I thought I wanted to build a generator based version.
    """
    lbound = 0

    if second is None:
        ubound = first
    else:
        lbound = first
        ubound = second

    count = lbound
    while count < ubound:
        yield count
        count += 1


def count_number_occurrences(input_data, number="7"):

    number = str(number)
    count = 0
    for candidate in range_generator(1, input_data+1):
        if number not in str(candidate):
            count += 1

    return count


if __name__ == "__main__":
  print count_number_occurrences(1)
  print count_number_occurrences(8)
  print count_number_occurrences(22)
  print count_number_occurrences(105)
  print count_number_occurrences(33)
  print count_number_occurrences(331)
  print count_number_occurrences(1500)
  print count_number_occurrences(80)
  print count_number_occurrences(44)
  print count_number_occurrences(7)
