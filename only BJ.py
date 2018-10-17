from collections import Counter


def dataFromFile():
    """Function which reads from the file and yields a generator"""
    with open('groupby.csv') as file_iter:
        with open('onlyBJ.txt', 'wb') as f :
         for line in file_iter:
            split = line.split('[')[1:]

            print(split)

        # print(line)
        # .rstrip(',')
        # Remove trailing comma'
        # list = line.split()[-1]
        #
        #     record = frozenset(line.split('\t'))
        #     f.write(line+'\n')
        # print(record)
        # yield record

# def count():
#
#     return Counter(dataFromFile())


if __name__ == "__main__":
    dataFromFile()