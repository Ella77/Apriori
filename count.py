def dataFromFile():
    """Function which reads from the file and yields a generator"""
    arr= []
    with open('onlyBJ.txt') as file_iter:

         for line in file_iter:
            line = line.split(",")
            print(line)

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
    chart()